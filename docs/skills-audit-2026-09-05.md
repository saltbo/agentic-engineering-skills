# BEP skills 仓库审计

本文保留优化前的审计快照，文件行号与问题状态对应审计时版本。后续已按用户补充要求实施优化；当前行为见 [README](../README.md)，回归场景见 [行为评测](skill-behavior-evaluation.md)。

日期：2026-09-05。范围：11 个 SKILL.md、11 个 agents/openai.yaml、参考文档的路由与约束、唯一的 Python 脚本、README。正文和关键参考做了细读，其余 OpenAPI 参考按目录、强制规则及重复内容定向检查；这不是逐条 HTTP 标准合规认证。本轮只新增审计报告，没有修改技能规则。

依据：[Eric Provencher — Rethinking skills and prompts for GPT-6 Astra](https://x.com/pvncher/status/2095991462416490862)。X 直连返回 403，通过 [FxTwitter 公开接口](https://api.fxtwitter.com/pvncher/status/2095991462416490862) 获取文章正文；文章 ID 为 2095989703967125509。未把图片中未读取的文字作为证据。

文章给出的审计方向是：缩短且明确触发描述；按任务渐进加载；减少僵硬步骤；重新检查停工边界和完成条件。关于模型行为的说法属于作者的观察，不能替代本仓库的行为评测。以下是将这些方向用于本仓库后的独立判断。

## 结论

保留现有 11 个技能的主要边界。此前拆分有价值，特别是调试、交付和审查入口已经很小。优先优化规则的适用条件与所有权，再缩短上下文；不需要把技能合回一个工程手册，也不需要为了减少行数删除真实工程偏好。

主要问题是：窄入口仍会读入大参考；技能之间会重新引入门禁；BEP 的严格工程配置和通用任务指导混合；部分停工规则把局部信息缺失放大为整个任务不能完成。

## 可复核发现

### P1：路径检查器的文件模式不可用

位置：`skills/bep-best-openapi-design/scripts/check_resource_paths.py`，`parse_args()`。

有效文件只有 `/orders` 一行时，运行 `python3 .../check_resource_paths.py --file <file>` 返回 2，提示 `provide at least one API path`。选择 `--file` 后，位置参数 `paths` 是空列表，后续检查仍把它判为错误。

建议：仅在未提供 `--file` 时检查位置参数是否为空。增加有效文件、空文件、注释文件和非法路径的行为测试。这个脚本是确定性执行资源，修复价值高于继续增加提示词。

### P1：可选 API 风格被脚本升级为无条件失败

位置：`skills/bep-best-openapi-design/SKILL.md:88`、`:248`；路径检查器 `PATH_VERSION_SEGMENT` 和 `FORBIDDEN_VERSION_QUERY_KEYS`。

正文把版本策略放在“没有兼容既有约定时”的 baseline profile 下，要求保留既有公共契约；脚本无条件拒绝 `/v1/orders`，实测返回 1。脚本也把命名风格和显式动作检查合并，调用者无法选择适用 profile。

建议：分开严格资源规则与项目风格校验，显式传入已选择的 profile；在现有版本化 API 上不能因脚本默认值自动开启迁移。报告必须区分 BEP 风格不符与真实契约错误。继续保留“词表检查不能证明资源成立”的能力限制说明。

### P1：HTTP 技能的软依赖会制造硬阻塞

位置：`skills/bep-http-engineering/SKILL.md:62`。

只要涉及 REST 路由，就引导加载 OpenAPI 技能；未安装时要求资源建模门禁保持未满足。对于只修缓存头或条件请求、完全不改变资源建模的任务，这个依赖并不必要。

建议：只有实际设计或改变资源模型时才路由到 OpenAPI；技能不存在时继续完成独立的 HTTP 工作，说明未执行专门资源审计。若用户明确要求严格 BEP 资源审计，再将缺少所需资料标记为该审计的限制。

### P1：常规测试任务可能被扩展为 BDD 和治理建设

位置：`skills/bep-software-testing/SKILL.md:168`、`:226`；`skills/bep-best-engineering-practice/references/core.md:32`、`:155`。

测试入口承诺仅在需要时加载治理技能，后文却要求变更行为先更新规格、维护追踪映射，并用 completion gate 拒绝缺少规格的实现。综合审计核心又直接要求 `.feature` 和 90% 覆盖率。

建议：普通测试保留“最便宜且能完整证明行为的层级”。BDD、证明 ID、覆盖率门槛只用于已经采用或本次明确要求建设该治理体系的项目。把严格配置放到一个有清晰启用条件的参考中；不要让审计技能的加载本身成为项目采纳整套制度的证据。

### P1：前端完整 Unit 矩阵与最便宜充分验证原则冲突

位置：`skills/bep-frontend-engineering/references/verification.md:83`；`skills/bep-software-testing/SKILL.md:28`。

前端 profile 要求每个 inventory pair 都有 Unit 证明，真实浏览器证明不能替代它。焦点、浏览器认证连续性等本来需要真实浏览器的行为，会有被要求补一套不足以证明它的 Unit 矩阵的风险。

建议：按行为选择权威证明层。模拟 DOM 能证明的状态逻辑放 Unit；真实浏览器独有语义由浏览器测试证明；高层验证仅在集成风险需要时补充。保持严格 profile 的覆盖完整性，但不强制所有 pair 归入同一层。

### P2：触发描述和参考路由仍然过宽

OpenAPI description 为 835 个字符，其他技能为 238–301 个字符；总计 3,486 个字符。这是字符统计，不是 tokenizer 测量。当前会话的技能目录已经出现长描述截断，OpenAPI 的大量尾部条款不能可靠承担触发职责。

`bep-best-openapi-design/SKILL.md:3` 把鉴权、重试、并发、版本、框架设施等全部列入触发条件，与 HTTP、交付、后端重叠。正文还有 343 行、六步流程和 12 项固定报告格式。

前后端入口仅 25/24 行，但分别路由到 335/435 行架构文件。修复一个状态所有权问题仍会读入鉴权、离线、持久化、性能等整套要求。

建议：description 只回答“什么时候该选我”；不放执行规则。大参考按实际决策边界拆分，并在入口明确读取条件。不要只把全文搬到一个 `references/full.md`；那不减少任务的加载量。

### P2：已限定的严格治理与普通架构仍有渗漏

位置：`skills/bep-frontend-engineering/references/architecture.md:85`；前后端 verification 开头；`skills/bep-verification-gates/SKILL.md:153`。

治理技能自身已明确不适用于普通测试，应保留这一进步。但前端架构直接要求阻塞 CI，运行时 verification 开头又覆盖广泛日常变更；之后再要求生产清单、适配器、原生报告核对和强制覆盖率，绕过了入口的窄边界。

建议：普通架构输出局部结构和行为证明；正式治理配置由项目采纳的 policy 决定。90%/100%、零重试、无前端例外等可以作为 BEP strict profile 保留，不能伪装成适用于所有项目的普遍正确性要求。治理实现阶段才需要清单来源、证明适配器及报告协议。

### P2：停工和交付规则需要区分任务模式

位置：OpenAPI 主文档的 resource/group/pagination gates 与 `:336`；调试技能 `:8`；综合审计 core `:197`。

只读审计本身保持只读是正确的，本次也应如此。问题在于：缺少分页选择可能中断全部工作；调试措辞可能把“修复这个问题”误读为还要另行授权；综合审计会因缺少两名独立审查上下文留下硬门禁，即使仓库没有该治理要求。

建议：阻塞仅针对依赖缺失决策的部分，继续准备独立且可审查的结果。明确用户已经提出 fix/implement 时包含局部实现与受影响验证；诊断-only 请求仍不改实现。独立审查按项目要求和可用授权执行，不因加载通用审计技能自动新设发布门禁。

## 逐个技能的优化方案

| 技能 | 当前入口行数 | 优先级 | 建议 |
| --- | ---: | --- | --- |
| bep-best-openapi-design | 343 | P1 | 缩短 description；保留资源优先偏好；拆资源建模、BEP 契约配置、兼容演进和框架实现路由；修脚本；按变更范围输出 |
| bep-http-engineering | 148 | P1 | 删除缺少可选技能即未通过的门禁；按读取/缓存、写入/并发、信任边界、追踪分别路由 |
| bep-software-testing | 241 | P1 | 保留证明层选择、真实边界和确定性；移出 BDD 治理；E2E 配置和证据要求按需读 |
| bep-verification-gates | 274 | P1 | 入口只做治理范围选择；拆 profile、生产清单、runner adapter、报告核对和 CI；明确严格配置的采纳条件 |
| bep-frontend-engineering | 24 | P1 | 重点改参考而非入口；拆状态/数据流、组件/可访问性、安全/存储、性能；修正全量 Unit 证明要求 |
| bep-backend-engineering | 25 | P2 | 保留依赖方向和真实边界判断；拆 ownership、transactions、messaging、lifecycle；验证参考只在需要时加载 |
| bep-best-engineering-practice | 30 | P2 | 保留 explicit-only；core 改成跨领域检查索引；删与专门技能重复的调试/交付步骤；不因审计自动采纳 BDD 与门禁 |
| bep-production-verification | 164 | P2 | 保留目标、身份、副作用、清理和证据边界；拆设计/执行/发布集成；匿名检查不应要求无关凭证 |
| bep-software-debugging | 28 | P2 | 保持短小；明确诊断-only 与已授权修复；允许最小受控探针，不把固定顺序当作唯一有效方法 |
| bep-delivery-engineering | 29 | P3 | 基本保留；缩描述；仅报告本次相关的迁移、版本和风险，不机械填齐所有项目 |
| bep-engineering-review | 36 | P3 | 基本保留；缩描述；保持真实发现优先、范围与严重度分开、不自动变更 |

入口合计 1,442 行，参考 3,102 行，共 4,544 行。行数只用于定位加载热点，不作为质量门槛。

## 建议的 description 草稿

以下是优化方向，不是本轮已经应用的变更；保留全部现有技能名和 invocation policy。

```yaml
# bep-best-openapi-design
description: Design or review resource-oriented REST/OpenAPI contracts. Use when resource models, routes, or representations change.
# bep-http-engineering
description: Design or fix HTTP lifecycle behavior, especially caching, retries, conditional writes, and trust boundaries.
# bep-software-testing
description: Design, implement, or review automated tests and choose their proof layer. Not needed just to run existing tests.
# bep-verification-gates
description: Build or audit formal test inventories, coverage policy, and blocking CI gates. Not for ordinary test changes.
# bep-frontend-engineering
description: Design or restructure frontend ownership, state, effects, and browser boundaries. Not for small visual edits.
# bep-backend-engineering
description: Design or restructure backend ownership, dependencies, transactions, messaging, and service lifecycle.
# bep-best-engineering-practice
description: Perform an explicitly requested comprehensive engineering-practice audit across relevant disciplines.
# bep-production-verification
description: Design or run bounded verification against a deployed environment, with explicit target and side-effect scope.
# bep-software-debugging
description: Diagnose or fix a reported defect, regression, intermittent failure, or performance change.
# bep-delivery-engineering
description: Plan or implement supported-contract changes, data migrations, releases, and rollback or roll-forward.
# bep-engineering-review
description: Review a concrete software change for outcome correctness, engineering risk, and supported-contract impact.
```

描述缩短后需要检查真实选择表现，不能仅凭字符减少判定优化成功。

## 应保留的内容

- 资源建模优先、领域归属、兼容性约束，以及“路径名是名词并不能证明它是资源”。严格动作路径禁令可保留为明确的 BEP 设计偏好。
- Unit 不证明被 mock 的外部边界，集成证明要运行真实语义；最便宜且充分的验证层；从真实缺陷形成回归证据。
- 已发布契约与未发布内部实现的区别，以及临时兼容路径的删除条件。
- 生产检查的明确目标、预期版本、已授权身份和副作用范围、清理、敏感证据处理。
- 用户明确规定的主页面不嵌创建/编辑/配置表单；它属于真实个人偏好，不应以“模型已经懂设计”为由删除。
- 综合审计的 explicit-only。无需把全部专家技能改成手动调用。

## 实施次序与验收

第一批：修复脚本两个已验证问题；缩短 description；去掉 HTTP 的不必要技能阻塞；限定 BDD/strict profile 的适用条件。保持现有命名和安装方式。

第二批：按工作模式拆分 OpenAPI、测试、治理和前后端大参考，删除重复规则和复述式 completion gate。每个要求只有一个权威定义；交叉引用说明何时需要，不自动串联全部技能。

第三批：建立小型行为评测集，比较旧版、新版及必要时无 skill 基线。记录使用模型与版本；若仓库继续支持多种模型，再跨模型比较。观察选择的技能、读取文件、任务结果、额外改动、不必要询问、实际验证和上下文消耗。不要把固定文件行数、固定措辞或一次模型运行当作质量证明。

| 真实请求样例 | 应观察的结果 |
| --- | --- |
| 修改一个按钮文案 | 不加载整套架构/治理，不生成测试制度 |
| 修复组件状态同步问题 | 定位状态所有权并验证行为，不建设生产清单 |
| 给现有 API 修 ETag/304 | 处理缓存语义，不要求完整资源重建 |
| 给既有 `/v1/orders` 补字段文档 | 保留支持中的 URI，不擅自启动版本迁移 |
| 为状态机补边界测试 | 使用现有框架，不强制创建 `.feature` |
| 修复分页跳行 | 复现并修复，检查排序/游标，不另问是否可以修 |
| 只诊断间歇故障 | 输出证据与不确定性，不改产品实现 |
| 新设计订单取消 API | 应用资源建模偏好；说明缺失决策，只暂停依赖部分 |
| 为项目引入 BEP 严格验证制度 | 完整使用所选 profile、真实分母和原生执行报告 |
| 检查公开生产健康端点 | 明确目标和成功标准，不要求无关登录或写入 |
| 只安装 HTTP 技能后修请求超时 | 不因缺失 OpenAPI 技能而阻塞独立工作 |
| 审查鉴权改动 | 保持审查范围，真实 findings 优先；不自动部署或新建制度 |

本轮已执行：工作树初始状态检查；11 个 description 字符数与入口/参考行数统计；Markdown 本地链接存在性检查（未发现缺失）；脚本四个实际运行案例（合法路径通过、动作路径拒绝、版本路径拒绝、文件模式错误退出）。仓库文件清单未见专门的 skill 行为评测集。

未执行：跨模型 A/B、完整前向任务评测、安装流程实测、联网生产验证。因此“误触发、扩大任务或过早停止”是由可定位规则支持的行为风险，尚不能声称已测出具体发生率或 token 节省比例。
