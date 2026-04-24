# Some Math behind Neural Tangent Kernel

> 来源: Lilian Weng  
> 发布时间: Thu, 08 Sep 2022 10:00:00 -0700  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<p>Neural networks are <a href="https://lilianweng.github.io/posts/2019-03-14-overfit/">well known</a> to be over-parameterized and can often easily fit data with near-zero training loss with decent generalization performance on test dataset. Although all these parameters are initialized at random, the optimization process can consistently lead to similarly good outcomes. And this is true even when the number of model parameters exceeds the number of training data points.</p>
<p><strong>Neural tangent kernel (NTK)</strong> (<a href="https://arxiv.org/abs/1806.07572">Jacot et al. 2018</a>) is a kernel to explain the evolution of neural networks during training via gradient descent. It leads to great insights into why neural networks with enough width can consistently converge to a global minimum when trained to minimize an empirical loss. In the post, we will do a deep dive into the motivation and definition of NTK, as well as the proof of a deterministic convergence at different initializations of neural networks with infinite width by characterizing NTK in such a setting.</p>

## 链接

https://lilianweng.github.io/posts/2022-09-08-ntk/

---

*ID: dbc11a2c5abdc924*
*抓取时间: 2026-03-05T10:01:44.823778*
