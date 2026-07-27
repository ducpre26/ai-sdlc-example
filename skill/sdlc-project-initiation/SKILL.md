---
name: sdlc-project-initiation
description: >-
  Thu thập, tạo, cập nhật và kiểm tra nội dung Project Charter và Project
  Management Plan trong AI-First SDLC. Dùng cho Initiation.verify_inputs,
  Initiation.execute và Initiation.validate; không dùng để tự phê duyệt dự án.
---

# Khởi tạo dự án

## Đầu vào bắt buộc

- Nhận stage contract, template, nguồn hiện có, task packet và progress từ Orchestrator.
- Xác minh vấn đề, giá trị, Sponsor, thẩm quyền, phạm vi, ràng buộc và nguồn.
- Nếu thiếu quyết định, thực hiện guided discovery bên dưới; không tự tạo ngân sách, thời hạn, bằng chứng khách hàng hoặc kết luận khả thi.

## Nguyên tắc nghiệp vụ

- Ưu tiên lý do kinh doanh, giá trị và người chịu trách nhiệm trước giải pháp.
- Không lập kế hoạch chi tiết như thể dự án đã được cấp quyền khi Charter chưa qua gate.
- Giữ tài liệu ở mức cao nhưng có thể kiểm chứng bằng owner, target, thời hạn và acceptance condition.
- Ưu tiên evidence; nếu chưa có baseline/nghiên cứu, ghi rõ điều chưa biết và cách xác minh.
- Tailor mức gọn nhẹ, tiêu chuẩn hoặc kiểm soát cao theo quy mô/rủi ro; không coi một định dạng Charter là duy nhất.
- Coi Charter approved là baseline ổn định; thay đổi đáng kể cần impact analysis và quyết định đúng thẩm quyền.

## Guided discovery cho Initiation

### Khi kích hoạt

Thực hiện discovery khi tạo/cập nhật Project Charter hoặc PMP mà thiếu dữ liệu có nguồn, nguồn mâu thuẫn, thẩm quyền chưa rõ hoặc người dùng yêu cầu khám phá. Không chạy lại discovery khi packet đã có câu trả lời còn hiệu lực. Với `review` hoặc `validate`, chỉ đặt câu hỏi nếu finding tạo blocker cần người có thẩm quyền giải quyết.

### Kiểm tra trước khi hỏi

1. Đọc repository convention, artifact, progress, quyết định, nghiên cứu, work item và evidence hiện có.
2. Lập danh sách dữ liệu đã có nguồn, dữ liệu mâu thuẫn và khoảng trống ảnh hưởng artifact/gate.
3. Xác định đúng stakeholder cần trả lời: Sponsor, Business Owner, Product Owner, Project Owner hoặc Tech Lead.
4. Không hỏi lại câu đã có trong `decisions_received` hoặc nguồn hiện hành.
5. Chỉ hỏi khoảng trống có tác động đến vòng hiện tại; không gửi toàn bộ ngân hàng câu hỏi.

### Chu kỳ đặt câu hỏi

1. Chọn một chủ đề có tác động cao nhất.
2. Bắt đầu bằng câu hỏi mở để lấy bối cảnh và mục tiêu.
3. Tiếp tục bằng câu hỏi cụ thể về số liệu, ngưỡng, owner, thời hạn, nguồn hoặc điều kiện quyết định.
4. Mỗi vòng hỏi từ ba đến năm câu cùng chủ đề.
5. Tóm tắt lại câu trả lời để stakeholder xác nhận.
6. Điều chỉnh câu tiếp theo theo câu trả lời; không bám kịch bản cố định khi câu hỏi không còn liên quan.
7. Phân loại kết quả rồi trả packet cho Orchestrator; không tự tiếp tục nếu cần quyết định mới.

Mỗi câu hỏi phải giúp xác minh nguồn/sự thật, lấy quyết định của con người, làm rõ owner/dependency/risk/gate hoặc tạo mục tiêu có thể đo. Có thể đưa ví dụ về dạng câu trả lời nhưng phải ghi rõ đó chỉ là ví dụ.

### Cách ghi nhận câu trả lời

Phân loại từng nội dung thành:

- `verified_fact`: sự thật kèm tài liệu, dữ liệu hoặc evidence có thể kiểm tra.
- `human_decision`: quyết định kèm nội dung, người cung cấp, vai trò, thời điểm và nguồn hội thoại/tài liệu.
- `assumption`: giả định tạm thời, tác động và kế hoạch xác minh; không dùng như quyết định đã duyệt.
- `open_question`: câu hỏi, lý do cần biết, tác động nếu chưa trả lời và vai trò chịu trách nhiệm.
- `conflict`: các nguồn mâu thuẫn, phạm vi ảnh hưởng và người có thẩm quyền giải quyết.

Không ghi câu trả lời thành requirement hoặc approval nếu người cung cấp không có thẩm quyền tương ứng. Không gộp ý kiến nhiều stakeholder thành một quyết định khi chưa có authority giải quyết. Không lưu secret, credential hoặc transcript nhạy cảm trực tiếp trong progress; chỉ tham chiếu evidence theo chính sách dự án.

### Chọn kỹ thuật khám phá

- Dùng phỏng vấn khi cần mục tiêu, pain point, constraint hoặc quyết định của một stakeholder.
- Dùng workshop khi nhiều bên phải thống nhất phạm vi, ưu tiên, responsibility hoặc conflict.
- Dùng phân tích tài liệu/dữ liệu khi cần baseline, bằng chứng vấn đề, policy, contract hoặc số đo hiện trạng.
- Dùng quan sát quy trình hiện tại khi mô tả của stakeholder không đủ thể hiện As-Is.
- Dùng prototype/spike khi cần xác minh giả thuyết giá trị hoặc feasibility; kết quả vẫn là evidence/candidate input, không tự trở thành quyết định.
- Dùng khảo sát khi cần tín hiệu từ nhiều người; không coi số đông là approval.
- Trước buổi discovery, xác định mục tiêu, người tham gia, kỹ thuật, thời lượng và đầu ra cần xác nhận.
- Trước khi ghi âm/lưu transcript hoặc xử lý dữ liệu cá nhân, xác nhận consent, nơi lưu, quyền truy cập và retention.
- Với nghiên cứu ngoài, ghi nguồn/URL, ngày truy cập, phạm vi áp dụng, độ mới và giới hạn tin cậy.

### Nhóm câu hỏi: vấn đề và giá trị

- Vấn đề/cơ hội cụ thể là gì, ai chịu tác động và evidence nào cho thấy nó tồn tại?
- Quy trình hoặc giải pháp hiện tại là gì, pain point và chi phí trì hoãn ra sao?
- Kết quả kinh doanh hoặc người dùng nào cần thay đổi?
- Giải pháp nào đã thử và vì sao chưa đủ?
- Có phương án không làm, mua sản phẩm hoặc đổi quy trình thay vì xây mới không?
- Điều gì sẽ chứng minh dự án không còn cần thiết hoặc giả thuyết ban đầu sai?

### Nhóm câu hỏi: stakeholder và thẩm quyền

- Ai là Sponsor, Business/Product Owner, người chịu trách nhiệm thực hiện và người phê duyệt?
- Ai sử dụng, vận hành, hỗ trợ hoặc chịu ảnh hưởng từ sản phẩm?
- Ai quyết định phạm vi, ngân sách, timeline, technology constraint và risk acceptance?
- Có stakeholder bắt buộc nào từ security, legal, compliance, data hoặc operations không?
- Có xung đột mục tiêu hoặc vai trò kiêm nhiệm nào cần ghi rõ không?

### Nhóm câu hỏi: mục tiêu và đo lường

- Mỗi mục tiêu có baseline, target, measurement source và thời hạn nào?
- Chỉ số nào phản ánh outcome; chỉ số nào chỉ phản ánh hoạt động triển khai?
- Ai sở hữu chỉ số và chu kỳ đánh giá?
- Điều kiện thành công, dừng, đổi hướng hoặc No-Go là gì?

### Nhóm câu hỏi: phạm vi, ràng buộc và rủi ro

- In-scope, out-of-scope, deliverable và acceptance condition là gì?
- Deadline, nguồn lực, khoảng ngân sách, contract, security, compliance hoặc technology constraint nào đã được quyết định?
- Dependency và milestone nào ảnh hưởng đường găng?
- Rủi ro chính, owner, response và escalation condition là gì?

### Kết thúc một vòng discovery

Kết thúc vòng hỏi khi:

- Câu hỏi mục tiêu đã được trả lời hoặc chuyển thành `open_question` có owner.
- Mâu thuẫn đã được giao đúng người có thẩm quyền.
- Có đủ input để tạo/cập nhật artifact `draft`, hoặc đã xác định blocker.
- Stakeholder đã xác nhận bản tóm tắt.

Trước khi đóng vòng, xác nhận còn chủ đề quan trọng nào chưa hỏi, cần gặp thêm ai, phần nào là fact/decision/assumption/open question và ai sẽ xác nhận bản tóm tắt. Không coi discovery hoàn tất chỉ vì đã hết danh sách câu hỏi.

Trả `questions`, `decisions_received`, assumptions, conflicts, open questions và đề xuất vòng tiếp theo trong packet. Không tạo tài liệu phỏng vấn riêng nếu packet, artifact và progress đã lưu đủ.

## Tạo hoặc cập nhật artifact

1. Phân loại thông tin theo kết quả discovery.
2. Viết Project Charter bằng ngôn ngữ kinh doanh; chỉ giữ ràng buộc kỹ thuật ảnh hưởng giá trị, phạm vi, chi phí, thời gian, tuân thủ hoặc rủi ro.
3. Gán `BO-###` ổn định. Mỗi mục tiêu có owner, baseline, target, thời hạn và nguồn đo khi đã được cung cấp.
4. Làm rõ phạm vi, ngoài phạm vi, deliverable, điều kiện chấp nhận, Sponsor và quyền được trao.
   Mỗi deliverable phải có owner và acceptance condition.
5. Khi lập PMP, liên kết đúng Project Charter đã duyệt; mô tả work package, milestone, dependency, trách nhiệm, rủi ro, chất lượng, bảo mật, thay đổi, truyền thông và tiêu chí kết thúc ở mức phù hợp.
6. Với update, giữ document ID, dùng candidate version hiện hành và ghi tác động theo Git/versioning contract trong packet.

## Quy trình theo thao tác

- `create`: chọn mức tailoring, kiểm tra input, dùng đúng template, thay metadata/ID mẫu, chỉ điền thông tin có nguồn, ghi `open_questions`, tự kiểm tra và chạy validator.
- `update`: xác minh baseline đã commit, giữ ID, mở một candidate version từ `draft`, đặt `supersedes_version` và phân tích tác động tới phạm vi, ngân sách, lịch, risk, requirement và downstream artifact.
- `review`: kiểm tra authority, business value, feasibility, scope, objective, resource, risk, evidence và tính nhất quán Charter/PMP; không sửa artifact nếu task chỉ review.
- `validate`: chạy validator rồi kiểm tra nội dung/nguồn; validator đạt không chứng minh business case hoặc approval đúng.
- `resume`: đọc version, status, packet và decision gần nhất; không tạo lại artifact hoặc lặp kiểm tra còn hiệu lực khi nguồn chưa đổi.

## Kiểm tra chất lượng

- Phân biệt business outcome với hoạt động triển khai.
- Không để phạm vi, deliverable, nguồn lực, ngân sách và thời hạn mâu thuẫn.
- Mỗi rủi ro có owner, response và escalation condition.
- Mỗi milestone PMP có owner, condition đạt và dependency; chỉ ghi ngày là chưa đủ.
- Project Charter xác định đúng Sponsor và thẩm quyền.
- PMP chỉ dùng Project Charter approved/committed làm baseline.
- Work package, milestone, dependency và responsibility của PMP phù hợp nguồn lực/constraint trong Charter.
- Risk, quality, security, communication, change/configuration và monitoring có owner cùng cadence hoặc nơi lưu control.
- Phân biệt điều kiện kết thúc planning với điều kiện đóng dự án.
- Phần approval thể hiện Go/Conditional Go/No-Go, lý do và điều kiện nhưng chỉ ghi khi con người cung cấp.
- Giữ nội dung chưa xác minh trong `open_questions`.

## Đầu ra và giới hạn

- Trả artifact, câu hỏi, quyết định có nguồn, evidence, blocker và handoff packet.
- Chỉ đưa artifact do AI tạo tới `ai_checked`.
- Không ghi Go/No-Go, `approved` hoặc quyết định thay Sponsor/con người.
