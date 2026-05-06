# 盯人日报 #064 | 2026-05-05

> 来源: Get笔记-高质量人类谈话库
> 导入日期: 2026-05-05
> 原始ID: 1909055658544708752


# 🛡️ 盯人日报 #064 | 2026-05-05

> Anthropic携华尔街三巨头成立企业AI服务公司、Musk庭审威胁曝光"最令美国人憎恨的男人"、ARC-AGI-3深度拆解前沿模型推理缺陷
> 关键词：Anthropic企业合资 / Musk庭审转折 / ARC-AGI-3推理分析

---

## 上期跟进

- **⭐ Anthropic Mythos 白宫角力**：白宫起草guidance路径被CNN 5/4独家报道进一步明确——五角大楼已与8家Big Tech签约（AWS/Google/MSFT/NVIDIA/OpenAI/SpaceX/Reflection AI/Palantir），正式排斥Anthropic。但Mythos的网安能力太独特，白宫幕僚长Wiles仍在私下与Amodei保持对话。Times of India 5/4长文分析Amodei"$900亿的理由"——为何他持续警告AI将消灭50%入门级白领岗位。Anthropic同日宣布"Claude将永远不投放广告"，与Google翻转广告承诺形成鲜明对比。
- **⭐ David Silver / Ineffable Intelligence**：WIRED深度报道持续传播，"反LLM、纯自学习"路线引发讨论。暂无新进展，处于种子轮后组建团队阶段。
- **⭐ NYT DeepSeek专题**：US政府机构5/5发布评估称DeepSeek V4-Pro"落后美国模型约8个月"，但多名专家和Stanford AI Index数据反驳——公开排行榜上中美差距仅2.7%。DeepSeek V4-Pro折扣延至5/31（$0.435/M input tokens），价格战持续。

---

## 今日动态

### ⭐ 值得深读

#### 1. Anthropic 联合 Blackstone/Goldman Sachs/H&F 成立企业AI服务合资公司
📍 **Dario Amodei / Anthropic** · Anthropic官方 / TechCrunch / Blackstone / PYMNTS · 2026-05-04
📝 Anthropic宣布与Blackstone、Hellman & Friedman、Goldman Sachs成立新的AI原生企业服务公司。背后还有General Atlantic、Leonard Green、Apollo、GIC、Sequoia Capital等一众另类资管巨头。定位：帮中型企业（社区银行、区域医疗、中型制造商）将Claude部署到核心业务运营中。CFO Krishna Rao称"对Claude的企业需求远超任何单一交付模式"。Anthropic Applied AI工程师将与合资公司团队一起驻场客户处。TechCrunch同日指出OpenAI也在搭建类似PE合资结构——两巨头同步进入"咨询+部署"商业模式。
🔗 https://www.anthropic.com/news/enterprise-ai-services-company
💡 这标志着AI竞争从"模型性能"正式扩展到"落地服务"。Anthropic拉上华尔街最大的PE/投行（Blackstone $1万亿+AUM, Goldman Sachs）不是为了融钱，而是为了**触达客户**——PE投资组合公司天然成为Claude的部署场景。对老刀：AI公司的竞争维度已经从"做最好的模型"变成"谁能最快帮企业用上"。

#### 2. Musk vs Altman 庭审爆炸性转折：开庭前威胁"你们将成为全美最令人憎恨的男人"
📍 **Musk vs Altman / Brockman** · CNBC / NYT / Ars Technica / BI / CNN · 2026-05-05
📝 Brockman出庭作证当日（5/5），OpenAI律师曝光爆炸性证据：开庭前两天（4/25），Musk主动短信Brockman试探和解意向。Brockman建议"双方各撤各诉"。Musk拒绝后发出威胁："By the end of this week, you and Sam will be the most hated men in America. If you insist, so it will be."（"到本周末，你和Sam将成为全美最令人憎恨的男人。你执意如此，那就如此。"）OpenAI律师请求法官允许此信息作为证据呈堂——证明Musk真实动机是胁迫而非保护慈善。NYT报道Musk律师追问Brockman"为何你价值$300亿"。观察者即刻指出：这不是关于AI安全的诉讼，而是关于从成功中勒索金钱、同时打击竞争对手。
🔗 https://www.cnbc.com/2026/05/04/musk-altman-open-ai-settlement-trial-brockman.html
💡 这条短信可能成为整个案件的转折点。"If you insist, so it will be"的措辞暴露了胁迫意图。如果法官采纳为证据，Musk的"保护AI安全"叙事将被从根本上削弱。对老刀：科技史上最昂贵的私人恩怨正在以法庭证词形式实时展开。

#### 3. ARC Prize 发布 GPT-5.5 & Opus 4.7 推理缺陷深度分析——开源分析工具包
📍 **François Chollet / ARC Prize** · arcprize.org · 2026-05-01（本期首次覆盖）
📝 ARC Prize团队对160条GPT-5.5和Opus 4.7的ARC-AGI-3推理轨迹做了系统性分析。结果：GPT-5.5得分0.43%，Opus 4.7仅0.18%（人类100%通过）。团队识别出三大系统性推理缺陷：①"True Local Effect, False World Model"——模型理解单步操作但无法推导全局规则；②"Wrong Level of Abstraction"——把ARC环境误认为训练集中的其他游戏；③"Solved The Level, Didn't Learn The Game"——即使通过某关也无法迁移学习。今日同步开源完整分析工具包，任何人可复现。Hacker News讨论热烈。
🔗 https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis
💡 这是目前对前沿模型推理能力最精确的"尸检报告"。0.43% vs 人类100%——差距不是量级问题，是质变问题。三种失败模式都指向同一个结论：当前LLM做的是"模式匹配"而非"真正推理"。对老刀：Chollet用数据证明了"jagged intelligence"——AI在特定任务上超人类，但在需要真正适应性的新情境中几乎完全失败。

---

### 📋 了解即可

📍 **Anthropic 宣布"Claude将永远不投放广告"** · anthropic.com · 2026-05-04
📝 Anthropic发布声明解释为何广告激励与"真正有帮助的AI助手"不兼容。这是对Google此前翻转Gemini广告承诺的直接回应——Anthropic选择用付费订阅+企业合同模式扩大接入，而非广告变现。
🔗 https://www.anthropic.com/news

📍 **Kimi K2.6 在编码挑战中击败 Claude Opus 4.7 和 GPT-5.5** · TechPlanet / Hacker News / Medium · 2026-05-04/05
📝 Moonshot AI的开源模型Kimi K2.6（1T参数/32B激活）在实时编程竞赛中胜过所有闭源模型。The Batch（Andrew Ng）报道K2.6在WebDev Arena排名第6/67（1529 Elo），紧追Opus 4.7（1565 Elo）。Medium深度分析称"这是第一个在真实多文件任务中可替代GPT-5.x的开源模型"。
🔗 https://news.ycombinator.com/item?id=47993235

📍 **Cerebras IPO：$26.6亿估值，2026最大科技IPO** · Reuters / TechCrunch · 2026-05-04
📝 OpenAI核心推理合作伙伴Cerebras正式定价IPO：融$35亿，估值$266亿。与OpenAI签有$200亿+多年合同（750MW推理产能至2028）。Altman/Brockman/Sutskever均为早期投资人。这将是2026年迄今最大科技IPO。
🔗 https://techcrunch.com/2026/05/04/openais-cozy-partner-cerebras-is-on-track-for-a-blockbuster-ipo/

📍 **US政府评估：DeepSeek V4-Pro"落后美国模型约8个月"，专家反驳** · Decrypt / GNCrypto · 2026-05-05
📝 美国情报机构发布评估称DeepSeek V4-Pro在关键能力指标上落后美国顶级模型约8个月。但Stanford AI Index数据显示公开排行榜差距仅2.7%。DeepSeek V4-Pro 75%折扣延至5/31。
🔗 https://decrypt.co/366685/us-says-china-best-ai-models-lag-behind-experts-not-sure

📍 **3Blue1Brown 新视频："如何（以及为什么）对一幅画取对数"** · YouTube / B站 · 2026-05-04
📝 Grant Sanderson发布新数学可视化视频，从埃舍尔的画作出发解释德罗斯特效应(Droste effect)的数学原理。B站19小时内获近3000播放。这是继4/24"毛球定理"后的又一纯数学视频。
🔗 https://www.youtube.com/watch?v=ldxFjLJ3rVY

📍 **Perplexity 深度报道：Forbes India 万字长文"如何重塑为智能数字同事"** · Forbes India · 2026-05-05
📝 Srinivas接受Forbes India深度采访，披露"2026年收入翻倍但团队仅增34%"，Personal Computer/Perplexity Computer定位为"AI CFO/AI同事"。Apple在财报电话会上直接点名表扬Personal Computer。
🔗 https://www.forbesindia.com/article/news/deep-dive/how-perplexity-is-remaking-itself-into-a-smart-digital-co-worker/2993628/1

📍 **a16z："AI周期正在重复移动互联网剧本"** · CapitalAI Daily · 2026-05-05
📝 a16z发布Charts of the Week分析，引用Morgan Stanley数据类比：半导体/基础设施领涨→平台层→应用层。暗示当前投资仍在"基础设施期"，应用爆发尚未到来。同期数据：ChatGPT周活已达9亿。
🔗 https://www.capitalaidaily.com/a16z-says-ai-cycle-following-the-same-playbook-as-mobile-and-if-history-repeats-this-sector-wins-biggest-in-the-end/

📍 **Karpathy Software 3.0 持续全球二次传播** · StartupHub / philippdubach.com · 2026-05-05
📝 Karpathy Sequoia AI Ascent演讲继续发酵。StartupHub.ai报道其核心论点"AI models need human-like reasoning"；philippdubach.com发布"12 Lessons from Karpathy's Software 3.0 Playbook"详细拆解。台湾数位时代播客专期讨论"Harness Engineering"。
🔗 https://philippdubach.com/posts/karpathys-software-3.0-playbook/

---

## 静默信号

- **苏剑林（科学空间）**：博客持续无法访问（403），连续多期完全失联
- **庞若鸣**：持续零动态（OpenAI内部，极低调）
- **Thomas Wolf / Hugging Face**：个人声音持续沉默5周+
- **Ilya Sutskever / SSI**：除Musk案证词录像外无公开发言。MIT Tech Review确认其将出庭作证，但时间未定
- **姚顺雨**：Hy3发布后转入静默，无新公开动态

---

## 态势判断

1. **AI竞争从"模型性能"正式扩展到"落地服务"**：Anthropic（Blackstone/Goldman）和OpenAI（TPG/Advent/Bain/Brookfield）同日宣布PE合资公司。上期（#063）还在讨论"谁的模型更强"，本期两巨头同步宣布"我们要帮企业部署"——竞争维度已经不可逆地扩展。这像极了云计算早期AWS/Azure之争从IaaS蔓延到专业服务。
2. **开源模型"够用"时刻已到**：Kimi K2.6在编程挑战中击败闭源模型+Forbes India报道Perplexity"同样小团队翻倍收入"+DeepSeek V4-Pro定价$0.435/M tokens。三个信号叠加：开源/低价模型已经在实际任务中达到"够用"阈值。上期的"开源改写竞赛规则"叙事（NYT/DoNews）正在被市场验证。
