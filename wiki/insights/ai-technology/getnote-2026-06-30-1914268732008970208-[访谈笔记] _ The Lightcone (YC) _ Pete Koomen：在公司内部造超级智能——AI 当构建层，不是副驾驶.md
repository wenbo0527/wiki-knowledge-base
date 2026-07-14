# [访谈笔记] | The Lightcone (YC) | Pete Koomen：在公司内部造超级智能——AI 当构建层，不是副驾驶

> 来源: Get 笔记
> 知识库: ai-technology
> 原始 ID: 1914268732008970208
> 创建时间: 2026-06-30 14:41:24
> 同步时间: 2026-07-14T14:03:53.085765

## 基本信息
- **节目**：The Lightcone（Y Combinator 出品播客）
- **嘉宾**：Pete Koomen（YC 合伙人，Optimizely 联合创始人；YC 内部 AI agent 基础设施负责人）
- **主持人**：Gary Tan（YC CEO）
- **时长**：约 46 分钟
- **日期**：2026-05-27
- **链接**：https://www.youtube.com/watch?v=B246K_G7mHU

---

## 一句话判断
> 这是目前最具体的一份「组织级 AI 怎么落地」的实战拆解——不是讲愿景，而是 YC 自己花一年多、从财务团队的一个痛点起步，一步步搭出「统一数据库 + 350 个共享工具 + 夜间自优化技能循环」的内部超级智能。对任何想在公司内部把 AI 从「副驾驶」升级成「操作系统」的人，这期是可抄作业级别的。Pete 的核心暴论：拖垮大多数公司 AI 落地的不是技术，是「安全主义」和层级文化。

---

## 人物侧写
### Pete Koomen
**身份**：YC 合伙人、Optimizely 联合创始人；过去一年多带队搭建 YC 内部 agent 基础设施；爆款文章《Horseless Carriages（无马马车）》作者。

**行为证据**（这次访谈暴露的）：
- 他**亲自下场写代码做内部工具**，不是纯管理者——用 Cursor/Claude Code 获得的个人生产力跃升，与 YC 内部传统研发的低效形成强烈反差，直接催生了这个项目。
- 他和团队的关键一步是**「悄悄」给 agent 开放生产 PostgreSQL 数据库只读权限**（Jared 干的），突破了最初设的窄域工具限制——结果效果炸裂。他由此总结：「过度担心安全和隐私，正是此前同类项目失败的核心原因。」这是一个用「先放开、再管控」打法的人。
- 他的产品哲学反潮流：写《无马马车》直接开炮「在传统软件里塞一小块 AI（如 Gmail 的 AI 写邮件）是错的」，主张反过来——**用 agent 去封装确定性工具**，把控制权还给用户。

---

## 核心观点

### 1. 别把 AI 当副驾驶，要当「构建层」
2023–24 流行的 copilot 思路已过时。正确做法是把 AI 作为所有业务系统的底层构建层，并**记录一切产物**（会议录音、工作产出）持续喂给 agent 优化。终极形态是「共享组织脑（shared organizational brain）」——最接近「把大家的大脑连起来」。

### 2. 一个数据库统治一切：为 agent 做数据去规范化
YC 自建所有系统，全部业务数据在**单一 PostgreSQL**里（被投公司、创始人、财务、CRM 笔记全在一起）。给 agent 开只读 SQL 权限后，原本数据团队要几小时写的查询变成自然语言一问即得，提问量和复杂度暴增。进一步参考 Google Bigtable 思路，把数据**去规范化**成适配 agent 检索的统一 schema（内部叫 GBrain，内置 RAG/图 RAG/RRF 重排）。关键经验：**agent 对 CLI 的适配优于单纯封装 MCP**。

### 3. 从「单人模式」到「多人模式」：工具注册表是核心
当前 Claude Code/OpenClaw 等还停留在「单用户单机」的单人模式，行业缺「多人模式」组织级方案。YC 的解法是**全员共建的工具注册表**：从 20 个工具增长到 **350+**，各团队自主添加，覆盖所有业务场景，对内部 agent 和员工本地 Claude Code 同时开放。配套 **Resolver 元技能 + "check resolvable"** 校验，强制所有技能符合 **DRY（不重复）+ MECE（不重叠、全覆盖）**，避免冗余技能堆积。

### 4. 自进化「梦循环」：技能会一夜变聪明
技能演进路径：手写 prompt → 手写自定义技能 → agent 自动生成/优化技能。YC 部署了一个**夜间通用 agent**，每晚读全员对话记录，自动找出可优化步骤和缺失上下文。典型案例：YC 的「两句话公司描述」技能，用春季批创始人办公会的反馈录音转写去优化后，**生成质量已超过 Pete 本人手写水平**。

### 5. 文化是前提：平等 + 默认信任
真正千倍级的超级智能组织必须具备两个特质：**全员平等 + 默认信任**。YC 默认所有 agent 对话对全职员工公开、自动同步到 Slack——新人靠围观同事用法快速上手，高信任环境下用社会监督替代严苛管控。这类文化在小创业公司天然，传统层级大公司很难具备。

### 6. 时间窗口红利 + 两条未来路径
**成本曲线**：现在每年 agent token 投入约 10 万–100 万美元，1 年后降到 1 万，2 年后只需几百美元——现在布局等于「穿越到 2028 年的生产力」。**未来分叉**：集中式（少数巨头垄断算力、锁死用户 prompt 权限 → 回到 1984 主机时代的反乌托邦）vs 分布式个人 AI（现在是「Apple 1 时刻」，十亿用户掌控自己的 AI、自选开源模型、私有数据自主）。Pete 旗帜鲜明站分布式：AI 是赋能人，不是替代人。

---

## 关键引言
> "How do you build super intelligence inside a company? Part of the key thing is not to just use AI as a copilot... you use it as the building layer for everything." ——Pete Koomen

> "It's like a shared organizational brain. It's the closest thing to us being able to connect our brains." ——Pete Koomen

> "The thing that was hampering the world was being worried about security and privacy... when you worry a bit less, these things are unbelievably powerful." ——Pete Koomen

> "We are at the Apple 1 moment right now. We are coming up with the primitives." ——Pete Koomen

> "Truly agentic 1000x super intelligent organizations have to be relatively egalitarian and trust by default—neither of those traits are common in most organizations." ——Pete Koomen

> "Chat is actually pretty good because it's the closest thing to human language, and human language is basically the closest thing to expression of thinking." ——Pete Koomen

> "The best AI software I've used tends to be very small—add the smallest amount of code ahead of time you need in order to let the model shine." ——Pete Koomen

---

## 信息增量
1. **YC 全部业务跑在单一自建 PostgreSQL 上**：被投公司/创始人/财务/CRM 笔记全在一个库，这是它能直接给 agent 开 SQL 权限的前提——大多数公司数据散在第三方 SaaS，这是结构性差距。
2. **工具注册表从 20 → 350+**：一年多内由各团队自主添加，不是工程团队集中开发，是「全员共建」模式。
3. **"check resolvable" 元技能**：用麦肯锡的 DRY + MECE 标准自动校验技能库，防止出现 10 个功能重叠的冗余技能——这是技能治理的具体机制。
4. **夜间自优化 agent（"梦循环"）**：每晚读全员对话自动优化，OpenClaw/GBrain/Codex 的 goal 类功能都内置同类原语。
5. **「两句话描述」技能超越人类**：用创始人办公会反馈录音转写来迭代技能，最终生成质量超过 Pete 本人——一个「经验沉淀成可迭代技能」的可复制样本。
6. **GBrain 重构数据点**：Gary 原本用 Rails 写了 50 万行代码的「Gary's list」，重构为开源 GBrain 后**仅 1 万行 TypeScript + 2000 行 markdown** 实现全部功能（含检索/语音提取/事实核查）。这是「即时软件 / just-in-time software」的极端案例。
7. **成本下降时间表**：token 年投入 10 万–100 万美元 → 1 年后 1 万 → 2 年后几百美元。这是判断「现在该不该 all-in」的量化锚点。
8. **新人上手周期被压缩**：YC 新人原本要 6 个月完全上手，agent 系统让新人直接复刻资深合伙人经验、放心问基础问题，不占老员工时间。
9. **agent 偏好 CLI > MCP**：把数据/工具整理成 CLI 友好格式比单纯封装 MCP 接口效果更强——给做 agent 工具链的人的反直觉经验。
10. **Pi 自引用编码 agent**：开源编码 agent Pi 能用自身代码修改扩展自身。极简设计（尽量少写前置代码、把空间留给模型）是当前最好 AI 软件的共性。

---

## 行动触发
- **给 Get笔记/得到的直接启发**：组织级 AI 的第一步不是买工具，是「**把数据收口到一个 agent 能直接查的统一层**」。如果数据散在多个 SaaS，先做去规范化的统一 schema，这比接十个 MCP 更值。
- **技能治理可抄**：建技能/工具注册表时，引入 DRY+MECE 校验机制（"check resolvable" 思路），防止技能库膨胀成一堆重叠冗余——这点对 AI 学习圈做内部工具沉淀尤其实用。
- **「梦循环」可落地**：部署一个夜间 agent 读团队对话记录、自动找可优化点和缺失上下文——把团队的真实使用沉淀成更好的技能，是低成本的自进化飞轮。
- **文化判断**：如果想在组织内推 AI，先评估「平等 + 默认信任」这两条文化前提是否具备。缺这两条，技术再好也推不动——这是 Pete 给的最硬的非技术判断。
- **叙事素材**：「把 AI 当构建层而非副驾驶」「Apple 1 时刻」「现在布局=穿越到 2028 的生产力」「无马马车」——高密度判断点，可直接用于对外输出。
