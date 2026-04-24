# Extrinsic Hallucinations in LLMs

> 来源: Lilian Weng  
> 发布时间: Sun, 07 Jul 2024 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<p>Hallucination in large language models usually refers to the model generating unfaithful, fabricated, inconsistent, or nonsensical content. As a term, hallucination has been somewhat generalized to cases when the model makes mistakes. Here, I would like to narrow down the problem of hallucination to cases where the model output is fabricated and <strong>not grounded</strong> by either the provided context or world knowledge.</p>
<p>There are two types of hallucination:</p>
<ol>
<li>In-context hallucination: The model output should be consistent with the source content in context.</li>
<li>Extrinsic hallucination: The model output should be grounded by the pre-training dataset. However, given the size of the pre-training dataset, it is too expensive to retrieve and identify conflicts per generation. If we consider the pre-training data corpus as a proxy for world knowledge, we essentially try to ensure the model output is factual and verifiable by external world knowledge. Equally importantly, when the model does not know about a fact, it should say so.</li>
</ol>
<p>This post focuses on extrinsic hallucination. To avoid hallucination, LLMs need to be (1) factual and (2) acknowledge not knowing the answer when applicable.</p>

## 链接

https://lilianweng.github.io/posts/2024-07-07-hallucination/

---

*ID: b402a18418f3be0c*
*抓取时间: 2026-03-05T10:01:44.823741*
