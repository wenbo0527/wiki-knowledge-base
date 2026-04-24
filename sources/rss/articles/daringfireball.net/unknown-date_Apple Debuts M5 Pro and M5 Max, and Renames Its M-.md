# Apple Debuts M5 Pro and M5 Max, and Renames Its M-Series CPU Cores

> 来源: daringfireball.net  
> 发布时间: 2026-03-03T18:11:32Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p>Apple Newsroom:</p>

<blockquote>
  <p>Apple today announced M5 Pro and M5 Max, the world’s most advanced
chips for pro laptops, powering the new MacBook Pro. The chips are
built using a new Apple-designed Fusion Architecture. This
innovative design combines two dies into a single system on a chip
(SoC), which includes a powerful CPU, scalable GPU, Media Engine,
unified memory controller, Neural Engine, and Thunderbolt 5
capabilities. M5 Pro and M5 Max feature a new 18-core CPU
architecture. It includes six of the highest-performing core
design, now called super cores, that are the world’s fastest CPU
core. Alongside these cores are 12 all-new performance cores,
optimized for power-efficient, multithreaded workloads. [...]</p>

<p>The industry-leading super core was first introduced as
performance cores in M5, which also adopts the super core name for
all M5-based products — MacBook Air, the 14-inch MacBook Pro,
iPad Pro, and Apple Vision Pro. This core is the
highest-performance core design with the world’s fastest
single-threaded performance, driven in part by increased front-end
bandwidth, a new cache hierarchy, and enhanced branch prediction.</p>

<p>M5 Pro and M5 Max also introduce an all-new performance core that
is optimized to deliver greater power-efficient, multithreaded
performance for pro workloads. Together with the super cores, the
chips deliver up to 2.5× higher multithreaded performance than M1
Pro and M1 Max. The super cores and performance cores give
MacBook Pro a huge performance boost to handle the most
CPU-intensive pro workloads, like analyzing complex data or
running demanding simulations with unparalleled ease.</p>
</blockquote>

<p>This is a bit confusing, but I think — after a media briefing with Apple reps this morning — I’ve got it straight. From the M1 through M4, there were two CPU core types: efficiency and performance. When the regular M5 chip debuted in October, Apple continued using those same names, efficiency and performance, for its two core types. But as of today, they’re renaming them, and introducing a third core type that they’re calling “performance”. They’re reusing the old <em>performance</em> name for an altogether new CPU core type. So you can see what I mean about it being confusing.</p>

<p>There are now three core types in M5-series CPUs. Efficiency cores are still “efficiency”, but they’re only in the base M5. What used to be called “performance” cores are now called “super” cores, and they’re present in all M5 chips. The new core type — more power-efficient than super cores, more performant than efficiency cores — are taking the old name “performance”. Here are the core counts in table form, with separate rows for the 15- and 18-core M5 Pro variants:</p>

<!-- Markdown table:
|        | Efficiency | Performance | Super |
| ------ | :--------: | :---------: | :---: |
| M5     |     6      | — |   4   |
| M5 Pro | — |     10      |   5   |
| M5 Pro | — |     12      |   6   |
| M5 Max | — |     12      |   6   |
-->

<div class="article">
<table width="500">
<thead>
<tr>
  <th></th>
  <th align="center">Efficiency</th>
  <th align="center">Performance</th>
  <th align="center">Super</th>
</tr>
</thead>
<tbody>
<tr>
  <td>M5</td>
  <td align="center">6</td>
  <td align="center">—</td>
  <td align="center">4</td>
</tr>
<tr>
  <td>M5 Pro</td>
  <td align="center">—</td>
  <td align="center">10</td>
  <td align="center">5</td>
</tr>
<tr>
  <td>M5 Pro</td>
  <td align="center">—</td>
  <td align="center">12</td>
  <td align="center">6</td>
</tr>
<tr>
  <td>M5 Max</td>
  <td align="center">—</td>
  <td align="center">12</td>
  <td align="center">6</td>
</tr>
</tbody>
</table>
</div>

<p>Another way to think about it is that there are regular efficiency cores in the plain M5, and new higher-performing efficiency cores called “performance” in the M5 Pro and M5 Max. The problem is that the old M1–M4 names were clear — one CPU core type was fast but optimized for efficiency so they called it “efficiency”, and the other core type was efficient but optimized for performance so they called it “performance”. Now, the new “performance” core types are the optimized-for-efficiency CPU cores in the Pro and Max chips, and despite their name, they’re not the most performant cores.</p>

<div>
<a href="https://daringfireball.net/linked/2026/03/03/apple-debuts-m5-pro-and-m5-max" title="Permanent link to ‘Apple Debuts M5 Pro and M5 Max, and Renames Its M-Series CPU Cores’">&nbsp;★&nbsp;</a>
</div>

## 链接

https://www.apple.com/newsroom/2026/03/apple-debuts-m5-pro-and-m5-max-to-supercharge-the-most-demanding-pro-workflows/

---

*ID: 8302c9e6b72d8c7d*
*抓取时间: 2026-03-05T10:01:55.507082*
