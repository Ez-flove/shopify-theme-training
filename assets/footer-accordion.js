if (!customElements.get('footer-accordion')) {
  customElements.define(
    'footer-accordion',
    class FooterAccordion extends HTMLElement {
      constructor() {
        super();
        this.desktop = window.matchMedia('(min-width: 990px)');
        this.sync = this.sync.bind(this);
      }

      connectedCallback() {
        this.details = this.querySelector('details');
        this.sync();
        this.desktop.addEventListener('change', this.sync);
      }

      disconnectedCallback() {
        this.desktop.removeEventListener('change', this.sync);
      }

      // The server renders the menu open so nothing is out of reach without JavaScript. On desktop
      // the heading is hidden and the menu stays open; below 990px it starts closed.
      sync() {
        if (this.details) this.details.open = this.desktop.matches;
      }
    }
  );
}
