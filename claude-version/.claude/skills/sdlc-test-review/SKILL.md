---
name: sdlc-test-review
description: >-
  Review độc lập test result, evidence, coverage, regression và defect so với
  acceptance criteria và đúng build. Dùng cho Testing.validate bởi QA Review
  Agent; không sửa kết quả hoặc quyết định UAT/release.
---

# Review kết quả kiểm thử

## Điều kiện thực hiện

- Đọc stage contract, SRS, RTM, acceptance criteria, exact build, test artifacts, evidence và packet.
- Xác minh execution identity khác QA Agent đã chạy test; nếu không, trả `blocked`.
- Làm việc read-only; không sửa test case, status, defect hoặc RTM.

## Nguyên tắc review

- Đánh giá theo risk, approved requirement và execution evidence độc lập.
- Yêu cầu result tái lập bằng build, environment, data, steps và evidence.
- Không che giấu test chưa chạy, coverage limit, open defect hoặc residual risk.
- Tách QA readiness recommendation khỏi UAT/release decision của con người.

## Review và validation

- Chạy document validator rồi đối chiếu mỗi result với acceptance criteria, requirement, `TC-###`, build và environment.
- Kiểm tra mapping `FR/NFR/BR → test level/type → TC/verification method` và gap có lý do/authority.
- Kiểm tra coverage của success, boundary, validation, permission/ownership, dependency failure, timeout, retry/idempotency, data integrity, concurrency và regression theo risk.
- Kiểm tra NFR metric, target, measurement condition, actual result và evidence.
- Xác minh summary count khớp từng execution và Test Report liên kết đúng Plan/Specification/build/evidence.
- Điều tra mọi `skipped`, `flaky`, `blocked`, `not_run`, failed hoặc test thiếu evidence.
- Kiểm tra defect severity/status/work item, residual risk impact/likelihood/mitigation/owner và exception acceptance.
- Kiểm tra UAT liên kết business scenario, requirement, build và decision có evidence từ đúng Business/Product Owner.
- Khi resume, chỉ lặp validation khi build, artifact, environment, evidence hoặc scope thay đổi.

## Findings và checklist chất lượng

- Phân loại finding `blocking`, `major`, `minor`; liên kết `TC-###`, requirement ID, evidence, impact và sửa đổi bắt buộc.
- Plan/Specification có scope, test type, environment, data, role, schedule và entry/exit criteria rõ.
- Expected result quan sát được; coverage, actual NFR, defect, risk và recommendation không mâu thuẫn.
- Không biến test chưa chạy/thiếu evidence thành pass và không tạo test/evidence giả để lấp coverage.
- Trả findings, coverage gap, blocker và readiness recommendation; không sửa output hoặc quyết định UAT/release.
