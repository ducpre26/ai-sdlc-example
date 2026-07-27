# Quy tắc repository

## Nguồn chuẩn theo runtime

- Bản Codex:
  - `skill/ai-first-sdlc/` và `skill/sdlc-*/` là nguồn chuẩn.
  - `.codex/agents/*.toml` là định nghĩa custom agent của repository.
- Bản Claude Code:
  - `claude-version/.claude/skills/` và `claude-version/.claude/agents/` là bản port độc lập.
  - Không tự đồng bộ hoặc ghi đè giữa bản Codex và bản Claude.
- Thay đổi dùng chung về artifact contract, template, schema hoặc workflow phải được đánh giá tác động cho cả hai bản.
- Việc cài vào thư mục discovery của người dùng hoặc repository là thao tác riêng, chỉ thực hiện khi được yêu cầu rõ.
- Với Codex hiện hành, ưu tiên `.agents/skills/` cho repository và `%USERPROFILE%\.agents\skills\` cho user skill. Chỉ dùng `%USERPROFILE%\.codex\skills\` khi surface Codex đang sử dụng đã được xác minh hỗ trợ đường dẫn đó.
- Companion skill phải được cài ngang hàng; không lồng trong `ai-first-sdlc`.

## Đồng bộ hướng dẫn sử dụng

- Cập nhật `huong-dan-su-dung-va-tich-hop.md` trong cùng thay đổi khi bất kỳ sửa đổi nào dưới `skill/ai-first-sdlc/` ảnh hưởng cách người dùng gọi, cấu hình, tích hợp hoặc vận hành skill.
- Thay đổi ảnh hưởng cách sử dụng gồm thao tác hoặc giai đoạn được hỗ trợ, first-use input, prompt, output contract, progress/resume, vị trí artifact, template hiển thị cho người dùng, lifecycle/status, dependency, human gate, lệnh validation và đường dẫn cài đặt.
- Refactor nội bộ, thay đổi chỉ liên quan test hoặc sửa câu chữ không làm đổi hành vi người dùng thì không bắt buộc cập nhật hướng dẫn.
- Trước khi hoàn tất thay đổi ảnh hưởng cách sử dụng, đối chiếu hướng dẫn với `SKILL.md`, workflow được tham chiếu, reference của giai đoạn liên quan, template và `agents/openai.yaml` khi áp dụng.
- Giữ hướng dẫn theo góc nhìn người dùng: tóm tắt hành vi và cung cấp ví dụ chạy được; không sao chép toàn bộ reference nội bộ.
- Kiểm tra liên kết Markdown cục bộ và chạy test hoặc validator liên quan sau khi cập nhật hướng dẫn.
- Khi thay đổi `claude-version/`, cập nhật `claude-version/README.md` nếu cách cài, gọi, cấu hình agent hoặc vận hành Claude thay đổi.
- Không cập nhật hướng dẫn Codex bằng chi tiết riêng của Claude, và ngược lại; chỉ liên kết chéo giữa hai bản.
