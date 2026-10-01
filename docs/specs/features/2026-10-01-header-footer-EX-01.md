# Spec EX-01 — Header và footer theo design Blakely, cùng dev store, denv, GitHub

Ngày: 2026-10-01 · Trạng thái: **đã duyệt (Gate 1)** — người dùng, 2026-10-01; tám OPEN QUESTION trả lời theo đề xuất (mục 9)

Đề: [`docs/exercises/EX-01-header-footer/brief.md`](../../exercises/EX-01-header-footer/brief.md) ·
Design: [`docs/exercises/EX-01-header-footer/design/`](../../exercises/EX-01-header-footer/design/) ·
Tiêu chí chung: [`docs/exercises/guidelines.md`](../../exercises/guidelines.md)

Spec này nói shopper thấy gì và merchant chỉnh được gì, không nói code viết thế nào. Mọi con số
về vị trí và màu đo từ ảnh design bằng script trên chính file PNG; vị trí tính theo pixel của ảnh.

---

## 1. Đề yêu cầu gì

Trích nguyên văn từ đề:

> - Tạo một development store
> - Khởi tạo theme Dawn, setup denv env shopify (0.5)
> - Integrate theme với Github (0.5)
> - Thực hiện các thay đổi ở header giống với design (1.5đ) … (không yêu cầu style menu)
> - Thực hiện các thay đổi sau ở footer giống với design (1đ)
> - Responsive tương thích với các thiết bị 0.5
>
> Lưu ý: Font chữ không cần chính xác nhưng vị trí và màu sắc các element cần phải đúng.
>
> Các link có thể click vào được và không cần phải chèn link chính xác, link tùy chọn.
>
> Có nhiều phần có thể dùng theme editor và shopify setting để làm được và cần phải tự tìm.

Ảnh design là ảnh chụp một store Dawn đã chỉnh: chữ trên banner ("Image banner test", "Talk about
your brand") là nội dung mặc định của section Dawn. Vậy đích của bài là Dawn được chỉnh bằng
setting, và code chỉ thêm ở chỗ setting không làm được — đúng cách đã chọn (D-2).

**Trong phạm vi:** announcement bar, header, footer, trên mọi trang; mobile và desktop; dev store,
denv, GitHub.

**Ngoài phạm vi:** style của menu trên mobile (menu drawer) — đề ghi "không yêu cầu style menu"
ngay cạnh design mobile; nội dung thân trang trong ảnh (banner, rich text, slideshow); checkout.

---

## 2. Shopper thấy gì

### 2.1 Announcement bar — mọi độ rộng

Một dải nền **#111111**, chữ **trắng**, một dòng căn giữa: "Free standard UK shipping on orders
over £70". Không có social icon, không có chọn country/language trên dải này.

### 2.2 Header — desktop

Nền **trắng**, một hàng, theo thứ tự từ trái sang phải (`header-desktop.png`, ảnh rộng 1218 px):

| Thành phần | Vị trí trong ảnh (x) | Ghi chú |
|---|---|---|
| Menu: MENS, WOMENS | 160–251 | chữ in hoa, màu xám đậm (Dawn tô menu nhạt hơn màu chữ chính). Ảnh ghi "MANS"; menu ghi "Mens", "Womens" như footer, in hoa bằng CSS (OQ-3) |
| Icon search | 274–286 | **nằm ngay sau menu, bên trái** — mở search như Dawn |
| Logo BLAKELY (đen) | 505–697 | **căn giữa**: tâm logo ở x 601; ảnh có thanh cuộn ở mép phải nên tâm vùng trang thấy được hơi lệch trái so với tâm ảnh (609) |
| Chữ "LOG IN" có gạch chân, rồi icon giỏ hàng | 978–1038 (cả cụm) | "LOG IN" là **chữ, không phải icon**, bấm vào là đăng nhập; giỏ có bong bóng số lượng khi có hàng, như Dawn |

Search nằm bên trái và "LOG IN" là chữ là hai chỗ Dawn không có sẵn: Dawn để search trong nhóm
icon bên phải và chỉ có icon account.

### 2.3 Header — mobile

Nền **trắng**, một hàng (`header-mobile.png`, ảnh rộng 414 px):

| Thành phần | Vị trí trong ảnh (x) |
|---|---|
| Icon menu ☰ | 41–58 |
| Icon search | 85–101 |
| Logo BLAKELY, căn giữa | 130–276 |
| Icon account (người) | 299–315 |
| Icon giỏ hàng | 343–361 |

Bố cục này là bố cục mobile sẵn có của Dawn khi store có menu và bật đăng nhập cho khách. Trên
mobile account là **icon**, không phải chữ "LOG IN".

### 2.4 Footer — desktop

Nền **#111111**, chữ trắng (`footer-desktop.png`, ảnh rộng 1439 px). Không có ô đăng ký email,
không có nút "Follow on Shop", không có "Powered by Shopify", không có danh sách policy riêng.

**Hàng trên — năm cột:**

| Cột | x | Link (từ trên xuống) |
|---|---|---|
| 1 | 184 | Mens · Womens · Accessories · Gift Card · Sign up for 10% off |
| 2 | 360 | Contact Us · Careers · About Blakely · Blakely Community · Events · APEX Games · Press |
| 3 | 535 | Delivery & Returns · Track Parcel · Klarna · FAQs · Influencers · Student Ambassadors |
| 4 | 710 | Privacy Policy · Terms & Conditions · Cookie Policy · Site Map |
| 5 | 1013–1242 | logo BLAKELY (trắng); bên dưới một hàng social icon 1014–1231: Facebook, Instagram, YouTube, TikTok, X, LinkedIn |

- Bốn cột link cách đều nhau khoảng 175 px. Cột logo nằm riêng ở bên phải, cùng một hàng với
  bốn cột link.
- Cột link **không có tiêu đề** trên desktop.
- Mọi link màu trắng và **có gạch chân sẵn**, không phải chỉ khi rê chuột.

**Hàng dưới:**

| Bên | x | Nội dung |
|---|---|---|
| Trái, dòng trên | 185–448 | "Copyright *tên shop* *năm hiện tại* \| All rights reserved" — ảnh ghi "ThanhDV Training 2025", là tên store của người làm design (OQ-1). Chữ nhỏ, xám nhạt (sáng nhất #CCCCCC trong ảnh) |
| Trái, dòng dưới | 185–450 | icon thanh toán theo các phương thức đang bật trên store (OQ-6). Ảnh có sáu: Visa, Mastercard, American Express, PayPal, Diners Club, Discover |
| Phải, cùng hàng | 989–1217 | "₫ VND" · "Vietnam ⌄" · "English ⌄", **không có nhãn** "Country/region" / "Language" phía trên. "₫ VND" chỉ hiển thị ký hiệu và mã tiền tệ của quốc gia đang chọn, không bấm được; chọn quốc gia khác thì nó đổi theo (OQ-2) |

Dawn đặt hàng dưới khác hẳn: chọn country/language bên trái, icon thanh toán bên phải, copyright
một hàng riêng bên dưới.

### 2.5 Footer — mobile

Nền **#111111**, mọi thứ một cột (`footer-mobile.png`, ảnh rộng 332 px), từ trên xuống:

1. Bốn dòng có thể mở ra: **Shop**, **Company**, **Info**, **Important**. Mỗi dòng có dấu **+**
   ở bên phải. Trong ảnh cả bốn đều đang đóng. Mở một dòng thì hiện các link của cột tương ứng
   ở bản desktop — giả định A-1. Mỗi dòng mở/đóng độc lập, mở nhiều dòng cùng lúc được; lúc tải trang
   cả bốn đều đóng (OQ-8). Dấu **+** đổi thành dấu trừ khi dòng đang mở.
2. Logo BLAKELY (trắng), căn giữa.
3. Hàng social icon, căn giữa.
4. Dòng copyright, căn giữa.
5. Hàng icon thanh toán, căn giữa.
6. "₫ VND", rồi "Vietnam ⌄", rồi "English ⌄", mỗi cái một dòng, căn giữa.

### 2.6 Các trạng thái ảnh không chụp

| Trạng thái | Shopper thấy |
|---|---|
| Khách **đã đăng nhập** | thay cho "LOG IN" là chữ cái đầu tên hoặc ảnh Shop profile của khách, do component account của Shopify tự hiện — như Dawn (OQ-4) |
| Store **tắt** đăng nhập cho khách | không có "LOG IN" (desktop) và icon account (mobile); các thành phần còn lại giữ vị trí |
| Giỏ hàng có hàng | icon giỏ có bong bóng số lượng, như Dawn |
| Chưa có logo | hiện tên shop bằng chữ ở chỗ logo, như Dawn |
| Một social link để trống | icon đó không hiện; các icon còn lại dồn lại, không để lỗ |
| Store chỉ có một quốc gia hoặc một ngôn ngữ | ô chọn tương ứng không hiện, như Dawn. "₫ VND" vẫn hiện tiền tệ hiện tại (OQ-2) |
| Một cột link không gán menu | cột đó không in gì, và trên mobile không có dòng mở ra rỗng |
| Tên link dài | xuống dòng trong cột, không tràn sang cột bên |

### 2.7 Responsive

Ở các độ rộng 375, 750, 990 và 1440 px không có thanh cuộn ngang, không có thành phần chồng lên
nhau, và thứ tự các thành phần giữ như mục 2.2–2.5. Design chỉ có bản ~414 px và bản ~1218/1439
px. **Dưới 990 px là bố cục mobile** (mục 2.3, 2.5) cho cả header lẫn footer; **từ 990 px là bố cục
desktop** (mục 2.2, 2.4). Mốc 990 px trùng mốc header Dawn đã dùng (OQ-5).

---

## 3. Merchant chỉnh được gì trong theme editor

Mọi thứ trong mục 2 là nội dung merchant chỉnh được — chữ announcement, menu, link, logo, social
link, màu — trừ cách sắp xếp: search bên trái, chữ "LOG IN", tiêu đề cột chỉ hiện trên mobile,
thứ tự hàng dưới footer. Những thứ đó là layout của theme, không thành setting mới (YAGNI).

| Merchant muốn | Chỉnh ở |
|---|---|
| Chữ, link, màu của announcement bar | section Announcement bar |
| Logo header, độ rộng logo | Theme settings → Logo |
| Logo footer (bản trắng) | Theme settings → Brand information → Image |
| Menu header | section Header → Menu |
| Bốn cột link footer, và tiêu đề Shop / Company / Info / Important | block Menu trong section Footer — **phần chú thích của ô tiêu đề phải nói rõ tiêu đề chỉ hiện trên mobile**, vì trên desktop nó không hiện và merchant sẽ không hiểu vì sao |
| Link social, **gồm cả LinkedIn** | Theme settings → Social media — **LinkedIn là ô mới**, Dawn chưa có |
| Bật/tắt chọn country, language, icon thanh toán | section Footer, như Dawn |
| Dòng copyright | không có setting: tự sinh từ tên shop (Settings → Store details) và năm hiện tại (OQ-1) |

Trong theme editor, bấm vào một cột link trong sidebar thì preview tô đúng cột đó, ở cả desktop
lẫn mobile.

Chữ shopper đọc mà không phải merchant nhập ("LOG IN", dòng copyright nếu OQ-1 chọn tự sinh) đi
qua file locale. Chữ "Log in" đã có sẵn ở `customer.log_in`.

---

## 4. Việc trên store, ngoài theme

Không có trong repo và không làm bằng code được. Người dùng làm trong admin của
`ngocmx-training`; plan sẽ có checklist từng bước.

- **Menu** (Content → Menus): menu header gồm Mens, Womens (OQ-3); bốn menu footer với đúng các
  link ở mục 2.4. Link trỏ đâu cũng được ("link tùy chọn"), nhưng phải bấm được.
- **Đăng nhập cho khách** (Settings → Customer accounts): bật nút đăng nhập, để header có "LOG IN".
- **Markets**: có Vietnam với VND, và ít nhất một quốc gia khác. Ô chọn country của Dawn chỉ hiện
  khi store có từ hai quốc gia trở lên.
- **Languages**: English và ít nhất một ngôn ngữ nữa được publish. Ô chọn language chỉ hiện khi có
  từ hai ngôn ngữ trở lên.
- **Thanh toán** (Settings → Payments): bật các phương thức muốn có icon ở footer — icon đi theo
  phương thức thật của store (OQ-6).
- **Upload logo**: hai file trong `design/` qua Theme settings (mục 3).

---

## 5. Môi trường — ba ý đầu của đề

| Ý | Xong khi | Hiện tại |
|---|---|---|
| Development store | store tồn tại, theme Dawn chạy lên được | **xong**: `ngocmx-training`, development theme `#187484766378` đã lên và render không lỗi |
| Khởi tạo Dawn, setup denv | `shopify theme dev` chạy **trong container denv** và preview mở được qua `https://<VIRTUAL_HOST>`, theo tài liệu denv của trainer (trích trong brief) | Dawn: xong. denv: chưa — đang chạy `shopify theme dev` trực tiếp trên máy; `denv svc init` chưa từng chạy |
| Integrate theme với GitHub | repo trên GitHub; một branch nối với một theme trên store qua Shopify GitHub app; sửa setting trong theme editor thì Shopify tự tạo commit về branch đó | chưa: repo chưa có commit, chưa có remote. Theme nối GitHub để **chưa publish**; trainer xem qua link preview của theme đó (OQ-7) |

Theo quy trình git của khoá (mục 4.2 trong tài liệu, trích trong brief): làm trên GitHub, không sửa
code trực tiếp trên store, tạo nhánh và viết commit message có nghĩa.

---

## 6. Tiêu chí chấp nhận

Bài xong khi tất cả những điều sau **thấy được trên preview và trong theme editor**, có ảnh chụp
làm bằng chứng:

1. Ở 1440 px: header và footer khớp mục 2.2 và 2.4 — thứ tự, căn trái/giữa/phải, màu nền, màu chữ.
2. Ở 375 px: header và footer khớp mục 2.3 và 2.5. Bấm một dòng accordion thì nó mở ra và hiện
   đúng các link, bấm lại thì đóng; dùng được bằng bàn phím (Tab đến, Enter/Space để mở).
3. Ở 750 và 990 px: đúng như OQ-5 quyết, không có thanh cuộn ngang.
4. Mọi link trong header và footer đều bấm được. "LOG IN" mở đăng nhập của Shopify; search mở ô
   tìm kiếm; chọn country/language đổi được quốc gia và ngôn ngữ.
5. Mỗi trạng thái ở mục 2.6 đã được thử ít nhất một lần.
6. Trong theme editor: đổi từng setting ở mục 3, preview đổi theo; bấm block cột link thì preview
   tô đúng cột; ô LinkedIn để trống thì icon mất.
7. Trang không có `Liquid error`, `Translation missing`; console trình duyệt không có lỗi mới.
8. `shopify theme check --fail-level error`: 0 error, vẫn 9 warning như Dawn gốc. Các guard
   trong `tests/guards/` xanh.
9. Mục 5: denv và GitHub đạt cột "Xong khi".

---

## 7. Quyết định đã có

| # | Điểm | Quyết định | Ai, khi nào |
|---|---|---|---|
| D-1 | Logo | Đề không kèm file. Dùng wordmark dựng lại theo design: `design/logo-blakely-black.png` cho header, `logo-blakely-white.png` cho footer | người dùng, 2026-10-01 ("tự tạo 1 logo phù hợp") |
| D-2 | Cách làm | Setting trước; code chỉ ở chỗ Dawn không làm được, sửa trực tiếp section header và footer của Dawn; không viết section mới | người dùng, 2026-10-01 |
| D-3 | Ai chỉnh gì | Setting của theme do Claude ghi vào `sections/header-group.json`, `sections/footer-group.json`, `config/settings_data.json` để xem được bằng `git diff`; việc chỉ làm được trong admin (mục 4) do người dùng làm theo checklist | người dùng đồng ý cùng D-2, 2026-10-01 |
| D-4 | Màu nền đen | Ảnh đo được #111111; color scheme có sẵn của Dawn (`scheme-4`) là #121212 — lệch 1/255 mỗi kênh, mắt không phân biệt được. **Đề xuất** dùng `scheme-4` có sẵn thay vì sửa màu của nó, vì `scheme-4` còn được dùng ở chỗ khác trong theme | người dùng duyệt cùng spec, 2026-10-01 |

## 8. Giả định — đề và ảnh không nói, chọn theo Dawn

Ghi ra để ai thấy sai thì sửa được; không phải OPEN QUESTION vì không ảnh hưởng điểm chấm theo đề.

- **A-1.** Thứ tự accordion trên mobile (Shop, Company, Info, Important) ứng với cột 1–4 trên desktop.
- **A-2.** Header dính trên đầu khi cuộn lên, như mặc định của Dawn; ảnh tĩnh không cho biết.
- **A-3.** Đường kẻ mảnh dưới header: giữ như Dawn. Trong ảnh, khung đỏ của người chụp đè đúng chỗ
  đó nên không nhìn thấy được.
- **A-4.** Ô tìm kiếm, menu drawer và hộp đăng nhập mở ra giữ nguyên giao diện của Dawn và Shopify.

## 9. OPEN QUESTIONS — đã trả lời

Cả tám câu: người dùng chọn theo đề xuất, 2026-10-01, **chưa hỏi trainer**. Nếu trainer trả lời
khác, câu của trainer thắng và spec được sửa ở cả mục 9 lẫn chỗ thân bài dẫn tới nó.

| # | Câu hỏi | Vì sao phải hỏi | Trả lời |
|---|---|---|---|
| OQ-1 | Copyright giữ **nguyên chữ** "Copyright ThanhDV Training 2025 \| All rights reserved", hay là "Copyright *tên shop* *năm hiện tại* \| All rights reserved"? | "ThanhDV Training" là tên store của người làm design; năm 2025 sẽ cũ | tên shop + năm hiện tại, tự sinh; không thêm setting |
| OQ-2 | "₫ VND" chỉ để **hiển thị** tiền tệ hiện tại, hay **bấm được** để đổi tiền? | Shopify không có ô chọn tiền tệ riêng: tiền tệ đi theo quốc gia, nên "₫ VND" không thể chọn độc lập với "Vietnam" | chỉ hiển thị tiền tệ của quốc gia đang chọn; đổi quốc gia thì nó đổi theo; vẫn hiện khi store chỉ có một quốc gia |
| OQ-3 | Menu header ghi "**MANS**" như ảnh, hay "**Mens**" như footer? | Hai chỗ của cùng design ghi khác nhau; "Mans" có vẻ là lỗi chính tả | "Mens", "Womens" — in hoa bằng CSS nên trên header vẫn ra "MENS", "WOMENS" |
| OQ-4 | Khách **đã đăng nhập** thì chỗ "LOG IN" hiện gì? | Ảnh chỉ có trạng thái chưa đăng nhập | để component account của Shopify hiện chữ cái đầu tên / ảnh của khách, như Dawn đang làm |
| OQ-5 | Từ **750 đến 989 px** (tablet) dùng bố cục nào? | Ảnh chỉ có ~414 px và ~1218/1439 px | dưới 990 px dùng bố cục mobile cho cả header lẫn footer — trùng mốc 990 px mà header Dawn đã dùng; từ 990 px là bố cục desktop |
| OQ-6 | Sáu icon thanh toán phải **đúng sáu cái trong ảnh**, hay **theo phương thức thanh toán thật** của store? | Dawn lấy icon từ phương thức thanh toán đang bật; dev store có thể không bật được đủ sáu loại | theo phương thức thật của store, chỉnh trong admin — đúng gợi ý "dùng shopify setting" của đề |
| OQ-7 | Trainer chấm trên **theme nào**: development theme (link preview), theme nối GitHub (chưa publish, xem qua link preview), hay theme phải **publish làm live**? | Ảnh hưởng ý "Integrate theme với Github"; repo này không bao giờ tự publish theme live | theme nối GitHub, chưa publish, gửi link preview cho trainer; publish chỉ khi người dùng tự quyết |
| OQ-8 | Accordion trên mobile: mở được **nhiều dòng cùng lúc** hay mở dòng này thì dòng kia đóng? | Ảnh chỉ có trạng thái đóng hết | mỗi dòng mở/đóng độc lập; lúc tải trang đóng hết |
