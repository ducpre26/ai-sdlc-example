# Khởi tạo và lập kế hoạch

## 1. Mục đích và phạm vi

Thiết lập lý do kinh doanh, mục tiêu, phạm vi, thẩm quyền, rủi ro và cách quản trị trước khi chuyển sang Requirements. Stage này không phê duyệt thay Sponsor và không giả định dự án đã được cấp quyền.

## 2. Điều kiện kích hoạt

- Dự án mới chưa có artifact SDLC có ý nghĩa.
- Người dùng yêu cầu tạo/cập nhật Project Charter hoặc Project Management Plan (PMP).
- Một thay đổi lớn cần đánh giá lại phạm vi, tài trợ hoặc quyền thực hiện.

## 3. Artifact đầu vào

- Problem statement, stakeholder input và quyết định đã có nguồn.
- Strategy, policy, research, constraint hoặc artifact hiện hữu khi có.
- Với PMP: Project Charter đã `approved` và baseline đã commit.

## 4. Artifact đầu ra

| Artifact | Template |
|---|---|
| Project Charter | `assets/templates/01-initiation/project-charter.md` |
| Project Management Plan | `assets/templates/01-initiation/project-management-plan.md` |

Chỉ giữ một file hiện hành cho mỗi `document_id`; version nằm trong metadata và Git history.

## 5. Nguồn và evidence bắt buộc

- Mỗi mục tiêu, constraint, ngân sách, thời hạn và quyết định có nguồn hoặc nằm trong `open_questions`.
- Evidence chỉ gồm tài liệu, quyết định người dùng, dữ liệu, đường dẫn hoặc kết quả thực sự tồn tại.
- Không coi giả định hoặc suy luận AI là quyết định dự án.

## 6. Ánh xạ step, agent và skill

| Step | Agent | Companion skill |
|---|---|---|
| `inspect`, `handoff` | `sdlc-orchestrator-agent` | Không |
| `verify_inputs`, `execute`, `validate` | `sdlc-orchestrator-agent` | `sdlc-project-initiation` |
| `human_gate` | `human` | Không |

## 7. Traceability contract

- Duy trì `BO-###` từ Project Charter sang SRS/RTM.
- Duy trì `RISK-###` sang stage có biện pháp kiểm soát.
- PMP liệt kê đúng Project Charter trong `source_documents`.

## 8. Điều kiện chặn

- Không xác định được Sponsor hoặc thẩm quyền phê duyệt.
- Nguồn bắt buộc mâu thuẫn mà chưa có owner giải quyết.
- PMP không có Project Charter approved/committed.
- Artifact đề nghị `approved` nhưng còn câu hỏi mở.

## 9. Human gate

Sponsor hoặc cấp quản trị có thẩm quyền quyết định Go, Conditional Go hoặc No-Go. AI chỉ chuẩn bị artifact tới `ai_checked` và ghi nhận quyết định được cung cấp rõ.

## 10. Handoff contract

Bàn giao Project Charter/PMP baseline, `BO`, risk, constraint, decision, open question, approval identity và Git commit sang Requirements.

## 11. Ngoại lệ

Dự án nhỏ có thể không cần PMP riêng nếu Project Charter và progress lưu đủ kế hoạch tối thiểu; phải ghi lý do tailoring. Không bỏ Project Charter hoặc human gate.
