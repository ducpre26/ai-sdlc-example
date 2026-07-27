---
name: sdlc-software-testing
description: >-
  Lập kế hoạch, thiết kế test case, thực thi kiểm thử và ghi evidence cho đúng
  build trong AI-First SDLC. Dùng cho Testing.verify_inputs và Testing.execute
  bởi QA Agent; không dùng để review độc lập hoặc quyết định UAT.
---

# Kiểm thử phần mềm

## Kiểm tra đầu vào

- Đọc stage contract, build identity, SRS, RTM, design, test baseline, environment, data, template và packet.
- Xác minh entry criteria, exact build, access, environment và test data.
- Không coi mô tả implementation là test evidence.

## Nguyên tắc nghiệp vụ

- Ưu tiên theo risk: critical behavior, data, permission, dependency failure và high-impact NFR.
- Kết luận dựa trên execution quan sát được, độc lập với mô tả của developer.
- Mỗi requirement/NFR có verification method hoặc lý do được authority chấp nhận khi chưa test.
- Ghi build, environment, data, step và result đủ để tái lập.
- Tối thiểu hóa/ẩn danh test data, kiểm soát access và cleanup theo policy.
- Công khai test chưa chạy, open defect, exception và coverage limitation.
- Tách QA technical assessment khỏi Business Owner UAT decision.

## Thiết kế và thực thi

- Ánh xạ mỗi `FR/NFR/BR` sang test level/type và ít nhất một `TC-###` hoặc verification method có lý do.
- Mỗi test case có objective, requirement source, precondition, data, steps, expected result, status và evidence.
- Bao phủ success, boundary, validation, permission/ownership, dependency failure, timeout, retry/idempotency, data integrity, concurrency và regression khi áp dụng.
- Với NFR, ghi metric, target, measurement condition, actual result và evidence.
- Lập Test Plan với scope, test type, environment, data, role, schedule và entry/exit criteria.
- Thực thi trên đúng build/environment; thu command, log, screenshot, report hoặc URL thực sự tồn tại.
- Chỉ dùng `passed`, `failed`, `blocked`, `skipped`, `flaky`, `not_run`.
- Mỗi defect có severity, requirement/test case, status và work item; không hạ severity để vượt gate.
- Mỗi residual risk có impact, likelihood, mitigation, owner và acceptance decision khi cần.
- UAT dùng business scenario và ghi accepted exception, impact, handling, owner, work item; QA không tự quyết định.
- Đối chiếu planned/executed/passed/failed/blocked/skipped/flaky/not_run với chi tiết và cập nhật RTM.

## Quy trình theo thao tác

- `create`: xác định scope/risk, dùng template, lập plan, tạo `TC-###`, chuẩn bị environment/data và xác nhận entry criteria.
- `update`: phân tích thay đổi requirement/design/build; giữ ID, mở candidate version từ `draft`, đặt `supersedes_version`, cập nhật regression/environment/evidence.
- `resume`: đọc exact build và run gần nhất; chỉ chạy lại khi build, environment, data, scope thay đổi hoặc evidence hết hiệu lực.

## Tự kiểm tra và đầu ra

- Mỗi requirement/NFR có verification phù hợp; high-risk case có error/boundary/permission path.
- Expected result quan sát được và không lặp đơn thuần requirement.
- Summary count khớp từng test execution và đúng build.
- Coverage, actual NFR, defect, residual risk và recommendation không mâu thuẫn.
- Không biến test chưa chạy hoặc thiếu evidence thành đạt.
- Trả test artifact/result/evidence/defect/risk/blocker và packet; không review output của mình hoặc quyết định UAT/release.
