# Large Transformer Model Inference Optimization

> 来源: Lilian Weng  
> 发布时间: Tue, 10 Jan 2023 10:00:00 -0700  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<p><span class="update">[Updated on 2023-01-24: add a small section on <a href="https://lilianweng.github.io/index.xml#distillation">Distillation</a>.]</span><br /></p>
<p>Large transformer models are mainstream nowadays, creating SoTA results for a variety of tasks. They are powerful but very expensive to train and use. The extremely high inference cost, in both time and memory, is a big bottleneck for adopting a powerful transformer for solving real-world tasks at scale.</p>
<p><strong>Why is it hard to run inference for large transformer models?</strong> Besides the increasing size of SoTA models, there are two main factors contributing to the inference challenge (<a href="https://arxiv.org/abs/2211.05102">Pope et al. 2022</a>):</p>

## 链接

https://lilianweng.github.io/posts/2023-01-10-inference-optimization/

---

*ID: 70cbe0cdbc957a5f*
*抓取时间: 2026-03-05T10:01:44.823773*
