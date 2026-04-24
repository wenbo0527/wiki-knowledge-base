# Exploration Strategies in Deep Reinforcement Learning

> 来源: Lilian Weng  
> 发布时间: Sun, 07 Jun 2020 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- Exploitation versus exploration is a critical topic in reinforcement learning. This post introduces several common approaches for better exploration in Deep RL. -->
<p><span class="update">[Updated on 2020-06-17: Add <a href="https://lilianweng.github.io/index.xml#exploration-via-disagreement">&ldquo;exploration via disagreement&rdquo;</a> in the &ldquo;Forward Dynamics&rdquo; <a href="https://lilianweng.github.io/index.xml#forward-dynamics">section</a>.</span></p>
<p><a href="https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/">Exploitation versus exploration</a> is a critical topic in Reinforcement Learning. We&rsquo;d like the RL agent to find the best solution as fast as possible. However, in the meantime, committing to solutions too quickly without enough exploration sounds pretty bad, as it could lead to local minima or total failure. Modern <a href="https://lilianweng.github.io/posts/2018-02-19-rl-overview/">RL</a> <a href="https://lilianweng.github.io/posts/2018-04-08-policy-gradient/">algorithms</a> that optimize for the best returns can achieve good exploitation quite efficiently, while exploration remains more like an open topic.</p>

## 链接

https://lilianweng.github.io/posts/2020-06-07-exploration-drl/

---

*ID: 95896ea75d150a0c*
*抓取时间: 2026-03-05T10:01:44.823831*
