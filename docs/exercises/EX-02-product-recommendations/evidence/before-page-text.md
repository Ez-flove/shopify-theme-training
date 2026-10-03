# Trang sản phẩm trước EX-02

Đo 2026-10-02 trên theme GitHub `187488927914` (`shopify-theme-training/main`, code `a4cb83d` — gốc
của branch `ex-02-product-recommendations`), trang `/products/the-complete-snowboard`.
`shopify theme dev` lúc đó đang tắt; theme GitHub chạy đúng code đó nên dùng thay.

Các section trong `<main>`, theo thứ tự:

| Section | Cao (1920 px) | Chữ |
|---|---|---|
| `template--27818214916266__main` | 764 px | thông tin sản phẩm, kết thúc bằng "Share" |
| `template--27818214916266__disclosures` | 0 px | trống |
| `template--27818214916266__related-products` | 64 px (1440), 48 px (375) | trống |

`related-products` của Dawn gửi một request khi cuộn tới:
`/recommendations/products?limit=4&product_id=15380095107242&section_id=template--27818214916266__related-products`.
Response không có sản phẩm nào (`product-recommendations` có 0 `li`), nên dưới phần thông tin sản
phẩm chỉ là một khoảng trắng trước footer. Không có nút chọn loại sản phẩm, không có
"sản phẩm đã xem".

Ảnh: `before-1440.png`, `before-375.png`.
