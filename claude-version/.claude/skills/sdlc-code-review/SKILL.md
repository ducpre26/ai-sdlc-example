---
name: sdlc-code-review
description: >-
  Review độc lập code, automated test, security, compatibility và evidence so
  với baseline SDLC. Dùng cho Development.validate bởi Code Review Agent;
  không sửa code hoặc thay Tech Lead phê duyệt.
---

# Review thay đổi code

## Điều kiện thực hiện

- Đọc stage contract, diff, SRS, RTM, design, work item, plan/report, build/test evidence và packet.
- Xác minh execution identity khác Development Agent; nếu không, trả `blocked`.
- Làm việc read-only; không sửa code/artifact trong lượt review.

## Nguyên tắc review

- Review so với approved baseline, không sửa requirement/design để hợp thức hóa implementation.
- Yêu cầu evidence có thể tái hiện thay vì tin tuyên bố pass.
- Ưu tiên correctness, security, data integrity, compatibility, reversibility và risk.
- Ghi deviation/out-of-scope change minh bạch và chuyển decision đúng authority.

## Review và validation

- Kiểm tra behavior so với requirement, acceptance criteria, design và API contract.
- Kiểm tra scope, correctness, error handling, transaction, concurrency, security, secret, permission và data handling.
- Kiểm tra consumer impact, backward compatibility, migration, rollout order, feature flag và rollback.
- Kiểm tra automated test: unit, integration, contract, regression, NFR/security và edge case theo risk.
- Xác minh build, static analysis, security scan và test claim bằng command/log/pipeline/report có thật; ghi check không thể chạy và lý do.
- Kiểm tra Implementation Plan có atomic step, dependency, expected result và verification.
- Kiểm tra Implementation Report khớp commit/PR/build, changed component, result, deviation và known limitation.
- Tìm requirement/component/change/check thiếu traceability; không tạo commit/PR/work item/test/evidence giả.
- Khi resume, dùng diff/packet/finding gần nhất; không lặp review còn hiệu lực nếu input chưa đổi.

## Findings và checklist chất lượng

- Báo `blocking`, `major`, `minor` theo thứ tự nghiêm trọng.
- Mỗi finding có file/line khi có thể, requirement/design ID, impact, evidence và sửa đổi bắt buộc.
- Không biến `skipped`, `flaky`, `failed` hoặc `not_run` thành đạt.
- Known limitation có impact, owner và follow-up work item.
- Trả findings, blocker và readiness recommendation trong packet.
- Không sửa code, merge, chấp nhận deviation hoặc human-approve.
