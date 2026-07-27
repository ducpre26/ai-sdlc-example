# Tiếp nhận lần đầu

## 1. Mục đích và phạm vi

- Dùng intake để thu thập sự thật tối thiểu, nhận diện phần chưa biết và chọn giai đoạn cùng artifact đầu tiên cho một dự án mới.
- Coi intake là bước định tuyến dùng chung, không phải một giai đoạn SDLC, artifact hay cổng phê duyệt mới.
- Chỉ dùng yêu cầu đầu vào chuyên biệt trong reference của giai đoạn sau khi đã định tuyến; không thay thế điều kiện đầu vào hoặc cổng phụ thuộc của giai đoạn đó.

## 2. Điều kiện kích hoạt

Đọc reference này khi thỏa một trong các điều kiện sau:

- Người dùng xác nhận đang khởi tạo một dự án mới.
- Không tìm thấy progress và cũng không có artifact SDLC có ý nghĩa để xác định trạng thái hoặc bản cơ sở của dự án.

Không dùng intake lần đầu khi:

- Có artifact SDLC hiện hành, kể cả khi progress bị thiếu; báo `progress_missing` và định tuyến từ artifact cùng yêu cầu hiện có.
- Thao tác là `update`, `review`, `validate`, `handoff` hoặc `resume`.
- Người dùng chỉ yêu cầu làm việc với một artifact hoặc giai đoạn đã xác định.

Không coi thư mục trống, template chưa được điền hoặc file progress mẫu là artifact SDLC có ý nghĩa.

## 3. Kiểm tra trước khi hỏi

1. Tìm quy ước repository, `docs/ai-sdlc/`, progress, artifact, quyết định, work item và evidence hiện có.
2. Kiểm tra Git. Nếu chưa có repository, thông báo Git là dependency lưu baseline và hỏi trước khi chạy `git init`; không tự tạo initial commit, commit hoặc push.
3. Phân biệt nội dung đã xác minh, quyết định của con người, giả định và phần chưa biết.
4. Tái sử dụng dữ liệu có nguồn trong repository; không hỏi lại thông tin đã có và không suy ra tiến độ từ artifact.
5. Nếu phát hiện artifact hiện hành, dừng intake lần đầu và quay lại quy trình định tuyến thông thường.
6. Nếu còn thiếu dữ liệu quan trọng, hỏi từng vòng từ ba đến năm câu dựa trên input tối thiểu bên dưới, rồi tóm tắt sự thật, quyết định, giả định và câu hỏi mở. Sau khi chọn Initiation, dùng `$sdlc-project-initiation` cho discovery chuyên môn; không hỏi toàn bộ danh sách trong một lượt.

## 4. Input tối thiểu

Để bắt đầu intake, cần có:

- Ý định khởi tạo dự án hoặc sản phẩm mới.
- Tên tạm thời, vấn đề/cơ hội hoặc kết quả chính đủ để nhận diện dự án.

Nếu chưa đủ nhận diện dự án, hỏi người dùng trước khi tạo file. Khi đã đủ, có thể định tuyến và tạo bản `draft`; không yêu cầu mọi input khuyến nghị phải hoàn chỉnh.

## 5. Input khuyến nghị

Thu thập từ người dùng hoặc nguồn có thật trong repository:

- Vấn đề/cơ hội và evidence hỗ trợ.
- Người dùng hoặc người thụ hưởng mục tiêu.
- Giá trị và kết quả mong đợi.
- Phạm vi ban đầu cùng phần ngoài phạm vi đã biết.
- Sponsor, Product/Business Owner và người chịu trách nhiệm dự án.
- Ràng buộc chính về thời gian, nguồn lực, khoảng ngân sách, kỹ thuật, hợp đồng, bảo mật hoặc tuân thủ.
- Target date, mốc hoặc sự kiện thúc đẩy khi có.
- Artifact mong muốn, mức áp dụng và vị trí đầu ra nếu khác quy ước của skill.
- Tài liệu, quyết định, nghiên cứu, work item hoặc evidence có thể dùng làm nguồn.

Các mục này là input khuyến nghị cho intake, không thay thế danh sách đầu vào bắt buộc của từng artifact trong reference giai đoạn.

## 6. Quy tắc khi thiếu hoặc mâu thuẫn dữ liệu

- Không tự tạo evidence, deadline, target date, budget, khoảng nguồn lực, Sponsor, Product Owner, approver, thẩm quyền hoặc quyết định.
- Ghi nội dung chưa biết hoặc mâu thuẫn vào `open_questions`, nêu tác động và chỉ định vai trò chịu trách nhiệm trả lời.
- Cho phép tạo artifact ở `draft` khi đã nhận diện được dự án và artifact phù hợp; chỉ điền sự thật có nguồn và ghi rõ giả định.
- Không chuyển artifact sang `ai_checked` nếu câu hỏi chặn hoặc nguồn bắt buộc chưa được giải quyết.
- Nếu người dùng yêu cầu artifact ở giai đoạn sau nhưng thiếu đầu vào đã duyệt bắt buộc, không vượt cổng phụ thuộc. Chỉ tạo `draft` khi người dùng yêu cầu rõ và phải ghi nguồn còn thiếu; nếu không, bàn giao hành động cần hoàn tất ở giai đoạn trước.
- Không tự phê duyệt artifact, tự nhận diện approver hoặc coi việc hoàn tất intake là quyết định Go.

## 7. Kết quả intake và định tuyến

Kết thúc intake bằng kết quả tối thiểu sau:

```text
Thao tác: create
Dự án: <tên hoặc định danh tạm thời>
Sự thật/nguồn: <thông tin đã xác minh và đường dẫn có thật>
Giai đoạn đề xuất: <stage và lý do>
Artifact đầu tiên: <loại artifact, status draft và đường dẫn dự kiến>
Câu hỏi mở: <nội dung, tác động và vai trò chịu trách nhiệm>
Cổng con người: <vai trò và quyết định cần có>
Bước tiếp theo: <hành động cụ thể và người chịu trách nhiệm>
```

- Với dự án mới chưa có bản cơ sở, mặc định định tuyến sang Khởi tạo/Lập kế hoạch và xem xét Project Charter trước.
- Chỉ định tuyến thẳng sang giai đoạn khác khi người dùng cung cấp đầu vào tương đương cùng nguồn có thể kiểm chứng; vẫn áp dụng chuỗi phụ thuộc trong `workflow-and-routing.md`.
- Sau khi chọn giai đoạn, đọc đúng một reference của giai đoạn đó và áp dụng điều kiện đầu vào, template, validation cùng human gate tương ứng.
