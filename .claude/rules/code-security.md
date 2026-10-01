# Code Security Standards — Shopify theme

Security rules for the theme code itself. For what the agent must never do, see `security.md`.

The kit's version of this file is a REST API checklist. A theme has no server of its own, so the
rules here are about what reaches the shopper's browser: everything in this repo is public the
moment it is published — anyone can read the rendered HTML and download `assets/`.

---

## Output escaping

Liquid does **not** escape output by default.

| Rule | How we enforce it |
|---|---|
| **Escape anything typed by a person** | `\| escape` on text settings, `search.terms`, form values echoed back, URL parameters, and any metafield of a text type — in element content and above all inside attributes |
| **HTML settings are HTML on purpose** | `richtext`, `html` and `inline_richtext` settings render unescaped by design. Never place them inside an attribute or a `<script>` |
| **Data into JavaScript goes through `json`** | `<script type="application/json">{{ product \| json }}</script>`, then `JSON.parse` in JS. Never build a JS string literal with `'{{ value }}'` — a quote in a product title breaks out of it |
| **No `innerHTML` with fetched text** | Section HTML from the Section Rendering API is the theme's own output and fine. Text from the Ajax API (product titles, cart line properties) goes in with `textContent` |

## Links and URLs

| Rule | How we enforce it |
|---|---|
| **Links come from `url` settings** | A `url`-type setting can only hold a link. A `text` setting used as `href` can hold `javascript:` |
| **Routes come from `routes`** | `routes.cart_url` in Liquid, `window.routes` in JS — never a hardcoded path |

## Secrets and personal data

| Rule | How we enforce it |
|---|---|
| **No secrets in the theme** | No Admin API token, app secret, or third-party key with write access in any theme file, setting default, or metafield rendered to the page. If a feature needs one, it needs an app or a proxy, not a theme change |
| **Do not dump the customer** | The `customer` object exists on every page once someone is logged in. Render only the fields the brief needs; never `customer \| json` into the page, never personal data in `data-` attributes for tracking |

## Forms

| Rule | How we enforce it |
|---|---|
| **Use the `form` tag** | `{% form 'product' %}`, `{% form 'contact' %}`, `{% form 'customer_login' %}` and the rest add the hidden fields Shopify expects. A hand-written `<form action="/account/login">` misses them |
| **Show Ajax errors** | A 422 from `/cart/add.js` (sold out, quantity rule) must reach the shopper as the API's message, not disappear |

## Scripts and assets

| Rule | How we enforce it |
|---|---|
| **No remote scripts without a reason in the plan** | A CDN script is a supply-chain dependency and a render cost. Prefer a file in `assets/`. Theme Check `RemoteAsset` warns |
| **Leave `content_for_header` alone** | Shopify injects analytics, apps and checkout scripts through it. Theme Check `ContentForHeaderModification` |
| **Scripts load with `defer`** | Theme Check `ParserBlockingScript` |

---

## Review checklist

Use this during `/flow-review`.

- [ ] Every text setting, search term, form value and text metafield rendered with `| escape`
- [ ] No `richtext` / `html` setting inside an attribute or a `<script>`
- [ ] Data handed to JS through `| json` in a `type="application/json"` script, never a string literal
- [ ] Fetched Ajax API text inserted with `textContent`, not `innerHTML`
- [ ] Every `href` from a `url` setting or `routes`, none from a `text` setting
- [ ] No token or key in any theme file, setting default, or rendered metafield
- [ ] No more customer data on the page than the brief needs
- [ ] Forms built with the `form` tag; Ajax errors shown to the shopper
- [ ] No new remote script without a reason in the plan; `content_for_header` untouched
