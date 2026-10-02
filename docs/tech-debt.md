# Tech debt

Anything deliberately left undone. A row is added **at the moment of deferring**, not collected
later from memory — by then the reason is gone and only the symptom is left.

Each row says what would unblock it. A row without that is a complaint, not debt.

| Date | What | Why deferred | What unblocks it | Where |
|---|---|---|---|---|
| 2026-10-01 | EX-01 — header when the store turns customer sign-in off: no "LOG IN", search still beside the menu at 1440 px, mobile still has search | the user chose to skip it (plan Task 11 step 4); it needs the setting switched off in the store admin and back on | turn off customer account links in Settings → Customer accounts, load the dev preview at 1440 and 375 px, turn it back on | `sections/header.liquid`, plan `docs/plans/2026-10-01-header-footer-EX-01.md` Task 11 |
| 2026-10-01 | EX-01 — footer with only one published language: the language selector goes away, "₫ VND" and the country selector stay, no gap left | the user chose to skip it (plan Task 11 step 4); it needs Tiếng Việt unpublished and published again | unpublish Tiếng Việt in Settings → Languages, check the footer at 1440 and 375 px, publish it again | `sections/footer.liquid`, `assets/section-footer.css`, plan Task 11 |
| 2026-10-01 | EX-01 — copyright line with a shop name containing `&` (does the `t` interpolation escape it, without breaking the HTML) | the user chose not to rename the shop (plan Task 10 step 9) | rename the store to e.g. `ngocmx & training` in Settings → Store details, read the copyright line on the dev preview (`&amp;` in the source, `&` on screen), rename it back | `sections/footer.liquid` copyright, `locales/en.default.json` `sections.footer.copyright` |
| 2026-10-01 | EX-01 — cart count bubble in the new header layout (spec §2.6) | every one of the store's 13 products has 0 available variants, so nothing can be added to the cart | give one variant stock (Products → variant → Inventory → Available) or "Continue selling when out of stock", add it to the cart, read the bubble at 1440 and 375 px | `sections/header.liquid`, `assets/base.css` |
| 2026-10-01 | EX-01 — signed-in header (OQ-4): initials/avatar instead of "LOG IN"; `.header__icon--account { width: auto; padding: 0 1.2rem }` also applies to the avatar | sign-in cannot run on `127.0.0.1:9292` (shop.app `frame-ancestors` allows only the store's domains) | enter the storefront password on `ngocmx-training.myshopify.com`, open `/?preview_theme_id=187484766378`, sign in, measure the account icon at 1440 px | `sections/header.liquid` (`shopify-account`), `assets/base.css` |
