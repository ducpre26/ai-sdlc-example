# Điều phối native Codex agent theo stage và step

## 1. Nguồn cấu hình

- `references/agent-workflow.yaml` ánh xạ mỗi `stage.step` tới agent và danh sách companion skill bắt buộc.
- `<project-root>/.codex/agents/*.toml` chứa custom agent theo phạm vi dự án; `%USERPROFILE%/.codex/agents/*.toml` chứa custom agent cá nhân.
- Mỗi custom agent dùng schema native của Codex: `name`, `description`, `developer_instructions` và các khóa session được Codex hỗ trợ.
- File Markdown hoặc TOML nằm riêng trong skill không được Codex discovery như custom agent.
- `.ai-sdlc/config.yaml` có thể binding agent name tới agent công ty. Không tạo lớp role trung gian.
- `agents/openai.yaml` chỉ là metadata UI và invocation policy của skill, không phải định nghĩa subagent.

## 2. Ranh giới cấu trúc

- `skill/ai-first-sdlc/agents/openai.yaml` chỉ là UI metadata, invocation policy và dependency metadata của skill.
- Không đặt custom agent TOML trong `skill/ai-first-sdlc/agents/`; thư mục này không phải custom-agent discovery path.
- Không giữ bản sao custom agent trong `assets/`; `assets/` dành cho file dùng để tạo đầu ra như template và media.
- Repository tích hợp phải quản lý năm agent trực tiếp trong `.codex/agents/`. Việc phân phối hoặc đồng bộ agent giữa các repository là thao tác cấu hình riêng, không phải hành vi của skill.

## 3. Năm agent pilot

| Agent | Stage/step chính |
|---|---|
| `sdlc-orchestrator-agent` | inspect, handoff và các stage chưa có agent chuyên môn |
| `qa-agent` | Requirements verify/execute; Testing verify/execute |
| `qa-review-agent` | Requirements validate; Testing validate |
| `development-agent` | Development verify/execute |
| `code-review-agent` | Development validate |

`human_gate` luôn ánh xạ tới `human`; agent chỉ chuẩn bị và ghi nhận quyết định được cung cấp rõ.

## 4. Binding và fallback

1. Nếu `.ai-sdlc/config.yaml` có binding, Orchestrator giao cho target công ty và ghi execution identity thật.
2. Nếu thiếu binding, Orchestrator spawn custom agent đã được Codex discovery bằng `name` trong workflow.
3. Nếu không discovery được agent, đặt step thành `blocked` hoặc `awaiting_user`; không chạy prompt definition trong cùng execution để giả lập delegation.
4. `qa-agent` và `qa-review-agent` phải có target và execution identity khác nhau.
5. `development-agent` và `code-review-agent` phải có target và execution identity khác nhau.
6. Không fallback validation sang agent đã thực hiện execute.
7. Orchestrator phải kiểm tra mọi `required_skills` tồn tại trước khi delegation và ghi rõ `$skill-name` trong task giao agent; không chỉ dựa vào implicit skill matching.
8. Nếu thiếu skill bắt buộc hoặc agent không xác nhận đã nạp skill, trả `blocked`; không tái tạo nghiệp vụ từ trí nhớ.

## 5. Task/handoff packet

Packet tối thiểu:

```yaml
packet_version: 2
work_id: <ID>
stage: <stage-id>
step: <step-id>
agent_id: <native agent name>
execution_id: <runtime execution identity>
objective: <mục tiêu>
required_skills: []
skill_inputs:
  stage_contract: <path>
  artifact_templates: []
  metadata_schema: <path|null>
inputs: []
questions: []
decisions_received: []
actions_performed: []
outputs: []
evidence: []
skills_used: []
findings: []
blockers: []
human_decision_required: null
next_agent: <agent-name|human|null>
status: <completed|blocked|awaiting_user|awaiting_human>
```

- `questions` ghi người cần trả lời; `decisions_received` ghi nội dung, người cung cấp và nguồn.
- `required_skills` ghi skill ID bắt buộc; `skills_used` ghi skill agent đã thực sự nạp và áp dụng.
- `skill_inputs` chỉ tới stage contract, template, schema và baseline cần cho step; companion skill không tự tìm toàn bộ repository.
- `inputs` ghi artifact ID, version, path và Git commit khi có.
- Requirements findings liên kết `FR/NFR/BR`; Testing findings liên kết requirement và `TC`.
- Evidence chỉ ghi đường dẫn, command, log, build hoặc URL thực sự tồn tại.
- Orchestrator kiểm tra packet trước khi cập nhật progress.

Nếu thiếu skill bắt buộc, agent trả:

```yaml
status: blocked
blockers:
  - code: required_skill_unavailable
    skill_id: <skill-id>
```

## 6. Requirements do QA sở hữu

1. Orchestrator giao Project Charter, quyết định sản phẩm, artifact hiện hành và `$sdlc-requirements-engineering` cho QA Agent.
2. QA Agent tìm khoảng trống, trả câu hỏi có mục tiêu; không tự tạo câu trả lời nghiệp vụ.
3. Orchestrator lấy quyết định từ stakeholder và trả lại kèm nguồn.
4. QA Agent viết/cập nhật SRS và RTM; phần chưa xác minh nằm trong `open_questions`.
5. QA Review Agent dùng `$sdlc-requirements-review` bằng execution độc lập. Blocking finding quay lại QA Agent.
6. Product Owner phê duyệt tại human gate; Orchestrator handoff baseline đã commit sang Design.

## 7. Validation

Kiểm tra custom agent của dự án cùng workflow của skill:

```powershell
python <skill-root>\scripts\validate_agents.py <skill-root> [<project-root>\.ai-sdlc\config.yaml] <project-root>
```

Dùng `-` ở tham số config nếu dự án chưa có `.ai-sdlc/config.yaml`. Validator kiểm tra schema TOML native trong `<project-root>/.codex/agents/`, đủ năm agent, mười companion skill, workflow 7×6, required skill, human gate và binding độc lập.
