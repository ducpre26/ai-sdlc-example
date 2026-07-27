---
document_id: RELEASEPLAN-TEMPLATE-001
document_type: release-plan
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: release-owner
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

# Kế hoạch phát hành (Release Plan)

## 1. Phạm vi và version release

- Release ID: REL-001.
- Version: {version}.
- Phạm vi (Scope): {tóm tắt}.

## 2. Requirement và fix được đưa vào release

| Requirement/Fix | Work item | Kết quả test | Ghi chú |
|---|---|---|---|
| FR-001 | WI-001 | TC-001 Pass | {notes} |

## 3. Dependency

| Phụ thuộc (Dependency) | Version/trạng thái bắt buộc | Owner | Đã xác minh |
|---|---|---|---|
| {dependency} | {value} | {role} | [ ] |

## 4. Lịch release

| Hoạt động | Khoảng thời gian | Owner | Truyền thông |
|---|---|---|---|
| {activity} | {window} | {role} | {channel} |

## 5. Readiness checklist

- [ ] Approved Test Report và UAT.
- [ ] Deployment Runbook đã diễn tập hoặc review.
- [ ] Backup và rollback được xác nhận.
- [ ] Monitoring/alerting sẵn sàng.
- [ ] Stakeholder được thông báo.

## 6. Data migration

{Migration, thời gian ước lượng, compatibility window và validation.}

## 7. Truyền thông (Communication)

{Đối tượng, thông điệp, thời điểm, kênh và owner.}

## 8. Tiêu chí Go/No-Go

| Tiêu chí | Kết quả bắt buộc | Evidence | Thực tế |
|---|---|---|---|
| Critical tests | 100% Pass | {report} | {result} |

## 9. Phê duyệt (Approval)

| Vai trò | Người duyệt | Quyết định | Ngày |
|---|---|---|---|
| Release Authority | {tên} | Chờ duyệt (Pending) | |

## AI tự kiểm tra (Self-check)

- [ ] Chỉ bao gồm requirement/fix đã có test evidence.
- [ ] Dependency, migration, monitoring và rollback đều có owner.
- [ ] AI không tự ra quyết định Go.
