(() => {
  const STORAGE_KEY = 'product-recommendations-tabs:viewed';
  const HISTORY_SIZE = 20;

  // Newest first, each product once. Ids are kept as strings: Liquid and dataset both give strings.
  function updateHistory(history, productId, max = HISTORY_SIZE) {
    const id = String(productId);
    return [id, ...history.map(String).filter((item) => item !== id)].slice(0, max);
  }

  function idsToShow(history, currentProductId, limit) {
    const current = String(currentProductId);
    return history.map(String).filter((id) => id !== current).slice(0, limit);
  }

  function searchQuery(ids) {
    return ids.map((id) => `id:${id}`).join(' OR ');
  }

  // Search answers in relevance order; the tab promises the most recently viewed first.
  function orderByIds(items, ids) {
    const rank = new Map(ids.map((id, index) => [String(id), index]));
    const position = (item) => (rank.has(item.dataset.productId) ? rank.get(item.dataset.productId) : ids.length);
    return [...items].sort((a, b) => position(a) - position(b));
  }

  function readHistory(storage) {
    try {
      const value = JSON.parse(storage.getItem(STORAGE_KEY));
      return Array.isArray(value) ? value.map(String) : [];
    } catch (error) {
      return [];
    }
  }

  function writeHistory(storage, history) {
    try {
      storage.setItem(STORAGE_KEY, JSON.stringify(history));
    } catch (error) {
      // Private mode or a full quota: the tab simply stays empty.
    }
  }

  // One request per tab per page view. A load overtaken by a later one resolves to null, so a slow
  // answer for a tab the shopper already left never replaces the tab they are looking at.
  class TabLoader {
    constructor(fetchHtml) {
      this.fetchHtml = fetchHtml;
      this.cache = new Map();
      this.pending = new Map();
      this.latest = null;
    }

    async load(key, url) {
      this.latest = key;
      let html = this.cache.get(key);
      if (html === undefined) {
        if (!this.pending.has(key)) {
          this.pending.set(key, this.fetchHtml(url).finally(() => this.pending.delete(key)));
        }
        html = await this.pending.get(key);
        this.cache.set(key, html);
      }
      return this.latest === key ? html : null;
    }
  }

  window.ProductRecommendationsTabs = {
    STORAGE_KEY,
    HISTORY_SIZE,
    updateHistory,
    idsToShow,
    searchQuery,
    orderByIds,
    readHistory,
    writeHistory,
    TabLoader,
  };

  if (!window.customElements || window.customElements.get('product-recommendations-tabs')) return;

  function storage() {
    try {
      return window.localStorage;
    } catch (error) {
      return null;
    }
  }

  function fetchHtml(url) {
    return fetch(url).then((response) => {
      if (!response.ok) throw new Error(`${response.status} ${url}`);
      return response.text();
    });
  }

  class ProductRecommendationsTabsElement extends HTMLElement {
    // Handlers are made once: the theme editor moves a section's node when sections are reordered,
    // which disconnects and reconnects this same element, and fresh handlers would be added twice.
    constructor() {
      super();
      this.onClick = (event) => this.select(event.currentTarget, { announce: true });
      this.onKeydown = this.onKeydown.bind(this);
      this.onBlockSelect = this.onBlockSelect.bind(this);
    }

    connectedCallback() {
      this.tabs = Array.from(this.querySelectorAll('[role="tab"]'));
      this.tablist = this.querySelector('[role="tablist"]');
      this.panel = this.querySelector('[data-panel]');
      this.live = this.querySelector('[data-live]');
      if (!this.tabs.length || !this.panel) return;

      // Kept across a reconnect, so a moved section does not fetch its tabs again.
      this.loader = this.loader || new TabLoader(fetchHtml);
      const store = storage();
      this.history = store ? readHistory(store) : [];
      if (store && this.dataset.productId) writeHistory(store, updateHistory(this.history, this.dataset.productId));

      this.tabs.forEach((tab) => tab.addEventListener('click', this.onClick));
      this.tablist.addEventListener('keydown', this.onKeydown);
      document.addEventListener('shopify:block:select', this.onBlockSelect);

      this.observer = new IntersectionObserver(
        (entries) => {
          if (!entries[0].isIntersecting) return;
          this.observer.disconnect();
          this.select(this.activeTab());
        },
        { rootMargin: '0px 0px 400px 0px' }
      );
      this.observer.observe(this);
    }

    disconnectedCallback() {
      this.observer?.disconnect();
      this.tabs?.forEach((tab) => tab.removeEventListener('click', this.onClick));
      this.tablist?.removeEventListener('keydown', this.onKeydown);
      document.removeEventListener('shopify:block:select', this.onBlockSelect);
    }

    activeTab() {
      return this.tabs.find((tab) => tab.getAttribute('aria-selected') === 'true') || this.tabs[0];
    }

    viewedIds() {
      return idsToShow(this.history, this.dataset.productId, Number(this.dataset.limit));
    }

    urlFor(type) {
      const { sectionId, productId, limit } = this.dataset;
      if (type === 'related') {
        return `${this.dataset.recommendationsUrl}?product_id=${productId}&limit=${limit}&intent=related&section_id=${sectionId}`;
      }
      const ids = this.viewedIds();
      if (!ids.length) return null;
      return `${this.dataset.searchUrl}?type=product&options%5Bunavailable_products%5D=show&q=${encodeURIComponent(
        searchQuery(ids)
      )}&section_id=${sectionId}`;
    }

    async select(tab, { announce = false } = {}) {
      this.observer?.disconnect();
      this.tabs.forEach((item) => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
      });
      this.panel.setAttribute('aria-labelledby', tab.id);

      const type = tab.dataset.tabType;
      const url = this.urlFor(type);
      if (!url) {
        // An earlier tab may still be loading. It never reaches the loader's "latest" check, so the
        // await below also asks whether its tab is still the selected one before writing the panel.
        this.panel.removeAttribute('aria-busy');
        this.show(this.template(`[data-empty-message="${type}"]`), announce);
        return;
      }

      this.panel.setAttribute('aria-busy', 'true');
      try {
        const html = await this.loader.load(type, url);
        if (html !== null && this.activeTab() === tab) this.show(this.extract(html, type), announce);
      } catch (error) {
        if (this.activeTab() === tab) this.show(this.template('[data-error-message]'), announce);
      } finally {
        if (this.activeTab() === tab) this.panel.removeAttribute('aria-busy');
      }
    }

    // The response is this section rendered by the theme itself, so its markup can go in as is.
    extract(html, type) {
      const content = new DOMParser().parseFromString(html, 'text/html').querySelector('[data-panel-content]');
      if (!content) return this.template('[data-error-message]');
      const list = content.querySelector('ul');
      if (type === 'recently_viewed' && list) {
        orderByIds(Array.from(list.children), this.viewedIds()).forEach((item) => list.appendChild(item));
      }
      const fragment = document.createDocumentFragment();
      fragment.append(...content.childNodes);
      return fragment;
    }

    template(selector) {
      const template = this.querySelector(selector);
      return template ? template.content.cloneNode(true) : document.createDocumentFragment();
    }

    show(fragment, announce) {
      this.panel.replaceChildren(fragment);
      const message = this.panel.querySelector('[data-announce]');
      if (announce && this.live && message) this.live.textContent = message.textContent.trim();
    }

    // Arrows only move focus; Enter or Space (a click on the button) selects. Selecting a tab can
    // send a request, so passing over a button on the way to another must not load it (spec §2.8).
    onKeydown(event) {
      const index = this.tabs.indexOf(document.activeElement);
      if (index === -1) return;
      const target = { ArrowRight: index + 1, ArrowLeft: index - 1, Home: 0, End: this.tabs.length - 1 }[event.key];
      if (target === undefined) return;
      event.preventDefault();
      this.tabs[(target + this.tabs.length) % this.tabs.length].focus();
    }

    onBlockSelect(event) {
      const tab = this.tabs.find((item) => item.dataset.blockId === event.detail?.blockId);
      if (tab) this.select(tab);
    }
  }

  customElements.define('product-recommendations-tabs', ProductRecommendationsTabsElement);
})();
