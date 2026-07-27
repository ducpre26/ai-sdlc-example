---
document_id: IMPLPLAN-TEMPLATE-001
document_type: implementation-plan
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: developer
approver: tech-lead
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

# Kế hoạch implementation (Implementation Plan)

## 1. Phạm vi và tham chiếu requirement

{Phạm vi thay đổi, FR/NFR/BR và nội dung ngoài phạm vi.}

## 2. Component bị ảnh hưởng

| Component | Thay đổi | Owner | Tham chiếu design |
|---|---|---|---|
| CMP-001 | {change} | {role} | {HLD/LLD/ADR} |

## 3. Thay đổi dự kiến (Planned Changes)

{Thay đổi hành vi, module, configuration và dependency.}

## 4. Thay đổi data và API

| Contract/Entity | Thay đổi | Compatibility | Hành động của consumer |
|---|---|---|---|
| API-001 | {change} | Backward compatible/Breaking | {action} |

## 5. Migration và compatibility

{Migration, rollout order, feature flag, backward/forward compatibility.}

## 6. Trình tự implementation

1. {Bước implementation nguyên tử và kết quả mong đợi}.

## 7. Test Strategy

{Unit, integration, contract, regression và NFR checks mapped to requirements.}

## 8. Các yếu tố security

{Trust boundary, permission, dữ liệu nhạy cảm, dependency và abuse case.}

## 9. Rủi ro và rollback

| Rủi ro | Phát hiện | Giảm thiểu | Rollback |
|---|---|---|---|
| {risk} | {signal} | {mitigation} | {action} |

## 10. Definition of Done

- [ ] Requirement và acceptance criteria đạt.
- [ ] Code review, build, unit/integration test đạt.
- [ ] Security/static checks đạt hoặc exception được duyệt.
- [ ] SRS/HLD/LLD/API/ADR được cập nhật khi cần.
- [ ] Implementation Report có đầy đủ evidence.

## AI tự kiểm tra (Self-check)

- [ ] Mỗi thay đổi liên kết requirement và design.
- [ ] Migration và rollback khả thi, đúng thứ tự.
- [ ] Kế hoạch không để implementer tự quyết định phần quan trọng.
