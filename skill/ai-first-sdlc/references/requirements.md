# Yêu cầu

## 1. Mục đích và phạm vi

Xác lập nhu cầu, hành vi, quy tắc, dữ liệu và thuộc tính chất lượng có nguồn, có thể kiểm thử trước khi thiết kế. Stage này không quyết định thay Product Owner.

## 2. Điều kiện kích hoạt

- Tạo hoặc cập nhật SRS, RTM, `FR-###`, `NFR-###`, `BR-###` hoặc acceptance criteria.
- Làm rõ yêu cầu cho feature/change trước Design hoặc Development.

## 3. Artifact đầu vào

- Project Charter/PMP được duyệt khi dự án yêu cầu.
- Product decision, stakeholder input, policy, research và artifact hiện có.
- Git baseline và progress gần nhất.

## 4. Artifact đầu ra

| Artifact | Template |
|---|---|
| SRS | `assets/templates/02-requirements/srs.md` |
| Requirements Traceability Matrix | `assets/templates/02-requirements/requirements-traceability-matrix.md` |

Chỉ giữ một SRS và một RTM hiện hành. Không tạo tài liệu riêng cho từng vòng elicitation.

## 5. Nguồn và evidence bắt buộc

- Mỗi requirement và quyết định quan trọng có nguồn/người cung cấp.
- Nội dung chưa xác minh nằm trong `open_questions` với owner.
- Không biến phát hiện, giả định hoặc suy luận AI thành requirement đã cam kết.

## 6. Ánh xạ step, agent và skill

| Step | Agent | Companion skill |
|---|---|---|
| `inspect`, `handoff` | `sdlc-orchestrator-agent` | Không |
| `verify_inputs`, `execute` | `qa-agent` | `sdlc-requirements-engineering` |
| `validate` | `qa-review-agent` | `sdlc-requirements-review` |
| `human_gate` | `human` | Không |

QA Agent và QA Review Agent phải có execution identity khác nhau.

## 7. Traceability contract

- Duy trì `BO → FR/NFR/BR → CMP/API/ADR → WI/PR → TC → REL`.
- RTM dùng ID và đường dẫn thật; không tạo ID/liên kết giả để lấp khoảng trống.
- Khi requirement bị loại hoặc thay thế, giữ lịch sử và cập nhật liên kết chịu tác động.

## 8. Điều kiện chặn

- Baseline đầu vào bắt buộc chưa approved/committed.
- Requirement quan trọng thiếu nguồn, mâu thuẫn hoặc acceptance criteria kiểm thử được.
- NFR bắt buộc chưa có target/phương pháp xác minh.
- Không tạo được QA Review execution độc lập.

## 9. Human gate

Product Owner hoặc người có thẩm quyền phê duyệt SRS/RTM. Im lặng không phải chấp thuận; artifact approved không còn câu hỏi mở.

## 10. Handoff contract

Bàn giao SRS/RTM baseline, requirement IDs, decisions, quality constraints, risks, open questions, approval identity và Git commit sang Design.

## 11. Ngoại lệ

Change nhỏ vẫn phải cập nhật nguồn chuẩn và traceability nhưng có thể tailoring section không liên quan. Không bỏ independent validation hoặc Product Owner gate.
