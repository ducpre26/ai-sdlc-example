# Điều phối Claude Code subagent theo stage và step

## 1. Nguồn cấu hình

- `references/agent-workflow.yaml` ánh xạ mỗi `stage.step` tới agent và companion skill bắt buộc.
- `<project-root>/.claude/agents/*.md` chứa project subagent; `~/.claude/agents/*.md` chứa personal subagent.
- Mỗi subagent dùng YAML frontmatter native của Claude Code với `name`, `description`, `skills` khi cần, sau đó là system prompt Markdown.
- `<project-root>/.claude/skills/<skill-name>/SKILL.md` là skill theo phạm vi dự án; `~/.claude/skills/<skill-name>/SKILL.md` là skill cá nhân.
- `.ai-sdlc/config.yaml` có thể binding agent name tới agent công ty. Không tạo lớp role trung gian.

## 2. Ranh giới cấu trúc và execution

- Giữ Orchestrator trong main conversation để có thể giao và tổng hợp nhiều subagent. Không spawn `sdlc-orchestrator-agent` như một worker trung gian rồi yêu cầu nó tiếp tục spawn agent khác.
- Có thể khởi động Orchestrator như main session bằng `claude --agent sdlc-orchestrator-agent`; khi đó agent có thể dùng Agent tool theo tool allowlist.
- File trong `.claude/agents/` là định nghĩa chạy thật. Skill trong `.claude/skills/` được discovery trực tiếp và có thể gọi bằng `/skill-name` hoặc Skill tool.
- Companion skill được preload qua trường `skills` của agent chuyên môn. Task packet vẫn phải khai báo `required_skills`; agent phải trả `skills_used` để chứng minh skill đúng đã được áp dụng.
- Repository tích hợp phải quản lý năm agent trực tiếp trong `.claude/agents/`. Việc phân phối hoặc đồng bộ agent giữa repository là thao tác cấu hình riêng, không phải hành vi tự động của skill.

## 3. Năm agent pilot

| Agent | Stage/step chính |
|---|---|
| `sdlc-orchestrator-agent` | main session cho inspect, handoff và các stage chưa có agent chuyên môn |
| `qa-agent` | Requirements verify/execute; Testing verify/execute |
| `qa-review-agent` | Requirements validate; Testing validate |
| `development-agent` | Development verify/execute |
| `code-review-agent` | Development validate |

`human_gate` luôn ánh xạ tới `human`; agent chỉ chuẩn bị và ghi nhận quyết định được cung cấp rõ.

## 4. Binding và fallback

1. Nếu `.ai-sdlc/config.yaml` có binding, Orchestrator giao cho target công ty và ghi execution identity thật.
2. Nếu thiếu binding, Orchestrator dùng Agent tool với subagent đã được Claude Code discovery bằng `name` trong workflow.
3. Nếu agent không được discovery, đặt step thành `blocked` hoặc `awaiting_user`; không chạy nội dung agent definition trong main conversation để giả lập delegation.
4. `qa-agent` và `qa-review-agent` phải có target và execution identity khác nhau.
5. `development-agent` và `code-review-agent` phải có target và execution identity khác nhau.
6. Không fallback validation sang agent đã thực hiện execute.
7. Orchestrator kiểm tra mọi `required_skills` tồn tại trước delegation và ghi rõ skill cần áp dụng trong task packet. Agent chuyên môn phải có skill đó trong `skills` frontmatter hoặc invoke được bằng Skill tool.
8. Nếu thiếu skill bắt buộc hoặc agent không xác nhận `skills_used`, trả `blocked`; không tái tạo nghiệp vụ từ trí nhớ.

## 5. Task/handoff packet

Packet tối thiểu:

```yaml
packet_version: 2
work_id: <ID>
stage: <stage-id>
step: <step-id>
agent_id: <native agent name>
execution_id: <Claude Code agent execution identity>
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
- `required_skills` ghi skill ID bắt buộc; `skills_used` ghi skill đã được preload/invoke và thực sự áp dụng.
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

1. Orchestrator giao Project Charter, quyết định sản phẩm, artifact hiện hành và yêu cầu áp dụng `sdlc-requirements-engineering` cho QA Agent.
2. QA Agent tìm khoảng trống, trả câu hỏi có mục tiêu; không tự tạo câu trả lời nghiệp vụ.
3. Orchestrator lấy quyết định từ stakeholder và trả lại kèm nguồn.
4. QA Agent viết/cập nhật SRS và RTM; phần chưa xác minh nằm trong `open_questions`.
5. QA Review Agent áp dụng `sdlc-requirements-review` bằng execution độc lập. Blocking finding quay lại QA Agent.
6. Product Owner phê duyệt tại human gate; Orchestrator handoff baseline đã commit sang Design.

## 7. Validation

Kiểm tra project subagent cùng workflow và skill:

```bash
python "<skill-root>/scripts/validate_agents.py" "<skill-root>" ["<project-root>/.ai-sdlc/config.yaml"] "<project-root>"
```

Dùng `-` ở tham số config nếu dự án chưa có `.ai-sdlc/config.yaml`. Validator kiểm tra Markdown frontmatter native trong `<project-root>/.claude/agents/`, đủ năm agent, mười companion skill, preload skill đúng vai trò, workflow 7×6, human gate và separation of duties.
