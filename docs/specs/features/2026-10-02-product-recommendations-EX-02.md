# Spec EX-02 — Section Product recommendations: "Sản phẩm liên quan" và "Sản phẩm đã xem"

Ngày: 2026-10-02 · Trạng thái: **đã duyệt (Gate 1)** — người dùng, 2026-10-02; chín OPEN QUESTION trả lời theo đề xuất (mục 8)

Đề: [`docs/exercises/EX-02-product-recommendations/brief.md`](../../exercises/EX-02-product-recommendations/brief.md) ·
Design: [`docs/exercises/EX-02-product-recommendations/design/`](../../exercises/EX-02-product-recommendations/design/) ·
Tiêu chí chung: [`docs/exercises/guidelines.md`](../../exercises/guidelines.md)

Spec này nói shopper thấy gì và merchant chỉnh được gì, không nói code viết thế nào. Số đo lấy từ
hai file PNG trong `design/` bằng script; vị trí tính theo pixel của ảnh (`carousel-slider.png` rộng
1444 px, `grid.png` rộng 1311 px).

---

## 1. Đề yêu cầu gì

Trích nguyên văn từ đề (thang điểm 6đ):

> 2) Tạo mới 1 section Product recommendations: 6d
>
> - Layout ( 1đ ): Heading · Description · List button: Chứa các nút để lựa chọn giữa các loại sản
>   phẩm như: Sản phẩm liên quan, Sản phẩm đã xem · Product grid: Danh sách sản phẩm hiển thị theo
>   action được chọn từ List Button.
> - Yêu cầu chi tiết: ( 5đ )
>
> 1. Settings Section/Block Schema: (0.25đ): Section chỉ hiển có thể config ở product · Các config
>    ngắn gọn dễ hiểu (Có note đối với những config gây confused)
> 2. List button ( 0.75đ ): Khi người dùng nhấn vào một trong các nút trong List Button (…), Product
>    Grid sẽ được cập nhật để hiển thị các sản phẩm tương ứng: Sản phẩm liên quan: Hiển thị các sản
>    phẩm liên quan đến sản phẩm hiện tại. · Sản phẩm đã xem: Hiển thị các sản phẩm mà người dùng đã
>    xem trước đó.
> 3. Product Grid ( 1đ ): (…) Sử dụng hai dạng hiển thị khác nhau: (viết config style type từ phía
>    admin) · Carousel (Slider): (…) cho phép người dùng cuộn qua các sản phẩm với các nút prev
>    (trước) và next (sau) · Grid: (…) giúp người dùng xem nhiều sản phẩm cùng lúc
> 4. Quy Trình Hoạt Động ( 2đ ): (…) tự động thay đổi các sản phẩm trong Product Grid mà không cần
>    tải lại trang. · Product Grid sẽ cập nhật (…) mà không cần phải gọi lại API nhiều lần. · Cover
>    trường hợp fetch data không có sản phẩm phù hợp.
> 5. Yêu cầu nâng cao ( 1đ ): Carousel và Grid View cần phải hoạt động mượt mà và tối ưu cho mọi
>    thiết bị. Sử dụng lazy loading để tải các sản phẩm khi người dùng cuộn xuống (…) · Đảm bảo API
>    được gọi đúng cách và không gây tải lại không cần thiết. · Giao diện phải tương thích tốt trên
>    cả thiết bị di động và máy tính để bàn (…).

Tài liệu tham khảo đề đưa: Product Recommendations API, storefront search, Predictive Search API;
một store demo và repo mẫu (`Duongtu1209/product-recommendations`).

Từ tiêu chí chung (`guidelines.md`), các ý áp vào bài này: giảm request lúc tải trang, lazy loading,
không import asset trong section render nhiều lần, mobile first với `min-width`, accessible, setting
đơn giản.

---

## 2. Shopper thấy gì

### 2.1 Bố cục

Từ trên xuống, trong khung `page-width` như các section khác của Dawn:

| Phần | Theo design | Ghi chú |
|---|---|---|
| Heading | không có trong hai ảnh (ảnh cắt từ hàng nút trở xuống) | trên cùng, căn trái; để trống thì không hiện (OQ-2) |
| Description | không có trong hai ảnh | dưới heading; để trống thì không hiện (OQ-2) |
| Hàng nút (List button) | bên trái, từ x 45: "SẢN PHẨM LIÊN QUAN 🔥" rồi "SẢN PHẨM ĐÃ XEM 📸" | nút đang chọn: nền gần đen (#101010), chữ trắng; nút còn lại: nền trắng, viền xám mảnh, chữ đen |
| Link bên phải hàng nút | "Hãy khám phá những sản phẩm mới nhất", chữ đậm gạch chân, x 1146–1390 | link tuỳ chọn (OQ-1) |
| Product grid | 4 sản phẩm một hàng ở cả hai ảnh | card sản phẩm của Dawn: ảnh, badge "Sale"/"Sold out", tên, vendor, giá theo tiền tệ của market |

### 2.2 Chuyển tab

- Lúc tải trang, tab đầu tiên (block đầu tiên) đang chọn (OQ-3).
- Bấm một nút: nút đó thành "đang chọn", product grid đổi sang sản phẩm của tab đó, **trang không tải
  lại**, vị trí cuộn không nhảy.
- Mỗi tab lấy dữ liệu **nhiều nhất một lần** trong một lần xem trang. Bấm lại một tab đã mở thì hiện
  ngay danh sách đã có, không gửi request mới. Request lỗi thì không giữ lại: bấm lại tab đó là thử lại.
- Trong lúc chờ dữ liệu của một tab, grid cũ không còn bấm được và có dấu hiệu đang tải; nút vừa bấm
  đã chuyển sang "đang chọn".
- Bấm liên tiếp hai tab khi tab trước chưa tải xong: grid hiện tab bấm sau cùng; dữ liệu về muộn của
  tab trước không được đè lên.

### 2.3 Sản phẩm liên quan

Sản phẩm Shopify gợi ý cho sản phẩm đang xem (Product Recommendations, loại "related"), tối đa số
lượng merchant đặt. Store mới có ít dữ liệu nên Shopify có thể trả ít sản phẩm hoặc không trả sản
phẩm nào — khi đó tab hiện câu báo không có sản phẩm (2.6).

### 2.4 Sản phẩm đã xem

- Mỗi lần shopper mở một trang sản phẩm có section này, sản phẩm đó được ghi vào lịch sử xem **trong
  trình duyệt của shopper** (không theo tài khoản, không đồng bộ giữa các thiết bị).
- Tab hiện các sản phẩm đã xem, **mới nhất trước**, **không gồm sản phẩm đang xem**, tối đa số lượng
  merchant đặt (OQ-4).
- Sản phẩm đã bị xoá hoặc ẩn khỏi Online Store thì không hiện.
- Trình duyệt chặn lưu trữ (một số chế độ ẩn danh) thì tab luôn hiện câu báo không có sản phẩm, trang không lỗi.

### 2.5 Carousel và grid (merchant chọn)

| | Carousel | Grid |
|---|---|---|
| Desktop (≥ 990 px) | một hàng, số card mỗi lần bằng setting số cột; nút prev/next; prev mờ ở đầu, next mờ ở cuối | nhiều hàng, mỗi hàng bằng setting số cột |
| Mobile (< 750 px) | vuốt ngang, card kế tiếp ló ra một phần để báo còn nữa; có nút prev/next | lưới 1 hoặc 2 cột theo setting |
| Tablet (750–989 px) | như mobile | như mobile, số cột mobile |

Ít sản phẩm hơn số cột thì carousel không hiện nút prev/next. Mốc 750/990 px là mốc của Dawn.

### 2.6 Các trạng thái ảnh không chụp

| Trạng thái | Shopper thấy |
|---|---|
| Tab không có sản phẩm nào | câu thông báo của tab đó (merchant đặt được, có mặc định), không có grid rỗng hay nút prev/next (OQ-5) |
| Request lỗi (mất mạng, server lỗi) | câu báo không tải được sản phẩm; bấm lại tab là thử lại |
| Section chỉ còn một block | vẫn hiện một nút (để shopper biết đang xem loại gì) |
| Section không còn block nào | storefront không hiện section; trong theme editor hiện một dòng nhắc thêm block |
| JavaScript tắt | heading, description, nút hiện; grid hiện câu báo cần JavaScript — dữ liệu chỉ có qua request |

### 2.7 Tải chậm và hiệu năng

- Lúc tải trang **không gửi request nào** cho section này; tab đầu tiên chỉ lấy dữ liệu khi section
  cách màn hình khoảng 400 px (như section "Related products" của Dawn). Tab còn lại chỉ lấy khi bấm.
- Ảnh trong card tải lười (lazy) như mọi card của Dawn.
- Script và CSS của section là file riêng, chỉ có trên trang có section này, tải `defer`.

### 2.8 Bàn phím và trình đọc màn hình

- Hàng nút là một nhóm tab: trình đọc màn hình đọc được "tab, 1 trên 2, đang chọn".
- Tab/Shift+Tab vào nhóm nút; mũi tên trái/phải chuyển giữa các nút; Enter/Space chọn.
- Khi grid đổi xong, trình đọc màn hình được báo số sản phẩm mới (hoặc câu báo không có sản phẩm).
- Nút prev/next của carousel có nhãn đọc được.

---

## 3. Merchant chỉnh được gì trong theme editor

Section chỉ thêm được vào **template sản phẩm** (đề: "chỉ có thể config ở product").

**Section — mỗi setting có `info` khi tên chưa đủ rõ:**

| Setting | Kiểu | Mặc định | Ghi chú cho merchant (`info`) |
|---|---|---|---|
| Heading | chữ ngắn | "You may also like" | — |
| Description | đoạn văn | trống | — |
| Chữ của link bên phải | chữ ngắn | trống | để trống thì không hiện link |
| Link bên phải | URL | trống | — |
| Kiểu hiển thị | chọn: Carousel / Grid | Carousel | — |
| Số sản phẩm tối đa | 2–10 | 8 | "Áp dụng cho từng tab." Shopify trả tối đa 10 sản phẩm gợi ý |
| Số cột trên desktop | 2–6 | 4 | "Carousel: số sản phẩm thấy được mỗi lần." |
| Số cột trên mobile | 1–2 | 2 | — |
| Tỉ lệ ảnh, ảnh thứ hai khi hover, hiện vendor | như "Related products" của Dawn | như Dawn | — |
| Color scheme, padding trên/dưới | như Dawn | như Dawn | — |

**Block — mỗi block là một nút** (D-1). Hai loại, mỗi loại tối đa một block; kéo để đổi thứ tự:

| Block | Setting | Mặc định |
|---|---|---|
| Sản phẩm liên quan | chữ trên nút · câu khi không có sản phẩm | chữ trên nút để trống → dùng chữ dịch sẵn của theme (OQ-9) |
| Sản phẩm đã xem | chữ trên nút · câu khi không có sản phẩm | như trên; `info`: "Lưu trong trình duyệt của khách, không gồm sản phẩm đang xem." |

Bấm một block trong sidebar thì preview chuyển sang tab đó và tô block. Đổi bất kỳ setting nào thì
section render lại và vẫn chạy (chuyển tab, carousel).

---

## 4. Ngoài phạm vi

Quick add trong card; cuộn vô hạn / tải thêm trang; "complementary products"; nút xoá lịch sử xem;
đồng bộ lịch sử theo tài khoản khách; section "Related products" của Dawn giữ nguyên file.

---

## 5. Tiêu chí chấp nhận

Theo thang điểm của đề:

1. **Layout (1đ):** heading, description, hàng nút, product grid đúng thứ tự mục 2.1 ở 1440 và 375 px.
2. **Schema (0.25đ):** section chỉ có trong danh sách "Add section" của template sản phẩm; mọi setting
   khó hiểu có `info`.
3. **List button (0.75đ):** bấm từng nút đổi đúng loại sản phẩm (mục 2.3, 2.4).
4. **Product grid (1đ):** đổi "Kiểu hiển thị" trong editor thì preview đổi giữa carousel (prev/next
   chạy) và grid.
5. **Quy trình (2đ):** network tab cho thấy: 0 request của section lúc tải trang; 1 request khi cuộn
   tới; 1 request khi bấm tab thứ hai; 0 request khi bấm qua lại sau đó; không có lần tải lại trang.
   Tab không có sản phẩm hiện câu báo không có sản phẩm của tab đó.
6. **Nâng cao (1đ):** ở 375, 750, 990, 1440 px không cuộn ngang, carousel vuốt được trên mobile,
   ảnh lazy; console không lỗi mới.
7. Theme Check không thêm error; guard xanh; `/vi` không có `Translation missing`.

---

## 6. Rủi ro đã biết

- **Lấy "sản phẩm đã xem" bằng search theo id (D-2).** Truy vấn `id:A OR id:B` trên trang search
  **đo được là chạy** trên store `ngocmx-training` ngày 2026-10-02 (trả đúng hai sản phẩm được hỏi), và
  section của template sản phẩm render trên trang search **giữ setting của merchant** (padding 28 px
  như template, không phải mặc định 36 px). Nhưng tài liệu storefront search của Shopify chỉ liệt kê
  các trường `body, product_type, tag, title, variants.*, vendor` — không có `id`. Nếu Shopify bỏ
  hành vi này, tab "Sản phẩm đã xem" sẽ luôn trống; cách dự phòng là một request cho mỗi sản phẩm
  (đã cân nhắc và loại ở D-2 vì nhiều request).
- **Kết quả search có thể ẩn sản phẩm hết hàng**, tuỳ cài đặt search của store. Khi đó sản phẩm đã xem
  mà hết hàng có thể không hiện.
- **Store dev ít dữ liệu:** 13 sản phẩm, đều hết hàng; Shopify có thể chưa có gợi ý. Cần đủ sản phẩm
  để thấy carousel có nút prev/next.

---

## 7. Quyết định đã có

| # | Điểm | Chốt | Nguồn |
|---|---|---|---|
| D-1 | Nút tab cấu hình thế nào | Mỗi nút là một block (hai loại, mỗi loại tối đa một): merchant đổi chữ, đổi thứ tự, bỏ bớt một tab | người dùng, 2026-10-02 |
| D-2 | Lấy dữ liệu từng tab | Cả hai tab dùng Section Rendering API của chính section này, để card là card của Dawn và giá theo market: "liên quan" qua Product Recommendations API, "đã xem" qua trang search với truy vấn theo id (mục 6) — mỗi tab một request | người dùng, 2026-10-02 |

---

## 8. OPEN QUESTIONS — đã trả lời

Người dùng chọn "theo đề xuất" cho cả chín câu, 2026-10-02: cột cuối là câu trả lời.

| # | Câu hỏi | Vì sao chưa rõ | Trả lời |
|---|---|---|---|
| OQ-1 | Dòng chữ gạch chân bên phải hàng nút ("Hãy khám phá những sản phẩm mới nhất") là **link** hay là **description**? | Đề liệt kê Heading, Description, List button, Product grid; ảnh có dòng chữ đậm gạch chân, trông như link | một link tuỳ chọn (chữ + URL) bên phải hàng nút; description là đoạn văn riêng dưới heading |
| OQ-2 | Heading và description nằm ở đâu? | Hai ảnh cắt từ hàng nút trở xuống | trên hàng nút, căn trái, theo thứ tự đề liệt kê; để trống thì không chiếm chỗ |
| OQ-3 | Lúc tải trang tab nào đang chọn? | Ảnh chỉ có "Sản phẩm liên quan" đang chọn | block đầu tiên; merchant kéo block để đổi |
| OQ-4 | "Sản phẩm đã xem": có gồm sản phẩm đang xem không, thứ tự nào, giữ bao nhiêu? | Đề chỉ nói "đã xem trước đó" | không gồm sản phẩm đang xem; mới nhất trước; giữ 20 sản phẩm gần nhất, hiện tối đa số merchant đặt |
| OQ-5 | Tab không có sản phẩm thì sao: ẩn nút hay hiện thông báo? | Đề: "Cover trường hợp fetch data không có sản phẩm phù hợp" | giữ nút, hiện câu thông báo của tab (merchant đặt được); không ẩn nút vì ẩn làm hàng nút nhảy |
| OQ-6 | "Lazy loading để tải các sản phẩm khi người dùng cuộn xuống" nghĩa là gì? | Có thể là tải khi section cuộn tới, hoặc cuộn vô hạn trong grid | tải dữ liệu khi section cuộn tới (≈400 px trước khi thấy), tab kia chỉ tải khi bấm, ảnh lazy — không cuộn vô hạn (mục 4) |
| OQ-7 | Carousel trên mobile hoạt động thế nào? | Ảnh carousel chỉ có desktop | vuốt ngang, card kế tiếp ló ra, vẫn có prev/next — như carousel có sẵn của Dawn |
| OQ-8 | Section mới có nằm sẵn trên trang sản phẩm không, và "Related products" của Dawn đang có ở đó thì sao? | Đề: "Tạo mới 1 section"; template sản phẩm hiện có "Related products" | thêm section mới vào template sản phẩm ngay sau phần thông tin sản phẩm và bỏ "Related products" khỏi template (file vẫn giữ), để trang không có hai danh sách gợi ý trùng nhau |
| OQ-9 | Chữ trên nút: theo ảnh ("SẢN PHẨM LIÊN QUAN 🔥") hay theo ngôn ngữ của trang? | Store tiếng Anh, có thêm tiếng Việt; ảnh ghi tiếng Việt in hoa có emoji | để trống thì dùng chữ dịch sẵn của theme (en "Related products" / "Recently viewed", vi "Sản phẩm liên quan" / "Sản phẩm đã xem"), merchant gõ chữ riêng (kể cả emoji) thì dùng chữ đó; chữ trên nút in hoa bằng CSS như ảnh |
