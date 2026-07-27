---
document_id: OPS-TEMPLATE-001
document_type: operations-runbook
project: template-project
version: 0.1.0
supersedes_version:
status: draft
previous_status:
owner: operations-owner
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

# Hướng dẫn vận hành (Operations Runbook)

## 1. Tổng quan hệ thống

{Mục đích, ranh giới production, user journey quan trọng và owner.}

## 2. Service và dependency

| Service/Dependency | Mục đích | Owner | Health check | Tác động khi lỗi |
|---|---|---|---|---|
| {service} | {purpose} | {role} | {check} | {impact} |

## 3. SLO và SLA

| Chỉ báo | SLO/SLA | Cửa sổ đo | Nguồn dữ liệu | Hành động theo error budget |
|---|---:|---|---|---|
| Availability | {target} | 30 days | {monitor} | {action} |

## 4. Dashboard và alert

| Dashboard/Alert | Tín hiệu | Ngưỡng | Owner | Mục trong runbook |
|---|---|---|---|---|
| {name} | {metric} | {threshold} | {role} | {section} |

## 5. Hoạt động vận hành định kỳ

| Tác vụ | Tần suất | Quy trình | Evidence | Owner |
|---|---|---|---|---|
| {task} | {frequency} | {steps/link} | {record} | {role} |

## 6. Backup và restore

{Phạm vi backup, tần suất, retention, các bước restore và chu kỳ restore test.}

## 7. Failure thường gặp

| Symptom | Likely cause | Diagnosis | Safe action |
|---|---|---|---|
| {symptom} | {cause} | {check} | {action} |

## 8. Troubleshooting

{Ordered checks with stop/escalation conditions; never expose secrets.}

## 9. Escalation

| Severity | Điều kiện | Phản ứng đầu tiên | Đường escalation | Target time |
|---|---|---|---|---|
| SEV-1 | {condition} | {role} | {path} | {time} |

## 10. Disaster Recovery

{RTO, RPO, failover/failback, dependency và lịch diễn tập.}

## AI tự kiểm tra (Self-check)

- [ ] Mỗi alert có owner và hành động an toàn.
- [ ] Restore và disaster recovery có cách kiểm chứng.
- [ ] Runbook không chứa secret hoặc thao tác phá hủy thiếu guardrail.
