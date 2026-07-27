# Kiểm thử và UAT

## 1. Mục đích và phạm vi

Xác minh đúng build so với requirement, acceptance criteria, NFR và risk bằng test result/evidence có thể review độc lập; chuẩn bị thông tin cho UAT và release decision.

## 2. Điều kiện kích hoạt

- Lập/cập nhật Test Plan, Test Specification, Test Report hoặc UAT Report.
- Thực thi functional, regression, integration, security, performance hoặc test liên quan.

## 3. Artifact đầu vào

- Build identity và implementation handoff.
- SRS, RTM, design, acceptance criteria và NFR baseline approved/committed.
- Environment, test data, access, risk và defect baseline.

## 4. Artifact đầu ra

| Artifact | Template |
|---|---|
| Test Plan | `assets/templates/05-testing/test-plan.md` |
| Test Specification | `assets/templates/05-testing/test-specification.md` |
| Test Report | `assets/templates/05-testing/test-report.md` |
| UAT Report | `assets/templates/05-testing/uat-report.md` |

## 5. Nguồn và evidence bắt buộc

- Mỗi result chỉ tới test case, requirement, build, environment và evidence thực tế.
- Evidence vắng mặt có nghĩa là chưa xác minh, không phải đạt.
- UAT decision chỉ được ghi khi Business Owner/Product Owner cung cấp rõ.

## 6. Ánh xạ step, agent và skill

| Step | Agent | Companion skill |
|---|---|---|
| `inspect`, `handoff` | `sdlc-orchestrator-agent` | Không |
| `verify_inputs`, `execute` | `qa-agent` | `sdlc-software-testing` |
| `validate` | `qa-review-agent` | `sdlc-test-review` |
| `human_gate` | `human` | Không |

QA Agent và QA Review Agent phải có execution identity khác nhau.

## 7. Traceability contract

- Duy trì `FR/NFR/BR → TC → execution/evidence → defect/risk → UAT/REL`.
- RTM phản ánh requirement chưa có test và test failed/blocked/skipped/flaky/not_run.
- Test Report và UAT chỉ tới đúng build.

## 8. Điều kiện chặn

- Build hoặc baseline không xác định/không committed.
- Environment/data/access không đủ cho test bắt buộc.
- Result quan trọng thiếu evidence hoặc số liệu không đối chiếu được.
- Không tạo được QA Review execution độc lập.

## 9. Human gate

QA Lead/Business Owner/Product Owner phù hợp quyết định chấp nhận kết quả hoặc UAT. Release Authority vẫn quyết định Go/No-Go ở Release.

## 10. Handoff contract

Bàn giao exact build, Test Plan/Specification/Report, RTM, evidence, defect, coverage gap, residual risk, UAT decision và approval identity sang Release.

## 11. Ngoại lệ

Tailoring loại test theo risk được phép nếu ghi lý do và người chấp nhận. Không đổi `not_run`, `skipped`, `blocked` hoặc thiếu evidence thành `passed`.
