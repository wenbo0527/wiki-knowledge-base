# DeepSeek-OCR开源：视觉压缩颠覆大模型输入范式

> **来源**: Get笔记
> **知识库**: ai-learning
> **导入日期**: 2026-06-16
> **原始ID**: 1890879727389007216
> **创建时间**: 2025-10-21 11:56:16
> **更新时间**: 2025-10-21 11:56:16
> **原始链接**: https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650996789&idx=1&sn=6666408d922d898394c688085b7ce05c&chksm=85975625d097389be0490589106d0dea481e5744d7f526f102632038f9c3f61f8e0a3860e213&scene=90&xtrack=1&sessionid=1761018963&subscene=93&clicktime=1761018966&enterid=1761018966&flutter_pos=0&biz_enter_id=4&ranksessionid=1761018909&jumppath=1001_1761018955883%2C1102_1761018959602%2C1001_1761018961046%2C1104_1761018963961&jumppathdepth=4&ascene=56&devicetype=iOS18.7&version=1800402b&nettype=WIFI&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&countrycode=CN&fontScale=100&exportkey=n_ChQIAhIQq02BwuOvd%2BnzYxQy%2FebSQhLXAQIE97dBBAEAAAAAABDtFf9mcjwAAAAOpnltbLcz9gKNyK89dVj0PWlwd80fNERUL7gqJiiVeoPJ06Tb3AjblPqSMWe59Qv8skhcBMbEREAc8ZTqgTwI4%2Bh2QfFVP23i0l%2B%2FJEymHnepQE7Bq1IxVEbwbrXvDA0qdmEYFAQe0b5fdyWyqy4K7PStw9xqwAzQW6QNI48uechNFeey56aXhAZ6uAZH%2B20SLcYo8UqtMXG8gqs7xYzL8lqOaBgESBt2CKfaKLNnBRA%2Bm8V%2FxDUo0MIwDCngq1MT&pass_ticket=%2Fg82YYRKzvIddDVxv8IFY5vLJqEBHHZ5rGMP%2FsDEVGK5TMVQelT1vfOgeoDa1huh&wx_header=3

---

🔍 **核心突破：视觉压缩技术**
- 文本转图像后压缩效率提升10倍：1000字文章→100视觉token（传统需1000+文本token）
- 精度保持97%，A100单卡日处理20万页数据
- 与稀疏注意力技术结合可扩展上下文窗口，潜在突破千万token级上下文限制

🚀 **技术优势与行业反响**
- 多模态统一输入：支持文本/图像/格式（粗体/彩色）混合内容
- 效率验证：vLLM框架下A100-40G达2500 tokens/s，400页PDF转Markdown仅需4分钟
- GitHub数据：1天获4k星标、154次分支，引发AI社区技术实验热潮

💡 **范式转变争议**
- Karpathy核心观点："LLM所有输入都应是图像，纯文本需先渲染"，主张移除分词器
  - 优势：信息压缩率提升、双向注意力支持、规避Unicode历史包袱
  - 质疑（Lucas Beyer）：字体大小阈值导致非渐进式失效，不符合人类认知模式

🔬 **落地案例与应用**
- 医疗场景：成功识别医生手写处方（含Amoxicillin等药物名称及剂量）
- 硬件适配：Claude Code辅助下40分钟完成NVIDIA Spark部署，Mac CPU可运行640分辨率模型
- 学术应用：快速转换尼采《查拉图斯特拉如是说》PDF至Markdown格式

📚 **技术溯源与发展**
- 思想先驱：2022年PIXEL模型已提出文本渲染图像思路，通过像素重建训练语言模型
- 技术演进：CVPR2023 CLIPPO、NeurIPS2024视觉token扩展等研究持续探索视觉-语言融合