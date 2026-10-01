# Setup môi trường training Shopify theme trên claude-flow-kit

Ngày: 2026-10-01
Spec: không có — đây là việc foundation cho môi trường, không phải một bài tập
Theme nền: Dawn v16.0.0 (`git clone --depth 1 --branch v16.0.0 https://github.com/Shopify/dawn.git`)

## 1. Sai hoặc thiếu cái gì

Kit mặc định cho repo Node/TypeScript có server. Theme Dawn là Liquid + JSON + JS thuần, không có
build, không có server. Cài nguyên kit thì:

- `sourceGlobs` chỉ nhận `*.ts/*.js`, nên hook `Stop` và `shared-rules discover` không thấy file
  `.liquid` nào — im lặng vì không có chỗ nhìn, không phải vì sạch.
- `commands` là `yarn test/lint/build` — Dawn không có `package.json`, mọi lệnh verify đều hỏng.
- `code-security.md` là checklist REST API (IDOR, DTO, rate limit) — không áp dụng cho theme, còn
  thứ áp dụng (escape output, token lộ trong theme, `| json` khi nhét dữ liệu vào `<script>`) thì
  không có.
- `change-reaches-every-end.md` không biết một setting hay block mới trong theme phải tới những
  đầu nào (schema, nhánh render, `shopify_attributes`, locale, preset).
- `guardGlobs` trỏ vào `__tests__/architecture/*.spec.ts` — không có guard nào, và chưa có test
  runner.

## 2. Ở đâu (đã đo)

| Chỗ | Đo được |
|---|---|
| `flow.config.json` | `sourceGlobs` TS/JS, `commands` = yarn — bản `install.sh --yes` ghi ra |
| `.claude/rules/code-security.md` | toàn bộ là REST API / server |
| `.claude/settings.json` | không có quyền cho `shopify`, `node`; không chặn `theme publish/delete` |
| `shopify theme check --fail-level error` | Dawn v16: 161 file, 9 warning, 0 error, exit 0 |
| `node --check assets/*.js` | 36/36 file qua |
| Theme Check `--list` | không check nào bắt "block type khai trong schema mà section không render" |
| 48 section Dawn | 19 section có block; section 1 type không rẽ nhánh; `main-cart-footer` render `buttons` bằng `else` của `case block.type`; 8 section khai `@app` đều có `{% render block %}` |

## 3. Sửa gì, và cố ý không sửa gì

Sửa:

- `flow.config.json` — glob theo thư mục theme, lệnh `shopify theme check` / `node --check` /
  `node --test`, `sourcesOfTruth` cho bài tập (đề bài → design → shopify.dev → spec → plan).
- `code-security.md` — viết lại phần "How we enforce it" cho Liquid theme (ADAPT.md cho phép).
- `change-reaches-every-end.md`, `business-logic-analysis.md` — thêm một dòng trỏ sang rule theme.
- Rule mới `.claude/rules/shopify-theme.md` — các đầu của một thay đổi trong theme, lớp lỗi riêng
  của theme, cách verify trên trình duyệt.
- `.claude/settings.json` — cho phép lệnh đọc của Shopify CLI và `node`; `theme push` phải hỏi;
  chặn `theme publish` / `theme delete`.
- Guard đầu tiên `tests/guards/section-blocks.test.js` (Node test runner có sẵn, không cần cài gì).
- `CLAUDE.md`, `docs/WORKFLOW.md`, `README.md`, khung `docs/exercises/`.

Cố ý không sửa:

- `tools/` — ADAPT.md: sửa config, không sửa tool, để lần cập nhật kit sau không đè mất.
- `harness.md`, `security.md`, `writing-style.md` — không phụ thuộc stack.
- `plugin/` của kit — không đụng.
- Không viết đề bài nào — người học tự thêm.
- Không đăng ký plugin, không kết nối store, không commit — đều là việc người dùng tự làm.
- Không cài Prettier hay npm package nào — giữ theme không phụ thuộc.

## 4. Kiểm bằng gì

1. `tools/run change-guards` sinh đúng 1 guard; `--check` xanh
2. `tools/run shared-rules` sạch và báo số file `discover` đã đọc (> 0, là file Liquid)
3. `shopify theme check --fail-level error` vẫn exit 0, số file inspected không đổi (161)
4. `node --test` xanh trên Dawn gốc
5. `tools/run mutate` — mỗi điều kiện của guard một mutation, đều phải đỏ:
   - đổi `when 'title'` trong `main-product.liquid` → thiếu nhánh render
   - bỏ `{{ block.shopify_attributes }}` trong `multicolumn.liquid` → theme editor không chọn được block
   - bỏ `{% render block %}` trong `footer.liquid` → app block khai mà không render
   - bỏ `else` của `case block.type` trong `main-cart-footer.liquid` → ngoại lệ không còn đúng
6. Hook: `guard-bash` chặn `git push --force`; `plan-gate` im khi có plan

## 5. Trạng thái

| # | Việc | Trạng thái | Bằng chứng |
|---|---|---|---|
| 1 | Dawn v16.0.0 vào thư mục gốc, `git init` | xong | `ls` có layout/sections/...; `.git` mới |
| 2 | `install.sh --yes` | xong | 23 file, cả 5 hook script có mặt |
| 3 | `flow.config.json` cho theme | đã kiểm | `walk_files` trả 256 file, toàn bộ trong thư mục theme (assets 101, locales 51, sections 48, snippets 39, templates 13, config 2, layout 2) |
| 4 | Rules: `code-security`, `shopify-theme`, hai dòng trỏ | xong | mọi điều nói về Dawn đo trên v16.0.0: `window.routes` ở `layout/theme.liquid:354`, danh sách id swap ở `assets/product-info.js:205-209`, breakpoint 750/990 |
| 5 | `.claude/settings.json` | đã kiểm | JSON hợp lệ; `theme publish/delete` + push live bị deny, `push/pull/share` phải hỏi. Hook chạy thật: `guard-bash` chặn force push (chặn cả lệnh test của chính setup này), `guard-paths` chặn ghi ngoài project và `.env`, `guard-read` chặn `~/.ssh` |
| 6 | Guard `section-blocks` + mutation | đã kiểm | xanh 4/4 trên Dawn gốc; 5 mutation đều đỏ đúng case (bảng dưới); `sections/` giống hệt Dawn sau khi hoàn nguyên (`diff -r -q`) |
| 7 | `CLAUDE.md`, `WORKFLOW.md`, `README.md`, `docs/exercises/` | xong | README gốc của Dawn chuyển sang `docs/dawn-README.md` |
| 8 | Chạy đủ mục §4 | đã kiểm | bảng dưới |

### Kết quả kiểm

| Kiểm | Kết quả |
|---|---|
| `tools/run change-guards --check` | 1 guard, clean, exit 0 |
| `tools/run shared-rules` | discover đọc 256 file, 0 rule, clean |
| `tools/run js-syntax` | 36 file, clean; mutation phá `assets/cart.js` → đỏ, nêu đúng file |
| `node --test 'tests/guards/*.test.js'` | 4 pass, 0 fail |
| `shopify theme check --fail-level error` | 161 file (không đổi so với Dawn gốc), 9 warning, exit 0 |

| Mutation | Case đỏ |
|---|---|
| `main-product.liquid`: `when 'title'` → `when 'titel'` | 1 — nêu `main-product.liquid → 'title'` |
| `multicolumn.liquid`: bỏ `{{ block.shopify_attributes }}` | 2 — nêu `multicolumn.liquid` |
| `footer.liquid`: bỏ `{% render block %}` | 3 — nêu `footer.liquid` |
| `main-cart-footer.liquid`: `else` → `when 'buttons'` | 4 — ngoại lệ cũ, nêu "has its own when now" |
| `main-cart-footer.liquid`: `else` → `when 'checkout'` | 1 và 4 — `buttons` không được render, ngoại lệ mất `else` |

### Phát hiện trong lúc làm

- `node --test tests/guards/` hỏng trên Node 22: thư mục bị coi là module. Lệnh `test` dùng glob
  có nháy `'tests/guards/*.test.js'` để Node tự mở rộng.
- Kiểm `shopify_attributes` theo từng nhánh `when` đo được 15 chỗ "thiếu" trên Dawn gốc, vì Dawn
  đặt nó ở wrapper ngoài `case` (collage, footer). Guard kiểm ở mức section và ghi giới hạn này
  ngay trong file.
- `plan-gate` không đọc `ignoreDirs`, chỉ đọc `sourceGlobs`. Glob theo thư mục theme là thứ giữ
  cho file JSON trong `claude-flow-kit/` và `docs/` không bị tính là source.

---

## Bổ sung: plugin superpowers (2026-10-01)

**Cài:** `claude plugin install superpowers@claude-plugins-official --scope project` → superpowers
6.4.1 (commit `5bf4e78`), 15 skill, 1 hook `SessionStart`, ~838 token mỗi session. Ghi vào
`.claude/settings.json` → `enabledPlugins`.

**Va chạm với kit, đã đo trong skill của nó:**

| Chỗ | superpowers | kit | Xử lý |
|---|---|---|---|
| Spec | `docs/superpowers/specs/` (`brainstorming/SKILL.md:135`) | `docs/specs/features/` | CLAUDE.md chỉ nơi lưu; skill ghi "User preferences for spec location override this default" |
| Plan | `docs/superpowers/plans/` (`writing-plans/SKILL.md:18`) | `docs/plans/` — `plan-gate` chỉ nhìn chỗ này | như trên |
| Commit | brainstorming commit spec, writing-plans "frequent commits", worktree commit `.gitignore` | không commit khi chưa được bảo | CLAUDE.md nói rõ là luật này thắng; `using-superpowers/SKILL.md:65` xếp CLAUDE.md trên skill |
| TDD | "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" | Liquid không render được ở local | CLAUDE.md định nghĩa "test đỏ" cho từng loại thay đổi trong theme |
| Worktree | `.worktrees/` ở gốc, chưa ignore thì tự thêm `.gitignore` rồi commit | | thêm `.worktrees/`, `.superpowers/` vào `.gitignore` và `ignoreDirs` ngay |

**Cố ý không sửa:** không đụng file nào của plugin (nằm trong cache, cập nhật sẽ đè); không tắt
skill nào; không đăng ký plugin `flow` của kit (người dùng chưa yêu cầu).

**Kiểm:** `settings.json` hợp lệ và có `enabledPlugins`; `git check-ignore` nhận `.worktrees` và
`.superpowers`; các lệnh verify của setup vẫn xanh.

**Trạng thái: đã kiểm.** `claude plugin list` → superpowers 6.4.1, scope project, enabled;
`settings.json` và `flow.config.json` hợp lệ; `git check-ignore -v` nhận `.worktrees/probe/x`
(`.gitignore:19`) và `.superpowers/sdd/x` (`.gitignore:20`); change-guards clean, shared-rules đọc
256 file, js-syntax 36 file clean, guard 4 pass 0 fail. Mục mới trong `CLAUDE.md`: "Superpowers
alongside the flow kit"; đoạn tiếng Việt tương ứng trong `docs/WORKFLOW.md`.

---

## Bổ sung: lần chạy `shopify theme dev` đầu tiên phá `settings_schema.json` (2026-10-01)

**Sai gì.** Preview `http://127.0.0.1:9292` lên được nhưng trang chủ có 4 `Liquid error`
(`layout/theme.liquid` dòng 75, 79, 294, 299: "font_face/font_url can only be used with a font
drop"), font và màu đều rỗng (`--font-body-family: , ;`, `--color-background: ,,;`), trong khi
`--page-width: 120rem` vẫn đúng.

**Ở đâu (đã đo).** `config/settings_schema.json` còn đúng `[]` (3 byte, bản Dawn v16.0.0 là 1470
dòng), bị ghi lúc 11:06:49. Lệnh đang chạy là `shopify theme dev --store ngocmx-training
--theme-editor-sync` (PID 101194, chạy từ terminal của người dùng). Cùng đợt 11:06:49–11:07:03,
sync còn ghi lại `sections/header-group.json`, `sections/footer-group.json`,
`config/settings_data.json` và `templates/{404,article,password,product}.json`: thêm comment
"auto-generated" ở đầu, đổi thứ tự key, bỏ một số setting. Nghi ngờ (chưa kiểm): development
theme mới tạo trên store có `settings_schema.json` rỗng trước khi upload xong, và sync coi đó là
thay đổi từ editor rồi kéo về đè bản local. Repo chưa có commit nên git không khôi phục được.

**Sửa gì.** Chép lại `config/settings_schema.json` từ Dawn v16.0.0
(`raw.githubusercontent.com/Shopify/dawn/v16.0.0/config/settings_schema.json`) — setup không sửa
file này, nên bản gốc chính là bản trước sự cố. **Cố ý không sửa:** các file JSON bị chuẩn hoá
còn lại — nếu chỉ bỏ setting bằng giá trị mặc định thì nội dung không đổi; kiểm trước khi kết
luận (mục Kiểm).

**Kiểm.** (1) `cmp` với bản gốc; (2) trang chủ trên preview hết `Liquid error`, có font và màu;
(3) `shopify theme check --fail-level error` lại đúng baseline 161 file, 0 error, 9 warning;
(4) mỗi setting bị bỏ khỏi các file JSON chuẩn hoá bằng đúng `default` trong schema.

| # | Việc | Trạng thái | Bằng chứng |
|---|---|---|---|
| 1 | Khôi phục `settings_schema.json` | đã kiểm | `cmp` với bản v16.0.0: giống hệt, 1470 dòng; sau khi `theme dev` upload lại, sync không ghi đè lần nữa |
| 2 | Trang chủ hết lỗi | đã kiểm | `127.0.0.1:9292/`: 0 `Liquid error`, 0 `Translation missing`; `--font-body-family: Assistant, sans-serif`; 5 color scheme có màu (18,18,18 · 243,243,243 · 255,255,255 · 36,40,51 · 51,79,180) |
| 3 | Theme Check về baseline | đã kiểm | exit 0, 0 error, 9 warning. Số file là 158 chứ không phải 161: Theme Check đếm cả JSON ở gốc repo (`flow.config.json`, `docs/architecture/*.json`) — bản sao chỉ có thư mục theme ra đúng 155 = số file `.liquid` + `.json` của theme. Số file vì vậy không phải baseline; 0 error / 9 warning mới là |
| 4 | JSON chuẩn hoá không mất giá trị | đã kiểm | `settings_data.json` và 4 template giống bản gốc về nội dung. `header-group.json` mất `text_alignment` và `color_scheme` của block `announcement-bar-0`: cả hai không còn trong schema của block `announcement` ở v16 (chỉ có `text`, `link`) và `announcement-bar.liquid` không đọc chúng (0 chỗ). `footer-group.json` mất `"block_order": []` rỗng |

**Bài học.** Lần đầu chạy `theme dev` lên một development theme mới thì **không** bật
`--theme-editor-sync`; bật từ lần chạy thứ hai, khi theme trên store đã đủ file. Sync coi file
trên store là nguồn, và lúc theme vừa tạo thì file trên store còn rỗng.
