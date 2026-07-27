---
name: sdlc-release-management
description: >-
  Chuẩn bị, cập nhật và kiểm tra Release Plan, Deployment Runbook, Release
  Notes và bằng chứng Go/No-Go trong AI-First SDLC. Dùng cho
  Release.verify_inputs, Release.execute và Release.validate; không tự phát
  hành production hoặc quyết định Go.
---

# Quản lý phát hành

## Đầu vào

- Đọc stage contract, immutable build identity, Test Report/UAT, defect, risk, change, template, packet và progress.
- Xác minh approval, dependency, release window, backup, migration, rollback, monitoring và Release Authority.

## Nguyên tắc nghiệp vụ

- Giữ build bất biến sau Go gate; thay code/package/packaged config phải đánh giá lại.
- Rollback có condition, step, order, data impact và verification; không dùng “revert nếu cần”.
- Release phải quan sát được bằng smoke test, metric, alert, observation window và stop condition.
- Go/No-Go dựa trên test, defect, risk, migration và operational readiness evidence.
- Tránh gộp out-of-scope change hoặc sửa trực tiếp khi deploy nếu không theo emergency process.
- Communication nêu change, required action, compatibility, known issue và support.
- Chỉ Release Authority chấp nhận risk và quyết định phát hành.

## Thực hiện

- Gán `REL-###`; liên kết requirement/fix, work item, exact build, test evidence, dependency, schedule, migration và owner.
- Mỗi Go/No-Go criterion có expected result, actual result và evidence.
- Mỗi deployment step có action, expected result, evidence và stop condition.
- Runbook bao phủ prerequisite, backup verification, deploy order, data compatibility, migration, smoke test, monitoring, observation window, rollback và escalation.
- Không ghi secret value; chỉ ghi nguồn/configuration reference an toàn.
- Release Notes khớp build/scope và nêu feature, fix, breaking change, upgrade, compatibility, known issue và support.
- Breaking change có consumer plan, deadline và required action.

## Quy trình theo thao tác

- `create`: xác định `REL-###`/build/scope, dùng template, lập Plan/Runbook/Notes, thu evidence và chuẩn bị Go/No-Go.
- `update`: phân tích build/scope/window/risk change; giữ ID, mở candidate version từ `draft`, đặt `supersedes_version`, cập nhật ba artifact và yêu cầu re-approval khi gate bị ảnh hưởng.
- `review`: kiểm tra build, scope, test/UAT, dependency, data, rollback, monitoring, communication, secret và authority.
- `validate`: chạy validator, đối chiếu ID/evidence và diễn tập hoặc review runbook theo risk.
- `resume`: xác minh build, gate status và release window chưa đổi; không lặp bước/evidence còn hiệu lực.

## Traceability và kiểm tra chất lượng

- Duy trì `FR/NFR/BR → WI/PR → build → TC/Test Report/UAT → REL`; không tạo ID/evidence giả.
- Plan, Runbook và Notes dùng cùng `REL-###` và build; mỗi Notes item liên kết work item/requirement/change thật.
- Ghi requirement/fix thiếu test, test không thuộc build hoặc change thiếu work item trong review.
- Release Plan nhất quán về scope, build, test/UAT, dependency, schedule, migration, communication và Go/No-Go; residual risk có owner, mitigation và acceptor.
- Runbook có prerequisite, backup, deploy, migration, smoke, monitoring, rollback, escalation; mỗi step có expected result/evidence/stop condition và không chứa secret.
- Notes dùng ngôn ngữ phù hợp người nhận, không bỏ breaking change, upgrade, compatibility, known issue hoặc support.

## Đầu ra và giới hạn

- Trả artifact, evidence, risk, blocker, readiness và handoff packet.
- Không tự ghi Go, che giấu defect/risk hoặc triển khai production khi chưa có quyền.
