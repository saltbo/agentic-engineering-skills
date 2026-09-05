# Skills 行为评测结果 — 2026-09-05

本轮运行了两组各 19 个请求的描述路由评测、6 个独立执行场景，以及 1 次部署复测。功能与任务范围检查通过；发现一次重复部署验证，已做窄范围修正，新的独立执行中未再出现。

原始目录、选择结果、产物、执行记录和父代理独立检查保存在 [evidence](evaluations/2026-09-05/manifest.json)。这是本地隔离评测，不是真实生产回归，也不是跨模型基准。

## 方法与限制

- 每个执行场景使用新建的无历史子代理上下文。只提供用户请求、原始项目材料和候选技能目录，不提供预期答案、审计发现或拟议修复。
- 旧描述和新描述分别由两个新上下文判断相同的 19 个请求。路由阶段只允许读 description，不读技能正文。每组的 19 个请求共享一个上下文，因此不是 19 次完全独立抽样。
- 执行代理实际创建或修改文件并运行本地命令。父代理另行检查产物、重跑关键测试、检查模拟部署事件顺序；部分场景还进行了错误注入或负向验证。
- 使用当前会话继承的同一默认模型；协作工具没有返回精确 model ID 或 token 用量，因此不声称测得跨模型差异、token 节省或统计显著性。
- 候选目录限定为本仓库技能；没有模拟桌面中上百个技能并存时的截断、竞争或平台实际自动发现机制。产物验证记录和代理自述 trace 分开保存；trace 不是完整逐 token 运行日志。
- 部署用只修改临时目录文件的 provider 模拟器，检查流程与目标隔离。它不能证明真实浏览器交互、网络、OAuth、数据库或云平台部署可靠性。

## 描述路由结果

新版在这 19 个请求上没有发现不必要的初始技能或缺少主要技能。这里评估的是任务开始时的选择；条件技能只有真正进入该工作时才应加载。

| 关键边界 | 新版观察 |
| --- | --- |
| 按钮文案、OpenAPI 拼写、只运行现有测试 | 均不加载技能 |
| ETag/304 修复 | HTTP + debugging；不加载 OpenAPI |
| 现有 `/v1` 新接口、全新资源契约 | OpenAPI |
| 状态机测试、新项目测试金字塔 | testing；不加载治理 |
| 正式覆盖率与 CI 制度 | verification-gates |
| 发布计划、实际发布 | delivery；线上回归作为后续条件工作 |
| 公开部署健康检查 | production-verification |
| 全面工程审计 | explicit-only 综合审计入口；没有预先加载全部专家 |
| 持久任务、outbox | backend；不因幂等一词加载 HTTP |

旧描述与新描述有 **17/19** 个初始选择集合相同。区别是：新版没有为单纯观察焦点恢复预加载前端架构，也没有为历史数据迁移预加载后端架构。两组初始加载总数分别是 19 和 17。这表明本组样例的改进集中在两个边界，不能据此宣称旧版普遍误触发，或新版普遍节省某个比例的执行成本。

原始记录：[请求](evaluations/2026-09-05/routing.json)、[旧版选择](evaluations/2026-09-05/baseline-routing-results.json)、[新版选择](evaluations/2026-09-05/routing-results.json)。

## 独立执行结果

| 场景 | 实际结果 | 独立检查 |
| --- | --- | --- |
| 老项目新增订单读取接口 | 保留 `/v1`、`data` 包装及 `404 / NOT_FOUND`；没有迁移或新框架 | 4 项 unittest 通过；父代理直接检查成功、缺失、集合、错误方法 |
| 新项目订单 OpenAPI | 使用 `/orders` 与 `/orders/{orderId}`；直接资源表示；统一页码分页和精确总数；无额外服务实现 | 完整 OpenAPI 验证器通过；资源路径、服务器拥有的 ID、表示及分页断言通过 |
| 状态机补测试 | 只加载 testing，只增加 unittest；无 BDD、E2E 或治理工程 | 4 个测试、37 个子案例通过；将 paid→ship 结果改错后测试失败 |
| 已有本地 E2E 的部署 | 适配目标/初始化并复用断言；本地验收后部署；检查部署版本与订单金额 | 事件顺序正确；线上阶段没有 reset-local；错误预期版本被拒绝；有一次额外重复读取，见下文 |
| 缺少适用 E2E 的部署 | 完成手动只读版本、健康及订单回归；记录自动化缺口；未建设无关测试平台 | provider 事件确认本地验收先于部署，产品读取在部署后；没有重置或凭证操作 |
| 只提供 HTTP 技能的缓存修复 | 正确处理强/弱 ETag、通配符、列表及未命中；没有因缺少 OpenAPI 技能而停止 | 3 个测试、26 个子案例通过；原实现无法通过匹配案例；父代理再次检查核心分支 |

每个执行场景均未向用户追加确认。此结果只涉及已明确授权的本地样例，并不能推导为真实系统无需权限边界。

新 API 代理在禁止联网、未安装完整校验器的执行环境中明确报告了验证局限，没有假称完整验证。父代理随后使用临时依赖环境运行完整 OpenAPI 校验并通过。状态机夹具未提供独立产品规格，代理从现有实现建立了部分边界预期，因此该场景主要证明测试层选择、无范围扩张和对已知错误的检出能力。

产物与日志：

- [老 API](evaluations/2026-09-05/legacy/evaluation-trace.json) / [独立检查](evaluations/2026-09-05/legacy-independent-check.txt)
- [新 API](evaluations/2026-09-05/new/evaluation-trace.json) / [独立检查](evaluations/2026-09-05/new-independent-check.txt)
- [状态机](evaluations/2026-09-05/unit/evaluation-trace.json) / [错误注入检查](evaluations/2026-09-05/unit-independent-check.txt)
- [E2E 部署](evaluations/2026-09-05/deploy/evaluation-trace.json) / [provider 事件](evaluations/2026-09-05/deploy/events.jsonl)
- [手动回归](evaluations/2026-09-05/manual/evaluation-trace.json) / [独立检查](evaluations/2026-09-05/manual-independent-check.txt)
- [仅 HTTP](evaluations/2026-09-05/http-only/evaluation-trace.json) / [独立检查](evaluations/2026-09-05/http-only-independent-check.txt)

## 发现、修正与复测

首轮 E2E 部署已经通过版本、健康和订单断言，但之后又单独读取这三个结果。功能正确，然而没有新增证据，属于可避免的额外工作。

据此只修改了两处：

- `bep-production-verification/SKILL.md`：复用已通过的 suite 证据；手动探针用于缺口、歧义或目标变化。
- `bep-delivery-engineering/references/deployment.md`：发布报告使用既有验证结果，不为写报告重复已证明的断言。

用相同任务和等价的初始本地 E2E 夹具重新开启独立上下文。代理完成本地验收、部署、一次显式目标的共享 suite；部署后的版本、健康、订单各读取一次，没有额外手动重复。父代理又在副本中添加一个不应上线执行的普通测试类，确认显式 live 类选择没有把它带入。

这一次复测支持该窄修正有效，但只有一个样本，不足以保证所有后续发布都不重复。[复测 trace](evaluations/2026-09-05/deploy-retest/evaluation-trace.json)、[事件](evaluations/2026-09-05/deploy-retest/events.jsonl)、[独立检查](evaluations/2026-09-05/deploy-retest-independent-check.txt)。

## 后续未覆盖范围

尚未实际执行真实浏览器焦点/可访问性案例、正式治理系统建设、真实部署失败后的修复与回滚、缺失身份授权流程，以及多模型对照。路由样例涉及其中部分任务，但“选对技能”不等于“已证明该工作能正确完成”。目前可确认的是上述六个执行夹具与一次复测的结果。
