---
document_id: DEPLOY-TEMPLATE-001
document_type: deployment-runbook
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: operations-owner
approver: release-owner
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

# Hướng dẫn triển khai (Deployment Runbook)

## 1. Điều kiện tiên quyết (Preconditions)

- [ ] Release artifact immutable và checksum xác nhận.
- [ ] Quyền truy cập, maintenance window và approval sẵn sàng.

## 2. Environment và configuration

| Environment | Artifact/version | Nguồn configuration | Nguồn secret |
|---|---|---|---|
| Production | {version} | {source} | {vault/reference} |

Không ghi secret trực tiếp trong tài liệu.

## 3. Backup

| Resource | Hành động backup | Xác minh | Retention |
|---|---|---|---|
| {resource} | {action} | {check} | {period} |

## 4. Các bước deployment

| Bước | Command/Hành động | Kết quả mong đợi | Điều kiện dừng |
|---:|---|---|---|
| 1 | {action} | {result} | {condition} |

## 5. Database migration

{Thứ tự, compatibility, thời gian dự kiến, xác minh và recovery.}

## 6. Verification và smoke test

| Kiểm tra | Mong đợi | Evidence |
|---|---|---|
| Health endpoint | Healthy | {link/log} |

## 7. Monitoring

{Dashboard, alert, error rate, latency, saturation và observation window.}

## 8. Điều kiện rollback

- {Ngưỡng rõ ràng hoặc điều kiện lỗi}.

## 9. Các bước rollback

| Bước | Hành động | Kết quả mong đợi | Lưu ý dữ liệu |
|---:|---|---|---|
| 1 | {action} | {result} | {impact} |

## 10. Đầu mối escalation

| Vai trò | Kênh liên hệ | Điều kiện escalation |
|---|---|---|
| {role} | {channel} | {condition} |

## 11. Evidence triển khai

| Thời gian | Hành động/kiểm tra | Kết quả | Evidence | Người vận hành |
|---|---|---|---|---|
| {time} | {action} | {result} | {link} | {name} |

## AI tự kiểm tra (Self-check)

- [ ] Step có expected result và stop condition.
- [ ] Rollback xử lý cả application và data compatibility.
- [ ] Không chứa secret hoặc dữ liệu nhạy cảm.
