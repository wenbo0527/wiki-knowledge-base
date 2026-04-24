# From GAN to WGAN

> 来源: Lilian Weng  
> 发布时间: Sun, 20 Aug 2017 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- This post explains the maths behind a generative adversarial network (GAN) model and why it is hard to be trained. Wasserstein GAN is intended to improve GANs' training by adopting a smooth metric for measuring the distance between two probability distributions. -->
<p><span class="update">[Updated on 2018-09-30: thanks to Yoonju, we have this post translated in <a href="https://github.com/yjucho1/articles/blob/master/fromGANtoWGAN/readme.md">Korean</a>!]</span>
<br />
<span class="update">[Updated on 2019-04-18: this post is also available on <a href="https://arxiv.org/abs/1904.08994">arXiv</a>.]</span></p>
<p><a href="https://arxiv.org/pdf/1406.2661.pdf">Generative adversarial network</a> (GAN) has shown great results in many generative tasks to replicate the real-world rich content such as images, human language, and music. It is inspired by game theory: two models, a generator and a critic, are competing with each other while making each other stronger at the same time. However, it is rather challenging to train a GAN model, as people are facing issues like training instability or failure to converge.</p>

## 链接

https://lilianweng.github.io/posts/2017-08-20-gan/

---

*ID: 3ee00b2c71c00828*
*抓取时间: 2026-03-05T10:01:44.823935*
