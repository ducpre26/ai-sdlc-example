---
name: sdlc-service-operations
description: >-
  Tạo, cập nhật và kiểm tra Operations Runbook, Incident Postmortem và
  Maintenance Backlog có evidence trong AI-First SDLC. Dùng cho
  Operations.verify_inputs, Operations.execute và Operations.validate; không
  tự chạy thao tác production nguy hiểm hoặc chấp nhận rủi ro.
---

# Vận hành dịch vụ

## Đầu vào

- Đọc stage contract, release, service identity, owner, current state, telemetry, incident/work item, template, packet và progress.
- Xác minh access, monitoring, backup, obligation và safety boundary trước thao tác.

## Nguyên tắc nghiệp vụ

- Ưu tiên bảo vệ user, data và recoverability trước tốc độ; dangerous action phải có guard/verification.
- Dựa trên signal, threshold và evidence thay vì cảm nhận.
- Operational change có stop condition, rollback/failback và data impact.
- Postmortem blameless, phân tích system/decision/condition/control thay vì dừng ở lỗi cá nhân.
- Timeline/cause phân biệt event, inference, unknown và confidence.
- Corrective action khép vòng về đúng SDLC artifact/work item.
- Dùng least privilege và không ghi/yêu cầu secret hoặc quyền rộng hơn cần thiết.

## Thực hiện

- Runbook mô tả service/dependency, owner, health check, SLI/SLO/SLA, dashboard, alert, routine task, backup/restore, known failure, escalation và RTO/RPO khi áp dụng.
- Mỗi alert có owner, threshold, severity và hành động runbook cụ thể.
- Mỗi dangerous action có prerequisite, exact target/scope, expected result, stop condition, verification và recovery.
- Postmortem ghi impact, detection, evidence-based timeline, trigger, technical/systemic cause, recovery và contributing factor.
- Mỗi corrective action có type, owner, due date, work item và verification method.
- Maintenance Backlog liên kết metric, incident, feedback, dependency risk hoặc technical-debt evidence.
- Ưu tiên security/data loss/SLO breach, repeated severe incident, user value và cost of delay; không ưu tiên chỉ theo số lượng feedback chưa xác minh.
- Chuyển item đã duyệt về đúng Requirements/Design/Development/Testing/Release stage.

## Quy trình theo thao tác

- `create`: xác định service/owner/source, dùng template, chỉ điền action/evidence thật, review safety và chạy validator.
- `update`: so sánh release/design/current state, xác minh baseline commit, giữ ID, mở candidate version từ `draft`, đặt `supersedes_version` và đánh giá impact tới runbook consumer.
- `review`: kiểm tra actionability, permission, secret, stop condition, backup/restore, signal, timeline, cause và corrective action.
- `validate`: chạy document validator và diễn tập/xác minh runbook/restore/DR theo cadence/risk; không tự chạy production.
- `resume`: đọc release, incident/work item, packet và evidence gần nhất; xác minh current state trước khi tiếp tục.

## Traceability và kiểm tra chất lượng

- Duy trì `REL → service/runbook → INC → corrective action/MAINT → FR/NFR/ADR/WI/TC → REL tiếp theo`; không tạo work item/metric/incident/evidence giả.
- Runbook liên kết release/design, dashboard, alert và service owner; mỗi signal dẫn tới safe action, owner và escalation.
- Backup/restore, RTO/RPO, failover/failback và DR có verification; không chứa secret/dangerous action thiếu guard.
- Postmortem phân biệt event/inference/unknown, dùng evidence timeline, tìm systemic cause và gắn corrective action với owner/due/work item/verification.
- Maintenance item có source, impact, priority, owner và target release khi được plan; approved item quay về đúng stage để triển khai.

## Đầu ra và giới hạn

- Trả artifact, service/incident state, evidence, action, risk, blocker và handoff packet.
- Không tự chạy destructive command, thay đổi production, đóng incident hoặc phê duyệt risk.
