---
name: sdlc-solution-design
description: >-
  Tạo, cập nhật và kiểm tra HLD, LLD, ADR và OpenAPI từ baseline yêu cầu đã
  duyệt trong AI-First SDLC. Dùng cho Design.verify_inputs, Design.execute và
  Design.validate; không tự phê duyệt quyết định kiến trúc.
---

# Thiết kế giải pháp

## Đầu vào

- Đọc stage contract, SRS, RTM, NFR, constraint, template, contract hiện có, packet và progress.
- Chỉ dùng Requirements baseline đã approved và committed.
- Trả blocker thay vì tự quyết định security, data, contract hoặc technology khi thiếu thẩm quyền.

## Nguyên tắc nghiệp vụ

- Bắt đầu từ requirement/NFR và giải thích cách mỗi quyết định đáp ứng, xác minh chúng.
- Xác định rõ responsibility, data ownership, interface, trust boundary và owner.
- Ghi option, decision factor, benefit, cost, consequence và risk cho trade-off quan trọng.
- Thiết kế cho failure: timeout, retry, isolation, recovery, rollback và degraded mode khi liên quan.
- Thiết kế security: identity, authorization, sensitive data, secret, audit và abuse case.
- Dùng OpenAPI/schema cho interface có thể biểu diễn bằng máy.
- Làm rõ compatibility, data migration, deployment order và cách supersede decision cũ.

## Thực hiện

- Gán `CMP-###` cho component chính và `API-###` cho interface; mô tả responsibility, owner, boundary và traceability.
- HLD bao phủ context, component, integration, data, deployment, security, reliability, performance và observability khi áp dụng.
- LLD bao phủ public interface, data/business rule, authentication/authorization, error, timeout, retry, idempotency, transaction, concurrency, telemetry, testability, migration và compatibility khi áp dụng.
- Tạo ADR cho decision ảnh hưởng constraint, quality attribute, dependency, data boundary, operational risk hoặc future choice.
- ADR đánh giá ít nhất hai option khả thi hoặc ghi rõ vì sao không có option khác; không sửa ADR đã accepted, tạo ADR thay thế và liên kết bản cũ.
- Dùng OpenAPI/schema cho contract máy đọc; mô tả success/error, access, version và component owner.
- Không để Development tự quyết định ngầm về security, transaction, failure, compatibility hoặc data migration.

## Quy trình theo thao tác

- `create`: xác minh requirement/NFR, chọn HLD/LLD/ADR/OpenAPI phù hợp, dùng template, mô hình option, ghi trade-off, traceability và chạy kiểm tra.
- `update`: xác minh baseline đã commit, giữ ID, mở candidate version từ `draft`, đặt `supersedes_version`, phân tích impact tới consumer/data/deployment/test và cập nhật ADR/contract liên quan.
- `review`: kiểm tra boundary, responsibility, NFR, security, data, failure, operability, compatibility, testability và decision chưa được ghi.
- `validate`: chạy Markdown validator và OpenAPI tool của dự án khi có; tiếp tục kiểm tra source, content và consistency xuyên artifact.
- `resume`: đọc design, ADR, contract, packet và decision mới nhất; không tạo lại decision/sơ đồ hoặc lặp kiểm tra còn hiệu lực.

## Traceability và kiểm tra chất lượng

- Duy trì `FR/NFR/BR → CMP/API/ADR → WI/PR → TC`; không tạo trace giả.
- HLD/LLD chỉ rõ requirement/NFR mà mỗi component/góc nhìn đáp ứng.
- ADR liên kết decision factor, requirement, NFR, component và ADR bị supersede.
- OpenAPI liên kết `API-###`, component owner và requirement liên quan.
- HLD có context, boundary, responsibility, data ownership, dependency và quality scenario đủ cho risk.
- LLD/OpenAPI nhất quán về interface, schema, error, permission, transaction, concurrency, retry/idempotency và compatibility.
- Test design bao phủ success, error, boundary và NFR.
- ADR so sánh option công bằng, ghi consequence/risk và cách xác nhận sau triển khai; không sửa lịch sử decision accepted.

## Đầu ra và giới hạn

- Trả design artifact, decision, trade-off, evidence, open question, blocker và handoff packet.
- Chỉ ghi command/tool result thực sự chạy; validator đạt không chứng minh decision đúng.
- Không tự phê duyệt technology choice hoặc breaking contract.
