# From Autoencoder to Beta-VAE

> 来源: Lilian Weng  
> 发布时间: Sun, 12 Aug 2018 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- Autocoders are a family of neural network models aiming to learn compressed latent variables of high-dimensional data. Starting from the basic autocoder model, this post reviews several variations, including denoising, sparse, and contractive autoencoders, and then Variational Autoencoder (VAE) and its modification beta-VAE. -->
<p><span class="update">[Updated on 2019-07-18: add a section on <a href="https://lilianweng.github.io/index.xml#vq-vae-and-vq-vae-2">VQ-VAE &amp; VQ-VAE-2</a>.]</span>
<br />
<span class="update">[Updated on 2019-07-26: add a section on <a href="https://lilianweng.github.io/index.xml#td-vae">TD-VAE</a>.]</span>
<br /></p>
<p>Autocoder is invented to reconstruct high-dimensional data using a neural network model with a narrow bottleneck layer in the middle (oops, this is probably not true for <a href="https://lilianweng.github.io/index.xml#vae-variational-autoencoder">Variational Autoencoder</a>, and we will investigate it in details in later sections). A nice byproduct is dimension reduction: the bottleneck layer captures a compressed latent encoding. Such a low-dimensional representation can be used as en embedding vector in various applications (i.e. search), help data compression, or reveal the underlying data generative factors.</p>

## 链接

https://lilianweng.github.io/posts/2018-08-12-vae/

---

*ID: 318bdba99e03e18c*
*抓取时间: 2026-03-05T10:01:44.823888*
