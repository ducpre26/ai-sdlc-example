---
name: ai-first-sdlc
description: >-
  Tạo, cập nhật, review, validate, handoff và tiếp tục các artifact SDLC
  theo quy trình AI-first có con người phê duyệt. Dùng cho công việc từ
  khởi tạo, yêu cầu, thiết kế, phát triển, kiểm thử, phát hành đến vận hành;
  bao gồm theo dõi tiến độ, evidence, traceability và approval gate.
  Không dùng cho code review, sửa lỗi hoặc CI thuần túy không liên quan
  đến artifact SDLC.
---

# AI-First SDLC

Tạo và kiểm soát tài liệu SDLC dựa trên nguồn có thể kiểm chứng, đồng thời giữ quyền phê duyệt cuối cùng cho con người.

## Kiểm tra và khôi phục tiến độ

1. Đọc [progress-tracking.md](references/progress-tracking.md) trước khi định tuyến công việc mới.
2. Tìm `docs/ai-sdlc/_progress.md` và `_progress.md` trong bảy thư mục stage.
3. Nếu chưa có progress, kiểm tra artifact SDLC hiện có trước khi định tuyến; không tự suy đoán tiến độ từ artifact.
   - Nếu không có artifact SDLC có ý nghĩa hoặc người dùng xác nhận đây là dự án mới, đọc [first-use-intake.md](references/first-use-intake.md) và thực hiện intake trước khi chọn giai đoạn.
   - Nếu đã có artifact SDLC, báo `progress_missing`, định tuyến từ yêu cầu và artifact hiện có, đồng thời không nạp quy trình intake lần đầu.
4. Nếu có stage đang `in_progress`, `awaiting_user`, `awaiting_human` hoặc `blocked`, báo công việc, bước hiện tại, lần cập nhật cuối và bước tiếp theo. Chờ người dùng chọn tiếp tục, xem chi tiết, đóng công việc hoặc chuyển stage; không tự resume.
5. Mỗi stage chỉ có một công việc đang hoạt động. Không mở công việc thứ hai trong cùng stage trước khi công việc hiện tại hoàn tất hoặc được đóng.
6. Sau mỗi bước có ý nghĩa, cập nhật checkbox, trạng thái bước, thời gian, ghi chú và lịch sử trong progress stage; sau đó đồng bộ progress toàn skill.

Khi thư mục `docs/ai-sdlc/` đã tồn tại, có thể kiểm tra cấu trúc và tổng hợp trạng thái bằng:

```bash
python "<AI_FIRST_SDLC_SKILL_DIR>/scripts/inspect_progress.py" docs/ai-sdlc
```

Giữ thư mục làm việc tại root dự án và thay `<AI_FIRST_SDLC_SKILL_DIR>` bằng đường dẫn tuyệt đối của skill. Lệnh chỉ đọc Markdown và báo lỗi; agent vẫn chịu trách nhiệm cập nhật `_progress.md` theo quyết định của người dùng.

## Định tuyến yêu cầu

1. Xác định một thao tác:
   - `create`: tạo artifact mới từ template và các nguồn có thật.
   - `update`: tạo phiên bản mới từ artifact hiện có, giữ ID và lịch sử quyết định.
   - `review`: đánh giá artifact và báo phát hiện; không sửa file.
   - `validate`: chạy kiểm tra tất định, sau đó kiểm tra nội dung, nguồn và evidence.
   - `handoff`: tổng hợp kết quả, câu hỏi mở, cổng con người và hành động tiếp theo.
   - `resume`: khôi phục checkpoint của công việc dang dở và chỉ tiếp tục sau khi người dùng xác nhận.
2. Kiểm tra progress, artifact SDLC và bản cơ sở hiện có trong dự án.
3. Đọc [workflow-and-routing.md](references/workflow-and-routing.md) trước để lấy stage map, lifecycle, template và quy ước ID.
   Đọc [agent-orchestration.md](references/agent-orchestration.md) và `references/agent-workflow.yaml` trước mọi `verify_inputs`, `execute`, `validate` hoặc delegation; dùng đúng Claude Code subagent và `required_skills`. Ghi rõ companion skill phải áp dụng trong task giao agent; không coi implicit matching, prompt hoặc file Markdown là một agent execution.
4. Chỉ khi dự án chưa có progress lẫn artifact SDLC có ý nghĩa hoặc người dùng xác nhận đây là dự án mới, đọc [first-use-intake.md](references/first-use-intake.md) trước khi xác định giai đoạn. Không dùng intake lần đầu cho `update`, `review`, `validate`, `handoff`, `resume` hoặc để thay thế việc kiểm tra artifact hiện có.
5. Xác định giai đoạn và loại artifact từ yêu cầu, kết quả intake khi có và các file hiện có trong dự án.
6. Chỉ đọc reference của giai đoạn đang xử lý:
   - Khởi tạo/lập kế hoạch: [initiation.md](references/initiation.md)
   - Yêu cầu: [requirements.md](references/requirements.md)
   - Kiến trúc/thiết kế: [design.md](references/design.md)
   - Phát triển: [development.md](references/development.md)
   - Kiểm thử/UAT: [testing.md](references/testing.md)
   - Phát hành/triển khai: [release.md](references/release.md)
   - Vận hành/bảo trì: [operations.md](references/operations.md)
7. Với `verify_inputs`, `execute` hoặc `validate`, nạp đúng companion skill được workflow yêu cầu bằng Skill tool hoặc dùng subagent đã preload skill đó; truyền stage contract, template, schema cùng baseline qua task packet. Nếu skill bắt buộc không được discovery/preload hoặc agent không trả `skills_used`, đặt step thành `blocked`; không tự tái tạo nghiệp vụ từ trí nhớ.
8. Với yêu cầu đi qua nhiều giai đoạn, lập thứ tự xử lý và hoàn tất checkpoint của từng giai đoạn trước khi nạp reference kế tiếp. Không tải đồng thời toàn bộ reference hoặc template.

Checkpoint tối thiểu phải giữ qua các giai đoạn:

```text
Giai đoạn/thao tác: <stage và operation>
Artifact hiện tại: <document_id@version, status, đường dẫn>
Bản cơ sở: <document_id@version hoặc không có>
Nguồn đã duyệt: <ID@version>
Evidence: <đường dẫn hoặc kết quả kiểm tra có thật>
Câu hỏi mở: <nội dung và người chịu trách nhiệm>
Cổng con người: <vai trò và quyết định cần có>
Bước tiếp theo: <stage, artifact hoặc hành động>
```

Ghi checkpoint này vào `_progress.md` của stage theo contract progress; không chỉ giữ trong hội thoại.

## Kiểm tra trước khi thực hiện

- Tìm quy ước lưu tài liệu, artifact nguồn đã `approved`, ID, version, work item và evidence trong dự án.
- Kiểm tra dự án nằm trong Git repository. Nếu chưa có Git, hỏi người dùng trước khi chạy `git init`; không tự commit hoặc push.
- Tuân theo cấu trúc hiện có; nếu chưa có, dùng `docs/ai-sdlc/<stage>/`.
- Coi artifact `approved` là bản cơ sở. Không sửa nội dung đã duyệt một cách âm thầm.
- Nếu thiếu nguồn bắt buộc hoặc các nguồn mâu thuẫn, giữ đầu ra ở `draft`, ghi câu hỏi vào `open_questions` và xác định người chịu trách nhiệm trả lời.
- Không biến giả định, suy luận của AI hoặc thông tin chưa kiểm chứng thành requirement hay quyết định đã duyệt.

## Tạo hoặc cập nhật artifact

- Chọn template từ danh mục trong `workflow-and-routing.md`; dùng `assets/templates/03-design/openapi-template.yaml` cho API contract.
- Giữ heading bắt buộc. Dùng `assets/schemas/artifact-metadata.schema.json` cho cấu trúc metadata và validator cho lifecycle cùng quy tắc xuyên tài liệu.
- Chỉ thay placeholder bằng sự thật được hỗ trợ bởi nguồn hoặc quyết định người dùng đã cung cấp.
- Gán ID ổn định và duy trì chuỗi `BO → FR/NFR/BR → CMP/API/ADR → WI/PR → TC → REL`.
- Tham chiếu chính xác bản cơ sở bằng `DOCUMENT-ID@x.y.z` trong `source_documents` và `related_documents` khi biết version.
- Mỗi `document_id` chỉ có một file hiện hành với tên ổn định; không tạo file `*-vX.Y.Z.*`. Git history giữ baseline cũ.
- Khi cập nhật artifact đã duyệt: trước hết xác minh baseline hiện tại đã được commit; giữ `document_id`, tăng semantic version đúng một lần cho candidate, đặt `supersedes_version` bằng version cũ và bắt đầu lifecycle mới với `status: draft`, `previous_status: null`. Các vòng sửa cùng candidate không tăng version.
- Baseline mới chỉ dùng cho downstream sau human approval và commit. Không tự sửa blob lịch sử sang `superseded`, commit, push hoặc tạo tag.
- Chỉ thêm evidence, lệnh, báo cáo hoặc URL công việc khi chúng thực sự tồn tại.

## Review artifact

Báo phát hiện trước phần tổng kết và sắp xếp theo mức độ nghiêm trọng:

- `blocking`: phê duyệt/phát hành không an toàn, thiếu đầu vào bắt buộc, mâu thuẫn, tuyên bố pass không thể kiểm chứng, sai ranh giới quyền hạn/dữ liệu, status không hợp lệ hoặc thiếu traceability quan trọng.
- `major`: requirement không thể kiểm thử, NFR không đo được, thiếu thiết kế, thiếu hành vi lỗi/rollback, thiếu coverage đáng kể hoặc bản cơ sở đã lỗi thời.
- `minor`: vấn đề về độ rõ ràng, tính nhất quán, cách đặt tên hoặc khả năng bảo trì nhưng không chặn cổng.

Với mỗi phát hiện, trích artifact và section hoặc line chính xác khi có thể; giải thích tác động và cách sửa bắt buộc. Không sửa file khi người dùng chỉ yêu cầu review.

## Bắt buộc con người phê duyệt

- AI chỉ được đưa công việc do AI tạo tới `ai_checked`.
- Không tự điền `human_decision` hoặc `human_approved_at`, giả danh người duyệt hay tuyên bố artifact đã `approved`.
- Chỉ ghi nhận quyết định khi người dùng cung cấp rõ quyết định và danh tính người duyệt; nếu không, bàn giao để review.
- Giữ câu hỏi chặn chưa giải quyết trong `open_questions`; artifact `approved` không được còn câu hỏi mở.

## Validate

Chạy validator cho một artifact hoặc thư mục artifact Markdown:

```powershell
python <skill-root>\scripts\validate_artifacts.py <artifact-path-or-docs-root>
python "<skill-root>/scripts/validate_agents.py" "<skill-root>" [<project-config>] [<project-root>]
```

Trước lần delegation đầu tiên, xác minh năm custom agent Markdown đã nằm trong `<project-root>/.claude/agents/` hoặc `~/.claude/agents/` và được Claude Code discovery. Skill không tự cài hoặc giả lập subagent. Giữ vai trò Orchestrator ở main conversation; chỉ dùng `sdlc-orchestrator-agent` làm main session qua `claude --agent sdlc-orchestrator-agent`, vì subagent thường không phải nơi điều phối chuỗi delegation. Với OpenAPI, dùng công cụ kiểm tra của dự án khi có. Validator thành công chỉ là điều kiện cần; tiếp tục kiểm tra nguồn, evidence, tính đúng kỹ thuật, bảo mật và chấp nhận nghiệp vụ.

## Contract đầu ra

Kết thúc mọi thao tác bằng cấu trúc sau; với `review`, đặt kết quả review trong `Kiểm tra/Phát hiện`:

```text
Thao tác/giai đoạn: <operation và stage>
Artifact: <đường dẫn, document_id@version, status>
Nguồn: <ID@version của đầu vào đã duyệt>
Kiểm tra/Phát hiện: <validator, evidence hoặc findings>
Câu hỏi mở: <câu hỏi chặn hoặc không có>
Cổng con người: <vai trò và quyết định cần có>
Bước tiếp theo: <artifact/hành động cụ thể và người chịu trách nhiệm>
Tiến độ: <stage status, current step, completed steps/6, last updated>
```

Không coi artifact tiếp theo là `approved` khi cổng đầu vào bắt buộc chưa hoàn tất.
