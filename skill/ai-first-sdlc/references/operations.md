# Vận hành và bảo trì

## 1. Mục đích và phạm vi

Duy trì dịch vụ an toàn, quan sát được và có thể khôi phục; ghi nhận incident, learning và maintenance item để khép vòng về đúng stage SDLC.

## 2. Điều kiện kích hoạt

- Tạo/cập nhật Operations Runbook, Incident Postmortem hoặc Maintenance Backlog.
- Review operational readiness, incident hoặc maintenance evidence.

## 3. Artifact đầu vào

- Release/build/deployment decision và service identity.
- Design/runbook, owner, telemetry, alert, backup, incident, risk và work item hiện có.

## 4. Artifact đầu ra

| Artifact | Template |
|---|---|
| Operations Runbook | `assets/templates/07-operations/operations-runbook.md` |
| Incident Postmortem | `assets/templates/07-operations/incident-postmortem.md` |
| Maintenance Backlog | `assets/templates/07-operations/maintenance-backlog.md` |

## 5. Nguồn và evidence bắt buộc

- Service state, metric, event, timeline, cause và action chỉ tới evidence có thật.
- Phân biệt event, inference và unknown.
- Không ghi secret hoặc giả lập incident/work item/metric để khép traceability.

## 6. Ánh xạ step, agent và skill

| Step | Agent | Companion skill |
|---|---|---|
| `inspect`, `handoff` | `sdlc-orchestrator-agent` | Không |
| `verify_inputs`, `execute`, `validate` | `sdlc-orchestrator-agent` | `sdlc-service-operations` |
| `human_gate` | `human` | Không |

## 7. Traceability contract

- Duy trì `REL → service/runbook → INC → corrective action/MAINT → FR/NFR/ADR/WI/TC → REL tiếp theo`.
- Runbook liên kết release/design, dashboard, alert và service owner.
- Postmortem liên kết incident, change/release, evidence và corrective work item.

## 8. Điều kiện chặn

- Không xác định service owner, target, quyền hoặc current state.
- Thao tác nguy hiểm thiếu prerequisite, stop condition hoặc recovery.
- Incident timeline/cause quan trọng không có evidence hoặc chưa phân loại uncertainty.
- Risk cần chấp nhận nhưng chưa có người có thẩm quyền.

## 9. Human gate

Service Owner, Product Owner hoặc authority phù hợp quyết định chấp nhận runbook, postmortem action, maintenance priority hoặc operational risk.

## 10. Handoff contract

Bàn giao service/incident state, evidence, action, owner, due date, risk và artifact/work item cần quay lại stage SDLC tương ứng.

## 11. Ngoại lệ

Incident khẩn cấp ưu tiên bảo vệ người dùng và dữ liệu nhưng vẫn giữ audit trail, authority và follow-up. AI không tự chạy thao tác phá hủy hoặc thay đổi production.
