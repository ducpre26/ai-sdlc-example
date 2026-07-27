---
name: sdlc-requirements-review
description: >-
  Review độc lập SRS và RTM về nguồn, độ rõ nghĩa, khả năng kiểm thử, NFR và
  traceability trong AI-First SDLC. Dùng cho Requirements.validate bởi QA
  Review Agent; không sửa artifact hoặc thay Product Owner phê duyệt.
---

# Review yêu cầu

## Điều kiện thực hiện

- Đọc stage contract, SRS, RTM, baseline, quyết định có nguồn và task packet.
- Xác minh execution identity khác QA Agent đã tạo artifact; nếu không, trả `blocked`.
- Làm việc read-only; không sửa SRS, RTM hoặc metadata trong lượt review.

## Kiểm tra

1. Tìm requirement mơ hồ, mâu thuẫn, trùng lặp, khóa giải pháp, thiếu nguồn hoặc thiếu phạm vi.
2. Kiểm tra FR có hành vi quan sát được, precondition, input, exception và acceptance criteria kiểm thử được.
3. Kiểm tra NFR có metric, target, operating condition và verification method.
4. Kiểm tra BR có nguồn, điều kiện, kết quả và ngoại lệ.
5. Kiểm tra happy, negative, boundary, exception, security, data, privacy, audit và error behavior khi liên quan.
6. Phát hiện nội dung do AI suy luận nhưng không có quyết định stakeholder.
7. Kiểm tra `BO → FR/NFR/BR`, ID, liên kết, hàng trùng và số liệu RTM.
8. Không tạo liên kết hoặc requirement giả để lấp khoảng trống.

## Quy trình review và validation

- Chạy validator trước, nhưng không coi kết quả máy đạt là bằng chứng requirement đúng nghiệp vụ.
- Kiểm tra scope, user group, assumption, constraint và glossary so với Project Charter/product decision.
- Tìm wording không quan sát được, solution bias, priority chưa có authority, business rule/NFR do AI suy đoán và câu hỏi chặn bị giấu khỏi `open_questions`.
- Kiểm tra mục tiêu không có requirement, requirement không có verification method, orphan downstream link và requirement bị thay thế chưa cập nhật RTM.
- Xác minh SRS/RTM dùng đúng baseline, source/version và một source of truth.
- Khi resume review, dùng packet/finding gần nhất; không lặp kiểm tra còn hiệu lực nếu artifact và nguồn chưa đổi.

## Checklist chất lượng

- FR có source, rationale, priority, precondition, input, observable behavior, exception, acceptance criteria, dependency và verification method.
- NFR có quality attribute, metric, numeric target, operating condition và verification method.
- BR có source, scope, condition, outcome và exception.
- Security/data/interface/privacy/audit/error behavior được bao phủ khi liên quan.
- RTM không có hàng trùng, ID sai hoặc link không tồn tại; gap và summary count khớp chi tiết.

## Findings và đầu ra

- Phân loại finding thành `blocking`, `major` hoặc `minor`.
- Liên kết mỗi finding tới requirement ID, section/line khi có, evidence, tác động và sửa đổi bắt buộc.
- Trả findings, blocker, coverage gap và readiness recommendation trong handoff packet.
- Không sửa artifact, không tự chấp nhận risk và không thay Product Owner phê duyệt.
