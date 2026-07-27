# Kiến trúc và thiết kế

## 1. Mục đích và phạm vi

Chuyển baseline Requirements thành kiến trúc, thiết kế chi tiết, quyết định và hợp đồng kỹ thuật có thể triển khai và kiểm chứng.

## 2. Điều kiện kích hoạt

- Tạo/cập nhật HLD, LLD, ADR, OpenAPI hoặc schema.
- Một thay đổi ảnh hưởng component boundary, data, security, quality attribute, integration hoặc compatibility.

## 3. Artifact đầu vào

- SRS và RTM approved/committed.
- Constraint, policy, platform baseline và hợp đồng hiện có.
- Decision, risk và open question được handoff từ Requirements.

## 4. Artifact đầu ra

| Artifact | Template |
|---|---|
| HLD | `assets/templates/03-design/hld.md` |
| LLD | `assets/templates/03-design/lld.md` |
| ADR | `assets/templates/03-design/adr/0000-adr-template.md` |
| OpenAPI | `assets/templates/03-design/openapi-template.yaml` |

## 5. Nguồn và evidence bắt buộc

- Mỗi decision/trade-off tham chiếu requirement, constraint, option và evidence có thật.
- OpenAPI/schema được kiểm tra bằng công cụ dự án khi có.
- Không ghi công nghệ, compatibility hoặc security decision là approved khi chưa có người có thẩm quyền quyết định.

## 6. Ánh xạ step, agent và skill

| Step | Agent | Companion skill |
|---|---|---|
| `inspect`, `handoff` | `sdlc-orchestrator-agent` | Không |
| `verify_inputs`, `execute`, `validate` | `sdlc-orchestrator-agent` | `sdlc-solution-design` |
| `human_gate` | `human` | Không |

## 7. Traceability contract

- Duy trì `FR/NFR/BR → CMP/API/ADR → WI/PR → TC`.
- Mỗi component/API/ADR chỉ tới requirement hoặc constraint liên quan.
- Contract version và consumer impact phải truy được khi thay đổi.

## 8. Điều kiện chặn

- Requirements baseline chưa approved/committed.
- Security/data/contract decision quan trọng chưa có owner.
- Breaking change thiếu impact, migration hoặc rollback.
- OpenAPI/schema không hợp lệ khi là đầu ra bắt buộc.

## 9. Human gate

Tech Lead, Architect hoặc contract owner phù hợp phê duyệt. AI không tự chấp nhận trade-off hoặc thay đổi hợp đồng.

## 10. Handoff contract

Bàn giao design baseline, `CMP/API/ADR`, contract, decision, risk, migration/compatibility requirement, approval identity và Git commit sang Development.

## 11. Ngoại lệ

Không bắt buộc mọi artifact cho mọi thay đổi; chọn HLD/LLD/ADR/OpenAPI theo tác động và ghi tailoring. Không bỏ decision hoặc contract cần thiết chỉ vì thay đổi nhỏ.
