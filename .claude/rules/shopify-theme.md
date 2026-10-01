# Shopify theme — the ends of a change, the theme flaw classes, and how to see it work

This repository is **Dawn v16.0.0** used as a training base. Every exercise is a change to it.
Sibling of `change-reaches-every-end.md` (the general mechanism) and `business-logic-analysis.md`
(the general flaw classes): this page is what those two mean in a Liquid theme.

Facts about Liquid objects, filters, tags, schema attributes and the Ajax API come from
shopify.dev, not memory — open the reference page before relying on one. Facts about Dawn come
from this repo's code; every Dawn claim below was measured on v16.0.0.

---

## 1. Which ends must know

Before writing, find your row and list every end in the plan. After writing, check each one.

| You add | Every end that must know |
|---|---|
| **A section setting** | the `settings` entry in `{% schema %}` (unique `id`, `type`, `default`) · the Liquid that reads `section.settings.<id>` · every snippet the section renders that reads it through `section` (grep the id) · `presets` if it needs a non-default value · JSON templates and `sections/*-group.json` that already hold this section · the label: Dawn writes labels as `t:` keys, so a new key goes into `locales/en.default.schema.json` |
| **A block type** | the `blocks` entry in the schema · a `when 'type'` in `case block.type` · `{{ block.shopify_attributes }}` on its wrapper so the editor can select it · `presets` if it should appear by default · its CSS. The guard `section-blocks` checks the first two and that the section outputs attributes at all |
| **A storefront string** | `{{ 'key' \| t }}` in Liquid · the key in `locales/en.default.json` (Theme Check `TranslationKeyExists` reads only the default locale) · other locales as the spec decides — Dawn turns `MatchingTranslations` off in `.theme-check.yml`, so a key missing from the other 50 locales is never reported |
| **A string used by JavaScript** | the key in `locales/en.default.json` · the `window.*Strings` object in `layout/theme.liquid` that hands it to JS · the JS that reads it |
| **A new section** | `{% schema %}` with `name` and `presets` if the merchant adds it from the editor · `enabled_on` / `disabled_on` if it belongs to a group · its stylesheet in `assets/` loaded with `stylesheet_tag` · its script in `assets/` loaded with `defer` · the JSON template that places it, when the brief says it is on a page by default |
| **A snippet parameter** | every caller — `grep -rn "render '<name>'" sections snippets layout templates blocks` · the snippet's `{% doc %}` block if it has one (only 2 Dawn snippets do; Theme Check validates arguments only where a doc exists) |
| **A global theme setting** | `config/settings_schema.json` · its value in `config/settings_data.json` · the CSS variable in the `{% style %}` block of `layout/theme.liquid` (Dawn keeps `--page-width`, `--font-body-family` and the rest there) · its label in `locales/en.default.schema.json` |
| **Something that depends on the selected variant** | the Liquid that renders it for the first variant · an element `id` of the form `<Name>-{{ section.id }}` · Dawn's variant swap: `assets/product-info.js` re-fetches the section HTML and copies **only** the ids it names (`price`, `Sku`, `Inventory`, `Volume`, `Price-Per-Item`, plus media, options, quantity rules and the submit button). A new element outside that list keeps the first variant's value — add it to the list or subscribe to `PUB_SUB_EVENTS.variantChange` |
| **A metafield on the page** | the definition in the store admin (not in this repo — `shopify theme metafields pull` writes `.shopify/metafields.json` so Theme Check knows it) · the Liquid that reads `.value` · what renders when it is blank · whether it is variant-level (then the variant row above applies too) |
| **A cart change** | the Ajax endpoint through `window.routes` (never a hardcoded `/cart/...` path — it breaks under a market or locale subfolder) · the cart drawer **and** the cart page, which Dawn renders from different sections · the cart count bubble · the error path when the API answers 422 |

---

## 2. Flaw classes that are specific to a theme

Walk these together with `business-logic-analysis.md` §2.

| Class | What to look for |
|---|---|
| **Editor lifecycle** | Script that initialises on `DOMContentLoaded` and goes dead when the editor re-renders the section. Dawn writes behaviour as custom elements, whose `connectedCallback` runs again on re-render — follow that. `shopify:section:load` is handled only in `assets/theme-editor.js` and `assets/animations.js` |
| **Variant change does not reach every element** | See the variant row in §1. Test by switching variants, not by loading the page once |
| **Blank values** | An image, link, metafield or text setting left empty renders an empty wrapper, a broken `<img>`, or `href=""`. Guard with `!= blank`, and check the editor's empty state, not only a filled one |
| **Hardcoded routes** | `/cart`, `/search`, `/collections/all` in Liquid (Theme Check `HardcodedRoutes`) or in JS (not checked — use `window.routes`) |
| **Money in JavaScript** | The Ajax API returns cents. Format with the shop's money format, never `price / 100` with a hand-written currency symbol |
| **Render scope** | `{% render %}` does not see the caller's variables. A snippet that "works" because a variable happened to be global is reading something else |
| **Style leakage** | A selector not scoped to the section leaks into every other section. Settings-driven CSS goes in a `{% style %}` block keyed by `#shopify-section-{{ section.id }}` |
| **Breakpoints** | Dawn's are 750px and 990px (`min-width: 750px` ×174, `min-width: 990px` ×57 in `assets/*.css`; the same values in `matchMedia` in JS). A third breakpoint is a design decision, not a habit |
| **Images** | `image_url: width:` plus `image_tag` with `widths` and `sizes`, explicit width/height (Theme Check `ImgWidthAndHeight`), lazy loading below the fold only |

---

## 3. How to see it work

Compiling is not available here — a Liquid theme is only proven by rendering it. `shopify theme
check` and the guards prove the code is well-formed; they do not prove the exercise is done.

1. `shopify theme dev` uploads a **development** theme to the connected store and serves a
   preview at `http://127.0.0.1:9292`, reloading on save. It needs a development store; the first
   run asks which one. Run it in the background — it does not exit.
2. Open the page the change is on. Search the page text for `Liquid error` and
   `Translation missing` — Shopify renders both inline instead of failing.
3. Open the theme editor link it prints. Add the section or block, change **every** new setting,
   and confirm the preview changes each time. Click the block in the sidebar and confirm the
   preview highlights it.
4. Check widths 375, 750, 990 and 1440 — either side of each Dawn breakpoint.
5. Check the empty state: every new setting cleared, the product without the metafield.
6. Read the browser console for errors.

When the chrome-devtools MCP is connected, use it for steps 2, 4 and 6: navigate to the preview
URL, read console messages and runtime errors, and take a screenshot per width. Put the
screenshots' paths in the plan as the evidence.

---

## 4. Store safety

- **Never publish, delete, or push to the live theme.** `shopify theme publish` and
  `shopify theme delete` are denied in `.claude/settings.json`; `theme push` and `theme pull`
  ask first. Work through `shopify theme dev`, which only ever touches a development theme.
- **`shopify theme pull` overwrites local files** with whatever is on the store. Never run it on a
  tree with uncommitted work.
- **`config/settings_data.json` and the JSON templates are merchant content.** The theme editor
  writes them; `shopify theme dev --theme-editor-sync` copies those writes back into this repo.
  Change them by hand only when the brief says the default page changes, and say so in the plan.
  Review them in `git diff` before a commit — an editor session leaves changes there.
