# Learning Word Embedding

> 来源: Lilian Weng  
> 发布时间: Sun, 15 Oct 2017 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- Word embedding is a dense representation of words in the form of numeric vectors. It can be learned using a variety of language models. The word embedding representation is able to reveal many hidden relationships between words. For example, vector("cat") - vector("kitten") is similar to vector("dog") - vector("puppy"). This post introduces several models for learning word embedding and how their loss functions are designed for the purpose. -->
<p>Human vocabulary comes in free text. In order to make a machine learning model understand and process the natural language, we need to transform the free-text words into numeric values. One of the simplest transformation approaches is to do a one-hot encoding in which each distinct word stands for one dimension of the resulting vector and a binary value indicates whether the word presents (1) or not (0).</p>

## 链接

https://lilianweng.github.io/posts/2017-10-15-word-embedding/

---

*ID: 0b9e2a6048a36431*
*抓取时间: 2026-03-05T10:01:44.823927*
