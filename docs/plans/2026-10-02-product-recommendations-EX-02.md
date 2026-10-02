# Plan EX-02 — Section Product recommendations: "Sản phẩm liên quan" và "Sản phẩm đã xem"

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Ngày: 2026-10-02 · Trạng thái: **đã duyệt (Gate 2)** — người dùng, 2026-10-02, chạy native · **xong phần của Claude, đã review, đã commit** · chờ người dùng push + PR và kiểm theme editor

**Spec:** [`docs/specs/features/2026-10-02-product-recommendations-EX-02.md`](../specs/features/2026-10-02-product-recommendations-EX-02.md) (đã duyệt).
Plan dẫn chiếu mục của spec bằng "spec §x", quyết định bằng "D-x" (D-1, D-2 ở spec, D-3 trở đi ở plan này).

**Goal:** một section mới chỉ dùng trên trang sản phẩm, có hai nút chuyển giữa "Sản phẩm liên quan"
và "Sản phẩm đã xem", danh sách hiện dạng carousel hoặc grid, đổi tab không tải lại trang và mỗi tab
gọi API nhiều nhất một lần.

**Architecture:** một section Liquid render ba ngữ cảnh: trên trang sản phẩm nó là cái vỏ (heading,
description, nút, panel rỗng); qua Product Recommendations API nó render card cho tab "liên quan";
qua trang search với truy vấn `id:` nó render card cho tab "đã xem" (D-2). Một custom element
`product-recommendations-tabs` lấy HTML đó bằng Section Rendering API khi section sắp cuộn tới, giữ
lại theo tab, và thay nội dung panel. Logic không cần DOM (lịch sử xem, truy vấn, cache, "request sau
cùng thắng") nằm trong cùng file JS và được test bằng `node --test`.

**Tech Stack:** Liquid, JSON template, CSS, một file JS thuần (custom element), Dawn `card-product`
và `slider-component`, Shopify CLI 4.8.3 (`shopify theme dev`), Node 22 test runner, chrome-devtools
MCP cho bằng chứng trên trình duyệt.

## Global Constraints

- Theme nền: Dawn v16.0.0, branch `ex-02-product-recommendations` tách từ `origin/main` (`a4cb83d`).
- Section chỉ thêm được ở template sản phẩm: `"enabled_on": { "templates": ["product"] }` (spec §3).
- Mốc responsive của Dawn: 750 px và 990 px; CSS viết mobile trước bằng `min-width` (`guidelines.md`).
- Chữ shopper đọc đi qua `{{ 'key' | t }}`; khoá mới vào `locales/en.default.json` **và**
  `locales/vi.json`; chuỗi số nhiều trong `vi.json` chỉ có `other`.
- Nhãn trong editor là khoá `t:` trong `locales/en.default.schema.json`; dùng lại khoá có sẵn của Dawn
  khi trùng nghĩa.
- Link từ setting kiểu `url`; text merchant nhập được `escape`; HTML chèn vào trang chỉ là HTML của
  chính theme (Section Rendering); script tải `defer`; không script từ xa (`code-security.md`).
- Không commit, không push khi người dùng chưa bảo; không publish theme; làm qua `shopify theme dev`.
- Bằng chứng lưu ở `docs/exercises/EX-02-product-recommendations/evidence/`, đường dẫn ghi vào bảng
  trạng thái cuối plan.
- Số dòng trong plan đo trên `origin/main` ngày 2026-10-02; lúc làm, tìm chỗ sửa theo đoạn được trích.

## Review Focus

Năm tình huống spec ngụ ý nhưng các bước test chính không chạm tới, dễ làm hỏng nhất trước:

1. **Lịch sử xem có sản phẩm đã bị xoá hoặc ẩn** — tab "đã xem" hiện đúng các sản phẩm còn lại, đúng
   thứ tự mới nhất trước, không có ô trống. Test: Task 5 bước 8.
2. **Bộ nhớ trình duyệt hỏng hoặc bị chặn** (JSON rác trong `localStorage`, `localStorage` ném lỗi) —
   không lỗi JS, tab "đã xem" hiện câu báo không có sản phẩm. Test: Task 3 bước 1 (unit) và Task 5
   bước 9 (trình duyệt).
3. **Trang ở thư mục ngôn ngữ `/vi`** — request đi qua `/vi/recommendations/products` và `/vi/search`
   (từ `routes`), chữ trên nút và câu báo bằng tiếng Việt. Test: Task 7 bước 4.
4. **Merchant đổi thứ tự block, xoá một block, xoá cả hai** — tab đầu là block đầu; một block vẫn có
   nút; không block thì storefront không hiện section, editor hiện dòng nhắc. Test: Task 5 bước 11.
5. **Carousel ít sản phẩm hơn số cột, và kéo cửa sổ qua 750/990 px khi đang ở carousel** — nút
   prev/next ẩn khi không cần, carousel tính lại số trang. Test: Task 6 bước 6.

---

## 1. Thiếu cái gì

Dawn có section "Related products" (`sections/related-products.liquid`) chỉ hiện sản phẩm liên quan,
dạng lưới, không có nút chuyển, không có "sản phẩm đã xem", không có carousel. Đề yêu cầu một section
mới có cả hai loại, chuyển qua lại không tải trang, gọi API ít nhất có thể (spec §1).

## 2. Ở đâu (đo trên `origin/main`, 2026-10-02)

| Chỗ | Đo được |
|---|---|
| `templates/product.json` | 116 dòng; `order` = `main`, `disclosures`, `related-products`; instance `related-products` ở dòng 92–112 |
| `sections/related-products.liquid:23-29` | Dawn lấy URL từ `routes.product_recommendations_url`, truyền `section_id` và `product_id` qua `data-*` |
| `assets/global.js:1193-1243` | `ProductRecommendations`: IntersectionObserver `rootMargin: '0px 0px 400px 0px'`, `fetch` rồi gán `innerHTML` — khuôn mà element mới theo |
| `assets/global.js:728-822` | `SliderComponent`: tìm `[id^="Slider-"]`, `[id^="Slide-"]`, nút `name="previous"`/`"next"` lúc **khởi tạo**; tự tắt nút ở đầu/cuối; `ResizeObserver` tính lại trang |
| `sections/featured-collection.liquid:95-199` | markup carousel của Dawn: `slider-component` → `ul#Slider-…` có `slider slider--desktop slider--tablet grid--peek` → `li#Slide-…` → `.slider-buttons` |
| `snippets/card-product.liquid:4-18` | tham số: `card_product`, `media_aspect_ratio`, `image_shape`, `show_secondary_image`, `show_vendor`, `show_rating`, `lazy_load`, `skip_styles`, `section_id`, `quick_add` |
| `assets/theme-editor.js:6` | Dawn nghe `shopify:block:select` trên `document`, dùng `event.target` |
| `locales/en.default.json` / `vi.json` | cùng 385 khoá, không thiếu khoá nào; khoá số nhiều của Dawn trong `vi.json` có cả `one` lẫn `other` (vd. `blogs.article.comments`) |
| `locales/en.default.json` → `general.slider` | `of`, `next_slide`, `previous_slide`, `name` — dùng lại cho nút carousel |

Đo trên store `ngocmx-training` (theme GitHub, 2026-10-02):

| Phép đo | Kết quả |
|---|---|
| `/search?type=product&q=id:A OR id:B` | trả đúng hai sản phẩm A, B |
| instance section của template sản phẩm, render bằng `section_id` trên `/search` | status 200, **giữ setting của template** (padding-bottom 28 px, mặc định của schema là 36) |
| `options[unavailable_products]` với truy vấn `id:` 6 sản phẩm hết hàng | không truyền: 6 · `show`: 6 · `hide`: 0 |
| `/recommendations/products.json?product_id=…&intent=related` cho 5 sản phẩm | 200, **0 sản phẩm** mỗi lần — tab "liên quan" trên store này sẽ hiện câu báo trống trừ khi có dữ liệu gợi ý (Task 7 bước 2) |
| Sản phẩm của store | 13, mọi variant hết hàng |

## 3. Sửa gì, và cố ý không sửa gì

**Tạo:**

| File | Trách nhiệm |
|---|---|
| `sections/product-recommendations-tabs.liquid` | vỏ section, ba ngữ cảnh render, schema |
| `assets/product-recommendations-tabs.js` | helper thuần (lịch sử, truy vấn, thứ tự, `TabLoader`) + custom element |
| `assets/section-product-recommendations-tabs.css` | hàng nút, link, panel, câu báo, trạng thái đang tải |
| `tests/unit/product-recommendations-tabs.test.js` | unit test cho helper thuần |
| `tests/guards/locale-parity.test.js` | guard: mọi khoá `en.default.json` có trong `vi.json` |

**Sửa:** `locales/en.default.json`, `locales/vi.json`, `locales/en.default.schema.json`,
`templates/product.json` (OQ-8, Task 4 bước 9), `flow.config.json` + `CLAUDE.md` (lệnh test gồm `tests/unit`, D-9),
`docs/architecture/change-guards.json` (sinh lại).

**Cố ý không sửa:** `sections/related-products.liquid` và `ProductRecommendations` trong `global.js`
(giữ file, chỉ bỏ khỏi template — OQ-8); `card-product.liquid`; `SliderComponent`; quick add, cuộn vô
hạn, nút xoá lịch sử (spec §4); 49 locale khác ngoài `en.default` và `vi`.

## 4. Kiểm bằng gì

- **Unit test chạy được ngoài trình duyệt** (CLAUDE.md): `tests/unit/product-recommendations-tabs.test.js`
  viết trước, đỏ vì file JS chưa có, xanh khi có. Mutation phải làm nó đỏ: bỏ dòng loại sản phẩm đang
  xem trong `idsToShow`; bỏ `this.latest === key` trong `TabLoader`.
- **Guard mới `locale-parity`:** xanh trên `origin/main` (385/385), đỏ khi thêm khoá EX-02 vào
  `en.default.json` mà chưa vào `vi.json`. Mutation: đổi tên một khoá trong `vi.json`; đổi `other`
  của một chuỗi số nhiều trong `vi.json` thành `few`.
- **Guard có sẵn `section-blocks`:** phải xanh với section mới (mỗi loại block có `when`, có
  `block.shopify_attributes`). Mutation: bỏ `when 'recently_viewed'` → đỏ.
- **Trình duyệt** cho markup, CSS, lazy load, số request, editor: ảnh **trước** (Task 1) và **sau** ở
  375, 750, 990, 1440 px và ở bề ngang hai ảnh design (1444, 1311 px); đếm request bằng
  `performance.getEntriesByType('resource')`; checklist `.claude/rules/shopify-theme.md` §3 và spec §5.
- **Lệnh của project:** `shopify theme check --fail-level error` (0 error, 9 warning như baseline),
  `tools/run js-syntax`, `node --test 'tests/guards/*.test.js' 'tests/unit/*.test.js'`,
  `tools/run change-guards --check`, `tools/run shared-rules`.

---

## Contract

### Schema — `sections/product-recommendations-tabs.liquid`

Đổi id sau khi merchant đã lưu thì giá trị cũ mất, nên chốt ở đây.

| id | type | mặc định | ghi chú |
|---|---|---|---|
| `heading` | `inline_richtext` | `You may also like` | |
| `description` | `richtext` | trống | |
| `link_label` | `text` | trống | `info`: hiện bên phải hàng nút; trống thì ẩn link (OQ-1) |
| `link_url` | `url` | trống | link chỉ hiện khi cả chữ lẫn URL có |
| `display_style` | `select`: `carousel` / `grid` | `carousel` | "style type" của đề |
| `products_to_show` | `range` 2–10, bước 1 | 8 | `info`: áp cho từng nút; Shopify trả tối đa 10 sản phẩm gợi ý |
| `columns_desktop` | `range` 2–6, bước 1 | 4 | `info`: carousel — số sản phẩm thấy được mỗi lần |
| `columns_mobile` | `select`: `1` / `2` | `2` | |
| `image_ratio` | `select`: `adapt` / `portrait` / `square` | `square` | như `related-products` |
| `show_secondary_image` | `checkbox` | `false` | |
| `show_vendor` | `checkbox` | `false` | |
| `color_scheme` | `color_scheme` | `scheme-1` | |
| `padding_top`, `padding_bottom` | `range` 0–100, bước 4, `px` | 36, 36 | |

Block (`max_blocks: 2`), mỗi loại `limit: 1`:

| type | setting | ghi chú |
|---|---|---|
| `related` | `label` (`text`), `empty_message` (`text`) | trống → khoá storefront `related_label`, `related_empty` (OQ-9) |
| `recently_viewed` | `paragraph` (`info` lưu trong trình duyệt), `label` (`text`), `empty_message` (`text`) | trống → `recently_viewed_label`, `recently_viewed_empty` |

### Request — Section Rendering API của chính instance này

| Tab | URL | Trả về |
|---|---|---|
| `related` | `{{ routes.product_recommendations_url }}?product_id=<product.id>&limit=<products_to_show>&intent=related&section_id=<section.id>` | HTML section; `[data-panel-content="related"]` chứa `ul > li[data-product-id]` + `[data-announce]`, hoặc câu báo trống |
| `recently_viewed` | `{{ routes.search_url }}?type=product&options%5Bunavailable_products%5D=show&q=<id:A OR id:B …>&section_id=<section.id>` — tối đa `products_to_show` id, mới nhất trước, không gồm sản phẩm đang xem | như trên, `[data-panel-content="recently_viewed"]`; thứ tự `li` do JS sắp lại theo lịch sử |

Không có lịch sử nào (sau khi bỏ sản phẩm đang xem) thì **không gửi request**: JS lấy câu báo trống
từ `<template data-empty-message="recently_viewed">`.

### Khoá locale mới

Storefront, `sections.product_recommendations_tabs.*` trong `en.default.json` và `vi.json`:

| khoá | en | vi |
|---|---|---|
| `tabs_label` | `Product lists` | `Danh sách sản phẩm` |
| `related_label` | `Related products` | `Sản phẩm liên quan` |
| `recently_viewed_label` | `Recently viewed` | `Sản phẩm đã xem` |
| `related_empty` | `No related products to show yet.` | `Chưa có sản phẩm liên quan.` |
| `recently_viewed_empty` | `Products you view will show up here.` | `Các sản phẩm bạn đã xem sẽ hiện ở đây.` |
| `error` | `Products couldn't be loaded. Select the button again to retry.` | `Không tải được sản phẩm. Bấm lại nút để thử lại.` |
| `noscript` | `Turn on JavaScript to see these products.` | `Bật JavaScript để xem các sản phẩm này.` |
| `add_block` | `Add a Related products or Recently viewed block to show this section.` | `Thêm block Sản phẩm liên quan hoặc Sản phẩm đã xem để hiện section này.` |
| `products_count.one` / `.other` | `{{ count }} product` / `{{ count }} products` | — / `{{ count }} sản phẩm` |

Schema, `sections.product-recommendations-tabs.*` trong `en.default.schema.json` — bảng đầy đủ ở Task 4
bước 4. Dùng lại khoá Dawn: `sections.all.colors.label`, `sections.all.padding.*`,
`sections.related-products.settings.image_ratio.*`, `…show_secondary_image.label`,
`…show_vendor.label`, `…columns_mobile.*` (Task 4 bước 5 kiểm từng khoá có thật).

### Tên dùng chung giữa các task

| Tên | Loại | Do task | Dùng ở |
|---|---|---|---|
| `window.ProductRecommendationsTabs` | object helper: `updateHistory(history, productId, max)`, `idsToShow(history, currentId, limit)`, `searchQuery(ids)`, `orderByIds(items, ids)`, `readHistory(storage)`, `writeHistory(storage, history)`, `TabLoader`, `STORAGE_KEY`, `HISTORY_SIZE` | 3 | 3 (test), 5 |
| `TabLoader#load(key, url)` | `Promise<string \| null>` — `null` khi một `load` sau hỏi khoá khác | 3 | 5 |
| `product-recommendations-tabs:viewed` | khoá `localStorage`, mảng id dạng chuỗi, mới nhất trước, tối đa 20 | 3 | 5 |
| `product-recommendations-tabs` | custom element | 5 | 4 (markup) |
| `data-section-id`, `data-product-id`, `data-limit`, `data-recommendations-url`, `data-search-url` | thuộc tính trên element | 4 | 5 |
| `[role="tab"][data-tab-type][data-block-id]`, `[data-panel]`, `[data-panel-content]`, `[data-announce]`, `[data-live]`, `template[data-empty-message="<type>"]`, `template[data-error-message]` | hook trong markup | 4 | 5, 6 |
| `ProductRecommendationsTab-<block.id>`, `ProductRecommendationsPanel-<section.id>` | id phần tử | 4 | 5 |

## Những đầu phải biết

Theo `.claude/rules/shopify-theme.md` §1 và `docs/architecture/change-guards.json`:

| Thêm | Các đầu | Cái gì giữ |
|---|---|---|
| Section mới | `{% schema %}` có `name`, `presets`, `enabled_on` · CSS riêng qua `stylesheet_tag` · JS riêng `defer` · template `product.json` đặt sẵn (OQ-8) | Theme Check; trình duyệt; editor |
| Hai loại block | `blocks` trong schema · `when 'related'` / `when 'recently_viewed'` trong `case block.type` · `{{ block.shopify_attributes }}` trên nút · `presets` có cả hai | guard `section-blocks` |
| Setting section/block | schema · Liquid đọc `section.settings.*` / `block.settings.*` · `product.json` giữ giá trị · nhãn `t:` trong `en.default.schema.json` | Theme Check (JSON template, khoá schema); Task 4 bước 5 (khoá có thật) |
| Chuỗi storefront | `{{ 'sections.product_recommendations_tabs.*' \| t }}` · `en.default.json` · `vi.json` | Theme Check `TranslationKeyExists` (en); guard mới `locale-parity` (vi) |
| Chuỗi cho JS | không có `window.*Strings`: câu báo trống/lỗi nằm trong `<template>` do Liquid render, số sản phẩm nằm trong `[data-announce]` của response | trình duyệt |
| Lịch sử xem | `localStorage` qua `readHistory`/`writeHistory` (bắt lỗi) | unit test |
| Request | URL từ `routes` (không viết cứng `/search`, `/recommendations`) | Theme Check `HardcodedRoutes` cho Liquid; Review Focus 3 |

Khái niệm Shopify plan này dùng, mỗi cái một câu vì sao:

- **Section Rendering API** — thêm `section_id` vào URL của bất kỳ trang nào để nhận riêng HTML của
  section đó, nên card là card của theme, giá theo market, không phải dựng lại trong JS
  ([shopify.dev](https://shopify.dev/docs/api/ajax/section-rendering)).
- **Product Recommendations API** — `/recommendations/products` với `product_id`, `limit` (tối đa 10),
  `intent=related`; trong ngữ cảnh đó Liquid có object `recommendations`
  ([shopify.dev](https://shopify.dev/docs/api/ajax/reference/product-recommendations)).
- **Object `search`** — có trên trang search: `search.performed`, `search.results`; tham số
  `options[unavailable_products]` quyết định sản phẩm hết hàng có hiện không
  ([shopify.dev](https://shopify.dev/docs/storefronts/themes/navigation-search/search)).
- **`enabled_on`** — giới hạn template nào thêm được section trong editor
  ([shopify.dev](https://shopify.dev/docs/storefronts/themes/architecture/sections/section-schema#enabled_on)).
- **Sự kiện editor `shopify:block:select`** — editor bắn khi merchant bấm block ở sidebar, để theme
  đưa block đó ra cho thấy
  ([shopify.dev](https://shopify.dev/docs/storefronts/themes/best-practices/editor/integrate-sections-and-blocks)).
- **`request.design_mode`** — `true` khi trang render trong theme editor, để dòng nhắc "thêm block"
  chỉ merchant thấy ([shopify.dev](https://shopify.dev/docs/api/liquid/objects/request)).

## Quyết định của plan

| # | Spec | Điểm chưa rõ | Chốt | Nguồn |
|---|---|---|---|---|
| D-3 | §3 | Tên | file `product-recommendations-tabs.*`, element `product-recommendations-tabs`; tên trong editor "Product recommendations" (Dawn đã đặt "Related products" cho section của nó, nên không trùng) | plan |
| D-4 | §2.4, OQ-4 | Lịch sử lưu ở đâu, dạng gì | `localStorage` khoá `product-recommendations-tabs:viewed`, mảng id dạng chuỗi, mới nhất trước, tối đa 20; ghi lúc element trên trang sản phẩm kết nối | plan |
| D-5 | §6 rủi ro 2 | Sản phẩm đã xem mà hết hàng | luôn gửi `options[unavailable_products]=show` (đo: `hide` làm mất cả 6) | đo 2026-10-02 |
| D-6 | §2.2 | Hai tab dùng một panel hay hai | một `tabpanel`, nội dung thay theo tab; cache giữ HTML response theo tab, mỗi lần hiện thì parse lại | plan |
| D-7 | §2.4 | Hỏi bao nhiêu id | chỉ `products_to_show` id đầu; sản phẩm đã xoá không được bù bằng sản phẩm cũ hơn | plan |
| D-8 | §2.6, OQ-9 | Chuỗi cho JS | không thêm `window.*Strings`: Liquid render câu báo vào `<template>`, số sản phẩm vào `[data-announce]` | plan |
| D-9 | CLAUDE.md | Unit test để đâu | `tests/unit/*.test.js`, nạp file asset bằng `vm`; lệnh `test` trong `flow.config.json` và CLAUDE.md thêm glob này | plan |
| D-10 | §5.7 | `vi.json` thiếu khoá thì không gì báo (Dawn tắt `MatchingTranslations`) | guard mới `locale-parity` | plan |
| D-11 | §2.6 | JS tắt | `<noscript>` trong panel; không render sẵn danh sách phía server | plan |
| D-12 | §2.7, OQ-6 | Lúc nào tải | IntersectionObserver `rootMargin: '0px 0px 400px 0px'` như Dawn; bấm block trong editor thì tải ngay | plan, theo Dawn |
| D-13 | OQ-8 | Sửa `product.json` bằng tay | spec quyết định trang mặc định đổi, nên đây là chỗ được phép sửa JSON template (`shopify-theme.md` §4); review lại trong `git diff` | spec OQ-8 |

---

### Task 1: Branch, baseline, ảnh "trước"

**Files:** không sửa file theme. Tạo `docs/exercises/EX-02-product-recommendations/evidence/`.

- [ ] **Bước 1 (Claude):** tách branch từ `origin/main`.

```bash
git fetch origin
git switch -c ex-02-product-recommendations origin/main
```

  Nếu working tree còn sửa đổi chưa commit của EX-01 (bảng trạng thái plan EX-01), `git switch` mang
  nó theo; để nguyên, không commit vào EX-02.
- [ ] **Bước 2 (người dùng):** chạy lại `shopify theme dev --store ngocmx-training` trong terminal của
  mình (nhập mật khẩu storefront). Claude kiểm `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:9292/` → `200`.
- [ ] **Bước 3 — baseline lệnh:**

```bash
shopify theme check --fail-level error     # kỳ vọng: 0 error, 9 warning
node --test 'tests/guards/*.test.js'       # kỳ vọng: 6 pass
tools/run js-syntax                        # kỳ vọng: 37 file, clean
```

- [ ] **Bước 4 — ảnh "trước":** mở một trang sản phẩm ở 1440 và 375 px; chụp vùng dưới thông tin sản
  phẩm: chỉ có "You may also like" của Dawn (hoặc không có gì vì API trả 0). Lưu
  `evidence/before-1440.png`, `evidence/before-375.png`; ghi page text vào `evidence/before-page-text.md`.

---

### Task 2: Guard `locale-parity` (spec §5.7, D-10)

**Files:** Create `tests/guards/locale-parity.test.js`; Modify `docs/architecture/change-guards.json` (sinh lại).

**Interfaces:** không dùng gì của task khác. Task 4 phải làm nó xanh lại.

- [ ] **Bước 1 — viết guard:**

```js
'use strict';
/**
 * @guard watches: a storefront string added to locales/en.default.json without its translation in locales/vi.json. Dawn turns MatchingTranslations off in .theme-check.yml, so Theme Check never reports it; the /vi storefront then shows "Translation missing: vi.…" where the text should be.
 * @guard extend: a new key in en.default.json needs the same key in vi.json. A pluralised string (an object of one/other …) needs at least "other" in vi.json, because Vietnamese has no grammatical plural. A string that stays English on purpose still goes into vi.json, with the English text.
 */

// What this cannot catch:
// - Wrong or untranslated text: an English sentence copied into vi.json passes.
// - The other 49 storefront locales (EX-01 D-5) and the *.schema.json files, which only the admin reads.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const LOCALES = path.resolve(__dirname, '..', '..', 'locales');
const PLURAL = new Set(['zero', 'one', 'two', 'few', 'many', 'other']);

function read(file) {
  return JSON.parse(fs.readFileSync(path.join(LOCALES, file), 'utf8'));
}

// key → 'text' | 'plural'. A plural group is an object whose keys are all CLDR plural categories.
function strings(object, prefix = '', out = new Map()) {
  for (const [name, value] of Object.entries(object)) {
    const key = prefix ? `${prefix}.${name}` : name;
    if (value && typeof value === 'object') {
      const names = Object.keys(value);
      if (names.length > 0 && names.every((category) => PLURAL.has(category))) out.set(key, 'plural');
      else strings(value, key, out);
    } else {
      out.set(key, 'text');
    }
  }
  return out;
}

function lookup(object, key) {
  return key.split('.').reduce((node, name) => (node == null ? undefined : node[name]), object);
}

const en = read('en.default.json');
const vi = read('vi.json');

test('every en.default.json string has a vi.json translation', () => {
  const english = strings(en);
  // Dawn ships 385 storefront strings; a parse that finds far fewer is not looking at the real file.
  assert.ok(english.size > 300, `only ${english.size} strings read from en.default.json`);
  const missing = [];
  for (const [key, kind] of english) {
    const value = lookup(vi, key);
    if (kind === 'plural' ? !(value && typeof value.other === 'string') : typeof value !== 'string') {
      missing.push(key);
    }
  }
  assert.deepEqual(missing, [], 'missing from vi.json (a plural needs "other")');
});
```

- [ ] **Bước 2:** `node --test tests/guards/locale-parity.test.js` → **pass 1/1** trên `origin/main`.
- [ ] **Bước 3 — mutation, mỗi cái phải đỏ và nêu đúng khoá:**

```bash
tools/run mutate locales/vi.json --sub '"linkedin": "LinkedIn"=>"linkedin_x": "LinkedIn"' -- node --test tests/guards/locale-parity.test.js
# kỳ vọng: đỏ, missing = [ 'general.social.links.linkedin' ]
tools/run mutate locales/vi.json --sub '"other": "{{ count }} bình luận"=>"few": "{{ count }} bình luận"' -- node --test tests/guards/locale-parity.test.js
# kỳ vọng: đỏ, missing có 'blogs.article.comments' (nếu chuỗi thay không duy nhất, mutate báo — chọn chuỗi số nhiều khác của vi.json)
```

- [ ] **Bước 4:** `tools/run change-guards` → 3 guard; `tools/run change-guards --check` → clean.

---

### Task 3: Helper thuần + unit test (spec §2.2, §2.4, D-4, D-6, D-7, D-9)

**Files:** Create `tests/unit/product-recommendations-tabs.test.js`, `assets/product-recommendations-tabs.js`;
Modify `flow.config.json` (`commands.test`), `CLAUDE.md` (khối Commands).

**Interfaces:** Produces `window.ProductRecommendationsTabs` (bảng "Tên dùng chung").

- [ ] **Bước 1 — viết test trước:**

```js
'use strict';
// Unit tests for the DOM-free half of assets/product-recommendations-tabs.js. The file is a browser
// script, so it is loaded into a vm context with a bare `window`: without customElements it stops
// after publishing window.ProductRecommendationsTabs.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const FILE = path.resolve(__dirname, '..', '..', 'assets', 'product-recommendations-tabs.js');

function load() {
  const context = { window: {}, console };
  vm.runInNewContext(fs.readFileSync(FILE, 'utf8'), context);
  return context.window.ProductRecommendationsTabs;
}

// Arrays made inside the vm context have another realm's prototype; copy before deepEqual.
const plain = (value) => JSON.parse(JSON.stringify(value));

test('updateHistory puts the product first, once, and keeps at most max ids', () => {
  const { updateHistory } = load();
  assert.deepEqual(plain(updateHistory(['2', '1'], 3, 20)), ['3', '2', '1']);
  assert.deepEqual(plain(updateHistory(['2', '3', '1'], 3, 20)), ['3', '2', '1']);
  assert.deepEqual(plain(updateHistory(['1', '2', '3'], 4, 3)), ['4', '1', '2']);
  assert.deepEqual(plain(updateHistory([7, 8], '9', 20)), ['9', '7', '8']);
});

test('idsToShow leaves out the product being viewed and stops at the limit', () => {
  const { idsToShow } = load();
  assert.deepEqual(plain(idsToShow(['5', '4', '3', '2'], '5', 2)), ['4', '3']);
  assert.deepEqual(plain(idsToShow(['5'], 5, 8)), []);
});

test('searchQuery asks for every id with OR', () => {
  const { searchQuery } = load();
  assert.equal(searchQuery(['11', '22']), 'id:11 OR id:22');
});

test('orderByIds sorts by history order and puts unknown ids last', () => {
  const { orderByIds } = load();
  const item = (id) => ({ dataset: { productId: id } });
  const sorted = orderByIds([item('1'), item('9'), item('3')], ['3', '1']);
  assert.deepEqual(plain(sorted.map((entry) => entry.dataset.productId)), ['3', '1', '9']);
});

test('readHistory survives garbage, a non-array and a storage that throws', () => {
  const { readHistory, STORAGE_KEY } = load();
  const storage = (value) => ({ getItem: (key) => (key === STORAGE_KEY ? value : null) });
  assert.deepEqual(plain(readHistory(storage('["3",2]'))), ['3', '2']);
  assert.deepEqual(plain(readHistory(storage('{not json'))), []);
  assert.deepEqual(plain(readHistory(storage('{"a":1}'))), []);
  assert.deepEqual(plain(readHistory(storage(null))), []);
  assert.deepEqual(plain(readHistory({ getItem() { throw new Error('SecurityError'); } })), []);
});

test('writeHistory does not throw when storage refuses the write', () => {
  const { writeHistory } = load();
  assert.doesNotThrow(() => writeHistory({ setItem() { throw new Error('QuotaExceededError'); } }, ['1']));
});

test('TabLoader fetches a tab once and answers later loads from memory', async () => {
  const { TabLoader } = load();
  const urls = [];
  const loader = new TabLoader(async (url) => { urls.push(url); return `<p>${url}</p>`; });
  assert.equal(await loader.load('related', '/a'), '<p>/a</p>');
  assert.equal(await loader.load('related', '/a'), '<p>/a</p>');
  assert.deepEqual(plain(urls), ['/a']);
});

test('TabLoader shares one request between two loads of the same tab', async () => {
  const { TabLoader } = load();
  let calls = 0;
  const loader = new TabLoader(async () => { calls += 1; return 'html'; });
  await Promise.all([loader.load('related', '/a'), loader.load('related', '/a')]);
  assert.equal(calls, 1);
});

test('TabLoader answers null to a load that a later tab overtook', async () => {
  const { TabLoader } = load();
  let release;
  const slow = new Promise((resolve) => { release = resolve; });
  const loader = new TabLoader((url) => (url === '/slow' ? slow : Promise.resolve('fast')));
  const first = loader.load('related', '/slow');
  assert.equal(await loader.load('recently_viewed', '/fast'), 'fast');
  release('slow');
  assert.equal(await first, null);
  assert.equal(await loader.load('related', '/slow'), 'slow');
});

test('TabLoader does not keep a failed request, so the next load retries', async () => {
  const { TabLoader } = load();
  let calls = 0;
  const loader = new TabLoader(async () => { calls += 1; if (calls === 1) throw new Error('offline'); return 'html'; });
  await assert.rejects(loader.load('related', '/a'), /offline/);
  assert.equal(await loader.load('related', '/a'), 'html');
  assert.equal(calls, 2);
});
```

- [ ] **Bước 2:** `node --test tests/unit/product-recommendations-tabs.test.js` → **fail**, mọi case báo
  `ENOENT … assets/product-recommendations-tabs.js`.
- [ ] **Bước 3 — phần helper của file JS** (custom element thêm ở Task 5, sau dòng `if (!window.customElements …) return;`):

```js
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
})();
```

- [ ] **Bước 4:** `node --test tests/unit/product-recommendations-tabs.test.js` → **pass 10/10**.
- [ ] **Bước 5 — mutation, mỗi cái phải đỏ:**

```bash
tools/run mutate assets/product-recommendations-tabs.js --sub 'id !== current)=>true)' -- node --test tests/unit/product-recommendations-tabs.test.js
# (OLD không được chứa "=>": mutate tách OLD/NEW ở "=>" đầu tiên — tools/mutate/main.py:71)
# kỳ vọng: đỏ ở "idsToShow leaves out the product being viewed"
tools/run mutate assets/product-recommendations-tabs.js --sub 'return this.latest === key ? html : null;=>return html;' -- node --test tests/unit/product-recommendations-tabs.test.js
# kỳ vọng: đỏ ở "TabLoader answers null to a load that a later tab overtook"
```

- [ ] **Bước 6 — lệnh test của project gồm unit test (D-9):** `flow.config.json` →
  `"test": "node --test 'tests/guards/*.test.js' 'tests/unit/*.test.js'"`; CLAUDE.md khối Commands thay
  dòng `node --test 'tests/guards/*.test.js'` bằng
  `node --test 'tests/guards/*.test.js' 'tests/unit/*.test.js'   # guards + unit tests of assets/*.js`.
  Chạy lệnh đó → guard 7/7 (6 cũ + locale-parity) + unit 10/10. `tools/run js-syntax` → 38 file, clean.

---

### Task 4: Section Liquid, schema, chuỗi dịch, đặt vào trang sản phẩm (spec §2.1, §2.6, §3, OQ-1, OQ-2, OQ-8, OQ-9)

**Files:** Create `sections/product-recommendations-tabs.liquid`, `assets/section-product-recommendations-tabs.css`
(khung, Task 6 hoàn thiện); Modify `locales/en.default.json`, `locales/vi.json`, `locales/en.default.schema.json`,
`templates/product.json` (dòng 92–114).

**Interfaces:** Produces markup và hook ở bảng "Tên dùng chung"; ba ngữ cảnh render ở bảng "Request".

- [ ] **Bước 1 — đỏ:** trang sản phẩm chưa có section này; `curl -s "http://127.0.0.1:9292/products/<handle>?section_id=product-recommendations-tabs" -o /dev/null -w '%{http_code}'` → `404`.
- [ ] **Bước 2 — section:**

```liquid
{{ 'component-card.css' | asset_url | stylesheet_tag }}
{{ 'component-price.css' | asset_url | stylesheet_tag }}
{{ 'component-slider.css' | asset_url | stylesheet_tag }}
{{ 'section-product-recommendations-tabs.css' | asset_url | stylesheet_tag }}
<script src="{{ 'product-recommendations-tabs.js' | asset_url }}" defer="defer"></script>

{%- style -%}
  .section-{{ section.id }}-padding {
    padding-top: {{ section.settings.padding_top | times: 0.75 | round: 0 }}px;
    padding-bottom: {{ section.settings.padding_bottom | times: 0.75 | round: 0 }}px;
  }

  @media screen and (min-width: 750px) {
    .section-{{ section.id }}-padding {
      padding-top: {{ section.settings.padding_top }}px;
      padding-bottom: {{ section.settings.padding_bottom }}px;
    }
  }
{%- endstyle -%}

{%- liquid
  # The same section answers three requests: the product page (an empty panel), the Product
  # Recommendations API (related cards) and the search page queried by id (viewed cards).
  assign panel_type = blank
  if recommendations.performed
    assign panel_type = 'related'
    assign panel_products = recommendations.products
  elsif search.performed
    assign panel_type = 'recently_viewed'
    assign panel_products = search.results
  endif
-%}

{%- if section.blocks.size == 0 -%}
  {%- if request.design_mode -%}
    <div class="page-width section-{{ section.id }}-padding">
      <p class="product-recommendations-tabs__message">
        {{ 'sections.product_recommendations_tabs.add_block' | t }}
      </p>
    </div>
  {%- endif -%}
{%- else -%}
  <div class="color-{{ section.settings.color_scheme }} gradient">
    <product-recommendations-tabs
      class="product-recommendations-tabs page-width section-{{ section.id }}-padding isolate"
      data-section-id="{{ section.id }}"
      data-product-id="{{ product.id }}"
      data-limit="{{ section.settings.products_to_show }}"
      data-recommendations-url="{{ routes.product_recommendations_url }}"
      data-search-url="{{ routes.search_url }}"
    >
      {%- if section.settings.heading != blank -%}
        <h2 class="product-recommendations-tabs__heading inline-richtext h2">{{ section.settings.heading }}</h2>
      {%- endif -%}
      {%- if section.settings.description != blank -%}
        <div class="product-recommendations-tabs__description rte">{{ section.settings.description }}</div>
      {%- endif -%}

      <div class="product-recommendations-tabs__bar">
        <div
          class="product-recommendations-tabs__tabs"
          role="tablist"
          aria-label="{{ 'sections.product_recommendations_tabs.tabs_label' | t }}"
        >
          {%- for block in section.blocks -%}
            {%- liquid
              case block.type
                when 'related'
                  assign default_label = 'sections.product_recommendations_tabs.related_label' | t
                when 'recently_viewed'
                  assign default_label = 'sections.product_recommendations_tabs.recently_viewed_label' | t
              endcase
              assign label = block.settings.label | default: default_label
            -%}
            <button
              type="button"
              role="tab"
              id="ProductRecommendationsTab-{{ block.id }}"
              class="product-recommendations-tabs__tab"
              aria-selected="{% if forloop.first %}true{% else %}false{% endif %}"
              aria-controls="ProductRecommendationsPanel-{{ section.id }}"
              tabindex="{% if forloop.first %}0{% else %}-1{% endif %}"
              data-tab-type="{{ block.type }}"
              data-block-id="{{ block.id }}"
              {{ block.shopify_attributes }}
            >
              {{ label | escape }}
            </button>
          {%- endfor -%}
        </div>
        {%- if section.settings.link_label != blank and section.settings.link_url != blank -%}
          <a href="{{ section.settings.link_url }}" class="product-recommendations-tabs__link link underlined-link">
            {{- section.settings.link_label | escape -}}
          </a>
        {%- endif -%}
      </div>

      <div
        id="ProductRecommendationsPanel-{{ section.id }}"
        class="product-recommendations-tabs__panel"
        role="tabpanel"
        aria-labelledby="ProductRecommendationsTab-{{ section.blocks.first.id }}"
        data-panel
      >
        {%- if panel_type != blank -%}
          {%- liquid
            assign panel_block = section.blocks | where: 'type', panel_type | first
            if panel_type == 'related'
              assign empty_default = 'sections.product_recommendations_tabs.related_empty' | t
            else
              assign empty_default = 'sections.product_recommendations_tabs.recently_viewed_empty' | t
            endif
            assign empty_message = panel_block.settings.empty_message | default: empty_default
            assign products_count = panel_products.size
            if products_count > section.settings.products_to_show
              assign products_count = section.settings.products_to_show
            endif
            assign columns_mobile_int = section.settings.columns_mobile | plus: 0
            assign show_desktop_slider = false
            assign show_mobile_slider = false
            if section.settings.display_style == 'carousel'
              if products_count > section.settings.columns_desktop
                assign show_desktop_slider = true
              endif
              if products_count > columns_mobile_int
                assign show_mobile_slider = true
              endif
            endif
          -%}
          <div data-panel-content="{{ panel_type }}">
            {%- if products_count > 0 -%}
              <slider-component class="slider-mobile-gutter{% if show_desktop_slider %} slider-component-desktop{% endif %}">
                <ul
                  id="Slider-{{ section.id }}"
                  class="grid product-grid contains-card contains-card--product{% if settings.card_style == 'standard' %} contains-card--standard{% endif %} grid--{{ section.settings.columns_desktop }}-col-desktop grid--{{ section.settings.columns_mobile }}-col-tablet-down{% if show_mobile_slider or show_desktop_slider %} slider{% if show_desktop_slider %} slider--desktop{% endif %}{% if show_mobile_slider %} slider--tablet grid--peek{% endif %}{% endif %}"
                  role="list"
                  aria-label="{{ 'general.slider.name' | t }}"
                >
                  {%- assign skip_card_product_styles = false -%}
                  {%- for card_product in panel_products limit: section.settings.products_to_show -%}
                    <li
                      id="Slide-{{ section.id }}-{{ forloop.index }}"
                      class="grid__item{% if show_mobile_slider or show_desktop_slider %} slider__slide{% endif %}"
                      data-product-id="{{ card_product.id }}"
                    >
                      {% render 'card-product',
                        card_product: card_product,
                        media_aspect_ratio: section.settings.image_ratio,
                        image_shape: 'default',
                        show_secondary_image: section.settings.show_secondary_image,
                        show_vendor: section.settings.show_vendor,
                        show_rating: false,
                        skip_styles: skip_card_product_styles,
                        section_id: section.id,
                        product_view_context: 'recommendation'
                      %}
                    </li>
                    {%- assign skip_card_product_styles = true -%}
                  {%- endfor -%}
                </ul>
                {%- if show_mobile_slider or show_desktop_slider -%}
                  <div class="slider-buttons">
                    <button
                      type="button"
                      class="slider-button slider-button--prev"
                      name="previous"
                      aria-label="{{ 'general.slider.previous_slide' | t }}"
                      aria-controls="Slider-{{ section.id }}"
                    >
                      <span class="svg-wrapper">{{- 'icon-caret.svg' | inline_asset_content -}}</span>
                    </button>
                    <div class="slider-counter caption">
                      <span class="slider-counter--current">1</span>
                      <span aria-hidden="true"> / </span>
                      <span class="visually-hidden">{{ 'general.slider.of' | t }}</span>
                      <span class="slider-counter--total">{{ products_count }}</span>
                    </div>
                    <button
                      type="button"
                      class="slider-button slider-button--next"
                      name="next"
                      aria-label="{{ 'general.slider.next_slide' | t }}"
                      aria-controls="Slider-{{ section.id }}"
                    >
                      <span class="svg-wrapper">{{- 'icon-caret.svg' | inline_asset_content -}}</span>
                    </button>
                  </div>
                {%- endif -%}
              </slider-component>
            {%- else -%}
              <p class="product-recommendations-tabs__message">{{ empty_message | escape }}</p>
            {%- endif -%}
            <p class="visually-hidden" data-announce>
              {%- if products_count > 0 -%}
                {{- 'sections.product_recommendations_tabs.products_count' | t: count: products_count -}}
              {%- else -%}
                {{- empty_message | escape -}}
              {%- endif -%}
            </p>
          </div>
        {%- else -%}
          <noscript>
            <p class="product-recommendations-tabs__message">
              {{ 'sections.product_recommendations_tabs.noscript' | t }}
            </p>
          </noscript>
        {%- endif -%}
      </div>

      {%- for block in section.blocks -%}
        {%- liquid
          case block.type
            when 'related'
              assign empty_default = 'sections.product_recommendations_tabs.related_empty' | t
            when 'recently_viewed'
              assign empty_default = 'sections.product_recommendations_tabs.recently_viewed_empty' | t
          endcase
          assign empty_message = block.settings.empty_message | default: empty_default
        -%}
        <template data-empty-message="{{ block.type }}">
          <p class="product-recommendations-tabs__message">{{ empty_message | escape }}</p>
          <p class="visually-hidden" data-announce>{{ empty_message | escape }}</p>
        </template>
      {%- endfor -%}
      <template data-error-message>
        <p class="product-recommendations-tabs__message">{{ 'sections.product_recommendations_tabs.error' | t }}</p>
        <p class="visually-hidden" data-announce>{{ 'sections.product_recommendations_tabs.error' | t }}</p>
      </template>
      <p class="visually-hidden" aria-live="polite" data-live></p>
    </product-recommendations-tabs>
  </div>
{%- endif -%}

{% schema %}
{
  "name": "t:sections.product-recommendations-tabs.name",
  "tag": "section",
  "class": "section",
  "enabled_on": {
    "templates": ["product"]
  },
  "max_blocks": 2,
  "settings": [
    {
      "type": "inline_richtext",
      "id": "heading",
      "default": "You may also like",
      "label": "t:sections.product-recommendations-tabs.settings.heading.label"
    },
    {
      "type": "richtext",
      "id": "description",
      "label": "t:sections.product-recommendations-tabs.settings.description.label"
    },
    {
      "type": "text",
      "id": "link_label",
      "label": "t:sections.product-recommendations-tabs.settings.link_label.label",
      "info": "t:sections.product-recommendations-tabs.settings.link_label.info"
    },
    {
      "type": "url",
      "id": "link_url",
      "label": "t:sections.product-recommendations-tabs.settings.link_url.label"
    },
    {
      "type": "select",
      "id": "display_style",
      "options": [
        { "value": "carousel", "label": "t:sections.product-recommendations-tabs.settings.display_style.options__1.label" },
        { "value": "grid", "label": "t:sections.product-recommendations-tabs.settings.display_style.options__2.label" }
      ],
      "default": "carousel",
      "label": "t:sections.product-recommendations-tabs.settings.display_style.label"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "min": 2,
      "max": 10,
      "step": 1,
      "default": 8,
      "label": "t:sections.product-recommendations-tabs.settings.products_to_show.label",
      "info": "t:sections.product-recommendations-tabs.settings.products_to_show.info"
    },
    {
      "type": "range",
      "id": "columns_desktop",
      "min": 2,
      "max": 6,
      "step": 1,
      "default": 4,
      "label": "t:sections.product-recommendations-tabs.settings.columns_desktop.label",
      "info": "t:sections.product-recommendations-tabs.settings.columns_desktop.info"
    },
    {
      "type": "select",
      "id": "columns_mobile",
      "options": [
        { "value": "1", "label": "t:sections.related-products.settings.columns_mobile.options__1.label" },
        { "value": "2", "label": "t:sections.related-products.settings.columns_mobile.options__2.label" }
      ],
      "default": "2",
      "label": "t:sections.product-recommendations-tabs.settings.columns_mobile.label"
    },
    {
      "type": "header",
      "content": "t:sections.product-recommendations-tabs.settings.header__card.content"
    },
    {
      "type": "select",
      "id": "image_ratio",
      "options": [
        { "value": "adapt", "label": "t:sections.related-products.settings.image_ratio.options__1.label" },
        { "value": "portrait", "label": "t:sections.related-products.settings.image_ratio.options__2.label" },
        { "value": "square", "label": "t:sections.related-products.settings.image_ratio.options__3.label" }
      ],
      "default": "square",
      "label": "t:sections.related-products.settings.image_ratio.label"
    },
    {
      "type": "checkbox",
      "id": "show_secondary_image",
      "default": false,
      "label": "t:sections.related-products.settings.show_secondary_image.label"
    },
    {
      "type": "checkbox",
      "id": "show_vendor",
      "default": false,
      "label": "t:sections.related-products.settings.show_vendor.label"
    },
    {
      "type": "header",
      "content": "t:sections.product-recommendations-tabs.settings.header__section.content"
    },
    {
      "type": "color_scheme",
      "id": "color_scheme",
      "label": "t:sections.all.colors.label",
      "default": "scheme-1"
    },
    {
      "type": "range",
      "id": "padding_top",
      "min": 0,
      "max": 100,
      "step": 4,
      "unit": "px",
      "label": "t:sections.all.padding.padding_top",
      "default": 36
    },
    {
      "type": "range",
      "id": "padding_bottom",
      "min": 0,
      "max": 100,
      "step": 4,
      "unit": "px",
      "label": "t:sections.all.padding.padding_bottom",
      "default": 36
    }
  ],
  "blocks": [
    {
      "type": "related",
      "name": "t:sections.product-recommendations-tabs.blocks.related.name",
      "limit": 1,
      "settings": [
        {
          "type": "text",
          "id": "label",
          "label": "t:sections.product-recommendations-tabs.blocks.related.settings.label.label",
          "info": "t:sections.product-recommendations-tabs.blocks.related.settings.label.info"
        },
        {
          "type": "text",
          "id": "empty_message",
          "label": "t:sections.product-recommendations-tabs.blocks.related.settings.empty_message.label",
          "info": "t:sections.product-recommendations-tabs.blocks.related.settings.empty_message.info"
        }
      ]
    },
    {
      "type": "recently_viewed",
      "name": "t:sections.product-recommendations-tabs.blocks.recently_viewed.name",
      "limit": 1,
      "settings": [
        {
          "type": "paragraph",
          "content": "t:sections.product-recommendations-tabs.blocks.recently_viewed.settings.paragraph.content"
        },
        {
          "type": "text",
          "id": "label",
          "label": "t:sections.product-recommendations-tabs.blocks.recently_viewed.settings.label.label",
          "info": "t:sections.product-recommendations-tabs.blocks.recently_viewed.settings.label.info"
        },
        {
          "type": "text",
          "id": "empty_message",
          "label": "t:sections.product-recommendations-tabs.blocks.recently_viewed.settings.empty_message.label",
          "info": "t:sections.product-recommendations-tabs.blocks.recently_viewed.settings.empty_message.info"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "t:sections.product-recommendations-tabs.presets.name",
      "blocks": [{ "type": "related" }, { "type": "recently_viewed" }]
    }
  ]
}
{% endschema %}
```

- [ ] **Bước 3 — khung CSS** `assets/section-product-recommendations-tabs.css` (Task 6 hoàn thiện):

```css
.product-recommendations-tabs__bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem 2rem;
  margin-bottom: 2rem;
}

.product-recommendations-tabs__panel[aria-busy='true'] {
  opacity: 0.5;
  pointer-events: none;
}

.product-recommendations-tabs__message {
  margin: 0;
  padding: 2rem 0;
}
```

- [ ] **Bước 4 — chuỗi schema** vào `locales/en.default.schema.json` → `sections`, khoá
  `product-recommendations-tabs` (thứ tự chữ cái như Dawn):

```json
"product-recommendations-tabs": {
  "name": "Product recommendations",
  "settings": {
    "heading": { "label": "Heading" },
    "description": { "label": "Description" },
    "link_label": { "label": "Link label", "info": "Shown on the right of the buttons. Leave blank to hide the link." },
    "link_url": { "label": "Link" },
    "display_style": { "label": "Layout", "options__1": { "label": "Carousel" }, "options__2": { "label": "Grid" } },
    "products_to_show": { "label": "Maximum products", "info": "Applies to each button. Shopify returns at most 10 related products." },
    "columns_desktop": { "label": "Products per row on desktop", "info": "With Carousel, how many products are visible at once." },
    "columns_mobile": { "label": "Products per row on mobile" },
    "header__card": { "content": "Product card" },
    "header__section": { "content": "Section" }
  },
  "blocks": {
    "related": {
      "name": "Related products",
      "settings": {
        "label": { "label": "Button text", "info": "Leave blank to show \"Related products\" in the shopper's language." },
        "empty_message": { "label": "Message when there are no products", "info": "Leave blank to use the theme's message in the shopper's language." }
      }
    },
    "recently_viewed": {
      "name": "Recently viewed",
      "settings": {
        "paragraph": { "content": "Saved in each shopper's browser. The product being viewed is left out." },
        "label": { "label": "Button text", "info": "Leave blank to show \"Recently viewed\" in the shopper's language." },
        "empty_message": { "label": "Message when there are no products", "info": "Leave blank to use the theme's message in the shopper's language." }
      }
    }
  },
  "presets": { "name": "Product recommendations" }
}
```

- [ ] **Bước 5 — mọi khoá `t:` của schema có thật:**

```bash
node -e "
const fs=require('fs');const s=fs.readFileSync('sections/product-recommendations-tabs.liquid','utf8');
const schema=JSON.parse(s.slice(s.indexOf('{% schema %}')+12,s.indexOf('{% endschema %}')));
const loc=JSON.parse(fs.readFileSync('locales/en.default.schema.json','utf8'));
const keys=[...JSON.stringify(schema).matchAll(/\"t:([^\"]+)\"/g)].map(m=>m[1]);
const missing=keys.filter(k=>typeof k.split('.').reduce((n,p)=>n&&n[p],loc)!=='string');
console.log(keys.length,'keys, missing:',missing);"
# kỳ vọng: "… keys, missing: []"
```

- [ ] **Bước 6 — đỏ của guard `locale-parity`:** thêm khối storefront vào `locales/en.default.json` →
  `sections`, khoá `product_recommendations_tabs` (bảng "Khoá locale mới", `products_count` có `one` và
  `other`). Chạy `node --test tests/guards/locale-parity.test.js` → **fail**, `missing` liệt kê đúng
  9 khoá `sections.product_recommendations_tabs.*`.
- [ ] **Bước 7 — xanh:** thêm cùng khối vào `locales/vi.json`, `products_count` chỉ có
  `"other": "{{ count }} sản phẩm"`. `node --test tests/guards/locale-parity.test.js` → pass.
- [ ] **Bước 8 — guard `section-blocks` và mutation:** `node --test tests/guards/section-blocks.test.js` → pass;
  `tools/run mutate sections/product-recommendations-tabs.liquid --sub "when 'recently_viewed'=>when 'viewed'" -- node --test tests/guards/section-blocks.test.js`
  → đỏ, nêu `product-recommendations-tabs.liquid: recently_viewed`.
- [ ] **Bước 9 — đặt section vào trang sản phẩm (OQ-8, D-13):** section render bằng tên file thì không có
  block (block chỉ có trong template), nên phải đặt vào `templates/product.json` trước khi kiểm. Thay instance
  `related-products` (dòng 92–112) bằng:

```json
"product-recommendations-tabs": {
  "type": "product-recommendations-tabs",
  "blocks": {
    "related": { "type": "related", "settings": {} },
    "recently_viewed": { "type": "recently_viewed", "settings": {} }
  },
  "block_order": ["related", "recently_viewed"],
  "settings": {
    "heading": "You may also like",
    "description": "",
    "link_label": "Discover our latest products",
    "link_url": "shopify://collections/all",
    "display_style": "carousel",
    "products_to_show": 8,
    "columns_desktop": 4,
    "columns_mobile": "2",
    "image_ratio": "square",
    "show_secondary_image": true,
    "show_vendor": true,
    "color_scheme": "scheme-1",
    "padding_top": 36,
    "padding_bottom": 36
  }
}
```

  và `order` thành `["main", "product-recommendations-tabs", "disclosures"]`. `git diff templates/product.json`
  chỉ có hai chỗ đó. Trang sản phẩm: section mới ngay dưới thông tin sản phẩm, không còn "You may also like"
  của Dawn ở cuối trang.
- [ ] **Bước 10 — ba ngữ cảnh, trước khi có JS:** lấy id instance thật từ HTML trang sản phẩm.

```bash
B=http://127.0.0.1:9292; H=<handle một sản phẩm>; ID=<id sản phẩm đó>; ID2=<id sản phẩm khác>
SID=$(curl -s "$B/products/$H" | grep -oE 'template--[0-9]+__product-recommendations-tabs' | head -1)
curl -s "$B/products/$H?section_id=$SID" | grep -c 'role="tab"'          # kỳ vọng 2
curl -s "$B/recommendations/products?product_id=$ID&limit=8&intent=related&section_id=$SID" | grep -o 'data-panel-content="[a-z_]*"'   # kỳ vọng data-panel-content="related"
curl -s "$B/search?type=product&options%5Bunavailable_products%5D=show&q=id:$ID2&section_id=$SID" | grep -cE 'data-panel-content="recently_viewed"|data-product-id="'"$ID2"'"'   # kỳ vọng 2
curl -s "$B/search?type=product&options%5Bunavailable_products%5D=show&q=id:$ID2&section_id=$SID" | grep -c 'card__vendor'   # kỳ vọng ≥ 1: show_vendor của template được giữ
```

  **Dừng nếu** dòng thứ ba không ra `2` (ví dụ `enabled_on` làm Shopify từ chối render section trên
  trang search, hoặc `search` không có trong section): ghi kết quả vào ledger và đưa người dùng phương
  án B của D-2 (một request `/products/<handle>?section_id=…` mỗi sản phẩm) trước khi làm tiếp.
- [ ] **Bước 11:** `shopify theme check --fail-level error` → 0 error, 9 warning (không thêm warning
  ở file mới); page text không có `Liquid error`, `Translation missing`.

---

### Task 5: Custom element — tải lười, đổi tab, cache, editor (spec §2.2, §2.4, §2.6–2.8, D-6, D-8, D-11, D-12)

**Files:** Modify `assets/product-recommendations-tabs.js` (thêm sau dòng
`if (!window.customElements || …) return;` của Task 3).

**Interfaces:** Consumes helper Task 3, markup Task 4.

- [ ] **Bước 1 — đỏ (trình duyệt):** trang sản phẩm đã có section (Task 4 bước 9): bấm nút thứ hai →
  không có gì đổi; panel trống; console không lỗi.
- [ ] **Bước 2 — custom element:**

```js
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
    connectedCallback() {
      this.tabs = Array.from(this.querySelectorAll('[role="tab"]'));
      this.panel = this.querySelector('[data-panel]');
      this.live = this.querySelector('[data-live]');
      if (!this.tabs.length || !this.panel) return;

      this.loader = new TabLoader(fetchHtml);
      const store = storage();
      this.history = store ? readHistory(store) : [];
      if (store && this.dataset.productId) writeHistory(store, updateHistory(this.history, this.dataset.productId));

      this.onClick = (event) => this.select(event.currentTarget, { announce: true });
      this.onKeydown = this.onKeydown.bind(this);
      this.onBlockSelect = this.onBlockSelect.bind(this);
      this.tabs.forEach((tab) => tab.addEventListener('click', this.onClick));
      this.querySelector('[role="tablist"]').addEventListener('keydown', this.onKeydown);
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

    async select(tab, { focus = false, announce = false } = {}) {
      this.observer?.disconnect();
      this.tabs.forEach((item) => {
        const selected = item === tab;
        item.setAttribute('aria-selected', String(selected));
        item.tabIndex = selected ? 0 : -1;
      });
      this.panel.setAttribute('aria-labelledby', tab.id);
      if (focus) tab.focus();

      const type = tab.dataset.tabType;
      const url = this.urlFor(type);
      if (!url) {
        // An earlier tab may still be loading; its own finally leaves the busy state to the tab now shown.
        this.panel.removeAttribute('aria-busy');
        this.show(this.template(`[data-empty-message="${type}"]`), announce);
        return;
      }

      this.panel.setAttribute('aria-busy', 'true');
      try {
        const html = await this.loader.load(type, url);
        if (html !== null) this.show(this.extract(html, type), announce);
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

    onKeydown(event) {
      const index = this.tabs.indexOf(document.activeElement);
      if (index === -1) return;
      const target = { ArrowRight: index + 1, ArrowLeft: index - 1, Home: 0, End: this.tabs.length - 1 }[event.key];
      if (target === undefined) return;
      event.preventDefault();
      this.select(this.tabs[(target + this.tabs.length) % this.tabs.length], { focus: true, announce: true });
    }

    onBlockSelect(event) {
      const tab = this.tabs.find((item) => item.dataset.blockId === event.detail?.blockId);
      if (tab) this.select(tab);
    }
  }

  customElements.define('product-recommendations-tabs', ProductRecommendationsTabsElement);
```

  Đầu IIFE (sau `const HISTORY_SIZE`) không cần thêm gì; class dùng tên helper trực tiếp vì cùng scope.
- [ ] **Bước 3:** `tools/run js-syntax` → clean; `node --test 'tests/unit/*.test.js'` → 10/10 (phần element
  không chạy trong vm vì thiếu `customElements`).
- [ ] **Bước 4 — xanh, lazy load (spec §5.5):** mở trang sản phẩm ở 1440 px, **không cuộn**:
  `performance.getEntriesByType('resource').filter(e => /recommendations\/products|\/search\?/.test(e.name)).length`
  → `0`. Cuộn tới section → `1` (related). Bấm "Recently viewed" → `2` (hoặc vẫn `1` nếu chưa có lịch
  sử — khi đó panel hiện câu báo trống). Bấm qua lại 4 lần → vẫn như cũ. Không lần tải lại trang
  (`performance.getEntriesByType('navigation').length` = 1).
- [ ] **Bước 5 — "đã xem":** mở lần lượt 5 sản phẩm khác, rồi sản phẩm thứ 6: tab "Recently viewed"
  hiện 5 card, sản phẩm mở gần nhất đứng đầu, không có sản phẩm đang xem; `localStorage` khoá
  `product-recommendations-tabs:viewed` có 6 id, sản phẩm đang xem đứng đầu.
- [ ] **Bước 6 — request sau cùng thắng:** DevTools throttle không có trong MCP, nên thử bằng cách bấm
  "Related" rồi "Recently viewed" ngay trong cùng một lệnh JS
  (`tabs[0].click(); tabs[1].click()`); chờ 3 giây → panel là của "Recently viewed", `aria-selected`
  đúng nút thứ hai, panel không còn `aria-busy`. Lặp lại khi chưa có lịch sử xem (xoá khoá `localStorage`,
  tải lại): bấm "Related" rồi ngay "Recently viewed" → câu báo trống, **không** `aria-busy` (lỗi đã thấy
  lúc viết plan: nhánh không gửi request phải tự xoá trạng thái đang tải).
- [ ] **Bước 7 — lỗi request:** trong console thay tạm `window.fetch = () => Promise.reject(new Error('offline'))`
  trước khi bấm nút chưa tải → câu báo lỗi; khôi phục `fetch`, bấm lại → tải được (unit test đã chứng
  minh không cache lỗi; bước này chứng minh markup).
- [ ] **Bước 8 — Review Focus 1:** đặt `localStorage['product-recommendations-tabs:viewed']` =
  `["<id sp 1>","999999999999","<id sp 2>"]`, tải lại một sản phẩm thứ ba → tab "đã xem" có 2 card theo
  đúng thứ tự sp 1, sp 2; không ô trống.
- [ ] **Bước 9 — Review Focus 2:** đặt giá trị khoá thành `{not json` → tải lại: không lỗi console; tab
  "đã xem" chỉ có sản phẩm vừa ghi (vì lịch sử hỏng được coi là rỗng rồi ghi lại).
- [ ] **Bước 10 — bàn phím và trình đọc màn hình:** Tab vào nút đầu; mũi tên phải → nút hai được chọn và
  focus; `[data-live]` có chữ "N products" hoặc câu báo trống; mũi tên trái về lại nút đầu.
- [ ] **Bước 11 — Review Focus 4 (editor):** trong theme editor của development theme: bấm block
  "Recently viewed" ở sidebar → preview chuyển sang tab đó; kéo block đổi thứ tự → tab đầu là block mới
  đầu; xoá một block → còn một nút; xoá cả hai → preview chỉ còn dòng nhắc, storefront (tab ẩn danh)
  không có section. Thêm lại hai block. Đổi một setting bất kỳ → section render lại, đổi tab vẫn chạy.

---

### Task 6: Giao diện theo design, carousel và grid (spec §2.1, §2.5, OQ-7, OQ-9)

**Files:** Modify `assets/section-product-recommendations-tabs.css`.

- [ ] **Bước 1 — đỏ:** ảnh 1440 px sau Task 5: nút là nút mặc định của trình duyệt, không có nền đen,
  không in hoa (lưu `evidence/task6-before-1440.png`).
- [ ] **Bước 2 — CSS nút và link** (thêm vào file của Task 4):

```css
.product-recommendations-tabs__heading {
  margin: 0 0 1rem;
}

.product-recommendations-tabs__description {
  margin-bottom: 2rem;
}

.product-recommendations-tabs__tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.product-recommendations-tabs__tab {
  padding: 0.4rem 0.8rem;
  border: 0.1rem solid rgba(var(--color-foreground), 0.2);
  background: rgb(var(--color-background));
  color: rgb(var(--color-foreground));
  font: inherit;
  font-size: 1.3rem;
  letter-spacing: 0.05rem;
  text-transform: uppercase;
  cursor: pointer;
}

.product-recommendations-tabs__tab[aria-selected='true'] {
  border-color: rgb(var(--color-foreground));
  background: rgb(var(--color-foreground));
  color: rgb(var(--color-background));
}

.product-recommendations-tabs__tab:focus-visible {
  outline: 0.2rem solid rgba(var(--color-foreground), 0.5);
  outline-offset: 0.3rem;
}

.product-recommendations-tabs__link {
  font-weight: 600;
  text-underline-offset: 0.3rem;
}
```

- [ ] **Bước 3 — xanh, 1440 px:** nút đang chọn nền đen chữ trắng, nút kia viền mảnh nền trắng, cả hai
  in hoa; link (nếu đặt) nằm cùng hàng bên phải; 4 card một hàng; carousel có nút prev/next (cần > 4
  sản phẩm — dùng tab "Recently viewed" sau Task 5 bước 5). So với `design/carousel-slider.png`, lưu
  `evidence/task6-carousel-1444.png` (cửa sổ 1444 px) và `evidence/task6-grid-1311.png` (đổi
  `display_style` sang Grid trong editor, cửa sổ 1311 px).
- [ ] **Bước 4 — 375 px:** carousel vuốt ngang được (`scrollLeft` đổi sau `slider.scrollBy`), card kế ló ra,
  nút prev/next hiện; grid 2 cột; hàng nút xuống dòng gọn, link xuống dưới nút; không cuộn ngang.
- [ ] **Bước 5 — 750 và 990 px:** như spec §2.5; không cuộn ngang.
- [ ] **Bước 6 — Review Focus 5:** đặt `products_to_show` = 3 (hoặc lịch sử 3 sản phẩm) với 4 cột → không
  có `.slider-buttons`; kéo cửa sổ 1440 → 375 → 1440 khi đang carousel 8 sản phẩm → nút prev mờ ở trang
  đầu, next chạy, bộ đếm đúng sau mỗi lần đổi bề ngang.

---

### Task 7: Kiểm toàn bộ (spec §5, `.claude/rules/shopify-theme.md` §3)

**Files:** tạo `evidence/after-*.png`.

- [ ] **Bước 1:** ảnh `after-1440.png`, `after-990.png`, `after-750.png`, `after-375.png`, cộng
  `after-1444.png` và `after-1311.png` (bề ngang hai ảnh design), cả carousel lẫn grid.
- [ ] **Bước 2 (người dùng, tuỳ chọn):** để tab "Related products" có sản phẩm trên store này (API đang
  trả 0), cài app **Shopify Search & Discovery** và thêm "related products" thủ công cho một sản phẩm.
  *Cần kiểm*: sản phẩm thêm thủ công có trả qua `/recommendations/products?intent=related` không —
  Claude đo bằng `.json` sau khi người dùng làm. Không làm thì tab "Related" chỉ kiểm được câu báo trống.
- [ ] **Bước 3:** page text không có `Liquid error`, `Translation missing` ở trang sản phẩm và `/vi/products/<handle>`;
  console không có lỗi mới so với Task 1.
- [ ] **Bước 4 — Review Focus 3:** ở `/vi/products/<handle>`: hai nút ghi "Sản phẩm liên quan", "Sản phẩm
  đã xem"; request đi qua `/vi/recommendations/products` và `/vi/search` (đọc `performance` entries).
- [ ] **Bước 5 — editor (spec §3, §5.2, §5.4):** "Add section" trên trang sản phẩm có "Product
  recommendations"; trên trang chủ thì không. Đổi từng setting của section và block, preview đổi theo;
  đổi Layout giữa Carousel và Grid; bấm từng block → preview chuyển tab và tô nút.
- [ ] **Bước 6 — lệnh:**

```bash
shopify theme check --fail-level error                     # 0 error, 9 warning
tools/run js-syntax                                        # 38 file, clean
node --test 'tests/guards/*.test.js' 'tests/unit/*.test.js' # guard 7/7, unit 10/10
tools/run change-guards --check                            # clean, 3 guard
tools/run shared-rules                                     # clean
```

- [ ] **Bước 7 — dọn:** không `console.log`, không code bị comment; việc hoãn ghi vào `docs/tech-debt.md`.
- [ ] **Bước 8 — bàn giao, khi người dùng bảo:** commit trên `ex-02-product-recommendations`, push, PR vào
  `main`; sau merge, kiểm theme GitHub bằng link preview.

---

## Trạng thái

| # | Việc | Trạng thái | Bằng chứng |
|---|---|---|---|
| 1 | Branch, baseline, ảnh "trước" | xong | branch `ex-02-product-recommendations` từ `a4cb83d` (bỏ upstream `origin/main` để `git push` trống không nhắm `main`). Baseline: theme check exit 0, 158 file, 9 warning; guard 6/6; js-syntax 37 clean. Ảnh "trước" chụp trên theme GitHub `187488927914` (code `a4cb83d`) vì `theme dev` đang tắt: dưới thông tin sản phẩm chỉ có `related-products` cao 64 px, trống — API trả 0 sản phẩm (`evidence/before-1440.png`, `before-375.png`, `before-page-text.md`) |
| 2 | Guard `locale-parity` | xong | `origin/main`: pass 1/1. Mutation đổi tên `linkedin` trong `vi.json` → đỏ, missing `general.social.links.linkedin`; `other` → `few` ở `blogs.article.comments` → đỏ, missing `blogs.article.comments`; file trả lại. `change-guards` → 3 guard, `--check` clean |
| 3 | Helper thuần + unit test | xong | Trước khi có file JS: 10/10 fail `ENOENT`. Sau: pass 10/10. Mutation `id !== current)` → `true)` → đỏ đúng case `idsToShow` (9/10); `return this.latest === key ? html : null;` → `return html;` → đỏ đúng case "overtook" (9/10). Mutation trong plan cũ chứa `=>` trong OLD nên làm file lỗi cú pháp, đỏ cả 10 — không đo gì, đã viết lại (ledger). Lệnh `test` mới (`flow.config.json`, CLAUDE.md): 17/17 (guard 7 + unit 10); js-syntax 38 clean |
| 4 | Section Liquid, schema, chuỗi dịch, đặt vào `product.json` | xong | Bước 1 (theme GitHub, code gốc): `?section_id=product-recommendations-tabs` → 404. Bước 5: 39 khoá `t:`, missing `[]`. Bước 6: `locale-parity` đỏ, missing đúng 9 khoá `sections.product_recommendations_tabs.*`; bước 7: xanh. Bước 8: `section-blocks` 4/4; mutation của plan (`--sub`) không đỏ vì file có hai `case block.type` mà mutate chỉ thay chỗ đầu, dùng `--drop "when 'recently_viewed'"` → đỏ, nêu `product-recommendations-tabs.liquid → 'recently_viewed'` (ledger). Bước 9: `git diff templates/product.json` chỉ có instance mới và `order` = `main`, `product-recommendations-tabs`, `disclosures`. Bước 11: theme check exit 0, 9 warning ở đúng 8 file của baseline. Bước 10 (`theme dev`, instance `template--27816890466474__product-recommendations-tabs`): trang sản phẩm 2 tab; `/recommendations/products` → `data-panel-content="related"` (API trả 0 → câu báo trống); `/search` `id:` → `data-panel-content="recently_viewed"` + đúng `data-product-id` (2/2, không chạm điểm dừng); vendor hiện (`Vendor:` 1 — `card__vendor` trong plan không phải class của Dawn, ledger). Sáu URL kể cả `/vi/recommendations`, `/vi/search` → 200, 0 `Liquid error`, 0 `Translation missing`; `/vi` ra "Chưa có sản phẩm liên quan.", "1 sản phẩm" |
| 5 | Custom element | xong, chờ người dùng kiểm editor + `localStorage` hỏng | Bước 1 (đỏ): bấm nút hai không đổi gì, panel chỉ `<noscript>`, 0 request. Bước 4: 1440×899 và 375×799 — section nằm trong 400 px nhìn trước (đỉnh 874 / 1118 px) nên tải ngay lúc mở trang, đúng D-12; 1440×399 (đỉnh 812): tải trang 0 request → cuộn 200 px 1 → bấm "Recently viewed" (chưa có lịch sử) vẫn 1, câu báo trống → bấm qua lại 4 lần vẫn 1, 1 navigation. Bước 6: **lỗi trong code plan** — tab không gửi request không qua `TabLoader`, nên response "Related" về muộn vẫn đè panel (đỏ: nút hai được chọn mà panel + live đọc "No related products to show yet."); sửa: chỉ ghi panel khi tab còn được chọn (`this.activeTab() === tab`) → xanh: "Products you view will show up here.", không `aria-busy`. Hai request cùng chờ → panel của tab bấm sau, 6 card. Bước 5: 6 card, mới nhất trước, không có sản phẩm đang xem; search trả theo độ liên quan, JS sắp lại theo lịch sử. Bước 7: lỗi → câu báo lỗi; bấm lại → 6 card. Bước 8 (lịch sử gán trong bộ nhớ element — MCP chặn đọc/ghi `localStorage`): id không tồn tại ở giữa → 2 card đúng thứ tự, không ô trống, "2 products". Bước 9 trên trình duyệt: chờ người dùng (Task 7). Bước 10 (phím tổng hợp): mũi tên, Home, End, quay vòng; `tabindex`, `aria-labelledby`, live đúng. Bước 11 giả lập ngoài editor: `shopify:block:select` → đúng tab; render lại section → vẫn chạy; tạm sửa `product.json` (đã trả lại, `cmp` khớp): đổi thứ tự → tab đầu là block đầu, request đầu là của nó; một block → một nút; không block → section 0 px. Editor thật: chờ người dùng |
| 6 | Giao diện, carousel, grid | xong | Đỏ (`evidence/task6-before-1440.png`): nút mặc định của trình duyệt, và cả section tràn mép vì custom element mặc định là `inline` nên `max-width` của `.page-width` không có tác dụng → thêm `display: block` (như `.related-products` của Dawn; ledger). Carousel của Dawn làm để tràn mép cửa sổ: lề card đầu cộng hai lần (card đầu x 329) → giữ carousel trong `page-width`, thẳng heading như design (ledger). Card khít đúng hàng làm `SliderComponent` đếm thiếu một card mỗi trang (đỏ: 7 sản phẩm → "1 / 5", next tắt ở "4 / 5") → slider vượt mép một khoảng cách + 0.4rem và bị cắt (`overflow-x: clip`) → xanh: "1 / 4" … "4 / 4", mỗi trang đúng 4 card trong 163–1263. 1444 px (`task6-carousel-1444.png`): nút in hoa, nút đang chọn nền #121212 chữ trắng, link đậm gạch chân bên phải, 4 card thẳng heading. 1311 px grid (`task6-grid-1311.png`, tạm đổi `display_style`, đã trả lại, `cmp` khớp): 4 + 3, không nút. Grid 375/750: 2 cột, 990: 4 cột. Carousel 375/750: 2 card + card ló 60 px, vuốt được, có nút, "1 / 6"; 990/1440: "1 / 4" (`task6-carousel-{375,750,990,1440}.png`). Không cuộn ngang ở mọi bề ngang. Review Focus 5: 3 sản phẩm, 4 cột → 1440 không nút, 375 có nút "1 / 2"; đang trang 2 đổi 1440 → 375 → 1440: "2 / 4" → "2 / 6" → "2 / 4". Theme check exit 0, 9 warning, không ở file mới. Khác design: khung nội dung hẹp hơn vì `page_width` 1200 px; nút prev/next nằm dưới danh sách kiểu Dawn, không đè lên mép trái như ảnh |
| 7 | Kiểm toàn bộ | xong phần của Claude; bước 2, 5 chờ người dùng; bước 8 khi người dùng bảo | Bước 1: CSS không đổi sau Task 6 nên ảnh "sau" là `task6-carousel-{375,750,990,1440,1444}.png` và `task6-grid-1311.png` (ledger). Bước 3: trang sản phẩm, gift card, hai trang `/vi` → 200, 0 `Liquid error`, 0 `Translation missing`; console không có lỗi từ code mới (chỉ lỗi có sẵn: Storefront API 400, menu `customer-account-main-menu`, CSP `shop.app`). Bước 4 (Review Focus 3): `/vi` — `lang=vi`, nút "Sản phẩm liên quan" / "Sản phẩm đã xem", nhãn nhóm "Danh sách sản phẩm", câu báo "Chưa có sản phẩm liên quan.", live "7 sản phẩm", nhãn nút trượt tiếng Việt; request qua `/vi/recommendations/products` và `/vi/search`; heading "You may also like" là chữ merchant đặt. Bước 6: theme check exit 0, 159 file, 9 warning; js-syntax 38 clean; `node --test` guard + unit 17/17; `change-guards --check` clean (3 guard); `shared-rules` clean. Bước 7: không `console.log`, không code comment; ba mục `DEFERRED` vào `docs/tech-debt.md` (tab Related có dữ liệu thật, `localStorage` hỏng trên trình duyệt thật, kiểm theme editor) |
| 8 | Review toàn branch | xong, sửa 3 mục | Reviewer mới (opus) trên diff working tree so với `a4cb83d`: 0 Critical, 2 Important, 11 Minor, kết luận "merge được sau khi sửa". Đã sửa, mỗi mục đỏ trước rồi xanh trên trình duyệt: (1) gỡ section ra rồi gắn lại (như editor di chuyển khi đổi thứ tự) làm listener bị gắn đôi và tải lại tab — đỏ: request 1 → 3, mũi tên không chạy; sửa: handler tạo một lần trong `constructor`, gỡ khi ngắt, giữ `TabLoader` → xanh: request 2 → 2, mũi tên chạy. (2) thứ tự template: `disclosures` là thông tin an toàn của chính sản phẩm nên danh sách gợi ý đặt sau nó — `main`, `disclosures`, `product-recommendations-tabs` (OQ-8: "ngay sau phần thông tin sản phẩm"). (3) spec §2.8 ghi "mũi tên chuyển giữa các nút; Enter/Space chọn", plan đã làm mũi tên chọn luôn (mỗi lần bấm một request) — đỏ: `ArrowRight` đổi `aria-selected`; sửa: mũi tên chỉ chuyển focus → xanh: không đổi `aria-selected`, không request; bấm nút → chọn, 1 request. Sau lượt sửa: theme check exit 0 / 9 warning, js-syntax 38, test 17/17, change-guards + shared-rules clean, `/` và `/vi` 0 lỗi. 10 mục Minor hoãn — danh sách trong ledger. Code trong các bước của Task 4 bước 8, Task 5, Task 6 là bản trước các ruling; code thật theo bảng này và ledger |
| 9 | Bàn giao (Task 7 bước 8) | đã commit, chờ người dùng push + PR | 2026-10-02, người dùng chọn commit + PR: `2252cc0` Guard(guards) `locale-parity`, `4c04944` Feature(EX-02), rồi commit Docs(EX-02) gồm spec, plan, ảnh, tech-debt. Shell của Claude không có credential GitHub nên người dùng push và tạo PR trên web (nội dung PR: `.local/pr-ex-02.md`). Sau merge: kiểm theme GitHub `187488927914` bằng link preview |
