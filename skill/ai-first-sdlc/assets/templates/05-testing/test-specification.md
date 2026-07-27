---
document_id: TESTSPEC-TEMPLATE-001
document_type: test-specification
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: qa-owner
approver: qa-reviewer
created_at: 2026-07-20
updated_at: 2026-07-20
source_documents: []
related_documents: []
related_work_items: []
evidence: []
open_questions: []
ai_generated: true
ai_checked_at:
human_decision:
human_approved_at:
---

# Đặc tả kiểm thử (Test Specification)

## Template cho test case

### TC-001 — {Tiêu đề test case}

- **Requirement:** FR-001.
- **Mục tiêu (Objective):** {Nội dung cần chứng minh}.
- **Mức/Loại (Level/Type):** {unit/integration/system/UAT/security/performance}.
- **Ưu tiên (Priority):** Critical/High/Medium/Low.
- **Điều kiện trước (Preconditions):** {trạng thái và environment}.
- **Test data:** {dữ liệu hoặc tham chiếu fixture}.

| Bước | Hành động | Kết quả mong đợi |
|---:|---|---|
| 1 | {action} | {observable result} |

- **Kết quả thực tế (Actual result):** {điền khi thực thi}.
- **Trạng thái (Status):** Not Run/Pass/Fail/Blocked.
- **Evidence:** {liên kết log/screenshot/report}.
- **Defect:** {ID khi test fail}.

## Checklist coverage

- [ ] Happy path.
- [ ] Validation boundaries.
- [ ] Authorization and ownership.
- [ ] Dependency failure and timeout.
- [ ] Retry/idempotency where applicable.
- [ ] Data integrity and concurrency where applicable.

## AI tự kiểm tra (Self-check)

- [ ] Expected result quan sát và xác minh được.
- [ ] Không tạo test trùng mà không tăng coverage.
- [ ] Test data không chứa dữ liệu cá nhân thật hoặc secret.
