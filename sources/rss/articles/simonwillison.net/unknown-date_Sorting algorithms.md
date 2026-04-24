# Sorting algorithms

> 来源: simonwillison.net  
> 发布时间: 2026-03-11T22:58:06+00:00  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><strong><a href="https://tools.simonwillison.net/sort-algorithms">Sorting algorithms</a></strong></p>
Today in animated explanations built using Claude: I've always been a fan of animated demonstrations of sorting algorithms so I decided to spin some up on my phone using Claude Artifacts, then added Python's timsort algorithm, then a feature to run them all at once. Here's the <a href="https://claude.ai/share/2c09f6f7-57ed-47eb-af2e-fc39ddc4c39f">full sequence of prompts</a>:</p>
<blockquote>
<p>Interactive animated demos of the most common sorting algorithms</p>
</blockquote>
<p>This gave me bubble sort, selection sort, insertion sort, merge sort, quick sort, and heap sort.</p>
<blockquote>
<p>Add timsort, look up details in a clone of python/cpython from GitHub</p>
</blockquote>
<p>Let's add Python's <a href="https://en.wikipedia.org/wiki/Timsort">Timsort</a>! Regular Claude chat can clone repos from GitHub these days. In the transcript you can see it clone the repo and then consult <a href="https://github.com/python/cpython/blob/d19de375a204c74ab5f3a28ec42335bae139033d/Objects/listsort.txt">Objects/listsort.txt</a> and <a href="https://github.com/python/cpython/blob/d19de375a204c74ab5f3a28ec42335bae139033d/Objects/listobject.c">Objects/listobject.c</a>. (I should note that when I asked GPT-5.4 Thinking to review Claude's implementation <a href="https://chatgpt.com/share/69b1fc93-f360-8006-b8b7-22c3da639367">it picked holes in it</a> and said the code "is a simplified, Timsort-inspired adaptive mergesort".)</p>
<blockquote>
<p>I don't like the dark color scheme on the buttons, do better</p>
<p>Also add a "run all" button which shows smaller animated charts for every algorithm at once in a grid and runs them all at the same time</p>
</blockquote>
<p>It came up with a color scheme I liked better, "do better" is a fun prompt, and now the "Run all" button produces this effect:</p>
<p><img alt="Animated sorting algorithm race visualization titled &quot;All algorithms racing&quot; with controls for SIZE (50) and SPEED (100), Stop and Shuffle buttons, and a &quot;Back to single&quot; button. A legend shows Comparing (pink), Swapping (orange), Pivot (red), and Sorted (purple) indicators. Seven algorithms race simultaneously in card panels: Bubble sort (Sorting… — Comparisons: 312, Swaps: 250), Selection sort (Sorting… — Comparisons: 550, Swaps: 12), Insertion sort (Sorting… — Comparisons: 295, Swaps: 266), Merge sort (#3 — Comparisons: 225, Swaps: 225), Quick sort (#2 — Comparisons: 212, Swaps: 103), Heap sort (Sorting… — Comparisons: 358, Swaps: 203), and Timsort (#1 — Comparisons: 215, Swaps: 332). Finished algorithms (Timsort, Quick sort, Merge sort) display fully sorted purple bar charts and are highlighted with purple borders." src="https://static.simonwillison.net/static/2026/sorts-32-colors-lossy.gif" />


    <p>Tags: <a href="https://simonwillison.net/tags/algorithms">algorithms</a>, <a href="https://simonwillison.net/tags/computer-science">computer-science</a>, <a href="https://simonwillison.net/tags/javascript">javascript</a>, <a href="https://simonwillison.net/tags/sorting">sorting</a>, <a href="https://simonwillison.net/tags/ai">ai</a>, <a href="https://simonwillison.net/tags/explorables">explorables</a>, <a href="https://simonwillison.net/tags/generative-ai">generative-ai</a>, <a href="https://simonwillison.net/tags/llms">llms</a>, <a href="https://simonwillison.net/tags/claude">claude</a>, <a href="https://simonwillison.net/tags/vibe-coding">vibe-coding</a></p>

## 链接

https://simonwillison.net/2026/Mar/11/sorting-algorithms/#atom-everything

---

*ID: 49556b6924ccd625*
*抓取时间: 2026-03-12T10:14:21.950982*
