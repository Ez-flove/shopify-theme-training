# EX-02 — Section Product recommendations

Nguồn: Jira [DJSFE-2](https://bss-commerce.atlassian.net/browse/DJSFE-2), mục "II. Bài tập tổng
hợp", trỏ tới Google Doc "Shopify theme document", **mục 4.6 Bài tập, ý 2)**:
<https://docs.google.com/document/d/1Ccd1qqwPF32b2uKV_92V_VIJKiWv9RSU9kIcJIshB08/edit?tab=t.ao3o7aizl5qn#heading=h.o9ks7y4ru33q>

Lấy về ngày 2026-10-01. Phần giữa hai vạch là nguyên văn của trainer; chỉ bỏ ký tự escape của bản
export Markdown. Chỗ duy nhất bị sửa: mật khẩu của store demo không chép vào repo, vì repo sẽ lên
GitHub — xem ở tài liệu gốc. Ảnh design nằm trong `design/`.

---

2) Tạo mới 1 section Product recommendations: 6d

- Layout ( 1đ )
  - Heading
  - Description
  - List button: Chứa các nút để lựa chọn giữa các loại sản phẩm như:
    - Sản phẩm liên quan
    - Sản phẩm đã xem
  - Product grid: Danh sách sản phẩm hiển thị theo action được chọn từ List Button.
- Yêu cầu chi tiết: ( 5đ )

1. Settings Section/Block Schema: (0.25đ):
   - Section chỉ hiển có thể config ở product
   - Các config ngắn gọn dễ hiểu (Có note đối với những config gây confused)
2. List button ( 0.75đ ):
   - Chức năng: Khi người dùng nhấn vào một trong các nút trong List Button (ví dụ: Sản phẩm liên quan, Sản phẩm đã xem), Product Grid sẽ được cập nhật để hiển thị các sản phẩm tương ứng:
     - Sản phẩm liên quan: Hiển thị các sản phẩm liên quan đến sản phẩm hiện tại.
     - Sản phẩm đã xem: Hiển thị các sản phẩm mà người dùng đã xem trước đó.
3. Product Grid ( 1đ ):
   - Chức năng: Product Grid sẽ hiển thị các sản phẩm dựa trên action mà người dùng chọn từ List Button.
   - Hình thức hiển thị: Sử dụng hai dạng hiển thị khác nhau: (viết config style type từ phía admin)
     - Carousel (Slider): Các sản phẩm sẽ được hiển thị dưới dạng băng chuyền (carousel slider), cho phép người dùng cuộn qua các sản phẩm với các nút prev (trước) và next (sau): <https://drive.google.com/file/d/1Dwtaqrp1o0OJQ4scdYYg_9tfl8afQ5az/view?usp=drive_link>
     - Grid: Các sản phẩm cũng có thể được hiển thị dưới dạng lưới thông thường (grid view), giúp người dùng xem nhiều sản phẩm cùng lúc: <https://drive.google.com/file/d/1G3HF6YKYMI2sd1ekA6VTEv260Jv3LToj/view?usp=drive_link>
4. Quy Trình Hoạt Động ( 2đ ):
   - Khi người dùng nhấn vào Sản phẩm liên quan hoặc Sản phẩm đã xem, hệ thống sẽ tự động thay đổi các sản phẩm trong Product Grid mà không cần tải lại trang.
   - Product Grid sẽ cập nhật và hiển thị các sản phẩm từ Sản phẩm liên quan hoặc Sản phẩm đã xem mà không cần phải gọi lại API nhiều lần.
   - Cover trường hợp fetch data không có sản phẩm phù hợp.
5. Yêu cầu nâng cao ( 1đ ):
   - Carousel và Grid View cần phải hoạt động mượt mà và tối ưu cho mọi thiết bị. Sử dụng lazy loading để tải các sản phẩm khi người dùng cuộn xuống, giúp tăng tốc độ tải trang.
   - Đảm bảo API được gọi đúng cách và không gây tải lại không cần thiết.
   - Giao diện phải tương thích tốt trên cả thiết bị di động và máy tính để bàn để đảm bảo trải nghiệm người dùng mượt mà.

Tham khảo:

<https://shopify.dev/docs/api/ajax/reference/product-recommendations>

<https://shopify.dev/docs/storefronts/themes/navigation-search/search>

<https://shopify.dev/docs/api/ajax/reference/predictive-search>

Video: <https://www.loom.com/share/fd7e68df89d04fd6bd56daa8e4fa5af9>

Demo:

- <https://dtn1-theme.myshopify.com/products/sony-srs-xg300-x-series-portable-wireless-speaker>
- Password: *(không chép vào repo — xem tài liệu gốc)*

Source code: <https://github.com/Duongtu1209/product-recommendations>

---
