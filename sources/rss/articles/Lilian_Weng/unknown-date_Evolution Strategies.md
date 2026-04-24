# Evolution Strategies

> 来源: Lilian Weng  
> 发布时间: Thu, 05 Sep 2019 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- Gradient descent is not the only option when learning optimal model parameters. Evolution Strategies (ES)  works out well in the cases where we don't know the precise analytic form of an objective function or cannot compute the gradients directly. This post dives into several classic ES methods, as well as how ES can be used in deep reinforcement learning. -->
<p>Stochastic gradient descent is a universal choice for optimizing deep learning models. However, it is not the only option. With black-box optimization algorithms, you can evaluate a target function $f(x): \mathbb{R}^n \to \mathbb{R}$, even when you don&rsquo;t know the precise analytic form of $f(x)$ and thus cannot compute gradients or the Hessian matrix. Examples of black-box optimization methods include <a href="https://en.wikipedia.org/wiki/Simulated_annealing">Simulated Annealing</a>, <a href="https://en.wikipedia.org/wiki/Hill_climbing">Hill Climbing</a> and <a href="https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method">Nelder-Mead method</a>.</p>

## 链接

https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/

---

*ID: e33ec4ea6bfc9a7d*
*抓取时间: 2026-03-05T10:01:44.823849*
