---
name: sdlc-software-development
description: >-
  Triển khai code, cấu hình và automated test từ Requirements, Design và work
  item đã duyệt trong AI-First SDLC. Dùng cho Development.verify_inputs và
  Development.execute bởi Development Agent; không dùng để review độc lập.
---

# Phát triển phần mềm

## Kiểm tra đầu vào

- Đọc stage contract, SRS, RTM, HLD/LLD/ADR/API, work item, template, packet, progress và Git baseline.
- Từ chối triển khai nếu requirement quan trọng chưa approved, baseline chưa committed hoặc design dependency còn chặn.
- Xác minh environment, dependency và entry condition; không tự tạo requirement/architecture decision để lấp khoảng trống.

## Nguyên tắc nghiệp vụ

- Bám requirement, design và contract approved.
- Chia thay đổi thành bước nhỏ, có expected result, dependency và verification.
- Dùng evidence thay tuyên bố; chỉ báo kết quả đã chạy và truy xuất được.
- Xem xét compatibility, migration, feature flag, deployment order và rollback trước thay đổi API/data.
- Không làm yếu security boundary, permission, secret hoặc data protection vì thuận tiện.
- Ghi deviation minh bạch và cập nhật đúng artifact/ADR thay vì sửa baseline để khớp implementation sai.
- Ghi version, configuration và command đủ để người khác tái hiện.

## Thực hiện

1. Xác định scope và liên kết `FR/NFR/BR`, `CMP/API/ADR`, work item, contract.
2. Lập Implementation Plan cho thay đổi rủi ro cao/nhiều bước/migration/compatibility-sensitive; mỗi bước có scope, expected result, dependency và verification.
3. Kế hoạch bao phủ unit, integration, contract, regression, NFR và security test phù hợp risk.
4. Thay đổi code, configuration và automated test đúng scope.
5. Làm rõ consumer, migration, rollout order, feature flag, rollback và data impact.
6. Chạy build, static analysis, security check và test phù hợp repository; ghi lệnh không thể chạy cùng lý do.
7. Ghi command, result, log, diff, commit/PR/build và evidence thực sự tồn tại.
8. Ghi deviation, known limitation, impact, owner và work item/decision cần có.
9. Khi tạo Implementation Report, ghi commit/PR, file/component thay đổi, build, static/security analysis và actual test result.
10. Chỉ tạo Implementation Report tại handoff/build candidate/thay đổi risk cao; ưu tiên PR/work item/commit/test evidence khi đủ.

## Quy trình theo thao tác

- `create`: đọc work item/baseline, xác định change, lập plan khi cần, giải quyết blocker rồi mới sửa code.
- `update`: khi artifact approved bị thay thế, giữ ID, mở candidate version từ `draft`, đặt `supersedes_version`; cập nhật plan theo scope/design và report theo result mà không xóa lịch sử deviation.
- `resume`: đọc work item, diff, plan/report, packet và result gần nhất; không lặp change hoặc verification còn hiệu lực.

## Tự kiểm tra

- Plan có in/out scope rõ và mỗi change liên kết requirement/design.
- Sequence, dependency, migration, compatibility, feature flag và rollback khả thi.
- Test/security strategy đủ cho risk; Definition of Done kiểm chứng được.
- Product/architecture question được chuyển đúng authority.
- Report khớp commit/PR/build/evidence; không đổi skipped/flaky/failed/not-run thành pass.
- API/data change, deviation và known limitation được ghi đầy đủ với owner/follow-up.

## Đầu ra và giới hạn

- Trả implementation packet gồm baseline, action, output, evidence, deviation, blocker và `next_agent: code-review-agent`.
- Không tự review thay đổi của mình, không bịa pass và không human-approve.
- Không commit, push hoặc tạo tag nếu người dùng chưa yêu cầu rõ.
