# The Transformer Family Version 2.0

> 来源: Lilian Weng  
> 发布时间: Fri, 27 Jan 2023 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<p>Many new Transformer architecture improvements have been proposed since my last post on <a href="https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/"><ins>&ldquo;The Transformer Family&rdquo;</ins></a> about three years ago. Here I did a big refactoring and enrichment of that 2020 post &mdash; restructure the hierarchy of sections and improve many sections with more recent papers. Version 2.0 is a superset of the old version, about twice the length.</p>
<h1 id="notations">Notations</h1>
<table>
  <thead>
      <tr>
          <th>Symbol</th>
          <th>Meaning</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td>$d$</td>
          <td>The model size / hidden state dimension / positional encoding size.</td>
      </tr>
      <tr>
          <td>$h$</td>
          <td>The number of heads in multi-head attention layer.</td>
      </tr>
      <tr>
          <td>$L$</td>
          <td>The segment length of input sequence.</td>
      </tr>
      <tr>
          <td>$N$</td>
          <td>The total number of attention layers in the model; not considering MoE.</td>
      </tr>
      <tr>
          <td>$\mathbf{X} \in \mathbb{R}^{L \times d}$</td>
          <td>The input sequence where each element has been mapped into an embedding vector of shape $d$, same as the model size.</td>
      </tr>
      <tr>
          <td>$\mathbf{W}^k \in \mathbb{R}^{d \times d_k}$</td>
          <td>The key weight matrix.</td>
      </tr>
      <tr>
          <td>$\mathbf{W}^q \in \mathbb{R}^{d \times d_k}$</td>
          <td>The query weight matrix.</td>
      </tr>
      <tr>
          <td>$\mathbf{W}^v \in \mathbb{R}^{d \times d_v}$</td>
          <td>The value weight matrix. Often we have $d_k = d_v = d$.</td>
      </tr>
      <tr>
          <td>$\mathbf{W}^k_i, \mathbf{W}^q_i \in \mathbb{R}^{d \times d_k/h}; \mathbf{W}^v_i \in \mathbb{R}^{d \times d_v/h}$</td>
          <td>The weight matrices per head.</td>
      </tr>
      <tr>
          <td>$\mathbf{W}^o \in \mathbb{R}^{d_v \times d}$</td>
          <td>The output weight matrix.</td>
      </tr>
      <tr>
          <td>$\mathbf{Q} = \mathbf{X}\mathbf{W}^q \in \mathbb{R}^{L \times d_k}$</td>
          <td>The query embedding inputs.</td>
      </tr>
      <tr>
          <td>$\mathbf{K} = \mathbf{X}\mathbf{W}^k \in \mathbb{R}^{L \times d_k}$</td>
          <td>The key embedding inputs.</td>
      </tr>
      <tr>
          <td>$\mathbf{V} = \mathbf{X}\mathbf{W}^v \in \mathbb{R}^{L \times d_v}$</td>
          <td>The value embedding inputs.</td>
      </tr>
      <tr>
          <td>$\mathbf{q}_i, \mathbf{k}_i \in \mathbb{R}^{d_k}, \mathbf{v}_i \in \mathbb{R}^{d_v}$</td>
          <td>Row vectors in query, key, value matrices, $\mathbf{Q}$, $\mathbf{K}$ and $\mathbf{V}$.</td>
      </tr>
      <tr>
          <td>$S_i$</td>
          <td>A collection of key positions for the $i$-th query $\mathbf{q}_i$ to attend to.</td>
      </tr>
      <tr>
          <td>$\mathbf{A} \in \mathbb{R}^{L \times L}$</td>
          <td>The self-attention matrix between a input sequence of lenght $L$ and itself. $\mathbf{A} = \text{softmax}(\mathbf{Q}\mathbf{K}^\top / \sqrt{d_k})$.</td>
      </tr>
      <tr>
          <td>$a_{ij} \in \mathbf{A}$</td>
          <td>The scalar attention score between query $\mathbf{q}_i$ and key $\mathbf{k}_j$.</td>
      </tr>
      <tr>
          <td>$\mathbf{P} \in \mathbb{R}^{L \times d}$</td>
          <td>position encoding matrix, where the $i$-th row $\mathbf{p}_i$ is the positional encoding for input $\mathbf{x}_i$.</td>
      </tr>
  </tbody>
</table>
<h1 id="transformer-basics">Transformer Basics</h1>
<p>The <strong>Transformer</strong> (which will be referred to as &ldquo;vanilla Transformer&rdquo; to distinguish it from other enhanced versions; <a href="https://arxiv.org/abs/1706.03762">Vaswani, et al., 2017</a>) model has an encoder-decoder architecture, as commonly used in many <a href="https://lilianweng.github.io/posts/2018-06-24-attention/#born-for-translation">NMT</a> models. Later simplified Transformer was shown to achieve great performance in language modeling tasks, like in encoder-only <a href="https://lilianweng.github.io/posts/2019-01-31-lm/#bert">BERT</a> or decoder-only <a href="https://lilianweng.github.io/posts/2019-01-31-lm/#openai-gpt">GPT</a>.</p>

## 链接

https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/

---

*ID: af0c5a0fd308b671*
*抓取时间: 2026-03-05T10:01:44.823769*
