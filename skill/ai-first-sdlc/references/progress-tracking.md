# Theo dõi và tiếp tục tiến độ

## Mục lục

1. [Mục đích và phạm vi](#1-mục-đích-và-phạm-vi)
2. [Vị trí file](#2-vị-trí-file)
3. [Luồng khi bắt đầu](#3-luồng-khi-bắt-đầu)
4. [Sáu bước chung](#4-sáu-bước-chung)
5. [Trạng thái bước](#5-trạng-thái-bước)
6. [Trạng thái stage](#6-trạng-thái-stage)
7. [Quy tắc cập nhật](#7-quy-tắc-cập-nhật)
8. [Tiếp tục công việc dang dở](#8-tiếp-tục-công-việc-dang-dở)
9. [Tiến độ toàn skill](#9-tiến-độ-toàn-skill)
10. [File thiếu hoặc không hợp lệ](#10-file-thiếu-hoặc-không-hợp-lệ)
11. [Giới hạn](#11-giới-hạn)

## 1. Mục đích và phạm vi

- Dùng `_progress.md` để ghi trạng thái thực thi của từng stage và toàn bộ SDLC.
- Cho phép agent báo chính xác công việc dang dở sau khi hội thoại hoặc tác vụ bị gián đoạn.
- Chỉ ghi điều có thể dùng để tiếp tục: bước, trạng thái, artifact, agent, execution ID, handoff packet, câu hỏi, blocker, ghi chú, thời gian và hành động tiếp theo.
- Không lưu chain-of-thought, secret, token, dữ liệu nhạy cảm hoặc suy luận chưa được ghi nhận trong artifact.
- Chỉ dùng Markdown; không dùng YAML frontmatter, JSON, fingerprint hoặc phần trăm.

## 2. Vị trí file

```text
docs/ai-sdlc/
├── _progress.md
├── 01-initiation/_progress.md
├── 02-requirements/_progress.md
├── 03-design/_progress.md
├── 04-development/_progress.md
├── 05-testing/_progress.md
├── 06-release/_progress.md
└── 07-operations/_progress.md
```

- Tạo progress stage từ `assets/templates/progress/stage/_progress.md`.
- Tạo progress toàn skill từ `assets/templates/progress/project/_progress.md`.
- Một stage chỉ có một công việc đang hoạt động trong `_progress.md`.
- Giữ công việc cũ trong bảng Lịch sử trước khi mở công việc mới.

## 3. Luồng khi bắt đầu

1. Tìm progress toàn skill và progress của bảy stage.
2. Nếu không có file nào, thông báo chưa có dữ liệu tiến độ và đề xuất khởi tạo.
3. Nếu file stage thiếu, ghi rõ `progress_missing`; không suy đoán checklist từ artifact.
4. Đọc bảng thuộc tính, sáu checkbox, câu hỏi, blocker và bước tiếp theo.
5. Khi có trường agent, đọc `Agent hiện tại`, `Execution ID` và `Handoff packet`; đây là checkpoint điều phối, không phải chain-of-thought.
6. Xác định stage đang hoạt động từ các trạng thái `in_progress`, `awaiting_user`, `awaiting_human` hoặc `blocked`.
7. Thông báo công việc, bước hiện tại, số bước hoàn thành, lần cập nhật cuối và hành động tiếp theo.
8. Chờ người dùng chọn tiếp tục, xem chi tiết, đóng công việc hoặc chuyển sang stage khác.
9. Không tự resume, kể cả khi chỉ có một công việc dang dở.

## 4. Sáu bước chung

| Bước | Mục đích |
|---|---|
| `inspect` | Đọc yêu cầu, artifact và progress hiện tại |
| `verify_inputs` | Kiểm tra đầu vào, bản cơ sở và cổng bắt buộc |
| `execute` | Tạo, cập nhật, review hoặc thực hiện thao tác chính |
| `validate` | Chạy validator và kiểm tra nội dung/evidence |
| `human_gate` | Chờ hoặc ghi nhận quyết định đúng thẩm quyền |
| `handoff` | Ghi kết quả và bàn giao sang bước/stage tiếp theo |

- Thực hiện theo thứ tự trừ khi reference của stage cho phép `skipped` và ghi rõ lý do.
- Checklist chi tiết của stage nằm trong mục Quy trình theo thao tác của reference tương ứng.
- `resume` không phải bước thứ bảy; đó là cách quay lại bước chưa hoàn tất.

## 5. Trạng thái bước

Trạng thái hợp lệ:

```text
pending
in_progress
awaiting_user
awaiting_human
blocked
completed
skipped
```

Quy tắc checkbox:

- Dùng `[x]` cho `completed` hoặc `skipped`.
- Dùng `[ ]` cho `pending`, `in_progress`, `awaiting_user`, `awaiting_human` hoặc `blocked`.
- Mỗi bước xuất hiện đúng một lần và dùng đúng ID chuẩn.
- Không đánh dấu `[x]` khi chỉ mới bắt đầu hoặc đang chờ phản hồi.
- Mỗi lần đổi trạng thái phải cập nhật bảng thuộc tính, mô tả dòng checklist và bảng Lịch sử.

## 6. Trạng thái stage

Trạng thái hợp lệ:

```text
not_started
ready
in_progress
awaiting_user
awaiting_human
blocked
completed
skipped
```

Suy ra theo thứ tự ưu tiên:

1. Có bước `blocked` → `blocked`.
2. Có bước `awaiting_user` → `awaiting_user`.
3. Có bước `awaiting_human` → `awaiting_human`.
4. Có bước `in_progress` → `in_progress`.
5. Sáu bước đều `completed` hoặc `skipped` → `completed`.
6. Cả stage không áp dụng, ghi lý do trong mục Ghi chú và sáu bước `skipped` → `skipped`.
7. Sáu bước đều `pending` → giữ `not_started` hoặc `ready` theo quyết định đã ghi trong progress.

Giá trị `Trạng thái` trong bảng thuộc tính phải khớp trạng thái suy ra.

## 7. Quy tắc cập nhật

- Cập nhật progress ngay sau mỗi bước có ý nghĩa.
- Cập nhật trước khi hỏi người dùng, chờ human gate, bàn giao hoặc kết thúc lượt agent.
- Dùng thời gian `YYYY-MM-DD HH:mm ±HH:mm`.
- Ghi `Bước hiện tại` là bước chưa hoàn tất đang có trạng thái hoạt động; dùng `—` khi không có.
- Ghi `Bước tiếp theo` thành một hành động cụ thể; không dùng câu mơ hồ như “tiếp tục xử lý”.
- Ghi artifact bằng `document_id@version` khi có.
- Ghi native agent name, execution identity và đường dẫn packet gần nhất khi step được delegate. Không ghi prompt nội bộ.
- Thêm một dòng Lịch sử cho mỗi lần chuyển trạng thái.
- Khi đóng công việc chưa hoàn tất, ghi lý do vào Ghi chú và Lịch sử trước khi đặt lại checklist cho công việc mới.
- Sau khi cập nhật stage, cập nhật bảng tổng hợp trong progress toàn skill.

## 8. Tiếp tục công việc dang dở

Khi người dùng chọn resume:

1. Đọc lại toàn bộ `_progress.md` của stage.
2. Xác nhận công việc và artifact người dùng muốn tiếp tục.
3. Đọc agent, execution ID, packet và các quyết định đã nhận; không hỏi lại câu hỏi đã có nguồn trả lời.
4. Bắt đầu từ bước `[ ]` đang `in_progress`, `awaiting_user`, `awaiting_human` hoặc `blocked`.
5. Nếu bước đang chờ đã được người dùng giải quyết, ghi Lịch sử rồi chuyển bước sang `in_progress` hoặc `completed` phù hợp.
6. Không lặp bước `[x]` và không suy đoán nội dung ngoài progress.
7. Nếu execution cũ không còn, Orchestrator spawn custom agent đã được Codex discovery với cùng native name và packet; vẫn giữ separation of duties. Nếu agent chưa được discovery, block thay vì giả lập agent trong execution hiện tại.
8. Nếu progress không đủ để tiếp tục an toàn, chuyển bước hiện tại sang `blocked`, ghi câu hỏi và yêu cầu người dùng làm rõ.

Thông báo resume tối thiểu:

```text
<Stage> đang làm dở tại bước <step>.
Cập nhật lần cuối: <timestamp>.
Bước tiếp theo: <next action>.
```

## 9. Tiến độ toàn skill

Trạng thái tổng thể hợp lệ:

```text
not_started
in_progress
attention_required
awaiting_human
completed
```

Suy ra từ bảy progress stage:

1. Có stage `blocked` hoặc `awaiting_user` → `attention_required`.
2. Không có mục cần chú ý nhưng có stage `awaiting_human` → `awaiting_human`.
3. Có stage `in_progress`, `ready` hoặc đã hoàn thành một phần → `in_progress`.
4. Bảy stage đều `completed` hoặc `skipped` → `completed`.
5. Tất cả stage `not_started` hoặc progress chưa được khởi tạo → `not_started`.

- Hiển thị số bước hoàn thành dạng `2/6`; không tính phần trăm.
- Liệt kê tất cả stage đang hoạt động nếu nhiều stage có công việc.
- Chọn stage chưa hoàn tất có thứ tự thấp nhất làm gợi ý tiếp theo, trừ khi progress ghi hành động khác do blocker hoặc human gate.
- Progress toàn skill là bản tổng hợp; progress stage giữ chi tiết công việc.

## 10. File thiếu hoặc không hợp lệ

- File không tồn tại: báo `progress_missing`.
- Thiếu bảng thuộc tính, mục Các bước hoặc một trong sáu bước: báo file không hợp lệ.
- Checkbox không khớp trạng thái: báo lỗi; không tự sửa mà không thông báo.
- Có hai dòng cho cùng bước: báo lỗi và dừng resume.
- Trạng thái stage không khớp checklist: báo giá trị khai báo và giá trị suy ra.
- Không suy đoán tiến độ từ artifact để lấp file thiếu trong phiên bản này.

## 11. Giới hạn

- `_progress.md` là nguồn duy nhất để xác định tiến độ trong phiên bản đầu tiên.
- Skill không phát hiện artifact bị sửa khi progress chưa được cập nhật.
- Agent chịu trách nhiệm cập nhật progress ngay sau mỗi bước có ý nghĩa.
- Cơ chế này theo dõi tiến độ tài liệu SDLC, không thay thế issue tracker hoặc quản lý tiến độ phát triển sản phẩm.
