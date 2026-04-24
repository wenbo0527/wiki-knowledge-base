# Learning with not Enough Data Part 3: Data Generation

> 来源: Lilian Weng  
> 发布时间: Fri, 15 Apr 2022 15:10:30 -0700  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<p>Here comes the Part 3 on learning with not enough data (Previous: <a href="https://lilianweng.github.io/posts/2021-12-05-semi-supervised/">Part 1</a> and <a href="https://lilianweng.github.io/posts/2022-02-20-active-learning/">Part 2</a>). Let’s consider two approaches for generating synthetic data for training.</p>
<ul>
<li><strong>Augmented data</strong>. Given a set of existing training samples, we can apply a variety of augmentation, distortion and transformation to derive new data points without losing the key attributes. We have covered a bunch of augmentation methods on text and images in a <a href="https://lilianweng.github.io/posts/2021-05-31-contrastive/">previous post</a> on contrastive learning. For the sake of post completeness, I <em>duplicate</em> the section on data augmentation here with some edits.</li>
<li><strong>New data</strong>. Given few or even no data points, we can rely on powerful pretrained models to generate a number of <em>new</em> data points. This is especially true in recent years given the fast progress in large pretrained <a href="https://lilianweng.github.io/posts/2019-01-31-lm/">language models (LM)</a>. Few shot prompting is shown to be effective for LM to learn within context without extra training.</li>
</ul>
<h1 id="data-augmentation">Data Augmentation</h1>
<p>The goal of data augmentation is to modify the input format (e.g. text wording, visual appearance) while the semantic meaning stays unchanged.</p>

## 链接

https://lilianweng.github.io/posts/2022-04-15-data-gen/

---

*ID: f16f6d68209f46a3*
*抓取时间: 2026-03-05T10:01:44.823787*
