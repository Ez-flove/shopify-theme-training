# EX-01 — Dev store, denv, GitHub, header và footer theo design

Nguồn: Jira [DJSFE-2](https://bss-commerce.atlassian.net/browse/DJSFE-2), mục "II. Bài tập tổng
hợp", trỏ tới Google Doc "Shopify theme document", **mục 4.6 Bài tập, ý 1)**:
<https://docs.google.com/document/d/1Ccd1qqwPF32b2uKV_92V_VIJKiWv9RSU9kIcJIshB08/edit?tab=t.ao3o7aizl5qn#heading=h.o9ks7y4ru33q>

Lấy về ngày 2026-10-01. Phần giữa hai vạch là nguyên văn của trainer; chỉ bỏ ký tự escape của bản
export Markdown, không sửa chữ nào. Ảnh design nằm trong `design/`.

---

1) Thực hiện bài tập với yêu cầu như sau: (4đ)

- Tạo một development store
- Khởi tạo theme Dawn, setup denv env shopify (0.5)
- Integrate theme với Github (0.5)
- Thực hiện các thay đổi ở header giống với design (1.5đ)

  Design mobile: <https://drive.google.com/file/d/1e6FFqI8HiEmcsjMk8ehkygUWUVk6-tmx/view?usp=sharing> (không yêu cầu style menu)

  Design desktop: <https://drive.google.com/file/d/1R38hLApOa7bZyXR75GPuFhUH1ahKwnsq/view?usp=sharing>

  Lưu ý: Font chữ không cần chính xác nhưng vị trí và màu sắc các element cần phải đúng.

- Thực hiện các thay đổi sau ở footer giống với design (1đ)

  Design mobile: <https://drive.google.com/file/d/1N_bt4tDABZNCazkWHg_rwKcB_kjtL0dB/view?usp=sharing>

  Design desktop: <https://drive.google.com/file/d/1RoSs3sWSAkIYDJGfp_UP-TjkmFs9dlrp/view?usp=sharing>

  Lưu ý:

  Font chữ không cần chính xác nhưng vị trí và màu sắc các element cần phải đúng.

  Các link có thể click vào được và không cần phải chèn link chính xác, link tùy chọn.

  Có nhiều phần có thể dùng theme editor và shopify setting để làm được và cần phải tự tìm.

- Responsive tương thích với các thiết bị 0.5

---

## Trích thêm từ cùng nguồn

Không phải đề bài, nhưng là chỗ trainer chỉ tới cho hai ý "setup denv env shopify" và "Integrate
theme với Github". Nguyên văn.

**"Shopify theme document", mục 4.2 Quy trình git trong chương trình training**

> Trong chương trình này chỉ yêu cầu dev connect Github với Store
>
> - Developers chỉ làm việc trên Github
> - Dev không thay đổi code trực tiếp trên Shopify Store
> - Tạo nhánh và commit message có nghĩa

**"6. Setup project với denv", mục Setup Shopify và Setup Shopify Theme**
(<https://docs.google.com/document/d/1YoGLao-1Wdo6i178fJjzovnlQr_MHEjjJkZRF37HRGY/edit?tab=t.0>, Jira
gọi nó là "Setup shopify CLI with denv")

> **Setup Shopify:**
>
> - Docker compose default ở ~/.denv/svc/platform/shopify
> - Folder code của shopify trong container nằm ở /app
> - 1 số env lưu ý:
>   - SHOPIFY_API_KEY và SHOPIFY_API_SECRET: thông tin api của app trên <https://partners.shopify.com>, nếu điền 2 thông tin này thì khi chạy app nó sẽ không hỏi connect với app nào trên shopify nữa
>   - Các giá trị như DOCKER_UID, DOCKER_GID, WORK_DIR không cần khai báo, tool sẽ tự check và sử dụng cho docker compose (WORK_DIR sẽ tương ứng với folder đang chạy tool), nếu project đã có docker trước đấy thì copy giá tri env tương ứng trong docker/enviroment/.env sang .denv.env là đc
> - Các bước tương tự như magento
> - Phần rewrite trong docker-compose sẽ thêm file .env vào .denv để dùng trên local và git lên
> - Thông tin login được lưu trong **~/.config/shopify-cli-kit-nodejs/config.json** của container shopify, để logout có thể xóa file này hoặc chạy lệnh **shopify auth logout**
>
> **Setup Shopify Theme:**
>
> - Tạo mới theme như hướng dẫn: <https://shopify.dev/docs/storefronts/themes/getting-started/create>
> - Chạy shopify theme dev --store {store-name} nó sẽ ra giao diện như này
> - Để vào link preview theme trên local (là cái 0.0.0.0:9292 như ảnh trên) sẽ vào qua url https://VIRTUAL_HOST với VIRTUAL_HOST là giá trị trong .denv.env

"Các bước tương tự như magento" là mục Setup Magento của cùng tài liệu: `denv svc init`, `denv env
init`, sửa `.denv.env`, `denv env up`.
