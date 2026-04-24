# Reward Hacking in Reinforcement Learning

> 来源: Lilian Weng  
> 发布时间: Thu, 28 Nov 2024 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<p>Reward hacking occurs when a <a href="https://lilianweng.github.io/(https:/lilianweng.github.io/posts/2018-02-19-rl-overview/)">reinforcement learning (RL)</a> agent <a href="https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#exploitation-vs-exploration">exploits</a> flaws or ambiguities in the reward function to achieve high rewards, without genuinely learning or completing the intended task. Reward hacking exists because RL environments are often imperfect, and it is fundamentally challenging to accurately specify a reward function.</p>
<p>With the rise of <a href="https://lilianweng.github.io/posts/2019-01-31-lm/">language models</a> generalizing to a broad spectrum of tasks and RLHF becomes a de facto method for alignment training, reward hacking in RL training of language models has become a critical practical challenge. Instances where the model learns to modify unit tests to pass coding tasks, or where responses contain biases that mimic a user&rsquo;s preference, are pretty concerning and are likely one of the major blockers for real-world deployment of more autonomous use cases of AI models.</p>

## 链接

https://lilianweng.github.io/posts/2024-11-28-reward-hacking/

---

*ID: 6b8d45d8c8b9a0b1*
*抓取时间: 2026-03-05T10:01:44.823736*
