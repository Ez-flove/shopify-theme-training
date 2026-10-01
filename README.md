# Shopify theme training

Chỗ thực hành bài tập Shopify theme. Theme nền là **Dawn v16.0.0**, quy trình làm bài chạy trên
**claude-flow-kit**: đề bài → spec → plan → code → guard → verify, với hai chỗ dừng để bạn đồng ý
trước khi có dòng code nào.

## Bắt đầu

Ba việc, mỗi việc làm một lần.

**1. Đăng ký plugin của kit** — cho Claude Code biết các lệnh `/flow-*`. Gõ trong Claude Code:

```
/plugin marketplace add /home/bss/Desktop/claude-flow-kit
/plugin install flow@claude-flow-kit
```

**2. Nối với development store** — cần một dev store từ Shopify Partners:

```bash
shopify theme dev --store <tên-store>.myshopify.com
```

Lần đầu CLI mở trình duyệt để đăng nhập. Preview chạy ở `http://127.0.0.1:9292`, và lệnh in ra
link mở theme editor.

**3. Commit bản Dawn gốc** — để mọi bài tập sau đó so được với Dawn bằng `git diff`:

```bash
git add -A && git commit -m "Foundation(setup): Dawn v16.0.0 with claude-flow-kit"
```

## Làm một bài tập

Tạo `docs/exercises/EX-01-<tên-ngắn>/brief.md`, dán nguyên văn đề, rồi gõ `/flow-feature EX-01`.
Chi tiết từng bước ở [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Có gì ở đâu

| | |
|---|---|
| `layout/` `sections/` `snippets/` `templates/` `config/` `locales/` `assets/` | theme Dawn |
| `docs/exercises/` | đề bài và design của từng bài tập — đang trống, bạn tự thêm |
| `docs/specs/features/` · `docs/plans/` | spec và plan Claude viết cho từng bài |
| `tests/guards/` | guard: test đọc source, bắt chuyện một thay đổi bỏ sót một đầu |
| `.claude/rules/shopify-theme.md` | một setting, block, chuỗi mới phải tới những đâu; lỗi hay gặp của theme |
| `flow.config.json` | mọi lệnh và nguồn tin của project |
| `docs/dawn-README.md` | README gốc của Dawn, có nguyên tắc viết theme của Shopify |

Mã nguồn của kit (plugin `flow` và template) nằm ngoài repo, ở `~/Desktop/claude-flow-kit`.
