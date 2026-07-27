# Phát hành và triển khai

## 1. Mục đích và phạm vi

Chuẩn bị một build bất biến, kế hoạch triển khai/rollback, communication và evidence để Release Authority quyết định Go/No-Go và bàn giao vận hành.

## 2. Điều kiện kích hoạt

- Chuẩn bị release candidate hoặc production deployment.
- Tạo/cập nhật Release Plan, Deployment Runbook hoặc Release Notes.

## 3. Artifact đầu vào

- Exact build, Test Report/UAT, defect, residual risk và approval liên quan.
- Dependency, migration, environment, release window và operational readiness.

## 4. Artifact đầu ra

| Artifact | Template |
|---|---|
| Release Plan | `assets/templates/06-release/release-plan.md` |
| Deployment Runbook | `assets/templates/06-release/deployment-runbook.md` |
| Release Notes | `assets/templates/06-release/release-notes.md` |

## 5. Nguồn và evidence bắt buộc

- `REL-###`, build, phạm vi, test/UAT, migration, rollback và risk tham chiếu nguồn thật.
- Go/No-Go criterion có actual result và evidence.
- Không ghi bí mật vào artifact hoặc che giấu known issue.

## 6. Ánh xạ step, agent và skill

| Step | Agent | Companion skill |
|---|---|---|
| `inspect`, `handoff` | `sdlc-orchestrator-agent` | Không |
| `verify_inputs`, `execute`, `validate` | `sdlc-orchestrator-agent` | `sdlc-release-management` |
| `human_gate` | `human` | Không |

## 7. Traceability contract

- Duy trì `FR/NFR/BR → WI/PR → build → TC/Test Report/UAT → REL`.
- Plan, Runbook và Notes dùng cùng `REL-###` và build identity.
- Mỗi release-note item liên kết change/work item hoặc nội dung build thực tế.

## 8. Điều kiện chặn

- Build, test/UAT hoặc approval bắt buộc không xác định.
- Migration/rollback/backup/monitoring bắt buộc chưa sẵn sàng.
- Blocking defect hoặc risk chưa có quyết định đúng thẩm quyền.
- Runbook không thể thực thi hoặc thiếu stop condition.

## 9. Human gate

Release Authority quyết định Go, Conditional Go hoặc No-Go. AI không tự triển khai production hoặc chấp nhận residual risk.

## 10. Handoff contract

Bàn giao release/build identity, decision, deployed state, runbook, dashboard, observation window, incident contact và residual risk sang Operations.

## 11. Ngoại lệ

Emergency release phải theo emergency authority và ghi rõ bước bị tailoring, compensating control và post-release action. Không bỏ build identity, rollback hoặc human decision.
