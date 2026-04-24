# Generalized Language Models

> 来源: Lilian Weng  
> 发布时间: Thu, 31 Jan 2019 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- As a follow up of word embedding post, we will discuss the models on learning contextualized word vectors, as well as the new trend in large unsupervised pre-trained language models which have achieved amazing SOTA results on a variety of language tasks. -->
<p><span class="update">[Updated on 2019-02-14: add <a href="https://lilianweng.github.io/index.xml#ulmfit">ULMFiT</a> and <a href="https://lilianweng.github.io/index.xml#gpt-2">GPT-2</a>.]</span><br />
<span class="update">[Updated on 2020-02-29: add <a href="https://lilianweng.github.io/index.xml#albert">ALBERT</a>.]</span><br />
<span class="update">[Updated on 2020-10-25: add <a href="https://lilianweng.github.io/index.xml#roberta">RoBERTa</a>.]</span><br />
<span class="update">[Updated on 2020-12-13: add <a href="https://lilianweng.github.io/index.xml#t5">T5</a>.]</span><br />
<span class="update">[Updated on 2020-12-30: add <a href="https://lilianweng.github.io/index.xml#gpt-3">GPT-3</a>.]</span><br />
<span class="update">[Updated on 2021-11-13: add <a href="https://lilianweng.github.io/index.xml#xlnet">XLNet</a>, <a href="https://lilianweng.github.io/index.xml#bart">BART</a> and <a href="https://lilianweng.github.io/index.xml#electra">ELECTRA</a>; Also updated the <a href="https://lilianweng.github.io/index.xml#summary">Summary</a> section.]</span></p>
<br />
<figure>
	<img src="https://lilianweng.github.io/elmo-and-bert.png" style="width: 60%;" />
	<figcaption>I guess they are Elmo & Bert? (Image source: <a href="https://www.youtube.com/watch?v=l5einDQ-Ttc" target="_blank">here</a>)</figcaption>
</figure>
<p>We have seen amazing progress in NLP in 2018. Large-scale pre-trained language modes like <a href="https://blog.openai.com/language-unsupervised/">OpenAI GPT</a> and <a href="https://arxiv.org/abs/1810.04805">BERT</a> have achieved great performance on a variety of language tasks using generic model architectures. The idea is similar to how ImageNet classification pre-training helps many vision tasks (*). Even better than vision classification pre-training, this simple and powerful approach in NLP does not require labeled data for pre-training, allowing us to experiment with increased training scale, up to our very limit.</p>

## 链接

https://lilianweng.github.io/posts/2019-01-31-lm/

---

*ID: 31b1bce0b20d95f2*
*抓取时间: 2026-03-05T10:01:44.823871*
