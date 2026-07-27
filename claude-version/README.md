# AI-first SDLC cho Claude Code

Đây là bản port độc lập dành cho Claude Code. Bản này không thay đổi hoặc ghi đè nguồn Codex tại `../skill/` và `../.codex/`.

## Cấu trúc

```text
claude-version/
└── .claude/
    ├── agents/                 # 5 Claude Code subagent Markdown
    └── skills/
        ├── ai-first-sdlc/      # Skill điều phối, reference, template và validator
        └── sdlc-*/             # 10 companion skill
```

Cấu trúc này theo discovery path chính thức của Claude Code:

- Project skill: `.claude/skills/<skill-name>/SKILL.md`
- Project subagent: `.claude/agents/<agent-name>.md`
- Personal skill/subagent: `~/.claude/skills/` và `~/.claude/agents/`

Tài liệu tham khảo:

- [Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent Skills authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## Cài cho một project

Sao chép nội dung `claude-version/.claude/` vào `<project-root>/.claude/`. Không sao chép đè file cùng tên nếu project đã có cấu hình Claude riêng; merge có chủ đích.

Sau khi tạo `.claude/skills/` hoặc `.claude/agents/` lần đầu trong một phiên Claude Code đang mở, khởi động lại phiên để watcher nhận thư mục mới.

Kiểm tra bản đã cài:

```bash
python ".claude/skills/ai-first-sdlc/scripts/validate_agents.py" ".claude/skills/ai-first-sdlc" - "."
python -m unittest discover -s ".claude/skills/ai-first-sdlc/scripts" -p "test_*.py"
```

## Cài dùng cá nhân

Sao chép từng thư mục trong `.claude/skills/` sang `~/.claude/skills/` và từng file trong `.claude/agents/` sang `~/.claude/agents/`. Không lồng companion skill bên trong `ai-first-sdlc`.

Khi project không có `.claude/agents/`, validator tự fallback sang `~/.claude/agents/` để kiểm tra personal installation.

## Chạy

Cách mặc định, từ project đã cài bản port:

```text
/ai-first-sdlc tạo bộ requirement cho dự án này
```

Claude cũng có thể tự invoke skill khi yêu cầu khớp `description`.

Để dùng Orchestrator làm main session agent:

```bash
claude --agent sdlc-orchestrator-agent
```

Không spawn `sdlc-orchestrator-agent` như worker trung gian. Orchestrator cần ở main conversation để giao `qa-agent`, `qa-review-agent`, `development-agent` và `code-review-agent`, rồi tổng hợp handoff packet và human gate.

## Khác biệt chủ yếu so với bản Codex

| Thành phần | Codex | Claude Code |
|---|---|---|
| Skill project | nguồn `skill/*`, cài theo Codex discovery | `.claude/skills/*` |
| Agent | `.codex/agents/*.toml` | `.claude/agents/*.md` |
| Agent prompt | `developer_instructions` trong TOML | Markdown body sau YAML frontmatter |
| Gắn companion skill | task ghi `$skill-name` | preload qua `skills` và xác nhận trong task packet |
| Review read-only | `sandbox_mode = "read-only"` | `permissionMode: plan` |
| Orchestrator | custom Codex agent | main Claude session hoặc `claude --agent sdlc-orchestrator-agent` |

Artifact contract, 7 stage, 6 step, traceability, evidence, progress và human gate được giữ nguyên.
