# Anatomize Deep Learning with Information Theory

> 来源: Lilian Weng  
> 发布时间: Thu, 28 Sep 2017 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- This post is a summary of Prof Naftali Tishby's recent talk on "Information Theory in Deep Learning". It presented how to apply the information theory to study the growth and transformation of deep neural networks during training. -->
<p><span class="update">Professor Naftali Tishby passed away in 2021. Hope the post can introduce his cool idea of information bottleneck to more people.</span></p>
<p>Recently I watched the talk <a href="https://youtu.be/bLqJHjXihK8">&ldquo;Information Theory in Deep Learning&rdquo;</a> by Prof Naftali Tishby and found it very interesting. He presented how to apply the information theory to study the growth and transformation of deep neural networks during training. Using the <a href="https://arxiv.org/pdf/physics/0004057.pdf">Information Bottleneck (IB)</a> method, he proposed a new learning bound for deep neural networks (DNN), as the traditional learning theory fails due to the exponentially large number of parameters. Another keen observation is that DNN training involves two distinct phases: First, the network is trained to fully represent the input data and minimize the generalization error; then, it learns to forget the irrelevant details by compressing the representation of the input.</p>

## 链接

https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/

---

*ID: f2bc91d00a29cdf9*
*抓取时间: 2026-03-05T10:01:44.823931*
