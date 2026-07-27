# Phát triển

## 1. Mục đích và phạm vi

Triển khai code, configuration và automated test từ Requirements, Design và work item đã được chấp nhận; cung cấp evidence có thể review độc lập.

## 2. Điều kiện kích hoạt

- Thực hiện work item thay đổi code/configuration/test.
- Chuẩn bị implementation evidence hoặc build candidate.

## 3. Artifact đầu vào

- SRS/RTM và design contract approved/committed theo mức áp dụng.
- Work item, repository convention, Git baseline và dependency.
- Decision, risk và constraint từ handoff Design.

## 4. Artifact đầu ra

| Artifact/evidence | Template hoặc nguồn |
|---|---|
| Implementation Plan khi cần | `assets/templates/04-development/implementation-plan.md` |
| Implementation Report khi cần | `assets/templates/04-development/implementation-report.md` |
| Code/test/build evidence | Repository, PR, work item, command hoặc pipeline có thật |

Không tạo Implementation Report cho từng work item nhỏ nếu PR/work item/commit/test evidence đã đủ.

## 5. Nguồn và evidence bắt buộc

- Mọi thay đổi đáng kể liên kết requirement/design/work item hoặc lý do được chấp nhận.
- Build/test/security claim có command, log, pipeline hoặc report thực tế.
- Deviation ghi tác động, owner và decision cần có.

## 6. Ánh xạ step, agent và skill

| Step | Agent | Companion skill |
|---|---|---|
| `inspect`, `handoff` | `sdlc-orchestrator-agent` | Không |
| `verify_inputs`, `execute` | `development-agent` | `sdlc-software-development` |
| `validate` | `code-review-agent` | `sdlc-code-review` |
| `human_gate` | `human` | Không |

Development Agent và Code Review Agent phải có execution identity khác nhau.

## 7. Traceability contract

- Duy trì `FR/NFR/BR → CMP/API/ADR → WI/PR/commit → automated test/build`.
- Implementation evidence chỉ tới đúng baseline và build.
- Không tạo commit, PR, command hoặc test result giả.

## 8. Điều kiện chặn

- Requirement quan trọng hoặc design dependency chưa approved/committed.
- Work item không đủ phạm vi hoặc có decision quan trọng chưa được giải quyết.
- Không tạo được Code Review execution độc lập.
- Build/test claim bắt buộc thiếu evidence.

## 9. Human gate

Reviewer hoặc Tech Lead quyết định merge/accept deviation theo quy định dự án. AI không tự merge hoặc human-approve.

## 10. Handoff contract

Bàn giao implementation packet, exact commit/diff/build, test evidence, deviation, known limitation, review findings và decision sang Testing.

## 11. Ngoại lệ

Hotfix vẫn phải ghi source, diff, evidence, review và risk acceptance theo quy trình khẩn cấp. Không dùng urgency để bỏ separation of duties nếu dự án yêu cầu.
