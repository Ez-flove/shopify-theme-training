# Workflow

Một lifecycle duy nhất, chạy từ trên xuống. Chi tiết từng bước nằm trong chính command —
file này chỉ nói thứ tự, chỗ dừng, và nó trông thế nào với một bài tập theme.

```
đề bài  →  spec  →  plan  →  build  →  guard  →  verify  →  cleanup
             ↑        ↑
           gate 1   gate 2      hai chỗ phải có người đồng ý trước khi sửa file đầu tiên
```

## Command nào cho việc gì

| Việc | Command |
|---|---|
| Làm một bài tập | `/flow-feature EX-01` |
| Có thứ đang sai | `/flow-fix-bug` |
| Đổi hành vi đang đúng | `/flow-enhance` |
| Soát một phạm vi | `/flow-review` |
| Soát một PR | `/flow-review-pr` |
| Thêm hoặc kiểm một guard | `/flow-guard` |
| Commit | `/flow-commit` |

## Một bài tập đi từ đầu tới cuối

1. **Dán đề.** Tạo `docs/exercises/EX-01-<slug>/brief.md`, dán nguyên văn đề của trainer, không
   sửa chữ nào. Ảnh design hoặc link Figma để trong `docs/exercises/EX-01-<slug>/design/`.
2. **`/flow-feature EX-01`.** Claude đọc đề, đọc code Dawn liên quan, rồi viết spec vào
   `docs/specs/features/`. Chỗ nào đề không nói rõ — setting nào merchant chỉnh được, mobile hiển
   thị ra sao, khi trống thì sao — sẽ thành OPEN QUESTION. **Gate 1:** bạn đọc spec, trả lời câu
   hỏi (hoặc mang đi hỏi trainer), rồi đồng ý.
3. **Plan.** Claude viết plan vào `docs/plans/`: sửa file nào ở dòng nào, cố ý không sửa gì, và
   **những đầu nào phải biết** theo `.claude/rules/shopify-theme.md` §1 — schema, nhánh render,
   locale, preset, JS. **Gate 2:** bạn đồng ý plan.
4. **Build.** Chạy `shopify theme dev` ở nền, sửa code, xem preview tự reload. Bảng trạng thái
   trong plan được cập nhật ngay khi mỗi việc xong, kèm bằng chứng.
5. **Guard.** Nếu bài tập thêm một luật mà guard hiện có không thấy được, `/flow-guard add` viết
   guard mới và chứng minh nó biết đỏ bằng `tools/run mutate`.
6. **Verify.** Chạy đủ lệnh ở mục Verify bên dưới, rồi kiểm trên trình duyệt và theme editor.
7. **Review và commit.** `/flow-review` soát lại theo spec, `/flow-commit` khi bạn bảo commit.

## Superpowers dùng ở đâu trong luồng này

Plugin superpowers đã bật cho project. Các command `/flow-*` vẫn là lối vào và giữ hai cái gate;
skill của superpowers là cách làm bên trong từng bước — `brainstorming` lúc viết spec,
`writing-plans` lúc viết plan, `systematic-debugging` trong `/flow-fix-bug`. Spec và plan vẫn nằm
ở `docs/specs/features/` và `docs/plans/`, không phải `docs/superpowers/`. Không skill nào tự
commit. Bảng đầy đủ và luật TDD cho theme ở mục "Superpowers alongside the flow kit" trong
`CLAUDE.md`.

## Đặt tên tài liệu

```
docs/exercises/EX-<nn>-<slug>/brief.md
docs/exercises/EX-<nn>-<slug>/design/
docs/specs/features/YYYY-MM-DD-<slug>-EX-<nn>.md
docs/plans/YYYY-MM-DD-<slug>-EX-<nn>.md
```

Plan ghi ở header nó implement spec nào. Nhiều bài thì dùng khoảng, ví dụ `EX-03-05`.

## Hai cái gate, và vì sao không bỏ được

**Gate 1 — spec.** Viết bài tập làm gì từ phía người dùng: shopper thấy gì, merchant chỉnh được gì
trong theme editor, mỗi trạng thái (trống, một item, nhiều item, hết hàng), mobile và desktop. Chỗ
nào đề chưa rõ thì ghi thành OPEN QUESTION chứ không tự chọn.

**Gate 2 — plan và contract.** Plan nói bốn điều: sai/thiếu cái gì (bằng lời của người dùng), ở
đâu (`file:line`, đo chứ không đoán), sửa gì và cố ý không sửa gì, và kiểm bằng cách nào — kèm
mutation nào phải làm nó đỏ. Contract của một theme là **schema**: id và type của từng setting,
type của từng block, giá trị mặc định, preset. Chốt ở đây, trước khi có dòng Liquid nào — đổi id
setting sau khi merchant đã lưu thì giá trị cũ mất.

Plan tới sau khi sửa thì không còn là plan, nó là bản tường thuật — và tường thuật thì không ai
phản đối được nữa vì tiền đã trả rồi.

## Plan là bảng theo dõi, không phải bản nháp một lần

Trạng thái đổi lúc nó đổi: đã đo → đã lên plan → đã làm → đã kiểm. Việc nào đóng thì bằng chứng
ghi **vào plan**, không phải chỉ nói trong chat — chat trôi mất. Việc nào hoãn thì sang
`docs/tech-debt.md` ngay lúc hoãn, kèm cái gì mở được nó.

## Luật build cho theme

1. **Schema trước Liquid** — chốt setting và block trong `{% schema %}` trước khi viết markup
2. **Đọc cách Dawn đã làm** — tìm section gần giống nhất trong `sections/` rồi theo convention
   của nó (class CSS, custom element, cách load asset), trừ khi đề nói khác
3. **Mỗi block type một nhánh `when`**, mỗi wrapper block một `{{ block.shopify_attributes }}`
4. **Chuỗi hiển thị đi qua locale** — `{{ 'key' | t }}` và key trong `locales/en.default.json`
5. **CSS và JS của section nằm trong `assets/`** — CSS scope theo section, JS viết thành custom
   element để sống sót khi theme editor render lại section
6. **Thêm setting, block, chuỗi thì đọc `docs/architecture/change-guards.json` và
   `.claude/rules/shopify-theme.md` §1 trước khi viết**, không phải sau

## Cleanup

Code cuối cùng phải đọc như thể lần đầu đã viết đúng. Không để lại comment kiểu "sửa từ X",
không code bị comment, không tên tạm (`id_new`), không `console.log`, không setting khai mà không
dùng.

## Verify

Chạy đúng lệnh của project (`flow.config.json` → `commands`) và **dán output thật**:

```bash
shopify theme check --fail-level error    # baseline Dawn v16: 0 error, 9 warning
tools/run js-syntax
node --test 'tests/guards/*.test.js'
tools/run change-guards --check
tools/run shared-rules
```

Rồi làm đủ checklist ở `.claude/rules/shopify-theme.md` §3: mở trang trên preview, tìm
`Liquid error` và `Translation missing`, thử từng setting trong theme editor, click block xem có
highlight, xem bốn độ rộng 375 / 750 / 990 / 1440, xem trạng thái trống, đọc console.

Hai cái bẫy khi đọc kết quả:

- **Theme Check xanh không có nghĩa là bài tập xong.** Nó kiểm code có hợp lệ không, không kiểm
  shopper có thấy đúng thứ đề yêu cầu không.
- **Preview có đang chạy code mới không?** File nào bị Shopify từ chối (lỗi cú pháp Liquid,
  schema sai) thì `shopify theme dev` báo lỗi ở output của nó, và trang đang xem có thể không phải
  code vừa sửa. Đọc output đó trước khi kết luận một sửa đổi không có tác dụng.

Muốn nói xong thì phải mở đúng trang, thấy đúng thứ đề yêu cầu, và ghi bằng chứng vào plan.
