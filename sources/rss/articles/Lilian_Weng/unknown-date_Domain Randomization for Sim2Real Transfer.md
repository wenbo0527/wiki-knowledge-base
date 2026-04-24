# Domain Randomization for Sim2Real Transfer

> 来源: Lilian Weng  
> 发布时间: Sun, 05 May 2019 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- If a model or policy is mainly trained in a simulator but expected to work on a real robot, it would surely face the sim2real gap. *Domain Randomization* (DR) is a simple but powerful idea of closing this gap by randomizing properties of the training environment. -->
<p>In Robotics, one of the hardest problems is how to make your model transfer to the real world. Due to the sample inefficiency of deep RL algorithms and the cost of data collection on real robots, we often need to train models in a simulator which theoretically provides an infinite amount of data. However, the reality gap between the simulator and the physical world often leads to failure when working with physical robots. The gap is triggered by an inconsistency between physical parameters (i.e. friction, kp, damping, mass, density) and, more fatally, the incorrect physical modeling (i.e. collision between soft surfaces).</p>

## 链接

https://lilianweng.github.io/posts/2019-05-05-domain-randomization/

---

*ID: 01da3496c875fa02*
*抓取时间: 2026-03-05T10:01:44.823862*
