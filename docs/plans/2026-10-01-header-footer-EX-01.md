# Plan EX-01 — Header và footer theo design Blakely

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Ngày: 2026-10-01 · Trạng thái: **đã duyệt (Gate 2)** — người dùng, 2026-10-01; chạy native (executing-plans)

**Spec:** [`docs/specs/features/2026-10-01-header-footer-EX-01.md`](../specs/features/2026-10-01-header-footer-EX-01.md) (đã duyệt).
Plan dẫn chiếu mục của spec bằng "spec §x", các quyết định bằng "D-x" (D-1…D-4 ở spec, D-5 trở đi ở plan này).

**Goal:** announcement bar, header và footer của Dawn trên store `ngocmx-training` trông như design
Blakely ở mobile và desktop, cộng ba ý môi trường (dev store, denv, GitHub).

**Architecture:** setting trước (JSON của section group và theme settings), code chỉ ở chỗ setting của
Dawn không làm được (D-2): sửa thẳng `sections/header.liquid`, `sections/footer.liquid`, CSS trong
`assets/base.css` và `assets/section-footer.css`, thêm một setting global LinkedIn, một custom
element nhỏ cho accordion footer, hai chuỗi locale. Không section mới.

**Tech Stack:** Liquid, JSON section groups, CSS, một file JS thuần (custom element), Shopify CLI
4.8.3 (`shopify theme dev`), Node 22 test runner cho guard, chrome-devtools MCP cho bằng chứng
trên trình duyệt.

## Global Constraints

- Theme nền: Dawn v16.0.0. Màu: announcement bar và footer dùng `scheme-4` (#121212, D-4); header
  dùng `scheme-1` (nền trắng).
- Mốc responsive: **dưới 990 px là bố cục mobile** cho cả header lẫn footer, **từ 990 px là
  desktop** (OQ-5). Mốc 750 px của Dawn giữ nguyên ở mọi chỗ khác.
- Chữ shopper đọc đi qua `{{ 'key' | t }}`; khoá mới vào `locales/en.default.json` **và**
  `locales/vi.json` (ngôn ngữ thứ hai, D-5).
- Link từ setting kiểu `url` hoặc `routes`; giá trị merchant nhập được escape; không script từ xa;
  script tải bằng `defer` (`.claude/rules/code-security.md`).
- Không commit, không push khi người dùng chưa bảo; không publish theme; làm qua `shopify theme
  dev` (CLAUDE.md).
- Bằng chứng ảnh chụp lưu ở `docs/exercises/EX-01-header-footer/evidence/`, đường dẫn ghi vào bảng
  trạng thái cuối plan.
- **Số dòng trong plan đo trên Dawn gốc, trước mọi sửa đổi.** Task trước chèn thêm dòng thì số
  dòng ở task sau lệch đi; lúc làm, tìm chỗ sửa theo đoạn code được trích, số dòng chỉ để định vị.

## Review Focus

Năm tình huống spec ngụ ý nhưng không bước test chính nào chạm tới, dễ làm hỏng nhất trước:

1. **Menu header dài ở 990–1200 px** — menu và icon search phải xuống dòng trong cột trái, không
   chạy dưới logo ở giữa. Test: Task 6 bước 6.
2. **Theme editor render lại footer** (đổi một setting footer khi preview ở bề ngang mobile) — các
   accordion vẫn đóng và vẫn bấm mở được, vì custom element chạy lại `connectedCallback`. Test:
   Task 8 bước 7.
3. **Kéo cửa sổ qua mốc 990 px khi một accordion đang mở** — lên desktop thì mọi cột hiện đủ link,
   xuống mobile thì đóng lại, không kẹt ở trạng thái nửa vời. Test: Task 8 bước 8.
4. **Cột menu có tiêu đề để trống** — trên mobile không có dòng accordion rỗng; list hiện luôn.
   Test: Task 8 bước 9.
5. **Trang ở ngôn ngữ thứ hai (`/vi`)** — dòng copyright và nhãn LinkedIn không ra
   `Translation missing`. Shopify.dev không nói storefront có lấy chuỗi của ngôn ngữ mặc định khi
   thiếu hay không, nên khoá được thêm vào `vi.json` và đo trên trang. Test: Task 10 bước 4.

---

## 1. Sai hoặc thiếu cái gì

Đứng ở phía shopper, so với design (spec §2):

- Announcement bar nền trắng, chữ "Welcome to our store" — design: nền đen, "Free standard UK
  shipping on orders over £70".
- Header desktop: logo bên trái, search nằm trong nhóm icon bên phải, account là icon — design: logo
  giữa, search ngay sau menu bên trái, account là chữ "LOG IN".
- Không có logo BLAKELY.
- Footer: nền trắng, có ô đăng ký email, "Follow on Shop", "Powered by Shopify", danh sách policy;
  không có cột menu, không có logo trắng, không có LinkedIn; link không gạch chân; trên mobile không
  có accordion; hàng dưới xếp khác design.
- Môi trường: chưa chạy qua denv, chưa nối GitHub (spec §5).

## 2. Ở đâu (đã đo trên Dawn v16.0.0)

| Chỗ | Đo được |
|---|---|
| `sections/header-group.json` | announcement `color_scheme: scheme-1`, text "Welcome to our store"; header `logo_position: middle-left`, `enable_country_selector: true`, `enable_language_selector: true` |
| `sections/footer-group.json` | `blocks: {}`, `color_scheme: scheme-1`, `newsletter_enable: true`, `enable_follow_on_shop: true`, `show_social: true`, `show_policy: true` |
| `config/settings_data.json` | `"current": "Dawn"` trỏ vào `presets.Dawn`; không có `logo`, `brand_image`; `logo_width: 90` (dòng 14), `brand_image_width: 100` (170), chín social link rỗng (171–179) |
| `sections/header.liquid:151-166` | khối `liquid` tính `social_links`, `country_selector`, `language_selector` |
| `sections/header.liquid:167` | thẻ `<header>` và các class bố cục |
| `sections/header.liquid:216-224` | render menu desktop (`header-dropdown-menu` / `header-mega-menu`) |
| `sections/header.liquid:283` | search trong nhóm icon (`Search-In-Modal`) |
| `sections/header.liquid:285-293` | `<shopify-account>`: icon + nhãn "Log in" ẩn (`customer.log_in`) |
| `assets/base.css:2642-2650` | ≥990 px: search bên trái bị ẩn khi có account, search trong nhóm icon hiện |
| `assets/base.css:2407-2411` | ≥990 px, `middle-center`: lưới `'navigation heading icons'`, cột `1fr auto 1fr` |
| `assets/base.css:2541-2580` | `.header__icon` vuông 4.4rem |
| `assets/base.css:2834-2838` | `.header__menu-item`, chữ thường, màu foreground 75% |
| `sections/footer.liquid:33` | điều kiện "không có social link nào" — liệt kê đủ 9 mạng |
| `sections/footer.liquid:71` | wrapper mỗi block, có `{{ block.shopify_attributes }}` (dòng 72) |
| `sections/footer.liquid:78-80` | tiêu đề block in chung cho mọi loại block |
| `sections/footer.liquid:89-103` | nhánh `when 'link_list'` |
| `sections/footer.liquid:253-321` | hàng dưới: localization trái, payment phải, rồi copyright + "Powered by" + policy ở một hàng riêng |
| `snippets/country-localization.liquid:36-40` | nút ghi "Vietnam \| VND ₫" |
| `assets/section-footer.css` | 7 `max-width: 749px` + 14 `min-width: 750px`: footer đổi bố cục ở 750 px |
| `assets/section-footer.css:338-341` | link footer màu foreground 75%, gạch chân chỉ khi hover (349-355) |
| `config/settings_schema.json:1303-1360` | nhóm Social media: 9 setting kiểu `text`; X/Twitter ở 1330-1335 |
| Social links liệt kê ở | `snippets/social-icons.liquid` (×2 mỗi mạng), `sections/header.liquid` (×2: dòng 153 và JSON-LD 470-478), `sections/footer.liquid` (×1), `sections/announcement-bar.liquid` (×1, dòng 6), `snippets/header-drawer.liquid` (×2), `sections/main-password-footer.liquid` (×2). `snippets/meta-tags.liquid` chỉ đọc X/Twitter — không phải danh sách |
| LinkedIn | 0 kết quả trong cả theme |

## 3. Sửa gì, và cố ý không sửa gì

**Sửa:** các file ở bảng trên, cộng file mới `assets/icon-linkedin.svg`, `assets/footer-accordion.js`,
`tests/guards/social-links.test.js`; khoá locale trong `locales/en.default.json`,
`locales/vi.json`, `locales/en.default.schema.json`. Ba file JSON nội dung (`header-group.json`,
`footer-group.json`, `settings_data.json`) sửa tay vì đề yêu cầu trang mặc định đổi theo design
(D-3, `.claude/rules/shopify-theme.md` §4).

**Cố ý không sửa:**

- Giao diện menu drawer, hộp search, hộp đăng nhập (spec §1 ngoài phạm vi, A-4).
- Bố cục header khác `middle-center` — search cạnh menu chỉ bật cho `middle-center` với menu dạng
  dropdown/mega (D-6); các bố cục khác giữ nguyên Dawn.
- `page_width` (setting global): giữ 1200 trừ khi Task 6 đo được bề ngang header lệch rõ so với
  design — khi đó đưa phương án cho người dùng chọn trước khi đổi, vì nó đổi bề ngang mọi section.
- 49 locale khác ngoài `en.default` và `vi` (D-5).
- Locale schema của các ngôn ngữ admin khác (`*.schema.json` ngoài `en.default`).
- `component-list-social.css` — dùng chung với announcement bar và drawer; căn giữa social của
  footer làm bằng selector riêng của footer.

## 4. Kiểm bằng gì

Theo CLAUDE.md, "test đỏ trước" trong theme này có ba dạng, và plan dùng cả ba:

- **Guard đọc source** cho luật social link: `tests/guards/social-links.test.js` viết trước, đỏ khi
  thêm `social_linkedin_link` vào schema mà chưa thêm vào sáu file, xanh khi đủ. Mutation phải làm
  nó đỏ: bỏ LinkedIn khỏi JSON-LD trong `header.liquid` (đếm 1× so với 2×); bỏ điều kiện LinkedIn
  trong `social-icons.liquid`.
- **Guard có sẵn** `section-blocks` phải vẫn xanh sau khi nhánh `link_list` đổi markup.
- **Trình duyệt** cho markup, CSS và hành vi editor: ảnh chụp **trước** (Task 3) và **sau** ở 375,
  750, 990, 1440 px và ở bề ngang của ảnh design (1218, 1439, 414, 332 px), cộng checklist
  `.claude/rules/shopify-theme.md` §3 và spec §6.
- Lệnh của project: `shopify theme check --fail-level error` (0 error, 9 warning như Dawn gốc),
  `tools/run js-syntax`, `node --test 'tests/guards/*.test.js'`, `tools/run change-guards --check`,
  `tools/run shared-rules`.

---

## Contract — schema

Đây là phần merchant lưu dữ liệu vào; đổi id sau khi merchant đã lưu thì giá trị cũ mất, nên chốt ở
đây trước khi có dòng Liquid nào.

| Nơi | id | type | Ghi chú |
|---|---|---|---|
| `config/settings_schema.json`, nhóm Social media, ngay sau `social_twitter_link` | `social_linkedin_link` | `url` | **mới**. Label `t:settings_schema.social-media.settings.social_linkedin_link.label` = "LinkedIn"; info `…social_linkedin_link.info` = "https://www.linkedin.com/company/shopify". Kiểu `url` thay vì `text` như tám mạng kia: xem D-7 |
| `sections/footer.liquid`, block `link_list`, setting `heading` | (giữ id) | (giữ type) | thêm `"info": "t:sections.footer.blocks.link_list.settings.heading.info"` = "Shown on mobile only, as the title of the collapsible menu." |
| `snippets/country-localization.liquid` | tham số `hide_currency` | Boolean, tuỳ chọn | **mới**. Chỉ `footer.liquid` truyền `true`; ba caller khác không truyền nên nút giữ nguyên |

Khoá locale mới:

| File | Khoá | en | vi |
|---|---|---|---|
| `en.default.json`, `vi.json` | `sections.footer.copyright` | `Copyright {{ shop_name }} {{ year }} \| All rights reserved` | `Bản quyền {{ shop_name }} {{ year }} \| Bảo lưu mọi quyền` |
| `en.default.json`, `vi.json` | `general.social.links.linkedin` | `LinkedIn` | `LinkedIn` |
| `en.default.schema.json` | `settings_schema.social-media.settings.social_linkedin_link.label` / `.info` | `LinkedIn` / `https://www.linkedin.com/company/shopify` | — |
| `en.default.schema.json` | `sections.footer.blocks.link_list.settings.heading.info` | `Shown on mobile only, as the title of the collapsible menu.` | — |

Tên dùng chung giữa các task (Interfaces):

| Tên | Loại | Do task | Dùng ở |
|---|---|---|---|
| `search_beside_menu` | biến Liquid trong `header.liquid` | 6 | 6 |
| `header--search-beside-menu` | class trên `<header>` | 6 | 6 (CSS) |
| `header__navigation` | class wrapper menu + search | 6 | 6 (CSS) |
| `Search-In-Modal-Menu` | `input_id` của search thứ ba | 6 | 6 |
| `header__account-icon`, `header__account-label` | class trong `<shopify-account>` | 7 | 7 (CSS) |
| `footer-accordion` | custom element, `assets/footer-accordion.js` | 8 | 8 |
| `footer-block__accordion`, `footer-block__summary`, `footer-block__toggle-icon--plus/--minus` | class | 8 | 8 (CSS) |
| `footer-block--brand` | class wrapper block brand | 9 | 9 (CSS) |
| `footer__currency` | class | 10 | 10 (CSS) |

## Những đầu phải biết

Theo `.claude/rules/shopify-theme.md` §1 và `docs/architecture/change-guards.json`:

| Thêm | Các đầu | Cái gì giữ |
|---|---|---|
| Setting global `social_linkedin_link` | `settings_schema.json` · giá trị trong `settings_data.json` · label + info trong `en.default.schema.json` · sáu file liệt kê social (bảng mục 2) · `assets/icon-linkedin.svg` · nhãn ẩn `general.social.links.linkedin` trong `en.default.json` + `vi.json` · không có biến CSS | guard mới `social-links` (sáu file); Theme Check `TranslationKeyExists` (nhãn storefront); trình duyệt (icon) |
| Chuỗi `sections.footer.copyright` | `{{ … \| t: shop_name:, year: }}` trong `footer.liquid` · `en.default.json` · `vi.json` | Theme Check (khoá mặc định); trình duyệt ở `/vi` (Review Focus 5) |
| Info cho `heading` của block `link_list` | schema `footer.liquid` · `en.default.schema.json` | theme editor (thấy dòng chú thích) |
| Tham số snippet `hide_currency` | `country-localization.liquid` (đọc + comment "Accepts") · 4 caller: `header.liquid:266`, `footer.liquid:266`, `header-drawer.liquid:152`, `announcement-bar.liquid:145` — chỉ footer truyền | trình duyệt: nút ở header drawer vẫn ghi "… \| VND ₫" |
| Custom element `footer-accordion` | `assets/footer-accordion.js` · `<script … defer>` trong `footer.liquid` · editor re-render (`connectedCallback`) | `tools/run js-syntax`; trình duyệt (Review Focus 2, 3) |
| Nhánh `link_list` đổi markup | `case block.type` giữ `when 'link_list'` · `{{ block.shopify_attributes }}` giữ trên wrapper | guard có sẵn `section-blocks` |

Khái niệm Shopify plan này dùng, mỗi cái một câu vì sao:

- **Section group** — `header-group.json` / `footer-group.json` giữ section và setting của header
  và footer cho mọi trang, nên sửa một chỗ là đổi toàn site
  ([shopify.dev](https://shopify.dev/docs/storefronts/themes/architecture/section-groups)).
- **`<shopify-account>`** — component Shopify cấp cho nút đăng nhập; slot `signed-out-avatar` là
  chỗ duy nhất được phép thay nội dung khi khách chưa đăng nhập
  ([shopify.dev](https://shopify.dev/docs/storefronts/themes/customer-engagement/account-component)).
- **`localization`** — object cho biết quốc gia, tiền tệ, ngôn ngữ hiện tại; `localization.country.currency`
  cho "₫ VND" mà không cần form ([shopify.dev](https://shopify.dev/docs/api/liquid/objects/localization)).
- **Filter `t` có tham số** — `{{ 'key' | t: shop_name: shop.name }}` chèn giá trị vào chuỗi dịch, và
  kết quả được escape mặc định nên tên shop có ký tự `&` hay `<` vẫn an toàn
  ([shopify.dev](https://shopify.dev/docs/storefronts/themes/architecture/locales/storefront-locale-files)).
- **Setting `url`** — nhận link ngoài, trả `nil` khi trống, không chứa được `javascript:` như ô
  `text` ([shopify.dev](https://shopify.dev/docs/storefronts/themes/architecture/settings/input-settings)).
- **Custom element trong theme editor** — editor thay HTML của section khi merchant đổi setting;
  `connectedCallback` chạy lại trên phần tử mới, nên không cần nghe `shopify:section:load`
  ([shopify.dev](https://shopify.dev/docs/storefronts/themes/best-practices/editor/integrate-sections-and-blocks)).
- **`image_picker` và Files** — ảnh logo nằm ở Content → Files của store; setting lưu tham chiếu
  `shopify://shop_images/<tên file>` ([shopify.dev](https://shopify.dev/docs/storefronts/themes/architecture/settings/input-settings#image_picker)).

## Quyết định của plan

| # | Spec | Điểm chưa rõ | Chốt | Nguồn |
|---|---|---|---|---|
| D-5 | §4 "ít nhất một ngôn ngữ nữa" | Ngôn ngữ thứ hai là gì | **Tiếng Việt**: Dawn có sẵn `locales/vi.json`, store bán cho Vietnam. Khoá mới thêm vào `vi.json`; 49 locale còn lại không | plan |
| D-6 | §2.2 | Search cạnh menu áp cho bố cục nào | chỉ `logo_position: middle-center` có menu và menu desktop không phải `drawer`. Bố cục khác giữ Dawn | plan, theo D-2 |
| D-7 | §3 LinkedIn | Kiểu setting | `url`, khác tám mạng kia (`text`): `code-security.md` cấm dùng ô `text` làm `href`. Hệ quả: không có placeholder, ví dụ URL đặt ở `info` | code-security.md |
| D-8 | §2.5, OQ-8 | Accordion làm bằng gì | `<details>`/`<summary>` (bàn phím và trình đọc màn hình có sẵn). Server render `open`; `footer-accordion` đóng lại dưới 990 px và giữ mở từ 990 px. Không JS thì list luôn mở — không ai bị chặn khỏi link; desktop không giật bố cục | plan |
| D-9 | §2.4, §2.6 | "₫ VND" hiện khi nào | khi section Footer bật "country selector", kể cả store chỉ có một quốc gia; tắt setting đó thì ẩn | spec OQ-2 + plan |
| D-10 | §2.4 | "Powered by Shopify", policy | bỏ "Powered by" khỏi markup; danh sách policy giữ trong code sau `show_policy` và tắt bằng setting (merchant bật lại được) | spec §2.4 |
| D-11 | §2.6 | Block menu có tiêu đề trống | list hiện luôn, không accordion | plan (Review Focus 4) |
| D-12 | D-3 | Ai chọn logo | người dùng upload và chọn trong theme editor; `--theme-editor-sync` ghi tham chiếu về `settings_data.json`, Claude đọc lại trong `git diff`. Không đoán tên file | plan, sửa cách làm của D-3 cho riêng ảnh |
| D-13 | §2.4 | Footer desktop nhiều hơn năm block | một hàng duy nhất như design (`nowrap`): cột menu co lại khi thiếu chỗ. Mỗi block giữ `padding-right: 2rem` (cột menu: bên trong 17.5rem; block text/image/app: `flex: 1 1 17.5rem`) để chữ không dính cột bên (review cuối). Merchant thêm block thứ sáu trở đi thì các cột hẹp dần — giới hạn đã biết của bố cục này, ghi ở đây thay vì giữ cách chia ba cột của Dawn | plan |
| D-14 | §2.2 | Bề ngang header desktop (Task 6 bước 4 dừng) | Đo ở 1218 px: header Dawn rộng 1200 px, chữ menu bắt đầu ở x 52, giỏ kết thúc ở 1144; design 158 → 1039, lệch đều ~106 px mỗi bên. **Phương án A:** chỉ header bố cục Blakely (`.header--search-beside-menu`) được `max-width: 99rem` từ 990 px. `page_width` giữ 1200, footer và các section khác không đổi. Cái giá: con số cố định, merchant đổi `page_width` thì header không đổi theo; và cột menu chỉ còn ~322 px ở mọi bề ngang desktop (Dawn 1200 px: ~427 px) — ba mục Mens/Womens/Accessories vừa một hàng, mục thứ tư xuống dòng (review cuối). Người dùng giữ 99rem sau khi được báo cái giá này. (Lúc đưa phương án mình ước lượng ~94rem; đo lại thì ra 99rem) | người dùng chọn A, 2026-10-01 |

---

## Task 1 — GitHub: commit nền, repo, nối branch (spec §5)

Làm trước để công việc EX-01 nằm trên branch riêng, theo quy trình git của khoá (brief, mục 4.2).
Mọi commit/push chỉ chạy khi người dùng bảo.

**Files:** không sửa file theme. `git` + Shopify admin + GitHub.

- [ ] **Bước 1 (Claude, khi được bảo):** đọc `.gitignore` (đã có `.env`, `.env.*`, `.shopify`,
  `.local/`, `.worktrees/`, `.superpowers/`), đổi tên branch và tạo commit nền:

```bash
git branch -m master main
git status --short | head -50          # soát: không có file bí mật, không có .local/
git add -A
git commit -m "Foundation(setup): Dawn v16.0.0 with the claude-flow-kit harness

Dawn v16.0.0 copied from github.com/Shopify/dawn without history, the kit's rules, hooks,
guards and tools adapted to a Liquid theme, and the EX-01/EX-02 briefs, designs and the EX-01
spec and plan.

Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
```

- [ ] **Bước 2 (người dùng):** tạo repo trống trên GitHub (khuyên private), gửi URL.
- [x] **Bước 3 (Claude, khi được bảo):** `git remote add origin <URL>` rồi `git push -u origin main`.
  Push do người dùng chạy (auto mode chặn Claude push); `git ls-remote` xác nhận `refs/heads/main` = `bbcc5ac`.
- [x] **Bước 4 (người dùng):** Shopify admin → Online Store → Themes → Add theme → Connect from
  GitHub → cài Shopify GitHub app cho tài khoản/org → chọn repo, branch `main`. Một theme mới,
  chưa publish, xuất hiện trong danh sách.
- [x] **Bước 5 (người dùng + Claude):** bot commit `a9d9c5e` (`templates/index.json`, tiêu đề Image
  banner thành "Text image banner", chưa đổi lại). Trong editor của theme vừa nối, đổi tiêu đề một section của
  trang chủ (ví dụ Image banner — file `templates/index.json`, branch EX-01 không đụng tới) rồi Save
  (không dùng announcement: bot sẽ ghi `sections/header-group.json`, file branch EX-01 đang sửa → conflict khi mở PR); chờ ~10 giây. Kỳ vọng: GitHub có commit mới của Shopify trên `main`. Đổi lại chữ cũ.
  Claude `git fetch` và ghi hash của commit đó vào bảng trạng thái.
- [ ] **Bước 6 (Claude, khi được bảo):** `git checkout -b ex-01-header-footer` — mọi task sau làm
  trên branch này.

## Task 2 — Việc trong admin (người dùng, spec §4)

**Files:** không. Admin của `ngocmx-training`. Người dùng báo lại từng mục; Claude ghi vào bảng.

- [ ] **Bước 1 — Menu** (Content → Menus):
  - Sửa `Main menu`: hai mục **Mens**, **Womens** (OQ-3), link `/collections/all`.
  - Tạo bốn menu, tên đúng như sau, link tuỳ chọn nhưng phải bấm được (gợi ý `/collections/all`,
    `/pages/contact`, `/search`):

| Tên menu | Các mục |
|---|---|
| Shop | Mens · Womens · Accessories · Gift Card · Sign up for 10% off |
| Company | Contact Us · Careers · About Blakely · Blakely Community · Events · APEX Games · Press |
| Info | Delivery & Returns · Track Parcel · Klarna · FAQs · Influencers · Student Ambassadors |
| Important | Privacy Policy · Terms & Conditions · Cookie Policy · Site Map |

  - Báo lại **handle** của bốn menu (Shopify sinh từ tên; kỳ vọng `shop`, `company`, `info`,
    `important`). Task 4 dùng đúng handle báo lại.
- [ ] **Bước 2 — Đăng nhập cho khách** (Settings → Customer accounts): bật hiện link đăng nhập.
- [ ] **Bước 3 — Markets**: Vietnam có tiền VND; thêm ít nhất một quốc gia khác (ví dụ United
  States) để ô chọn country hiện.
- [ ] **Bước 4 — Languages**: thêm **Tiếng Việt** và publish (D-5).
- [ ] **Bước 5 — Thanh toán** (Settings → Payments): bật các phương thức muốn có icon (OQ-6); báo
  lại những phương thức đã bật.
- [ ] **Bước 6 — Logo** (D-12): mở theme editor của development theme (link `shopify theme dev` in
  ra), Theme settings → Logo → upload và chọn
  `docs/exercises/EX-01-header-footer/design/logo-blakely-black.png`; Theme settings → Brand
  information → Image → upload và chọn `logo-blakely-white.png`; Save.
- [ ] **Bước 7 (Claude):** `git diff config/settings_data.json` phải có `"logo":
  "shopify://shop_images/…"` và `"brand_image": "shopify://shop_images/…"`. Ghi giá trị vào bảng.

## Task 3 — Bằng chứng "trước" trên trình duyệt

**Files:** tạo `docs/exercises/EX-01-header-footer/evidence/before-*.png`.

- [ ] **Bước 1:** `mcp__chrome-devtools__chrome_status`. Nếu chưa kết nối, đưa người dùng đúng lệnh
  mở Chrome mà tool báo, rồi thử lại.
- [ ] **Bước 2:** kiểm `shopify theme dev` còn chạy: `curl -s -o /dev/null -w '%{http_code}'
  http://127.0.0.1:9292/` phải ra `200`.
- [ ] **Bước 3:** chụp `http://127.0.0.1:9292/` ở 1440, 990, 750, 375 px, cả trang (fullpage). Nếu
  tool không đổi được viewport, mở trang trống cùng origin và nhúng
  `<iframe src="/" width="375" height="2400">`, rồi chụp phần tử iframe — media query chạy theo bề
  ngang iframe. Lưu thành `before-1440.png`, `before-990.png`, `before-750.png`, `before-375.png`.
- [ ] **Bước 4:** đọc page text: 0 `Liquid error`, 0 `Translation missing`; đọc console: ghi lại
  lỗi có sẵn (nếu có) để sau này không nhận nhầm là lỗi mới.

## Task 4 — Setting bằng JSON (D-3)

**Files:**
- Modify: `sections/header-group.json` (announcement, header)
- Modify: `sections/footer-group.json` (footer)
- Modify: `config/settings_data.json` (`presets.Dawn`: logo width, brand width, social links)

**Interfaces:** Consumes handle menu từ Task 2 bước 1. Produces trạng thái "chỉ setting" để Task 6–10
so sánh.

- [ ] **Bước 1 — `header-group.json`:** trong `announcement-bar.blocks.announcement-bar-0.settings`
  đổi `"text": "Welcome to our store"` → `"text": "Free standard UK shipping on orders over £70"`;
  trong `announcement-bar.settings` đổi `"color_scheme": "scheme-1"` → `"scheme-4"`; trong
  `header.settings` đổi `"logo_position": "middle-left"` → `"middle-center"`,
  `"enable_country_selector": true` → `false`, `"enable_language_selector": true` → `false`.
- [ ] **Bước 2 — `footer-group.json`:** thay object `sections.footer` bằng:

```json
"footer": {
  "type": "footer",
  "blocks": {
    "link_list_shop": { "type": "link_list", "settings": { "heading": "Shop", "menu": "shop" } },
    "link_list_company": { "type": "link_list", "settings": { "heading": "Company", "menu": "company" } },
    "link_list_info": { "type": "link_list", "settings": { "heading": "Info", "menu": "info" } },
    "link_list_important": { "type": "link_list", "settings": { "heading": "Important", "menu": "important" } },
    "brand_information": { "type": "brand_information", "settings": { "show_social": true } }
  },
  "block_order": ["link_list_shop", "link_list_company", "link_list_info", "link_list_important", "brand_information"],
  "settings": {
    "color_scheme": "scheme-4",
    "newsletter_enable": false,
    "newsletter_heading": "Subscribe to our emails",
    "enable_follow_on_shop": false,
    "show_social": false,
    "enable_country_selector": true,
    "enable_language_selector": true,
    "payment_enable": true,
    "show_policy": false,
    "margin_top": 0,
    "padding_top": 36,
    "padding_bottom": 36
  }
}
```

  (Handle `shop`/`company`/`info`/`important` thay bằng handle Task 2 báo lại nếu khác.)
  `show_social` của section tắt vì social đã nằm trong block brand.
- [ ] **Bước 3 — `settings_data.json`:** sửa trong object `current`. Sau lần Save ở Task 2 bước 6,
  Shopify ghi `current` thành object chứa toàn bộ setting; chỉ khi `current` vẫn là chuỗi `"Dawn"`
  thì sửa trong `presets.Dawn`. Các giá trị: `"logo_width": 90` → `190`;
  `"brand_image_width": 100` → `230` (hai số đo từ logo trong design: 192 px, 230 px);
  `social_facebook_link` → `"https://facebook.com/shopify"`, `social_instagram_link` →
  `"https://instagram.com/shopify"`, `social_youtube_link` → `"https://www.youtube.com/shopify"`,
  `social_tiktok_link` → `"https://tiktok.com/@shopify"`, `social_twitter_link` →
  `"https://x.com/shopify"` (link tuỳ chọn theo đề). Giữ comment "auto-generated" ở đầu file.
- [ ] **Bước 4:** mỗi file vẫn là JSON hợp lệ sau khi bỏ comment đầu:
  `python3 -c "import json,re,sys;[json.loads(re.sub(r'^\s*/\*.*?\*/','',open(f).read(),flags=re.S)) for f in sys.argv[1:]];print('ok')" sections/header-group.json sections/footer-group.json config/settings_data.json`
  → `ok`. Output của `shopify theme dev` không báo file bị từ chối.
- [ ] **Bước 5:** chụp `settings-only-1440.png`, `settings-only-375.png`. Kỳ vọng ở 375 px:
  header đã giống spec §2.3 (bố cục mobile sẵn có của Dawn). Ghi vào bảng những gì setting đã làm
  được và những gì còn chờ code.

## Task 5 — LinkedIn, guard trước (spec §2.4, §3)

**Files:**
- Create: `tests/guards/social-links.test.js`
- Modify: `config/settings_schema.json` (sau dòng 1335)
- Modify: `snippets/social-icons.liquid` (sau dòng 62), `sections/header.liquid` (dòng 153, sau
  dòng 470), `sections/footer.liquid:33`, `sections/announcement-bar.liquid:6`,
  `snippets/header-drawer.liquid` (sau dòng 263), `sections/main-password-footer.liquid` (sau dòng 94)
- Create: `assets/icon-linkedin.svg`
- Modify: `locales/en.default.schema.json`, `locales/en.default.json`, `locales/vi.json`,
  `config/settings_data.json`

**Interfaces:** Produces `settings.social_linkedin_link` (url hoặc `nil`), nhãn
`general.social.links.linkedin`, icon `icon-linkedin.svg`.

- [ ] **Bước 1 — viết guard:**

```js
'use strict';
/**
 * @guard watches: a social link setting declared in config/settings_schema.json (Theme settings → Social media) but missing from one of the theme files that list every social network — the icon rows in the footer, announcement bar and menu drawer, the password page, the "is any social link set" checks and the Organization JSON-LD. Theme Check passes; the icon just never shows on that one surface, or a footer whose only social link is the new one renders no social row at all.
 * @guard extend: a new social_<name>_link in the Social media group must be named in every file this guard lists, the same number of times as the other networks in that file. A file that reads a single network for its own reason (meta-tags.liquid reads only X/Twitter) is not a list and is not checked.
 */

// What this cannot catch:
// - It counts mentions, not meaning: a mention in the wrong branch still counts.
// - It scans sections/, snippets/, layout/ and blocks/. Templates and JavaScript are not read.
// - The storefront label in locales/*.json and the icon file in assets/ are not checked here:
//   Theme Check reports a missing default-locale key, and the icon is checked in the browser.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..', '..');
const SCAN_DIRS = ['sections', 'snippets', 'layout', 'blocks'];

// Files that list every network on Dawn v16. Each case checks the scan still finds them, so an
// empty scan cannot pass as "nothing is missing".
const KNOWN_LISTS = ['snippets/social-icons.liquid', 'sections/footer.liquid', 'sections/header.liquid'];

function socialIds() {
  const schema = JSON.parse(fs.readFileSync(path.join(ROOT, 'config', 'settings_schema.json'), 'utf8'));
  return schema
    .flatMap((group) => group.settings || [])
    .map((setting) => setting.id)
    .filter((id) => /^social_[a-z]+_link$/.test(id || ''));
}

function liquidFiles() {
  return SCAN_DIRS.flatMap((dir) => {
    const abs = path.join(ROOT, dir);
    if (!fs.existsSync(abs)) return [];
    return fs
      .readdirSync(abs)
      .filter((name) => name.endsWith('.liquid'))
      .map((name) => `${dir}/${name}`);
  });
}

function mentions(file, ids) {
  const text = fs.readFileSync(path.join(ROOT, file), 'utf8');
  return Object.fromEntries(ids.map((id) => [id, (text.match(new RegExp(`settings\\.${id}\\b`, 'g')) || []).length]));
}

// A file naming two or more networks is a list of networks.
function socialLists(ids) {
  return liquidFiles()
    .map((file) => ({ file, count: mentions(file, ids) }))
    .filter(({ count }) => Object.values(count).filter(Boolean).length >= 2);
}

function assertScanIsReal(lists) {
  const found = lists.map((list) => list.file);
  const lost = KNOWN_LISTS.filter((file) => !found.includes(file));
  assert.deepEqual(lost, [], `the scan no longer finds these known lists: ${lost.join(', ')}`);
}

test('the schema declares the social links to compare against', () => {
  const ids = socialIds();
  assert.ok(ids.length >= 9, `expected Dawn's nine social settings or more, found ${ids.length}: ${ids.join(', ')}`);
});

test('every list of networks names every social link, as often as the others', () => {
  const ids = socialIds();
  const lists = socialLists(ids);
  assertScanIsReal(lists);
  const problems = [];
  for (const { file, count } of lists) {
    const expected = Math.max(...Object.values(count));
    for (const id of ids) {
      if (count[id] !== expected) problems.push(`${file}: ${id} named ${count[id]}×, the other networks ${expected}×`);
    }
  }
  assert.deepEqual(problems, []);
});
```

- [ ] **Bước 2:** `node --test tests/guards/social-links.test.js` → **pass 2/2** trên Dawn hiện tại
  (chín mạng, sáu file, đếm đều — đã đo khi viết plan).
- [ ] **Bước 3 — thêm setting vào schema**, ngay sau object `social_twitter_link` (đóng ở dòng 1335):

```json
      {
        "type": "url",
        "id": "social_linkedin_link",
        "label": "t:settings_schema.social-media.settings.social_linkedin_link.label",
        "info": "t:settings_schema.social-media.settings.social_linkedin_link.info"
      },
```

- [ ] **Bước 4 — đỏ:** `node --test tests/guards/social-links.test.js` → **fail**, `problems` liệt kê
  đúng sáu file với `social_linkedin_link named 0×`. Dán output vào bảng.
- [ ] **Bước 5 — icon** `assets/icon-linkedin.svg` (chữ "in" không khung, cùng kiểu
  `icon-facebook.svg`: class `icon icon-…`, `fill="currentColor"`):

```svg
<svg class="icon icon-linkedin" viewBox="2 2 20 20"><path fill="currentColor" d="M5.337 7.433a2.063 2.063 0 1 1 0-4.126 2.063 2.063 0 0 1 0 4.126zM3.555 9h3.564v11.452H3.555zm5.796 0h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351z"/></svg>
```

- [ ] **Bước 6 — sáu đầu.**
  `snippets/social-icons.liquid`, sau dòng 62 (hết khối X/Twitter, để thứ tự ra Facebook, Instagram,
  YouTube, TikTok, X, LinkedIn như design):

```liquid
  {%- if settings.social_linkedin_link != blank -%}
    <li class="list-social__item">
      <a href="{{ settings.social_linkedin_link }}" class="link list-social__link">
        <span class="svg-wrapper">
          {{- 'icon-linkedin.svg' | inline_asset_content -}}
        </span>
        <span class="visually-hidden">{{ 'general.social.links.linkedin' | t }}</span>
      </a>
    </li>
  {%- endif -%}
```

  `snippets/header-drawer.liquid`, sau dòng 263 (hết khối Vimeo):

```liquid
                {%- if settings.social_linkedin_link != blank -%}
                  <li class="list-social__item">
                    <a href="{{ settings.social_linkedin_link }}" class="list-social__link link">
                      <span class="svg-wrapper">
                        {{- 'icon-linkedin.svg' | inline_asset_content -}}
                      </span>
                      <span class="visually-hidden">{{ 'general.social.links.linkedin' | t }}</span>
                    </a>
                  </li>
                {%- endif -%}
```

  `sections/main-password-footer.liquid`, sau dòng 94 (hết khối Vimeo):

```liquid
    {%- if settings.social_linkedin_link != blank -%}
      <li class="list-social__item">
        <a href="{{ settings.social_linkedin_link }}" class="link list-social__link">
          <span class="svg-wrapper">
            {{- 'icon-linkedin.svg' | inline_asset_content -}}
          </span>
          <span class="visually-hidden">{{ 'general.social.links.linkedin' | t }}</span>
        </a>
      </li>
    {%- endif -%}
```

  `sections/header.liquid:153`: nối thêm ` or settings.social_linkedin_link != blank` vào cuối điều
  kiện. `sections/header.liquid`, sau dòng 470 (`{{ settings.social_twitter_link | json }},`), thêm
  `      {{ settings.social_linkedin_link | json }},`. `sections/footer.liquid:33` và
  `sections/announcement-bar.liquid:6`: nối thêm ` and settings.social_linkedin_link == blank` vào
  cuối điều kiện.
- [ ] **Bước 7 — locale.** `en.default.schema.json` → `settings_schema.social-media.settings`:
  `"social_linkedin_link": { "label": "LinkedIn", "info": "https://www.linkedin.com/company/shopify" }`.
  `en.default.json` và `vi.json` → `general.social.links`: `"linkedin": "LinkedIn"`.
- [ ] **Bước 8 — xanh:** `node --test tests/guards/social-links.test.js` → pass 2/2.
- [ ] **Bước 9 — mutation, mỗi cái phải đỏ:**

```bash
tools/run mutate sections/header.liquid --sub '{{ settings.social_linkedin_link | json }},=>' -- node --test tests/guards/social-links.test.js
tools/run mutate snippets/social-icons.liquid --sub 'settings.social_linkedin_link != blank=>false' -- node --test tests/guards/social-links.test.js
```

  Kỳ vọng: lần 1 nêu `sections/header.liquid: social_linkedin_link named 1×, the other networks
  2×`; lần 2 nêu `snippets/social-icons.liquid … 1× … 2×`.
- [ ] **Bước 10:** `tools/run change-guards` → 2 guard; `tools/run change-guards --check` → clean.
- [ ] **Bước 11:** `settings_data.json`, cùng object như Task 4 bước 3: thêm
  `"social_linkedin_link": "https://www.linkedin.com/company/shopify"`.
- [ ] **Bước 12 — trình duyệt:** footer 1440 px có sáu icon theo thứ tự Facebook, Instagram, YouTube,
  TikTok, X, LinkedIn; icon LinkedIn cùng cỡ và màu với năm icon kia. Theme editor: xoá ô LinkedIn →
  icon mất, năm icon còn lại không để lỗ; điền lại.

## Task 6 — Header desktop: search ngay sau menu (spec §2.2, D-6)

**Files:**
- Modify: `sections/header.liquid:151-166` (khối liquid), `:167` (class `<header>`), `:216-224`
  (render menu)
- Modify: `assets/base.css` — rule mới ngay sau khối `@media screen and (max-width: 989px)` của
  search (2652-2679)

**Interfaces:** Produces `search_beside_menu`, class `header--search-beside-menu`,
`header__navigation`, search `Search-In-Modal-Menu`.

Vì sao một ô search thứ ba: muốn icon search đi liền sau menu thì nó phải nằm cùng một hàng flex với
menu. Hai ô search sẵn có của Dawn đều không dời được — ô bên trái là con trực tiếp của `.header`
mà mọi rule mobile (`.header > .header__search`, base.css 2602-2679) dựa vào, ô trong nhóm icon vẫn
được dùng trên mobile ở bố cục `mobile-left` và khi không có account. Ô thứ ba chỉ hiện từ 990 px
và chỉ ở `middle-center`; Dawn tự nó đã render hai ô và ẩn một bằng CSS.

- [ ] **Bước 1 — đỏ:** ảnh `before-1440.png` (Task 3) cho thấy search nằm trong nhóm icon bên phải.
- [ ] **Bước 2 — Liquid.** Trong khối `liquid` dòng 151-166, trước `-%}`:

```liquid
    assign search_beside_menu = false
    if section.settings.logo_position == 'middle-center' and section.settings.menu != blank and section.settings.menu_type_desktop != 'drawer'
      assign search_beside_menu = true
    endif
```

  Dòng 167: thêm `{% if search_beside_menu %} header--search-beside-menu{% endif %}` vào cuối
  chuỗi class của `<header>`, trước `">`. Dòng 216-224 thay bằng:

```liquid
    {%- if search_beside_menu -%}
      <div class="header__navigation">
    {%- endif -%}
    {%- liquid
      if section.settings.menu != blank
        if section.settings.menu_type_desktop == 'dropdown'
          render 'header-dropdown-menu'
        elsif section.settings.menu_type_desktop != 'drawer'
          render 'header-mega-menu'
        endif
      endif
    %}
    {%- if search_beside_menu -%}
        {% render 'header-search', input_id: 'Search-In-Modal-Menu' %}
      </div>
    {%- endif -%}
```

- [ ] **Bước 3 — CSS**, `assets/base.css` ngay sau dòng 2679:

```css
.header__navigation {
  display: none;
}

@media screen and (min-width: 990px) {
  .header__navigation {
    grid-area: navigation;
    justify-self: start;
    display: flex;
    align-items: center;
    min-width: 0;
  }

  .header--search-beside-menu .header__icons > .header__search {
    display: none;
  }
}
```

  Rule ẩn đặt sau `.header--has-account .header__icons > .header__search` (dòng 2648, cùng
  specificity 0,3,0) để thắng nhờ thứ tự.
- [ ] **Bước 4 — xanh, 1440 px và 1218 px:** thứ tự Menu → search → logo giữa → LOG IN/icon → giỏ;
  tâm logo trùng tâm vùng trang ±2 px (đo bằng `getBoundingClientRect`); khoảng từ chữ menu cuối
  tới icon search ≈ 23 px như design (251 → 274). Bấm icon search → hộp search mở, gõ được. Ở
  1218 px đo vị trí x của menu, logo, giỏ, so với spec §2.2; nếu cả cụm rộng hơn design rõ rệt (menu
  bắt đầu ở x < 140 thay vì 160), dừng và đưa phương án `page_width` cho người dùng (mục 3).
- [ ] **Bước 5 — 375 và 989 px:** vẫn đúng một icon search (bên trái, cạnh ☰); không có ô search
  thứ hai. `document.querySelectorAll('.header__search')` đếm 3 nhưng chỉ 1 có
  `offsetParent !== null`.
- [ ] **Bước 6 — Review Focus 1:** trong editor, tạm chọn menu `Shop` (năm mục) cho header, xem ở
  990 px: menu xuống dòng trong cột trái, không đè lên logo. Chọn lại `Main menu`.

## Task 7 — "LOG IN" bằng chữ, menu in hoa (spec §2.2, §2.6, OQ-3, OQ-4)

**Files:**
- Modify: `sections/header.liquid:285-293`
- Modify: `assets/base.css` — sau `.header__icon--cart` (2577-2580) và trong phần Header menu (sau
  2838)

**Interfaces:** Consumes khoá có sẵn `customer.log_in` ("Log in"). Produces
`header__account-icon`, `header__account-label`.

- [ ] **Bước 1 — đỏ:** `before-1440.png`: account là icon người, menu chữ thường.
- [ ] **Bước 2 — markup**, thay hai `span` trong `<shopify-account>` (dòng 290-291):

```liquid
          <span slot="signed-out-avatar" class="svg-wrapper header__account-icon">{{ 'icon-account.svg' | inline_asset_content }}</span>
          <span slot="signed-out-avatar" class="header__account-label">{{ 'customer.log_in' | t }}</span>
```

- [ ] **Bước 3 — CSS**, sau rule `.header__icon--cart` (dòng 2580):

```css
.header__account-label {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}

@media screen and (min-width: 990px) {
  .header__icon--account {
    width: auto;
    padding: 0 1.2rem;
  }

  .header__account-icon {
    display: none;
  }

  .header__account-label {
    position: static;
    width: auto;
    height: auto;
    overflow: visible;
    clip: auto;
    font-size: 1.3rem;
    letter-spacing: 0.1rem;
    text-transform: uppercase;
    text-decoration: underline;
    text-underline-offset: 0.3rem;
  }
}
```

  Và trong phần Header menu, sau `.header__menu-item` (dòng 2838):

```css
@media screen and (min-width: 990px) {
  .header__inline-menu .list-menu--inline > li > .header__menu-item,
  .header__inline-menu .list-menu--inline > li > header-menu > details > .header__menu-item {
    text-transform: uppercase;
    letter-spacing: 0.1rem;
  }
}
```

- [ ] **Bước 4 — xanh, 1440 px:** chữ "LOG IN" có gạch chân ngay trước icon giỏ; menu ghi "MENS",
  "WOMENS". Bấm "LOG IN" → hộp đăng nhập của Shopify mở. 375 px: vẫn là icon người.
- [ ] **Bước 5 — rủi ro đã biết:** shopify.dev chỉ minh hoạ slot `signed-out-avatar` bằng ảnh, không
  nói slot có nhận chữ hay không. Nếu chữ bị cắt, thêm
  `shopify-account.header__icon--account::part(signed-out-avatar) { width: auto; height: auto; }` vào
  khối ≥990 ở bước 3 rồi kiểm lại. Nếu component không hiện chữ trong slot, **dừng** và đưa phương
  án cho người dùng (ví dụ link `routes.account_login_url` khi chưa đăng nhập) — không tự đổi cách
  đăng nhập.
- [ ] **Bước 6 — đã đăng nhập (OQ-4):** đăng nhập một khách thử; header 1440 px hiện chữ cái đầu
  tên / ảnh của khách ở chỗ "LOG IN", không đẩy lệch logo.

## Task 8 — Footer: mốc 990 px và accordion trên mobile (spec §2.5, OQ-5, OQ-8, D-8)

**Files:**
- Modify: `assets/section-footer.css` — đổi mốc, thêm rule accordion cuối file
- Modify: `sections/footer.liquid:1-6` (script), `:78` (điều kiện tiêu đề), `:89-103` (nhánh
  `link_list`), schema `link_list.heading` (dòng 336-340)
- Create: `assets/footer-accordion.js`
- Modify: `locales/en.default.schema.json` (`sections.footer.blocks.link_list.settings.heading.info`)

**Interfaces:** Produces `footer-accordion`, `footer-block__accordion`, `footer-block__summary`,
`footer-block__toggle-icon--plus`, `footer-block__toggle-icon--minus`.

- [ ] **Bước 1 — đỏ:** `before-375.png` và `before-750.png`: không có accordion; ở 750 px footer đã
  chia cột.
- [ ] **Bước 2 — mốc**, chỉ trong `assets/section-footer.css`:

```bash
sed -i 's/max-width: 749px/max-width: 989px/; s/min-width: 750px/min-width: 990px/' assets/section-footer.css
grep -c -E 'max-width: 749px|min-width: 750px' assets/section-footer.css   # phải ra 0
grep -c -E 'max-width: 989px|min-width: 990px' assets/section-footer.css   # phải ra 23 (21 đổi + 2 có sẵn)
```

- [ ] **Bước 3 — Liquid.** Dòng 78: `{%- if block.settings.heading != blank and block.type != 'link_list' -%}`.
  Nhánh `when 'link_list'` (dòng 89-103) thay bằng:

```liquid
                  {%- when 'link_list' -%}
                    {%- if block.settings.menu != blank -%}
                      {%- capture menu_links -%}
                        <ul class="footer-block__details-content list-unstyled">
                          {%- for link in block.settings.menu.links -%}
                            <li>
                              <a
                                href="{{ link.url }}"
                                class="link link--text list-menu__item list-menu__item--link{% if link.active %} list-menu__item--active{% endif %}"
                              >
                                {{ link.title | escape }}
                              </a>
                            </li>
                          {%- endfor -%}
                        </ul>
                      {%- endcapture -%}
                      {%- if block.settings.heading != blank -%}
                        <footer-accordion>
                          <details class="footer-block__accordion" open>
                            <summary class="footer-block__summary">
                              <h2 class="footer-block__heading inline-richtext">{{- block.settings.heading -}}</h2>
                              <span class="svg-wrapper footer-block__toggle-icon footer-block__toggle-icon--plus">
                                {{- 'icon-plus.svg' | inline_asset_content -}}
                              </span>
                              <span class="svg-wrapper footer-block__toggle-icon footer-block__toggle-icon--minus">
                                {{- 'icon-minus.svg' | inline_asset_content -}}
                              </span>
                            </summary>
                            {{ menu_links }}
                          </details>
                        </footer-accordion>
                      {%- else -%}
                        {{ menu_links }}
                      {%- endif -%}
                    {%- endif -%}
```

  Sau dòng 6 (stylesheet cuối): `<script src="{{ 'footer-accordion.js' | asset_url }}" defer="defer"></script>`.
  Schema `link_list` → setting `heading`: thêm
  `"info": "t:sections.footer.blocks.link_list.settings.heading.info"`; khoá trong
  `en.default.schema.json`: `"info": "Shown on mobile only, as the title of the collapsible menu."`.
- [ ] **Bước 4 — JS** `assets/footer-accordion.js`:

```js
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
```

- [ ] **Bước 5 — CSS**, cuối `assets/section-footer.css`:

```css
.footer-block__summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.2rem 0;
  cursor: pointer;
  list-style: none;
}

.footer-block__summary::-webkit-details-marker {
  display: none;
}

.footer-block__summary .footer-block__heading {
  margin: 0;
}

.footer-block__toggle-icon .icon {
  width: 1.2rem;
  height: 1.2rem;
}

.footer-block__accordion[open] .footer-block__toggle-icon--plus,
.footer-block__accordion:not([open]) .footer-block__toggle-icon--minus {
  display: none;
}

@media screen and (max-width: 989px) {
  .footer-block--menu.grid__item {
    margin: 0;
  }
}

@media screen and (min-width: 990px) {
  .footer-block__summary {
    display: none;
  }
}
```

- [ ] **Bước 6 — xanh, 375 px và 750 px:** bốn dòng Shop, Company, Info, Important, mỗi dòng dấu +
  bên phải, đều đóng khi tải trang. Bấm "Shop" → mở, dấu + thành dấu trừ, hiện năm link; bấm lại →
  đóng. Mở hai dòng cùng lúc được. Tab tới dòng và bấm Enter/Space → mở/đóng.
- [ ] **Bước 7 — Review Focus 2:** trong editor, preview ở bề ngang mobile, đổi một setting footer
  (ví dụ bật/tắt payment icons) → accordion vẫn đóng và vẫn bấm mở được; console không lỗi.
- [ ] **Bước 8 — Review Focus 3:** ở 375 px mở "Shop", kéo lên 1440 px → bốn cột hiện đủ link,
  không còn tiêu đề; kéo về 375 px → bốn dòng đóng.
- [ ] **Bước 9 — Review Focus 4:** trong editor xoá tiêu đề của block "Info" → ở 375 px không có
  dòng rỗng, list Info hiện luôn; điền lại "Info".
- [ ] **Bước 10:** `node --test 'tests/guards/*.test.js'` — `section-blocks` vẫn xanh;
  `tools/run js-syntax` clean.

## Task 9 — Footer desktop: năm cột trên một hàng, link gạch chân, cột brand (spec §2.4)

**Files:**
- Modify: `sections/footer.liquid:71` (class brand)
- Modify: `assets/section-footer.css:338-341` (màu link) và thêm rule cuối file

**Interfaces:** Produces `footer-block--brand`.

- [ ] **Bước 1 — đỏ:** `settings-only-1440.png` (Task 4): năm block chia ba cột và xuống dòng; link
  màu nhạt, không gạch chân.
- [ ] **Bước 2 — class:** dòng 71, sau `{% if block.type == 'link_list' %} footer-block--menu{% endif %}`
  thêm `{% if block.type == 'brand_information' %} footer-block--brand{% endif %}`.
- [ ] **Bước 3 — màu link.** Dòng 338-341 thay bằng:

```css
.copyright__content a {
  color: rgba(var(--color-foreground), 0.75);
}

.footer-block__details-content .list-menu__item--link {
  color: rgb(var(--color-foreground));
  text-decoration: underline;
  text-underline-offset: 0.3rem;
}
```

- [ ] **Bước 4 — bố cục**, cuối file:

```css
@media screen and (max-width: 989px) {
  .footer-block__brand-info {
    text-align: center;
  }

  .footer-block__brand-info > .footer-block__image-wrapper {
    margin-left: auto;
    margin-right: auto;
  }

  .footer-block__brand-info .footer__list-social.list-social {
    justify-content: center;
  }
}

@media screen and (min-width: 990px) {
  .footer__blocks-wrapper.grid {
    flex-wrap: nowrap;
    column-gap: 0;
  }

  .footer__blocks-wrapper .footer-block.footer-block--menu {
    flex: 0 1 17.5rem;
    width: 17.5rem;
    max-width: 17.5rem;
    min-width: 0;
  }

  .footer__blocks-wrapper .footer-block.footer-block--brand {
    flex: 0 0 auto;
    width: auto;
    max-width: none;
    margin-left: auto;
  }

  .footer-block__brand-info .footer__list-social.list-social {
    margin-left: -1.1rem;
  }
}
```

  17.5rem = 175 px, khoảng cách đo giữa bốn cột trong design (184, 360, 535, 710). `nowrap` và
  `flex: 0 1` để ở đúng 990 px (vùng nội dung 890 px < 4 × 175 + 230) bốn cột menu co lại thay vì
  đẩy cột logo xuống hàng (D-13).
  `margin-left: -1.1rem` bù padding của link social để icon đầu thẳng mép trái logo (design: logo
  1013, icon 1014).
- [ ] **Bước 5 — xanh, 1440 px và 1439 px:** bốn cột link và cột logo + social trên cùng một hàng;
  đo x đầu mỗi cột, cách đều ~175 px; logo trắng ở bên phải, social ngay dưới thẳng mép trái logo;
  link trắng có gạch chân sẵn. 990 px: vẫn một hàng, cột logo không rớt xuống; link dài nhất
  "Student Ambassadors" xuống dòng trong cột của nó, không đè cột bên. 375 px: logo và social căn giữa.
- [ ] **Bước 6 — editor:** bấm block "Company" trong sidebar → preview tô đúng cột Company ở 1440 px
  và đúng dòng Company ở 375 px.

## Task 10 — Footer hàng dưới: copyright, payment, "₫ VND", chọn country/language (spec §2.4, §2.5, OQ-1, OQ-2, D-9, D-10)

**Files:**
- Modify: `sections/footer.liquid:253-321`
- Modify: `snippets/country-localization.liquid:1-6` (comment), `:36-40` (nhãn nút)
- Modify: `assets/section-footer.css` — bỏ rule chết, thêm rule cuối file
- Modify: `locales/en.default.json`, `locales/vi.json` (`sections.footer.copyright`)

**Interfaces:** Consumes `hide_currency` (Contract). Produces `footer__currency`.

- [ ] **Bước 1 — đỏ:** `settings-only-1440.png`: localization trái + payment phải, copyright "©
  2026, …" và "Powered by Shopify" ở hàng riêng; nút country ghi "Vietnam | VND ₫", có nhãn
  "Country/region" phía trên.
- [ ] **Bước 2 — snippet.** Comment "Accepts" thêm dòng
  `- hide_currency: {Boolean} leave the currency out of the button label (optional)`. Dòng 36-40
  thay bằng:

```liquid
    <span>
      {{- localization.country.name -}}
      {%- unless hide_currency %} |
        {{ localization.country.currency.iso_code }}
        {{ localization.country.currency.symbol -}}
      {%- endunless -%}
    </span>
```

- [ ] **Bước 3 — markup hàng dưới.** Dòng 259-320 (từ `<div class="footer__content-bottom-wrapper page-width">`
  đầu tiên tới hết wrapper copyright) thay bằng:

```liquid
    <div class="footer__content-bottom-wrapper page-width">
      <div class="footer__column footer__column--info">
        {%- assign current_year = 'now' | date: '%Y' -%}
        <div class="footer__copyright caption">
          <small class="copyright__content">
            {{- 'sections.footer.copyright' | t: shop_name: shop.name, year: current_year -}}
          </small>
          {%- if section.settings.show_policy -%}
            <ul class="policies list-unstyled">
              {%- for policy in shop.policies -%}
                {%- if policy != blank -%}
                  <li>
                    <small class="copyright__content"
                      ><a href="{{ policy.url }}">{{ policy.title | escape }}</a></small
                    >
                  </li>
                {%- endif -%}
              {%- endfor -%}
            </ul>
          {%- endif -%}
        </div>
        {%- if section.settings.payment_enable -%}
          <div class="footer__payment">
            <span class="visually-hidden">{{ 'sections.footer.payment' | t }}</span>
            <ul class="list list-payment" role="list">
              {%- for type in shop.enabled_payment_types -%}
                <li class="list-payment__item">
                  {{ type | payment_type_svg_tag: class: 'icon icon--full-color' }}
                </li>
              {%- endfor -%}
            </ul>
          </div>
        {%- endif -%}
      </div>
      <div class="footer__column footer__localization isolate">
        {%- if section.settings.enable_country_selector -%}
          <p class="footer__currency caption-large">
            {{ localization.country.currency.symbol }}
            {{ localization.country.currency.iso_code }}
          </p>
        {%- endif -%}
        {%- if section.settings.enable_country_selector and localization.available_countries.size > 1 -%}
          <localization-form>
            {%- form 'localization', id: 'FooterCountryForm', class: 'localization-form' -%}
              <div>
                <h2 class="visually-hidden" id="FooterCountryLabel">{{ 'localization.country_label' | t }}</h2>
                {%- render 'country-localization', localPosition: 'FooterCountry', hide_currency: true -%}
              </div>
            {%- endform -%}
          </localization-form>
        {%- endif -%}
        {%- if section.settings.enable_language_selector and localization.available_languages.size > 1 -%}
          <localization-form>
            {%- form 'localization', id: 'FooterLanguageForm', class: 'localization-form' -%}
              <div>
                <h2 class="visually-hidden" id="FooterLanguageLabel">{{ 'localization.language_label' | t }}</h2>
                {%- render 'language-localization', localPosition: 'FooterLanguage' -%}
              </div>
            {%- endform -%}
          </localization-form>
        {%- endif -%}
      </div>
    </div>
```

  Nhãn country/language giữ trong DOM (`visually-hidden`) vì nút trỏ tới chúng qua
  `aria-describedby`.
- [ ] **Bước 4 — locale.** `en.default.json` → `sections.footer`:
  `"copyright": "Copyright {{ shop_name }} {{ year }} | All rights reserved"`. `vi.json` →
  `sections.footer`: `"copyright": "Bản quyền {{ shop_name }} {{ year }} | Bảo lưu mọi quyền"`.
- [ ] **Bước 5 — CSS.** Bỏ ba rule không còn phần tử nào trúng: `.footer__localization:empty +
  .footer__column--info` (dòng 79-81) và bản mobile (83-87) — thứ tự hai cột đã đảo;
  `.footer__content-bottom-wrapper--center` (289-291) — class không còn trong markup;
  `.footer__localization h2` (267-270) và bản desktop (278-280) — nhãn đã ẩn. Rule
  `.footer__content-bottom-wrapper:not(.footer__content-bottom-wrapper--center) .footer__copyright
  { text-align: right; }` (298-302, sau Task 8 là `min-width: 990px`) thay bằng
  `.footer__copyright { text-align: left; }` trong cùng media query. Thêm cuối file:

```css
.footer__currency {
  margin: 0;
}

@media screen and (max-width: 989px) {
  .footer__localization {
    flex-direction: column;
    align-items: center;
    row-gap: 0.5rem;
  }
}

@media screen and (min-width: 990px) {
  .footer__content-bottom-wrapper {
    justify-content: space-between;
    align-items: flex-start;
  }

  .footer__column--info {
    width: auto;
    align-items: flex-start;
  }

  .footer__localization {
    width: auto;
    flex-wrap: nowrap;
    align-items: center;
    column-gap: 2rem;
  }
}
```

- [ ] **Bước 6 — xanh, 1440 px:** trái: "Copyright *tên shop* 2026 | All rights reserved", dưới là
  icon thanh toán; phải, cùng hàng: "₫ VND", "Vietnam ⌄", "English ⌄", không nhãn; không còn
  "Powered by Shopify". 375 px: copyright → icon thanh toán → "₫ VND" → "Vietnam ⌄" → "English ⌄",
  mỗi thứ một dòng, căn giữa. Chọn United States → "₫ VND" đổi thành tiền của US; chọn lại Vietnam.
  Chọn Tiếng Việt → trang `/vi`.
- [ ] **Bước 7 — Review Focus 5, ở `/vi`:** dòng "Bản quyền …" hiện đúng; page text không có
  `Translation missing`; nhãn ẩn của LinkedIn có chữ (`document.querySelector('a[href*="linkedin"]
  .visually-hidden').textContent`).
- [ ] **Bước 8 — header drawer không đổi:** 375 px, mở ☰ → nút country trong drawer vẫn ghi
  "Vietnam | VND ₫" (caller không truyền `hide_currency`).
- [ ] **Bước 9 — escape:** đổi tạm tên shop có `&` (Settings → Store details) → dòng copyright hiện
  `&` đúng, không vỡ HTML; đổi lại. Nếu người dùng không muốn đổi tên shop, ghi bước này là
  `DEFERRED` vào `docs/tech-debt.md` kèm lý do.

## Task 11 — Kiểm toàn bộ (spec §6, `.claude/rules/shopify-theme.md` §3)

**Files:** tạo `docs/exercises/EX-01-header-footer/evidence/after-*.png`.

- [ ] **Bước 1:** chụp `after-1440.png`, `after-990.png`, `after-750.png`, `after-375.png`, cộng
  `after-1218.png`, `after-1439.png`, `after-414.png`, `after-332.png` (bề ngang của bốn ảnh design)
  để đặt cạnh design.
- [ ] **Bước 2:** ở mỗi bề ngang: không có thanh cuộn ngang
  (`document.documentElement.scrollWidth <= innerWidth`), không phần tử nào chồng nhau.
- [ ] **Bước 3:** page text không có `Liquid error`, `Translation missing` ở `/`, `/vi`,
  `/collections/all`, một trang sản phẩm; console không có lỗi mới so với Task 3 bước 4.
- [ ] **Bước 4 — trạng thái spec §2.6:** giỏ có hàng (bong bóng số); chưa có logo (tạm bỏ logo trong
  editor → hiện tên shop); store tắt đăng nhập (người dùng tạm tắt ở admin → không "LOG IN", search
  vẫn cạnh menu ở 1440 px, mobile vẫn có search); bật lại. Store chỉ còn một ngôn ngữ (người dùng
  tạm unpublish Tiếng Việt → ô chọn language mất, "₫ VND" và ô country vẫn còn, không để khoảng
  trống); publish lại. Block menu không gán menu (trong editor tạm bỏ menu của block "Info" → cột
  đó trống, trên mobile không có dòng "Info"); gán lại. Bước nào người dùng không muốn làm trên
  store thì ghi `DEFERRED` vào `docs/tech-debt.md`.
- [ ] **Bước 5 — theme editor:** đổi từng setting ở spec §3, preview đổi theo; bấm từng block cột
  link → preview tô đúng.
- [ ] **Bước 6 — lệnh**, dán output thật vào bảng:

```bash
shopify theme check --fail-level error     # kỳ vọng 0 error, 9 warning
tools/run js-syntax                        # kỳ vọng 37 file, clean (36 + footer-accordion.js)
node --test 'tests/guards/*.test.js'       # kỳ vọng 2 file, pass hết
tools/run change-guards --check            # clean
tools/run shared-rules                     # clean
```

- [ ] **Bước 7 — dọn:** không `console.log`, không code bị comment, không class/rule không dùng; mọi
  việc hoãn đã ở `docs/tech-debt.md`.
- [ ] **Bước 8 — bàn giao cho trainer (OQ-7), khi người dùng bảo:** commit trên
  `ex-01-header-footer`, push, mở PR vào `main`, merge. Theme nối GitHub (Task 1 bước 4) tự cập
  nhật; mở theme đó bằng link preview (chưa publish), kiểm lại 1440 và 375 px, gửi link cho trainer.
  **`config/settings_data.json` khi gộp với `main`:** bot commit `66484bf` đổi `"current": "Dawn"` thành
  object, và khi `current` là object thì Shopify bỏ qua `presets.Dawn`. Nếu branch vẫn giữ `"current": "Dawn"`,
  git gộp **không conflict** và lặng lẽ mất logo 190, brand 230, sáu social link (review cuối, đo bằng
  `git merge-file`). Vì vậy file của branch được dựng theo dạng của `main`: object `current` của bot cộng
  các giá trị của branch. Gộp giờ dừng ở 3 conflict; chọn bản của branch (`git checkout --ours
  config/settings_data.json` khi merge `main` vào branch) là đúng, vì nó đã chứa mọi giá trị của bot. Sau
  merge, mở theme GitHub: logo header rộng 190, footer có sáu icon social. Nếu `main` có commit mới của
  bot vào file này trước lúc gộp, lấy bản mới của bot rồi áp lại mười giá trị trong `presets.Dawn` của
  branch vào `current`.

## Task 12 — denv (người dùng, spec §5)

Claude không đọc, không sửa `.denv.env` (`.claude/rules/security.md` §1), nên bước nào chạm file đó
là của người dùng.

- [ ] **Bước 1:** `denv auth` (user/token Gitea; tài khoản có 2FA thì dùng token quyền "read
  repository"), rồi `denv svc init`, `denv svc up`.
- [ ] **Bước 2:** ở gốc repo, `denv env init` → sinh `.denv.env`; đặt platform shopify và
  `VIRTUAL_HOST` theo tài liệu denv của trainer.
- [ ] **Bước 3:** tắt `shopify theme dev` đang chạy trên máy (Ctrl+C), rồi `denv env up`,
  `denv shell`, trong container chạy `shopify theme dev --store ngocmx-training` — **không**
  `--theme-editor-sync` ở lần đầu (CLAUDE.md).
- [ ] **Bước 4:** mở `https://<VIRTUAL_HOST>` → thấy store với header/footer mới. Báo lại để Claude
  ghi vào bảng.
- [ ] **Bước 5:** hỏi người dùng có commit `.denv.env` và `.denv/` không (tài liệu denv khuyên
  commit cho cả team; repo này chưa ignore chúng). Trước khi commit, người dùng tự soát file đó không
  chứa token.

---

## Trạng thái

| # | Việc | Trạng thái | Bằng chứng |
|---|---|---|---|
| 1 | GitHub: commit nền, repo, nối branch | đã làm một phần | commit nền `bbcc5ac` trên `main` (399 file); branch `ex-01-header-footer`; remote `origin` đã thêm; `main` đã push (`bbcc5ac`); đã nối GitHub; bot commit `a9d9c5e` (`templates/index.json`) và `66484bf` (`settings_data.json`: logo upload trong editor theme GitHub → `current` thành object, xem Task 11 bước 8) |
| 2 | Việc trong admin | xong, trừ kiểm "&" và đăng nhập | đọc từ storefront dev: bốn menu footer đúng tên, handle khớp; Shop/Company/Important đúng mục, **Info thừa** "Terms & Conditions", "Site Map" (design 6 mục); **Main menu còn "Home"** (design chỉ Mens, Womens); link đăng nhập "Log in" hiện; ngôn ngữ English + Tiếng việt; country list chỉ Canada, United States — **market Vietnam chưa có condition** nên chưa hiện; logo + brand image hiện (190/230); sáu icon thanh toán có sẵn — OQ-6 không cần làm gì thêm. Lần 2: Main menu chỉ còn Mens, Womens; Info đủ 6 mục; country list Canada, United States, **Vietnam VND ₫** |
| 3 | Ảnh "trước" | đã làm một phần | `evidence/before-page-text.md`, `evidence/before-1920.png`. Lỗi có sẵn khi tải trang: 400 Storefront API + "menu customer-account-main-menu not found" (của `<shopify-account>`), `shop.app` bị chặn trên localhost. Ảnh hẹp (375/750/990) chờ: MCP không đổi được viewport, storefront cấm iframe, popup bị chặn |
| 4 | Setting bằng JSON | đã làm, chờ admin | `header-group.json`, `footer-group.json` (handle dự kiến `shop`/`company`/`info`/`important`), `settings_data.json` (`presets.Dawn`: logo 190, brand 230, sáu social link). JSON hợp lệ. Logo chờ người dùng upload |
| 5 | LinkedIn + guard `social-links` | đã làm, chờ editor | guard `social-links`: xanh trên Dawn 2/2 → đỏ khi thêm setting (6 file "0×") → xanh 2/2; mutation JSON-LD và `social-icons` đều đỏ "1× vs 2×"; change-guards 2 guard, clean. Trình duyệt 1920: 6 icon đúng thứ tự, LinkedIn cùng cỡ (`evidence/task5-footer-socials-1920.png`). Xoá LinkedIn (tạm, qua `settings_data.json`, đã trả lại): còn năm icon, cách đều 42 px, không lỗ |
| 6 | Search cạnh menu | đã làm, chờ menu dài (bước 6) | 1920 px: class `header--search-beside-menu`, chỉ `Search-In-Modal-Menu` hiện, nằm sau menu; tâm logo 953 = tâm header; bấm search → hộp mở, input focus (`evidence/task6-*.png`). 375/750/989 px: bố cục mobile, đúng một search. Bước 4 dừng ở bề ngang (trước: menu x 52, giỏ 1144 ở 1218 px — `evidence/compare-header-1218.png`) → D-14, `max-width: 99rem`; sau: menu 157, giỏ 1039, design 158/1039, tâm logo 601.5 = tâm trang (`evidence/task6-header-width-1218.png`); 989 px giữ 1200, 990 px header full 975, 1440 px 218→1208, 1920 px 458→1448, không cuộn ngang. Theme Check 0 lỗi/9 cảnh báo, guard 6/6, change-guards clean. Bước 6 (tạm đặt menu `shop` qua `header-group.json`, đã trả lại): 990 px năm mục xuống hai dòng trong cột trái, mép phải menu 303 / search 321–365 / logo bắt đầu 385 — không đè (`evidence/task6-long-menu-990.png`) |
| 7 | "LOG IN" chữ, menu in hoa | đã làm, chờ kiểm mobile | "LOG IN" in hoa, gạch chân, cách giỏ 12 px (design 11 px); menu in hoa; bấm → hộp "Sign in or create account" của Shopify (`evidence/task7-login-open-1920.png`). Slot nhận chữ — rủi ro bước 5 không xảy ra. Ruling: specificity icon (ledger) |
| 8 | Footer mốc 990 + accordion | đã kiểm | mốc footer 749/750 → 989/990 (23 chỗ); accordion `<details open>` + `footer-accordion.js`; js-syntax 37 clean; guard 6/6. 375 + 750 px: bốn dòng đóng khi tải, dấu +; bấm → mở, dấu −, Shop năm link; mở hai dòng cùng lúc được; bấm lại → đóng; summary focus được (Enter/Space là hành vi gốc của `<summary>`, không giả lập được bằng sự kiện tổng hợp). Kéo 750 → 1440: bốn list mở, tiêu đề ẩn; về 375: bốn dòng đóng. Render lại section qua Section Rendering API (thay DOM như editor): bốn dòng đóng, bấm mở được, không lỗi. Info tiêu đề trống (tạm, đã trả lại): không accordion, list hiện luôn, không dòng rỗng (`evidence/task8-*.png`). Editor (bước 7): người dùng tự kiểm trong editor và báo đạt, 2026-10-01 |
| 9 | Footer năm cột, link, brand | đã kiểm | class `footer-block--brand`, link trắng gạch chân, năm cột một hàng; bỏ đường kẻ trên hàng dưới (design không có — ruling). 1440/1439/990 px: năm block một hàng, cột cách 175 px; icon social đầu thẳng mép trái logo (1022/1022); link trắng gạch chân offset 3 px; 990 px "Student Ambassadors" một dòng trong cột 158 px; 375 px logo + social căn giữa (180/180). So design 1439: cột chữ 162/337/512/687 so với 185/360/536/711 (lệch trái 23 px), logo 1021 so với 1013 (`evidence/task9-footer-compare-1439.png`). Editor (bước 6, tô viền block Company): người dùng tự kiểm và báo đạt, 2026-10-01 |
| 10 | Footer hàng dưới | đã kiểm, chờ escape | 1920 px: "Copyright ngocmx-training 2026 \| All rights reserved" + 6 icon bên trái; "$ USD" + "United States ⌄" không khung, không nhãn, thẳng hàng (tâm 2070/2070); không còn "Powered by" (`evidence/task10-footer-1920.png`). Ruling: bỏ khung nút + margin thừa (ledger). 375 px: copyright → payment → "$ USD" → "United States" → "English", căn giữa (180). `/vi`: lang vi, "Bản quyền ngocmx-training 2026 \| Bảo lưu mọi quyền", 0 `Translation missing`, nhãn LinkedIn "LinkedIn", "Đăng nhập"; drawer 375 px nút country "Hoa Kỳ \| USD $" — vẫn có tiền tệ (`evidence/task10-vi-drawer-375.png`). `?country=VN` (form `/localization` qua proxy `theme dev` trả 401 nên đổi bằng tham số URL): 1440 px phải "₫ VND" · "Vietnam ⌄" · "English ⌄" cùng hàng (tâm y 807), nhãn h2 ẩn, không "Powered by"; 375 px copyright → payment → "₫ VND" → "Vietnam" → "English", căn giữa 180; giá sản phẩm thành VND; US → "$ USD". Drawer 375 px: "Vietnam \| VND ₫". Sửa thêm: "₫ VND" từ trắng 75% thành trắng như ô country (ruling, ledger) (`evidence/task10-footer-vn-*.png`) |
| 11 | Kiểm toàn bộ | đã kiểm, chờ đăng nhập + giỏ | Bước 2: 1440/1439/1218/990/750/414/375/332 — không cuộn ngang, không phần tử header/footer nào chồng nhau, đúng một search hiện. Bước 3: `/`, `/vi`, `/collections/all`, `/products/gift-card`, `/vi/products/gift-card` → 200, 0 `Liquid error`, 0 `Translation missing`; console chỉ lỗi có sẵn (Storefront API 400, `customer-account-main-menu`, CSP `shop.app`). Bước 6: theme check exit 0 (9 warning), js-syntax 37 clean, guard 6/6, change-guards clean, shared-rules clean. Bước 1 chờ: development theme đang có sửa trong editor (header bật country/language, banner "Update from local theme") khác repo. Bước 4: giỏ có hàng chưa kiểm được — 13 sản phẩm đều hết hàng. Bước 4: tắt đăng nhập và chỉ một ngôn ngữ — người dùng bỏ qua → `DEFERRED` trong `docs/tech-debt.md`. Đăng nhập trên `127.0.0.1:9292` lỗi: CSP `frame-ancestors` của `shop.app` chỉ cho domain myshopify — kiểm trạng thái đã đăng nhập trên `https://ngocmx-training.myshopify.com/?preview_theme_id=187484766378`. Bước 4 (tạm sửa JSON, đã trả lại, cmp giống bản sao): bỏ logo → header hiện "ngocmx-training", tâm 713 / tâm trang 712.5 ở 1440, 176/180 ở 375 (lưới mobile của Dawn); block Info không gán menu → block rỗng không chiếm chỗ: desktop Important dồn vào chỗ Info (513), mobile không có dòng Info, khoảng giữa các dòng 0. Dev theme bị ghi đè lại sau khi đã đưa về repo (header bật country/language, banner "Update from local theme") — nghi một tab editor cũ của development theme Save lại; chờ người dùng. Bước 1 (2026-10-02, sau khi `theme dev` chạy lại và dev theme khớp repo): `evidence/after-{1440,1439,1218,990,750,414,375,332}.png`, `?country=VN`; header mobile 414 khớp `header-mobile.png`. Sau review: footer có thêm block text tạm ở 990 px — sáu block một hàng, cột 127 px, chữ cách cột bên ≥ 28 px (`evidence/final-footer-text-block-990.png`); bố cục design ở 990 px: một hàng, cách ≥ 21 px, "Student Ambassadors" một dòng. Preview dev theme chạy trên `ngocmx-training.myshopify.com/?preview_theme_id=187484766378` — đăng nhập kiểm ở đó. Bước 8 (2026-10-02, người dùng chọn push + PR): commit `55294bf` (guard), `931ea26` (EX-01), merge `origin/main` `3812ce9` — `settings_data.json` conflict như dự đoán, giữ bản branch (114 giá trị của bot giữ nguyên + 10 giá trị branch); suite trên bản merge: theme check 0 error / 9 warning, guard 6/6, js-syntax 37 clean, change-guards + shared-rules clean. Push từ shell của Claude không có credential GitHub → người dùng push; `gh` chưa cài → PR tạo trên web |
| 12 | denv | chờ người dùng |  |
