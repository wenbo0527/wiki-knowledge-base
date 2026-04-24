# Policy Gradient Algorithms

> 来源: Lilian Weng  
> 发布时间: Sun, 08 Apr 2018 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- Abstract: In this post, we are going to look deep into policy gradient, why it works, and many new policy gradient algorithms proposed in recent years: vanilla policy gradient, actor-critic, off-policy actor-critic, A3C, A2C, DPG, DDPG, D4PG, MADDPG, TRPO, PPO, ACER, ACTKR, SAC, TD3 & SVPG. -->
<p><span class="update">[Updated on 2018-06-30: add two new policy gradient methods, <a href="https://lilianweng.github.io/index.xml#sac">SAC</a> and <a href="https://lilianweng.github.io/index.xml#d4pg">D4PG</a>.]</span>
<br />
<span class="update">[Updated on 2018-09-30: add a new policy gradient method, <a href="https://lilianweng.github.io/index.xml#td3">TD3</a>.]</span>
<br />
<span class="update">[Updated on 2019-02-09: add <a href="https://lilianweng.github.io/index.xml#sac-with-automatically-adjusted-temperature">SAC with automatically adjusted temperature</a>].</span>
<br />
<span class="update">[Updated on 2019-06-26: Thanks to Chanseok, we have a version of this post in <a href="https://talkingaboutme.tistory.com/entry/RL-Policy-Gradient-Algorithms">Korean</a>].</span>
<br />
<span class="update">[Updated on 2019-09-12: add a new policy gradient method <a href="https://lilianweng.github.io/index.xml#svpg">SVPG</a>.]</span>
<br />
<span class="update">[Updated on 2019-12-22: add a new policy gradient method <a href="https://lilianweng.github.io/index.xml#impala">IMPALA</a>.]</span>
<br />
<span class="update">[Updated on 2020-10-15: add a new policy gradient method <a href="https://lilianweng.github.io/index.xml#ppg">PPG</a> &amp; some new discussion in <a href="https://lilianweng.github.io/index.xml#ppo">PPO</a>.]</span>
<br />
<span class="update">[Updated on 2021-09-19: Thanks to Wenhao &amp; 爱吃猫的鱼, we have this post in <a href="https://tomaxent.com/2019/04/14/%E7%AD%96%E7%95%A5%E6%A2%AF%E5%BA%A6%E6%96%B9%E6%B3%95/">Chinese1</a> &amp; <a href="https://paperexplained.cn/articles/article/detail/31/">Chinese2</a>].</span></p>

## 链接

https://lilianweng.github.io/posts/2018-04-08-policy-gradient/

---

*ID: 6c9e2f417ef65643*
*抓取时间: 2026-03-05T10:01:44.823901*
