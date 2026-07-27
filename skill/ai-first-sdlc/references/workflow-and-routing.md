# Workflow và định tuyến

## Mục lục

1. [Bản đồ các giai đoạn](#1-bản-đồ-các-giai-đoạn)
2. [Quy tắc theo thao tác](#2-quy-tắc-theo-thao-tác)
3. [Tác vụ nhiều giai đoạn và checkpoint](#3-tác-vụ-nhiều-giai-đoạn-và-checkpoint)
4. [Metadata và lifecycle phiên bản](#4-metadata-và-lifecycle-phiên-bản)
5. [Danh mục template](#5-danh-mục-template)
6. [Quy ước ID](#6-quy-ước-id)
7. [Quy tắc trạng thái](#7-quy-tắc-trạng-thái)
8. [Chuỗi phụ thuộc tối thiểu](#8-chuỗi-phụ-thuộc-tối-thiểu)
9. [Theo dõi và tiếp tục tiến độ](#9-theo-dõi-và-tiếp-tục-tiến-độ)

## 1. Bản đồ các giai đoạn

| Bước | Từ khóa/artifact kích hoạt | Thư mục template | Thư mục đầu ra mặc định | Cổng con người |
|---:|---|---|---|---|
| 1 | Charter, project plan, scope, feasibility | `assets/templates/01-initiation/` | `docs/ai-sdlc/01-initiation/` | Sponsor |
| 2 | SRS, FR, NFR, acceptance criteria, RTM | `assets/templates/02-requirements/` | `docs/ai-sdlc/02-requirements/` | Product Owner |
| 3 | HLD, LLD, ADR, OpenAPI, architecture | `assets/templates/03-design/` | `docs/ai-sdlc/03-design/` | Tech Lead |
| 4 | Implementation Plan/Report, PR evidence | `assets/templates/04-development/` | `docs/ai-sdlc/04-development/` | Reviewer/Tech Lead |
| 5 | Test Plan/Specification/Report, UAT | `assets/templates/05-testing/` | `docs/ai-sdlc/05-testing/` | QA và Business Owner |
| 6 | Release Plan/Notes, deployment, rollback | `assets/templates/06-release/` | `docs/ai-sdlc/06-release/` | Người có thẩm quyền phát hành |
| 7 | Operations, SLO, incident, postmortem | `assets/templates/07-operations/` | `docs/ai-sdlc/07-operations/` | Service/Product Owner |

## 2. Quy tắc theo thao tác

- **Tạo (`create`):** kiểm tra đầu vào, sao chép một template, điền sự thật có nguồn, giữ phần chưa biết minh bạch, kiểm tra và bàn giao.
- **Cập nhật (`update`):** so sánh với bản cơ sở đã duyệt, giữ ID, tăng version, mở lifecycle mới, ghi tác động thay đổi, kiểm tra và bàn giao.
- **Review (`review`):** không sửa file; báo phát hiện `blocking`, `major`, `minor` kèm evidence.
- **Kiểm tra (`validate`):** chạy validator tất định, sau đó kiểm tra chất lượng nội dung và evidence.
- **Bàn giao (`handoff`):** tổng hợp danh tính artifact, nguồn, kiểm tra, câu hỏi, người duyệt và hành động tiếp theo.
- **Tiếp tục (`resume`):** đọc progress stage, thông báo checkpoint đang dở và chỉ tiếp tục sau khi người dùng quyết định.

## 3. Tác vụ nhiều giai đoạn và checkpoint

- Chia yêu cầu thành các giai đoạn theo thứ tự phụ thuộc; không xử lý song song khi đầu ra của giai đoạn trước là đầu vào bắt buộc của giai đoạn sau.
- Mỗi lần chỉ nạp reference và template của giai đoạn hiện tại.
- Trước khi chuyển giai đoạn, ghi checkpoint gồm thao tác/giai đoạn, `document_id@version`, status, bản cơ sở, nguồn đã duyệt, evidence, câu hỏi mở, cổng con người và bước tiếp theo.
- Nếu cổng bắt buộc chưa hoàn tất, dừng tại handoff; không giả định đầu vào đã được duyệt để tiếp tục.
- Khi quay lại tác vụ, khôi phục context từ artifact và checkpoint có thật; không tái tạo quyết định từ trí nhớ hội thoại nếu không có bằng chứng.

## 4. Metadata và lifecycle phiên bản

- JSON Schema quy định cấu trúc metadata; validator quy định lifecycle, tính duy nhất và quan hệ xuyên tài liệu.
- `document_id` đại diện cho một tài liệu logic và giữ ổn định qua các version.
- Cặp `(document_id, version)` là danh tính duy nhất của một artifact cụ thể.
- Worktree chỉ giữ một file hiện hành có tên ổn định cho mỗi `document_id`; version nằm trong metadata và baseline cũ nằm trong Git history.
- Version đầu tiên hoặc version mới đều bắt đầu bằng `status: draft` và `previous_status: null`.
- Khi tạo version thay thế, đặt `supersedes_version` bằng version cũ. Giá trị này phải nhỏ hơn version hiện tại và thuộc cùng `document_id`.
- Dùng `DOCUMENT-ID@x.y.z` trong `source_documents` và `related_documents` khi biết version; chỉ dùng ID trần khi nguồn bên ngoài không cung cấp version.
- Trước khi mở candidate mới, baseline approved hiện tại phải được commit. Tăng version một lần; mọi vòng sửa draft/review tiếp theo giữ nguyên version đó.
- Baseline lịch sử giữ trạng thái tại commit; version mới approved xác lập quan hệ thay thế qua `supersedes_version`, không sửa lịch sử.
- Baseline mới chỉ là đầu vào downstream khi human approval đã được commit. Skill không tự commit, push hoặc tạo tag.

Validator giải quyết `DOCUMENT-ID@version` trong worktree trước rồi Git history. Dự án legacy có nhiều file versioned phải dùng migration dry-run trước:

```powershell
python <skill-root>\scripts\migrate_artifact_storage.py docs/ai-sdlc
python <skill-root>\scripts\migrate_artifact_storage.py docs/ai-sdlc --apply
```

`--apply` yêu cầu safety commit và không tự commit/reset.
Sau apply, commit các file ổn định rồi chạy validator bình thường; chỉ khi đó baseline approved mới sẵn sàng cho downstream.

## 5. Danh mục template

| Bước | Artifact | Template |
|---:|---|---|
| 1 | Project Charter | `assets/templates/01-initiation/project-charter.md` |
| 1 | Project Management Plan | `assets/templates/01-initiation/project-management-plan.md` |
| 2 | SRS | `assets/templates/02-requirements/srs.md` |
| 2 | Requirements Traceability Matrix | `assets/templates/02-requirements/requirements-traceability-matrix.md` |
| 3 | HLD | `assets/templates/03-design/hld.md` |
| 3 | LLD | `assets/templates/03-design/lld.md` |
| 3 | ADR | `assets/templates/03-design/adr/0000-adr-template.md` |
| 3 | OpenAPI | `assets/templates/03-design/openapi-template.yaml` |
| 4 | Implementation Plan | `assets/templates/04-development/implementation-plan.md` |
| 4 | Implementation Report | `assets/templates/04-development/implementation-report.md` |
| 5 | Test Plan | `assets/templates/05-testing/test-plan.md` |
| 5 | Test Specification | `assets/templates/05-testing/test-specification.md` |
| 5 | Test Report | `assets/templates/05-testing/test-report.md` |
| 5 | UAT Report | `assets/templates/05-testing/uat-report.md` |
| 6 | Release Plan | `assets/templates/06-release/release-plan.md` |
| 6 | Deployment Runbook | `assets/templates/06-release/deployment-runbook.md` |
| 6 | Release Notes | `assets/templates/06-release/release-notes.md` |
| 7 | Operations Runbook | `assets/templates/07-operations/operations-runbook.md` |
| 7 | Incident Postmortem | `assets/templates/07-operations/incident-postmortem.md` |
| 7 | Maintenance Backlog | `assets/templates/07-operations/maintenance-backlog.md` |

OpenAPI là template bổ trợ và không tính vào 19 template Markdown.

Template tiến độ dùng chung:

- Stage: `assets/templates/progress/stage/_progress.md`.
- Toàn dự án: `assets/templates/progress/project/_progress.md`.

## 6. Quy ước ID

- Đặt phần lớn `document_id` theo dạng `<PREFIX>-<PROJECT>-<NNN>`, viết hoa và ổn định giữa các version; ví dụ `SRS-TASKFLOW-001`.
- Chỉ dùng hậu tố `TEMPLATE` trong template; thay bằng mã dự án khi tạo artifact.
- Dùng số thứ tự có ít nhất ba chữ số; ADR dùng bốn chữ số trong tên file `NNNN-short-decision-title.md`.
- Không tái sử dụng ID đã phát hành cho một tài liệu logic khác.

| Đối tượng | Prefix/mẫu ID |
|---|---|
| Project Charter / Project Management Plan | `PC-<PROJECT>-001` / `PMP-<PROJECT>-001` |
| SRS / Requirements Traceability Matrix | `SRS-<PROJECT>-001` / `RTM-<PROJECT>-001` |
| HLD / LLD / ADR | `HLD-<PROJECT>-001` / `LLD-<PROJECT>-001` / `ADR-0001` |
| Implementation Plan / Report | `IMPLPLAN-<PROJECT>-001` / `IMPLREPORT-<PROJECT>-001` |
| Test Plan / Specification / Report / UAT | `TESTPLAN-<PROJECT>-001` / `TESTSPEC-<PROJECT>-001` / `TESTREPORT-<PROJECT>-001` / `UAT-<PROJECT>-001` |
| Release Plan / Deployment Runbook / Release Notes | `RELEASEPLAN-<PROJECT>-001` / `DEPLOY-<PROJECT>-001` / `RELNOTES-<PROJECT>-001` |
| Operations / Incident / Maintenance | `OPS-<PROJECT>-001` / `INCIDENT-<PROJECT>-001` / `MAINT-<PROJECT>-001` |

| Đối tượng truy vết | Mẫu ID |
|---|---|
| Business Objective | `BO-001` |
| Functional Requirement | `FR-001` |
| Non-functional Requirement | `NFR-001` |
| Business Rule | `BR-001` |
| Component | `CMP-001` |
| API | `API-001` |
| Architecture Decision Record | `ADR-0001` |
| Work Item | `WI-001` |
| Test Case | `TC-001` |
| Release | `REL-001` |
| Risk | `RISK-001` |
| Incident | `INC-001` |
| Maintenance Item | `MAINT-001` |

## 7. Quy tắc trạng thái

Mỗi version đi theo chuỗi:

```text
draft → ai_checked → human_review → approved → superseded
```

- AI có thể đặt `draft` hoặc `ai_checked` sau khi kiểm tra thành công.
- Con người chủ động chuyển artifact sang review/phê duyệt và cung cấp metadata quyết định.
- Ghi quyết định `rejected` hoặc `conditional` trong kênh review/work item; không gắn artifact là `approved`.
- `previous_status` mô tả trạng thái ngay trước đó của cùng version, không phải trạng thái của version bị thay thế.
- `superseded` được giữ để đọc dự án legacy; workflow Git mới không sửa baseline đã commit sang trạng thái này.

## 8. Chuỗi phụ thuộc tối thiểu

| Đầu ra | Đầu vào đã duyệt bắt buộc |
|---|---|
| Project Management Plan | Project Charter |
| SRS/RTM | Project Charter hoặc quyết định sản phẩm rõ ràng |
| HLD | SRS baseline |
| LLD | HLD cùng requirement/ADR liên quan |
| Implementation Plan | SRS, HLD/LLD và ADR liên quan |
| Test Report/UAT | Requirement, build và Test Specification |
| Release Plan | Khuyến nghị kiểm thử đã duyệt và UAT khi bắt buộc |
| Operations Runbook | HLD, thiết kế triển khai và version đã phát hành |

## 9. Theo dõi và tiếp tục tiến độ

- Dùng [progress-tracking.md](progress-tracking.md) làm contract duy nhất cho `_progress.md`.
- Lưu progress toàn skill tại `docs/ai-sdlc/_progress.md`; lưu progress stage tại `docs/ai-sdlc/<stage>/_progress.md`.
- Chỉ dùng Markdown, checkbox và bảng; không dùng YAML, JSON, fingerprint hoặc phần trăm.
- Mỗi stage dùng sáu bước `inspect`, `verify_inputs`, `execute`, `validate`, `human_gate`, `handoff`.
- Đánh dấu `[x]` chỉ cho bước `completed` hoặc `skipped`; các trạng thái còn lại dùng `[ ]`.
- Cập nhật progress sau mỗi bước, trước khi chờ người dùng, trước human gate và trước handoff.
- Khi skill được gọi lại, đọc progress trước, báo tình trạng và chờ người dùng quyết định; không tự tiếp tục.
- `_progress.md` là nguồn xác định tiến độ ở phiên bản này. Nếu progress không được cập nhật sau thay đổi ngoài agent, skill không tự phát hiện.
