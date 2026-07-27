---
document_id: TESTPLAN-TEMPLATE-001
document_type: test-plan
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

# Kế hoạch kiểm thử (Test Plan)

## 1. Mục tiêu kiểm thử (Test Objectives)

{Mục tiêu chất lượng và quyết định phát hành cần hỗ trợ.}

## 2. Phạm vi và nội dung loại trừ

### Trong phạm vi (In Scope)
- {feature/quality attribute}.

### Nội dung loại trừ (Exclusions)
- {Hạng mục bị loại trừ và lý do}.

## 3. Coverage của requirement

| Requirement | Test level/type | Test specification |
|---|---|---|
| FR-001 | Integration/System | TC-001 |

## 4. Test level và test type

{Unit, integration, contract, system, regression, security, performance và UAT.}

## 5. Test environment

| Environment | Version/configuration | Phụ thuộc | Owner |
|---|---|---|---|
| {env} | {version} | {dependency} | {role} |

## 6. Test data

{Tạo dữ liệu, ẩn danh, reset, retention và dữ liệu production bị cấm dùng.}

## 7. Entry criteria và exit criteria

### Điều kiện bắt đầu (Entry)
- [ ] Build deploy thành công và implementation evidence có sẵn.

### Điều kiện kết thúc (Exit)
- [ ] Tất cả critical scenarios pass.
- [ ] Không còn blocker/critical defect.
- [ ] Residual risk được người có thẩm quyền chấp nhận.

## 8. Mức độ nghiêm trọng của defect

| Severity | Định nghĩa | Ví dụ | Rule phát hành |
|---|---|---|---|
| Blocker | Không thể tiếp tục hoặc mất dữ liệu nghiêm trọng | {example} | Must fix |
| Critical | Chức năng cốt lõi sai, không có workaround | {example} | Must fix |
| Major | Tác động đáng kể, có workaround | {example} | Explicit decision |
| Minor | Tác động thấp | {example} | May defer |

## 9. Vai trò và lịch trình

| Hoạt động | Owner | Khoảng thời gian | Đầu ra |
|---|---|---|---|
| {activity} | {role} | {date/range} | {artifact} |

## 10. Rủi ro

| Rủi ro | Tác động | Giảm thiểu |
|---|---|---|
| {risk} | {impact} | {mitigation} |

## 11. Phê duyệt (Approval)

| Vai trò | Người duyệt | Quyết định | Ngày |
|---|---|---|---|
| Product Owner | {tên} | Chờ duyệt (Pending) | |

## AI tự kiểm tra (Self-check)

- [ ] Mỗi requirement có test level/type phù hợp.
- [ ] NFR có phương pháp và môi trường đo.
- [ ] Exit criteria định lượng được.
