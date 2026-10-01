# EX-01 — trạng thái "trước", đọc từ HTML của preview

`curl http://127.0.0.1:9292/` lúc 2026-10-01, development theme `#187484766378`, Dawn v16.0.0 chưa
sửa gì ngoài `config/settings_schema.json` đã khôi phục. Ảnh chụp "trước" chờ Chrome
(plan Task 3); đây là bằng chứng bằng page text mà CLAUDE.md cho phép.

| Điểm | Trước | Spec muốn |
|---|---|---|
| Class `<header>` | `header--middle-left header--mobile-center … header--has-account header--has-localizations` | `header--middle-center`, không còn localization trên header |
| Chữ announcement | "Welcome to our store", `scheme-1` | "Free standard UK shipping on orders over £70", nền đen |
| Ô search | 2: `Search-In-Modal-1` trước nhóm icon (dùng ở mobile), `Search-In-Modal` trong nhóm icon (dùng ở desktop) | desktop: search ngay sau menu |
| Account | `<shopify-account>` dạng icon | desktop: chữ "LOG IN" |
| Logo | không có ảnh, in tên shop | logo BLAKELY |
| Footer | `color-scheme-1`, 0 block, có ô newsletter, có "Powered by Shopify", copyright "© 2026, ngocmx-training" | nền đen, 4 cột menu + cột brand, không newsletter, không "Powered by", "Copyright … \| All rights reserved" |
| LinkedIn | không có | icon thứ sáu |
| Accordion footer | không có | 4 dòng trên mobile |
| Lỗi trên trang | 0 `Liquid error`, 0 `Translation missing` | giữ 0 |
