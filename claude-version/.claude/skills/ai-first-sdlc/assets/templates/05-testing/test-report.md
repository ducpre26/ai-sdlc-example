---
document_id: TESTREPORT-TEMPLATE-001
document_type: test-report
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: qa-owner
approver: product-owner
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

# Báo cáo kiểm thử (Test Report)

## 1. Tổng hợp kết quả thực thi

| Đã lập kế hoạch | Đã thực thi | Đạt (Passed) | Không đạt (Failed) | Bị chặn (Blocked) |
|---:|---:|---:|---:|---:|
| {n} | {n} | {n} | {n} | {n} |

## 2. Coverage của requirement

| Requirement | Test | Kết quả | Evidence |
|---|---|---|---|
| FR-001 | TC-001 | Pass/Fail | {link/path} |

## 3. Defect

| Defect | Mức độ (Severity) | Trạng thái | Requirement | Workaround/Quyết định |
|---|---|---|---|---|
| {ID} | {severity} | {status} | {ID} | {decision} |

## 4. Kết quả kiểm thử non-functional

| NFR | Metric | Target | Thực tế (Actual) | Kết quả | Evidence |
|---|---|---:|---:|---|---|
| NFR-001 | {metric} | {target} | {actual} | Pass/Fail | {link/path} |

## 5. Rủi ro còn lại (Residual Risks)

| Rủi ro | Tác động | Khả năng | Giảm thiểu/Chấp nhận | Owner |
|---|---|---|---|---|
| {risk} | {impact} | {value} | {decision} | {role} |

## 6. Khuyến nghị release

Go / Conditional Go / No-Go — {lý do}.

## AI tự kiểm tra (Self-check)

- [ ] Số liệu tổng hợp khớp evidence nguồn.
- [ ] Requirement chưa test và failed test được nêu rõ.
- [ ] Không biến “Not Run” thành “Pass”.
- [ ] Recommendation phản ánh defect và residual risk.
