---
name: sdlc-requirements-engineering
description: >-
  Thu thập yêu cầu, đặt câu hỏi stakeholder và tạo hoặc cập nhật SRS cùng RTM
  có nguồn, có thể kiểm thử trong AI-First SDLC. Dùng cho
  Requirements.verify_inputs và Requirements.execute bởi QA Agent; không dùng
  để review độc lập hoặc tự quyết định nghiệp vụ.
---

# Kỹ nghệ yêu cầu

## Đầu vào bắt buộc

- Đọc stage contract, Project Charter, product decision, stakeholder input, SRS/RTM hiện có, template, packet và progress.
- Xác minh approved/committed baseline, stakeholder có thẩm quyền, nguồn nghiệp vụ, ưu tiên và câu hỏi đang mở.
- Không hỏi lại quyết định đã có trong `decisions_received`.

## Nguyên tắc nghiệp vụ

- Liên kết mỗi requirement với giá trị, nghĩa vụ hoặc nhu cầu có nguồn.
- Mô tả hành vi/kết quả quan sát được; tránh từ mơ hồ như “hỗ trợ”, “nhanh”, “thân thiện”.
- Giữ requirement kiểm thử được và trung lập về giải pháp, trừ technology constraint đã được quyết định.
- Mỗi NFR phải đo được bằng metric, target, operating condition và verification method.
- Đưa security và data vào requirement khi liên quan: ownership, classification, retention, access, privacy, audit và failure behavior.
- Giữ một source of truth; không sao chép cùng requirement sang nhiều tài liệu thiếu ID/liên kết.

## Guided discovery và elicitation

### Khi kích hoạt

Thực hiện elicitation khi tạo/cập nhật SRS hoặc RTM mà thiếu dữ liệu có nguồn, nguồn mâu thuẫn, acceptance criteria/NFR chưa xác minh hoặc người dùng yêu cầu khám phá. Chỉ hỏi khoảng trống ảnh hưởng requirement/gate hiện tại. Không dùng discovery để thay Product Owner quyết định phạm vi hoặc ưu tiên.

### Kiểm tra trước khi hỏi

1. Đọc Charter, SRS, RTM, policy, research, support/incident data, design constraint và quyết định hiện có.
2. Xác định requirement/câu hỏi đã có nguồn, mâu thuẫn và khoảng trống traceability.
3. Xác định mục tiêu elicitation, stakeholder phù hợp và kỹ thuật cần dùng.
4. Chọn đúng người trả lời: Product Owner, Business Owner, end user, operations, security/data owner hoặc Tech Lead khi cần feasibility input.
5. Không hỏi lại nội dung đã có nguồn hoặc đã được trả lời trong packet.

### Chu kỳ đặt câu hỏi

1. Chọn một nhóm khoảng trống có tác động cao nhất.
2. Hỏi mở để hiểu As-Is, mục tiêu hoặc hành vi mong muốn.
3. Hỏi sâu về trigger, actor, precondition, input, state, business rule, exception và observable result.
4. Hỏi số liệu/threshold/operating condition/verification method đối với NFR.
5. Mỗi vòng hỏi từ ba đến năm câu cùng chủ đề.
6. Tóm tắt câu trả lời, điểm mâu thuẫn và candidate requirement để stakeholder xác nhận.
7. Điều chỉnh câu hỏi kế tiếp theo câu trả lời; bỏ câu không còn liên quan.
8. Trả packet cho Orchestrator khi cần quyết định; không tự trả lời thay stakeholder.

Mỗi câu hỏi phải giúp xác minh nguồn/sự thật, lấy quyết định, làm acceptance criteria kiểm thử được, làm NFR đo được hoặc xác định owner/dependency/risk/gate. Ví dụ đưa ra để minh họa không được ghi thành dữ liệu đã xác minh.

### Cách ghi nhận câu trả lời

Phân loại từng nội dung thành:

- `verified_fact`: sự thật có tài liệu, dữ liệu, hệ thống hoặc evidence hỗ trợ.
- `human_decision`: quyết định kèm người cung cấp, vai trò, thời điểm và nguồn.
- `candidate_requirement`: nhu cầu/phát hiện chưa được người có thẩm quyền chấp nhận.
- `assumption`: giả định, tác động và cách xác minh; không đưa vào committed requirement.
- `open_question`: câu hỏi, tác động và stakeholder chịu trách nhiệm.
- `conflict`: nguồn/ý kiến mâu thuẫn và người có thẩm quyền giải quyết.

Chỉ chuyển `candidate_requirement` thành FR/NFR/BR khi có nguồn hoặc quyết định phù hợp. Giữ provenance của quyết định trong artifact hoặc packet. Không gộp ý kiến nhiều stakeholder thành quyết định khi chưa có authority giải quyết. Không lưu secret, credential hoặc transcript nhạy cảm trong progress; tham chiếu evidence theo policy của dự án.

### Chọn kỹ thuật elicitation

- Dùng phỏng vấn cho mục tiêu, pain point, business rule, exception và quyết định cá nhân có thẩm quyền.
- Dùng workshop cho luồng xuyên vai trò, terminology, priority hoặc conflict cần thống nhất.
- Dùng phân tích tài liệu cho policy, contract, regulation, report, ticket và requirement cũ.
- Dùng quan sát/contextual inquiry cho As-Is và workaround thực tế.
- Dùng prototype/storyboard cho UX state và hành vi khó diễn đạt; phản hồi là candidate input cho đến khi được quyết định.
- Dùng interface/data analysis cho integration, field, ownership, quality, migration và audit.
- Dùng survey/data analysis để tìm pattern ở quy mô lớn; không coi kết quả là approval.
- Trước buổi elicitation, xác định mục tiêu, người tham gia, kỹ thuật, thời lượng và đầu ra cần xác nhận.
- Trước khi ghi âm/lưu transcript hoặc xử lý dữ liệu cá nhân, xác nhận consent, nơi lưu, quyền truy cập và retention.
- Với research ngoài, ghi nguồn/URL, ngày truy cập, phạm vi áp dụng, độ mới và giới hạn tin cậy.

### Nhóm câu hỏi: kế hoạch elicitation và hiện trạng

- Mục tiêu vòng elicitation là gì và quyết định nào cần đạt?
- Stakeholder nào biết nghiệp vụ, sử dụng, vận hành, quản trị dữ liệu hoặc có thẩm quyền?
- Quy trình As-Is, pain point, workaround và hệ thống liên quan là gì?
- Thuật ngữ, policy, artifact và nguồn dữ liệu nào phải đọc trước?
- Bước nào của As-Is bắt buộc phải giữ vì policy hoặc business obligation?
- Mâu thuẫn nào đang tồn tại và ai có quyền giải quyết?

### Nhóm câu hỏi: hành vi chức năng và quy tắc

- Actor nào khởi tạo hành vi, trigger và precondition là gì?
- Input, state transition, output và observable result là gì?
- Happy path, alternate path, negative, boundary, exception và recovery behavior là gì?
- Business rule áp dụng trong điều kiện nào, kết quả và ngoại lệ ra sao?
- Ai được xem, tạo, thay đổi, phê duyệt hoặc hủy dữ liệu/hành động?
- Hành vi khi validation, dependency hoặc downstream service thất bại là gì?

### Nhóm câu hỏi: dữ liệu, tích hợp và chuyển đổi

- Dữ liệu nào được tạo/đọc/sửa/xóa, owner và source of truth là gì?
- Classification, privacy, consent, retention, deletion và audit requirement nào áp dụng?
- Interface/event/file nào trao đổi dữ liệu; contract, version, authentication và error behavior là gì?
- Yêu cầu data quality, duplicate, reconciliation và idempotency là gì?
- Có migration/backfill/cutover nào; mapping, validation, rollback và owner là ai?

### Nhóm câu hỏi: NFR và trải nghiệm

- Performance, capacity, availability, reliability hoặc recovery target nào cần đạt và trong điều kiện nào?
- Load, concurrency, data volume và growth rate dự kiến là bao nhiêu?
- Security, privacy, compliance, audit và abuse case nào liên quan?
- UX state nào cần mô tả: empty, loading, validation, partial success, error, permission denied hoặc offline?
- Accessibility, localization, device/browser và compatibility constraint nào áp dụng?
- Metric, threshold, environment và verification method cho từng NFR là gì?

### Nhóm câu hỏi: ưu tiên và truy vết

- Requirement hỗ trợ `BO-###`, obligation hoặc risk nào?
- Ai có thẩm quyền quyết định priority và scope?
- Mục nào là Must, Should, Could hoặc Won't và Product Owner đã quyết định chưa?
- Dependency, assumption và conflict nào ảnh hưởng requirement?
- Acceptance criteria nào chứng minh requirement đạt?
- Requirement nào bị thay thế/loại bỏ và liên kết downstream nào phải cập nhật?

### Kết thúc một vòng elicitation

Kết thúc vòng khi:

- Mục tiêu vòng hỏi đã đạt hoặc phần thiếu trở thành `open_question` có owner.
- Candidate requirement và bản tóm tắt đã được stakeholder xác nhận hoặc chuyển đúng người quyết định.
- Conflict có authority chịu trách nhiệm.
- Có đủ dữ liệu để cập nhật SRS/RTM `draft`, hoặc blocker đã rõ.

Trả `questions`, `decisions_received`, candidate requirements, assumptions, conflicts và open questions trong packet. Không tạo biên bản phỏng vấn riêng nếu artifact, packet và progress đã lưu đủ nguồn.

Trước khi đóng vòng, xác nhận còn chủ đề quan trọng nào chưa hỏi, cần gặp thêm ai, phần nào là fact/decision/assumption/open question và ai xác nhận bản tóm tắt. Không coi elicitation hoàn tất chỉ vì đã hết ngân hàng câu hỏi.

## Viết SRS và RTM

- Dùng ID ổn định `FR-###`, `NFR-###`, `BR-###`; không tái sử dụng ID cho ý nghĩa khác.
- Mỗi FR có nguồn, lý do, ưu tiên, precondition, input, hành vi quan sát được, ngoại lệ, acceptance criteria, dependency và verification method.
- Mỗi NFR có quality attribute, metric, target, operating condition và verification method.
- Mỗi BR có nguồn, phạm vi, điều kiện, kết quả và ngoại lệ.
- Bao phủ happy, negative, boundary, exception và error behavior khi liên quan.
- Làm rõ authentication, authorization, data ownership, privacy, retention, audit và failure behavior khi liên quan.
- Liên kết mỗi requirement với `BO-###`; trường hợp nền tảng/tuân thủ không liên kết trực tiếp phải có lý do.
- Acceptance criteria phải bổ sung tình huống, điều kiện và kết quả kiểm thử được, không lặp lại câu requirement.
- Chỉ giữ một SRS và một RTM hiện hành; không tạo tài liệu riêng cho từng vòng phỏng vấn.

## Quy trình theo thao tác

- `create`: xác minh nguồn, stakeholder và glossary; dùng đúng template, gán ID, viết requirement/acceptance criteria/RTM, tự kiểm tra và chạy validator.
- `update`: xác minh baseline đã commit, giữ ID khi ý nghĩa không đổi, mở một candidate version từ `draft`, đặt `supersedes_version`, phân tích tác động tới Design/Development/Testing/Release và cập nhật RTM; không tăng version từng vòng elicitation/review.
- `resume`: đọc SRS/RTM, packet và decision gần nhất; không tạo lại ID, hỏi lại câu đã trả lời hoặc lặp phân tích còn hiệu lực.

## Tự kiểm tra và đầu ra

- Không đánh dấu sẵn sàng khi còn câu hỏi chặn hoặc acceptance criteria chưa kiểm thử được.
- Cập nhật RTM và phân tích tác động khi requirement thay đổi; không tăng version theo từng vòng elicitation/review.
- Xác minh scope, user group, assumption, constraint và glossary nhất quán với Charter.
- Xác minh FR có observable behavior, exception và testable acceptance criteria; NFR có metric/threshold/environment/cách đo.
- Xác minh business rule, data, interface, security và privacy có nguồn/phạm vi rõ.
- Xác minh RTM không có hàng trùng, ID sai, link không tồn tại; gap và số tổng hợp khớp chi tiết.
- Trả SRS, RTM, `questions`, `decisions_received`, `open_questions`, evidence và handoff packet cho Orchestrator.
- Không validate độc lập output của mình và không human-approve.
