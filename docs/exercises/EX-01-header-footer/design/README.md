# Design EX-01

Ảnh gốc trên Google Drive, chỉ mở được bằng tài khoản BSS. Tải về và lưu đúng tên dưới đây vào thư
mục này — spec và plan trỏ tới các tên này.

| File | Nội dung | Drive | Đã lưu từ (2026-10-01) |
|---|---|---|---|
| `header-mobile.png` | header, mobile (không yêu cầu style menu) | <https://drive.google.com/file/d/1e6FFqI8HiEmcsjMk8ehkygUWUVk6-tmx/view> | <https://prnt.sc/wyq2moKuoeul> · 414×693 |
| `header-desktop.png` | header, desktop | <https://drive.google.com/file/d/1R38hLApOa7bZyXR75GPuFhUH1ahKwnsq/view> | <https://prnt.sc/Vft5oXpXs_Dt> · 1218×692 |
| `footer-mobile.png` | footer, mobile | <https://drive.google.com/file/d/1N_bt4tDABZNCazkWHg_rwKcB_kjtL0dB/view> | <https://prnt.sc/b706dum2BRnl> · 332×691 |
| `footer-desktop.png` | footer, desktop | <https://drive.google.com/file/d/1RoSs3sWSAkIYDJGfp_UP-TjkmFs9dlrp/view> | <https://prnt.sc/yK2r7QJZfCwI> · 1439×566 |

Ảnh lấy bằng `tools/run fetch-shot` từ các link Lightshot ở cột cuối. Khung đỏ đánh dấu header
và footer — chưa đối chiếu với ảnh gốc trên Drive nên chưa biết khung có sẵn trong design hay do
người chụp vẽ thêm; nó không phải một phần của giao diện.

## Logo

Đề không kèm file logo. Hai file dưới đây là wordmark dựng lại theo logo trong design, không phải
logo gốc của Blakely.

| File | Dùng ở | Kích thước |
|---|---|---|
| `logo-blakely-black.png` | header — Theme settings → Logo | 1184×117, nền trong suốt, chữ #121212 |
| `logo-blakely-white.png` | footer — Theme settings → Brand information → Image | 1184×117, nền trong suốt, chữ #FFFFFF |

Cách dựng: chữ BLAKELY bằng Inter Bold (`/usr/share/fonts/opentype/inter/Inter-Bold.otf`, giấy
phép SIL OFL), mỗi chữ kéo ngang 1,38 lần, khoảng cách giữa các chữ chỉnh để cả cụm có tỉ lệ
10,1 : 1. Hai con số đó đo từ logo trong `header-desktop.png` (192×19 px, tỉ lệ 10,1) và
`footer-desktop.png` (230×22 px, tỉ lệ 10,5). Chữ trong design rộng 0,89–1,26 lần chiều cao,
khoảng cách trung bình 0,47 lần; bản dựng lại có khoảng cách 0,43 lần.
