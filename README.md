# Bộ tài liệu kỹ thuật AI-First SDLC

Bộ template kỹ thuật tinh gọn cho cá nhân và nhóm MVP. AI có thể tạo và tự kiểm tra tài liệu; con người chịu trách nhiệm phê duyệt.

Nội dung hướng dẫn và nhãn mô tả dùng tiếng Việt. Các thuật ngữ kỹ thuật thông dụng như SRS, HLD, LLD, ADR, NFR, OpenAPI, traceability, rollback và handoff được giữ bằng tiếng Anh. Machine key, ID, enum trạng thái và contract của schema không được dịch.

Hướng dẫn áp dụng vào repository và tạo ứng dụng: [Hướng dẫn sử dụng và tích hợp](huong-dan-su-dung-va-tich-hop.md).

## Chuẩn tham chiếu

- Project Management Plan: ISO/IEC/IEEE 16326:2019.
- Requirements/SRS: ISO/IEC/IEEE 29148:2018.
- Architecture Description: ISO/IEC/IEEE 42010:2022.
- ADR: MADR 4.0.
- Test Documentation: ISO/IEC/IEEE 29119-3:2021.
- Product Quality/NFR: ISO/IEC 25010:2023.

Các template chỉ áp dụng cấu trúc tinh gọn, không sao chép nguyên văn tiêu chuẩn có bản quyền.

## Cấu trúc

```text
ai-first-sdlc/
├── AGENTS.md                       Quy tắc phát triển repository
├── README.md                       Tổng quan bộ kit
├── ai-first-sdlc-process.md        Quy trình và approval flow
├── huong-dan-su-dung-va-tich-hop.md
├── .codex/agents/                  Năm custom agent cho Codex
├── skill/                          Nguồn chuẩn bản Codex
│   ├── ai-first-sdlc/
│   └── sdlc-*/
└── claude-version/                 Bản port độc lập cho Claude Code
    ├── README.md
    └── .claude/
        ├── agents/
        └── skills/
```

Repository duy trì hai distribution độc lập:

- **Codex:** nguồn tại `skill/` và `.codex/`.
- **Claude Code:** nguồn tại `claude-version/.claude/`.

Hai bản dùng chung mô hình SDLC, artifact contract, traceability và human gate, nhưng có cấu trúc discovery và agent configuration khác nhau. Xem [hướng dẫn bản Claude](claude-version/README.md).

`skill/ai-first-sdlc/` và `skill/sdlc-*/` là nguồn chuẩn của bản Codex. `claude-version/.claude/` là nguồn của bản port Claude Code. Bản đã cài vào user hoặc application repository chỉ là distribution và phải được cập nhật có chủ đích sau khi validation đạt.

## Quy trình trạng thái

```text
draft → ai_checked → human_review → approved → superseded
```

Trong workflow Git mới, baseline lịch sử giữ trạng thái tại commit và version mới dùng `supersedes_version` để chỉ quan hệ thay thế. `superseded` được giữ để tương thích dữ liệu cũ.

- AI chỉ được chuyển tài liệu đến `ai_checked`.
- `approved` bắt buộc có `human_decision: approved`, người duyệt và ngày duyệt.
- Nếu còn mâu thuẫn hoặc dữ liệu chặn, giữ `status: draft` và ghi vào `open_questions`.
- Tài liệu approved không được chứa `TBD`, `{placeholder}` hoặc câu hỏi mở.

## Nguồn dữ liệu chuẩn

- Công cụ quản lý công việc giữ backlog, work item, trạng thái và assignee.
- Git giữ Charter, Project Plan, SRS, HLD, LLD, ADR, test evidence và runbook.
- Worktree chỉ giữ một file tên ổn định cho mỗi `document_id`; Git history giữ các baseline cũ.
- Liên kết theo chuỗi: `BO → FR/NFR → CMP/API/ADR → WI/PR → TC → REL`.
- Không sao chép toàn bộ backlog vào Git; SRS chỉ giữ yêu cầu baseline và liên kết work item.

## Cách sử dụng

1. Bảo đảm dự án có Git; skill phải hỏi trước nếu cần chạy `git init`.
2. Sao chép template phù hợp từ `skill/ai-first-sdlc/assets/templates/` sang `docs/ai-sdlc/<stage>/` với tên file ổn định.
3. Thay metadata và placeholder; giữ nguyên các heading bắt buộc.
4. Workflow giao đúng agent cùng companion skill bắt buộc; Requirements/Testing dùng QA Agent, Development dùng Development Agent và validation dùng agent độc lập.
5. Chạy validator trước khi gửi con người duyệt.
6. Người duyệt cập nhật quyết định; commit baseline trước khi downstream sử dụng.

```powershell
python skill/ai-first-sdlc/scripts/validate_artifacts.py --no-git-history skill/ai-first-sdlc/assets/templates
python skill/ai-first-sdlc/scripts/validate_agents.py skill/ai-first-sdlc
```

Artifact validator kiểm tra YAML front matter, ID, lifecycle, Git baseline, liên kết và traceability. Agent validator kiểm tra năm custom agent, mười companion skill, workflow 7×6, required skill, human gate và separation of duties.

## Danh mục template

| Bước | Tài liệu |
|---|---|
| 1 | Project Charter, Project Management Plan |
| 2 | SRS, Requirements Traceability Matrix |
| 3 | HLD, LLD, ADR |
| 4 | Implementation Plan, Implementation Report |
| 5 | Test Plan, Test Specification, Test Report, UAT Report |
| 6 | Release Plan, Deployment Runbook, Release Notes |
| 7 | Operations Runbook, Incident/Postmortem, Maintenance Backlog |

## Quy ước ID

| Đối tượng | Mẫu ID |
|---|---|
| Business objective | `BO-001` |
| Functional requirement | `FR-001` |
| Non-functional requirement | `NFR-001` |
| Business rule | `BR-001` |
| Component | `CMP-001` |
| API | `API-001` |
| Work item | `WI-001` |
| Test case | `TC-001` |
| Release | `REL-001` |
| Risk | `RISK-001` |
