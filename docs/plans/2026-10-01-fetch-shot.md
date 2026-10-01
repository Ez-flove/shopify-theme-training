# Tool fetch-shot: tải ảnh chụp màn hình từ link về `.local/shoot/`

Ngày: 2026-10-01
Spec: không có — tooling cho môi trường training

## 1. Thiếu cái gì

Trainer hay gửi ảnh chụp màn hình dưới dạng link Lightshot (`https://prnt.sc/wyq2moKuoeul`). Link
đó là một trang HTML, không phải ảnh, nên Claude không đọc được ảnh và cũng không có chỗ cố định
để lưu làm bằng chứng.

## 2. Đã đo

| Trường hợp | Kết quả |
|---|---|
| `curl https://prnt.sc/wyq2moKuoeul` không User-Agent | HTTP 520 |
| Có User-Agent trình duyệt | 200, ảnh thật ở `<img id="screenshot-image" src=…>` và `og:image`: `https://img.lightshot.app/dZtWI-ELQF-vMyLtf4c3SQ.png` |
| Tải ảnh đó | 200 `image/png`, 212909 byte, PNG 414×693 |
| Id không tồn tại (`zzzzzzzzzzzzz9`) | 302 → `https://prnt.sc/` |
| Id cũ/bị xoá (`aaaaaa`) | 200, ảnh là placeholder `//st.prntscr.com/.../img/0_173a7b_211be8ff.png` |

## 3. Sửa gì, cố ý không sửa gì

- Tool mới `tools/fetch-shot/main.py` (Python 3.8, chỉ stdlib), gọi qua `tools/run fetch-shot`
  nên đã nằm trong quyền `Bash(tools/run *)`.
- Nhận link `prnt.sc` / `prntscr.com` và link ảnh trực tiếp. Mỗi đối số được quét tìm URL, nên dán
  nguyên một đoạn chat có nhiều link cũng được.
- Lưu `.local/shoot/<id>.<ext>`; đã có thì bỏ qua, trừ khi `--force`. Ghi `index.tsv` để biết file
  nào từ link nào.
- Từ chối, không lưu gì, khi: trang về trang chủ, ảnh là placeholder, nội dung tải về không phải
  ảnh (kiểm magic bytes), hoặc là trang HTML của site khác.
- `.local/` vào `.gitignore` và `ignoreDirs`.

Cố ý không làm: không đoán `og:image` cho site chưa đo (gyazo, imgur, Drive…) — `og:image` của một
trang bất kỳ có thể là logo chứ không phải ảnh chụp; thêm từng site khi đã đo. Không retry.

## 4. Kiểm bằng gì

1. Link mẫu → lưu `wyq2moKuoeul.png`, PNG 414×693
2. Chạy lại → bỏ qua, không tải lại
3. Id không tồn tại → lỗi, không có file
4. Id `aaaaaa` → lỗi "placeholder", không có file
5. Link ảnh trực tiếp → lưu
6. Một đối số chứa nhiều link → lưu từng cái
7. `https://example.com` → từ chối
8. Có một link lỗi thì exit 1 và nêu tên link đó

## 5. Trạng thái

| # | Việc | Trạng thái | Bằng chứng |
|---|---|---|---|
| 1 | Tool | xong | `tools/run` liệt kê `fetch-shot` |
| 2 | `.gitignore`, `ignoreDirs`, `CLAUDE.md` | đã kiểm | `git check-ignore -v` → `.gitignore:23:.local/`; `ignoreDirs` có `.local`; CLAUDE.md có lệnh và luật "fetch trước khi trả lời" |
| 3 | 8 ca ở §4 | đã kiểm | bảng dưới |

| Ca | Kết quả |
|---|---|
| 1 link mẫu | `saved .local/shoot/wyq2moKuoeul.png 414x693 212909 B`, exit 0; `file` xác nhận PNG 414×693; Read xem được ảnh |
| 2 chạy lại | `exists`, không tải lại, exit 0 |
| 3 id không tồn tại | "no such screenshot — Lightshot redirected to https://prnt.sc/", không có file, exit 1 |
| 4 id `aaaaaa` | "removed or expired — … placeholder image … st.prntscr.com …", không có file, exit 1 |
| 5 link ảnh trực tiếp | saved, 414x693, exit 0 |
| 6 nhiều link trong một đối số | 3 link: 1 `exists`, 1 `saved` (JPEG 500x477, khớp `file`), 1 lỗi có tên |
| 7 `https://example.com/` | "an HTML page, not an image…", exit 1 |
| 8 có link lỗi | exit 1, nêu đúng link lỗi; các link khác vẫn được lưu |
| thêm: `--force` | tải lại, exit 0 |
| thêm: `--out ../outside` | "must stay inside the project", exit 2, không tạo thư mục |

Không có file tạm sót lại trong `.local/shoot/` sau các ca lỗi. File của ca 5 và 6 đã xoá sau khi
kiểm; chỉ giữ ảnh của link mẫu.
