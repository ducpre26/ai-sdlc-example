---
document_id: INCIDENT-TEMPLATE-001
document_type: incident-postmortem
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: incident-commander
approver: service-owner
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

# Báo cáo incident và Blameless Postmortem

## Tổng hợp incident

- Incident ID: {INC-ID}.
- Severity: {SEV}.
- Bắt đầu/kết thúc/thời lượng: {timestamp}.
- Trạng thái: Resolved/Monitoring.

## Tác động (Impact)

{Người dùng, dữ liệu, khu vực, thời lượng và tác động business; dùng dữ kiện đã đo.}

## Phát hiện (Detection)

{Cách phát hiện, độ trễ phát hiện và lý do control hiện có hoạt động/không hoạt động.}

## Timeline

| Thời gian | Event/Quan sát | Hành động | Tác nhân/Nguồn |
|---|---|---|---|
| {time} | {fact} | {action} | {role/system} |

## Nguyên nhân gốc (Root cause)

{Nguyên nhân kỹ thuật và hệ thống có evidence; phân biệt với trigger.}

## Khắc phục và phục hồi

{Khoanh vùng, khắc phục, validation và trình tự recovery.}

## Yếu tố góp phần (Contributing Factors)

- {Yếu tố về process, design, test, monitoring hoặc tổ chức; không quy trách nhiệm cá nhân.}

## Điều làm tốt / Điều chưa tốt

| Điều làm tốt | Điều chưa tốt |
|---|---|
| {item} | {item} |

## Hành động khắc phục (Corrective action)

| Hành động | Loại | Owner | Due date | Work item | Xác minh |
|---|---|---|---|---|---|
| {action} | Prevent/Detect/Mitigate | {role} | {date} | {ID} | {evidence} |

## Bài học và cập nhật requirement/design

{SRS, HLD, LLD, ADR, test và runbook cần cập nhật.}

## AI tự kiểm tra (Self-check)

- [ ] Fact, inference và unknown được phân biệt.
- [ ] Root cause có evidence, không quy lỗi cá nhân.
- [ ] Action có owner, deadline và verification.
