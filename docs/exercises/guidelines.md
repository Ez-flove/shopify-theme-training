# Lưu ý khi customize theme — dùng chung cho mọi bài

Nguyên văn mục **4.3 Lưu ý khi customize theme** của Google Doc "Shopify theme document"
(<https://docs.google.com/document/d/1Ccd1qqwPF32b2uKV_92V_VIJKiWv9RSU9kIcJIshB08/edit?tab=t.ao3o7aizl5qn>),
lấy về ngày 2026-10-01. Không phải đề của bài nào, nhưng là tiêu chí trainer đặt cho mọi thay đổi
theme, nên spec của từng bài trích từ đây thay vì chép lại.

---

Guiding principles:

- Be performant

  Chú trọng performance, dùng snippets để tái sử dụng các đoạn code lặp lại, giảm thiểu việc sử dụng javascript

  Check network tab xem có nhiều request asset được fetch vào thời điểm load trang không ?

  Giảm bớt các request không cần thiết load ngay

  Sử dụng lazy loading

  Không import các file asset vào section/snippets, nếu section đó được render nhiều lần trong một page, quá trình [repaint](https://developer.mozilla.org/en-US/docs/Glossary/Repaint) của browser sẽ bị lặp lại nhiều lần ảnh hưởng performance

- Be purpose-built

  Mỗi theme cần có layout, style, và feature set được thiết kế tối ưu cho một nhóm người bán hàng hoặc phân khúc thị trường cụ thể. Ngay từ khi sử dụng, theme nên cung cấp cho người bán bộ công cụ được tối ưu hóa để đáp ứng nhu cầu của họ, dựa trên những gì họ bán và đối tượng họ hướng đến. Các theme chuyên biệt mang lại giá trị cao hơn cho người bán so với các giao diện chung chung.

- Offer best-in-class UX

  Với sự gia tăng số lượng cửa hàng Shopify, theme có khả năng dẫn đầu ngành và định hình các mẫu trải nghiệm người dùng trong thương mại điện tử. Theme cần được thiết kế với chất lượng cao, lấy khách hàng làm trung tâm.

- Be mobile first

  Với phần lớn lưu lượng truy cập cửa hàng trực tuyến diễn ra trên thiết bị di động, thiết kế dành cho thiết bị di động phải được đặt lên hàng đầu trong suốt quá trình build theme.

  Mobile design cần được ưu tiên trong quá trình build theme

  Xử lý responsive cần được thực hiện từ màn mobile trở lên. Vì mobile có kích thước viewport nhỏ, việc hiển thị content sẽ khó hơn desktop, việc cover các case khó ở mobile sẽ làm giảm các lỗi style responsive

  => Ưu tiên sử dụng min-width media query

  ```css
  /* Default styles for mobile */
  .grid-container-flex {
      font-size: 1rem;
    }

  /* Media query for tablet*/
  @media (min-width: 768px) {
    .grid-container-flex {
      font-size: 1.3rem;
    }
  }

  /* Media query for desktops */
  @media (min-width: 1024px) {`
    .grid-container-flex {
      font-size: 2rem;
    }
  }
  ```

  Chú ý độ tương thích của các thuộc tính trên các browser khác nhau <https://caniuse.com/?search=gap>

- Be accessible

  Để mang lại trải nghiệm tốt nhất cho nhiều nhóm người bán và khách hàng, theme cần được xây dựng từ nền tảng với sự quan tâm đến mọi loại người dùng và các best practice về khả năng truy cập.

- Make customization simple

  Người bán sử dụng theme để thể hiện thương hiệu của họ tới khách hàng tiềm năng. Theme cần linh hoạt với các tùy chọn được thiết kế hợp lý để người bán có thể dễ dàng thực hiện các tùy chỉnh, nhưng vẫn đủ đơn giản để quản lý, giúp họ thiết lập cửa hàng nhanh chóng và bắt đầu bán sản phẩm.

---

Ví dụ CSS trong tài liệu dùng breakpoint 768px và 1024px; Dawn dùng 750px và 990px
(`.claude/rules/shopify-theme.md` §2). Bài nào cần breakpoint thì spec của bài đó ghi rõ dùng bộ
nào.
