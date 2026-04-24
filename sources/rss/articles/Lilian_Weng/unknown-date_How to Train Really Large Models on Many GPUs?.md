# How to Train Really Large Models on Many GPUs?

> 来源: Lilian Weng  
> 发布时间: Fri, 24 Sep 2021 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- How to train large and deep neural networks is challenging, as it demands a large amount of GPU memory and a long horizon of training time. This post reviews several popular training parallelism paradigms, as well as a variety of model architecture and memory saving designs to make it possible to train very large neural networks across a large number of GPUs. -->
<p><span class="update">[Updated on 2022-03-13: add <a href="https://lilianweng.github.io/index.xml#ec">expert choice routing</a>.]</span><br />
<span class="update">[Updated on 2022-06-10]: <a href="https://gregbrockman.com/">Greg</a> and I wrote a shorted and upgraded version of this post, published on OpenAI Blog: <a href="https://openai.com/blog/techniques-for-training-large-neural-networks/">&ldquo;Techniques for Training Large Neural Networks&rdquo;</a></p>

## 链接

https://lilianweng.github.io/posts/2021-09-25-train-large/

---

*ID: 91dc283a618e9b54*
*抓取时间: 2026-03-05T10:01:44.823801*
