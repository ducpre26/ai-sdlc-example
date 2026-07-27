---
document_id: UAT-TEMPLATE-001
document_type: uat-report
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: product-owner
approver: business-owner
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

# Biên bản kiểm thử chấp nhận người dùng (User Acceptance Test Report — UAT)

## 1. Phạm vi và người tham gia UAT

{Phạm vi, phiên bản, môi trường, người tham gia và vai trò.}

## 2. Business scenario

| Scenario | Requirement | Kết quả mong đợi | Kết quả thực tế | Kết quả | Evidence |
|---|---|---|---|---|---|
| UAT-001 | FR-001 | {outcome} | {outcome} | Pass/Fail | {link} |

## 3. Exception được chấp nhận

| Exception | Tác động business | Workaround | Work item | Người chấp nhận |
|---|---|---|---|---|
| {exception} | {impact} | {workaround} | {ID} | {name} |

## 4. Quyết định (Decision)

`accept` / `conditional accept` / `reject`.

Lý do (Rationale): {lý do business}.

## 5. Xác nhận (Sign-off)

| Vai trò | Người duyệt | Quyết định | Ngày |
|---|---|---|---|
| Business Owner | {tên} | Chờ duyệt (Pending) | |

## AI tự kiểm tra (Self-check)

- [ ] UAT phản ánh business scenario, không chỉ kiểm tra kỹ thuật.
- [ ] Exception có người chấp nhận và work item theo dõi.
- [ ] AI không tự ký UAT.
