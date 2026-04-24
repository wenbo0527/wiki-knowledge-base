# Adversarial Attacks on LLMs

> 来源: Lilian Weng  
> 发布时间: Wed, 25 Oct 2023 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<p>The use of large language models in the real world has strongly accelerated by the launch of ChatGPT. We (including my team at OpenAI, shoutout to them) have invested a lot of effort to build default safe behavior into the model during the alignment process (e.g. via <a href="https://openai.com/research/learning-to-summarize-with-human-feedback">RLHF</a>). However, adversarial attacks or jailbreak prompts could potentially trigger the model to output something undesired.</p>
<p>A large body of ground work on adversarial attacks is on images, and differently it operates in the continuous, high-dimensional space. Attacks for discrete data like text have been considered to be a lot more challenging, due to lack of direct gradient signals. My past post on <a href="https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/">Controllable Text Generation</a> is quite relevant to this topic, as attacking LLMs is essentially to control the model to output a certain type of (unsafe) content.</p>

## 链接

https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/

---

*ID: 95371cd4e844df5c*
*抓取时间: 2026-03-05T10:01:44.823756*
