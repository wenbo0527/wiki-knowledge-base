# Flow-based Deep Generative Models

> 来源: Lilian Weng  
> 发布时间: Sat, 13 Oct 2018 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- In this post, we are looking into the third type of generative models: flow-based generative models. Different from GAN and VAE, they explicitly learn the probability density function of the input data. -->
<p>So far, I&rsquo;ve written about two types of generative models, <a href="https://lilianweng.github.io/posts/2017-08-20-gan/">GAN</a> and <a href="https://lilianweng.github.io/posts/2018-08-12-vae/">VAE</a>. Neither of them explicitly learns the probability density function of real data, $p(\mathbf{x})$ (where $\mathbf{x} \in \mathcal{D}$) &mdash; because it is really hard! Taking the generative model with latent variables as an example, $p(\mathbf{x}) = \int p(\mathbf{x}\vert\mathbf{z})p(\mathbf{z})d\mathbf{z}$ can hardly be calculated as it is intractable to go through all possible values of the latent code $\mathbf{z}$.</p>

## 链接

https://lilianweng.github.io/posts/2018-10-13-flow-models/

---

*ID: ea228eb43c7c763c*
*抓取时间: 2026-03-05T10:01:44.823883*
