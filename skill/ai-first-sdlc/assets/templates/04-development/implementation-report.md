---
document_id: IMPLREPORT-TEMPLATE-001
document_type: implementation-report
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: developer
approver: reviewer
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

# Báo cáo implementation (Implementation Report)

## 1. Tham chiếu requirement và design

| Requirement | Design/ADR | Kết quả |
|---|---|---|
| FR-001 | CMP-001 / ADR-0001 | {implemented behavior} |

## 2. Tham chiếu commit và Pull Request

- Work item: {WI-ID/link}.
- Commit/PR: {hash/link}.

## 3. File và component đã thay đổi

| Component/Khu vực file | Tóm tắt thay đổi | Lý do |
|---|---|---|
| {area} | {change} | {requirement/design} |

## 4. Thay đổi API và data

{Contract, schema, migration và compatibility evidence.}

## 5. Kết quả build và static analysis

| Kiểm tra | Command/Pipeline | Kết quả | Evidence |
|---|---|---|---|
| Build | {command} | Pass/Fail | {link/path} |

## 6. Kết quả unit test

| Suite | Đạt (Passed) | Không đạt (Failed) | Coverage/Ghi chú | Evidence |
|---|---:|---:|---|---|
| {suite} | {n} | {n} | {value} | {link/path} |

## 7. Sai khác so với design (Deviations)

{Không có, hoặc mô tả deviation, rationale và tài liệu đã cập nhật.}

## 8. Hạn chế đã biết (Known Limitations)

- {Giới hạn, tác động, work item}.

## 9. Quyết định của reviewer

| Reviewer | Quyết định | Ngày | Ghi chú |
|---|---|---|---|
| {tên} | Chờ duyệt (Pending) | | |

## AI tự kiểm tra (Self-check)

- [ ] Chỉ báo cáo check đã thực sự chạy và có evidence.
- [ ] Mọi deviation đều được nêu, không che giấu khác biệt với design.
- [ ] Không tuyên bố pass nếu command/pipeline thất bại hoặc chưa chạy.
