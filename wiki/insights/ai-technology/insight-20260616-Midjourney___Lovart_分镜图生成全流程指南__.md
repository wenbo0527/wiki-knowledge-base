---
title: insight 20260616 Midjourney   Lovart 分镜图生成全流程指南  
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology]
date: 2026-06-30
---

# Midjourney + Lovart 分镜图生成全流程指南 🎨

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1888948440583527912
> **创建时间**: 2025-09-30 16:18:45
> **更新时间**: 2025-09-30 16:18:45
> **原始链接**: https://mp.weixin.qq.com/s?__biz=MzkxNzYzODgwNw==&mid=2247492943&idx=1&sn=ccd2663171fbd48ae1a55cc21020846b&chksm=c053c8bef889f5b45c7dd3f5f3f22341650b30be4814bbccc6c06c252c902f4d13bbac48675b&scene=90&xtrack=1&sessionid=1759220197&subscene=93&clicktime=1759220215&enterid=1759220215&flutter_pos=1&biz_enter_id=4&ranksessionid=1759220191&jumppath=1001_1759219876448%2C1102_1759219879409%2C1001_1759219880455%2C1104_1759220198628&jumppathdepth=4&ascene=56&devicetype=iOS18.7&version=18003f2f&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQOMQvRhC2%2BpDoXdTDBEi88BLXAQIE97dBBAEAAAAAANQ3F%2B8wsywAAAAOpnltbLcz9gKNyK89dVj07qXINJuW9KugClgvWvFur7KmH63%2FuYPOd%2FM0qb7OxNw3zauKEvDSRr5V%2Bpakr9xOwMXHM1NExkXXMYDX07DHcMlHtBtYGxznj2F0ZZ31ot1y8Y0gW97HQJd0zJT78Ewz35e0ubkP1sydSVmWrAFCFfRjCP42k7TPAa009R9SPk7rFYpFJq9MVVvTCDYy5uBBxy%2B62kS5RAnXfL7o7cV6rQ2WnsDY6aUGZNOXWvcQ1y8N&pass_ticket=vI0hUO1CuG78vk3kOz4stKAcLV9Jcb18QXDFiOx%2FRe9ViWXNszz1ElCPOadPIqal&wx_header=3

---

### 🌟 核心功能与工具矩阵
- **Lovart平台优势**：整合Midjourney、NanoBanana(NB)、Seedream 4.0等AI模型，实现"一条龙"分镜生成
- **模型分工**：
  - Midjourney：美学天花板，擅长高质量图片生成（视频素材首选）
  - NB模型：基于原图拓展，擅长多角度/动作延续
  - Seedream 4.0：序列图生成，保持视觉一致性
  - Gemini Imagen 4：精准遵循提示词
  - Recraft：真实感与插画效果突出
  - Ideogram：Logo与英文海报生成

### 📝 Midjourney分镜生成流程
1. **提示词公式**  
   `[主体] + [环境/背景] + [动作/场景] + [风格/材质] + [光影/氛围] + [构图/镜头] + [可选参数]`  
   ✅ 案例：*"A medieval knight kneeling in prayer in front of a cathedral altar, stained glass light patterns, realistic style"*

2. **批量生成策略**  
   - 单次可输入多组提示词（测试8组成功），每组生成4张图
   - 比例控制：--ar参数（如--ar 16:9）或中文直接指定
   - 质量提升：生成后可用"Upscale"功能最高4倍放大

3. **风格控制技巧**  
   - Sref code参数控制风格（如--sref 3171847554）
   - 对话框全局设置：`"后缀参数全部使用--sref 3171847554"`

### 🔄 分镜延展三大核心场景

#### 1. Seedream 4.0故事序列图
- **操作路径**：选图→右键"add to chat"→调用Seedream 4.0
- **提示词框架**（12镜分镜参考）：  
  ```
  分析视觉风格/色彩/动作/氛围  
  创建12镜故事序列：  
  01-03开场建立 | 04-06事件发展 | 07-09冲突高潮 | 10-12结局收尾  
  要求：逻辑连贯+镜头多样性（远景/特写等）
  ```
- **输出形态**：分镜表格（含镜号/场景描述/镜头类型/视觉重点）

#### 2. NanoBanana多角度生成
- **核心功能**：保持场景一致性，仅改变拍摄角度
- **提示词示例**：  
  ```
  生成8个不同角度镜头：  
  1. 相同场景/光线/氛围  
  2. 仅改变拍摄角度和距离  
  3. 物体/人物保持一致  
  输出专业分镜表格
  ```
#### 3. 动作延续生成
- **提示词框架**：  
  ```
  基于当前动作推断8个后续镜头：  
  分析：身体姿态/运动方向/物体轨迹  
  规则：物理规律+角色性格+动作三阶段（预备-执行-结果）  
  镜头设计：多角度+反应镜头+节奏控制
  ```
### 💼 商业应用案例：广告分镜生成
1. **产品替换流程**：  
   上传参考图→选图Tab→替换产品（如口红替换案例）

2. **12镜广告分镜结构**：  
   - 01-02开场吸引 | 03-05产品展示 | 06-08使用场景  
   - 09-10情感共鸣 | 11产品特写 | 12品牌收尾  

3. **多构图方案**：  
   提供8种商业摄影构图（极致特写/产品全景/俯视角度/创意视角等）

### 💰 成本参考
- 批量生成32张骑士主题图仅消耗少量积分（具体明细见消费截图）
- 付费会员权益：Midjourney/NB/Seedream 4.0免费用不消耗积分