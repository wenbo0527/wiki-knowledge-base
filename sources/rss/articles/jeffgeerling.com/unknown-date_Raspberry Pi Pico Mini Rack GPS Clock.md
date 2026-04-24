# Raspberry Pi Pico Mini Rack GPS Clock

> 来源: jeffgeerling.com  
> 发布时间: Mon, 12 Jan 2026 09:00:00 -0600  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p>I wanted to have the most accurate timepiece possible mounted in my mini rack. Therefore I built this:</p>
<figure class="insert-image"><img alt="Raspberry Pi Pico GPS Clock for Mini Rack" height="auto" src="https://www.jeffgeerling.com/blog/2026/pico-gps-clock-mini-rack/pico-gps-clock-mini-rack.jpg" width="700" />
</figure>

<p>This is a GPS-based clock running on a Raspberry Pi Pico in a custom 1U 10&quot; rack faceplate. The clock displays time based on a GPS input, and will not display time until a GPS timing lock has been acquired.</p>
<ul>
<li>When you turn on the Pico, the display reads <code>----</code></li>
<li>Upon 3D fix, you get a time on the clock, and the colon starts blinking</li>
<li>If the 3D fix is lost, the colon goes solid</li>
<li>When the 3D fix is regained, the colon starts blinking again</li>
</ul>
<p>For full details on designing and building this clock, see:</p>

## 链接

https://www.jeffgeerling.com/blog/2026/pico-gps-clock-mini-rack/

---

*ID: 58226ca4918fadae*
*抓取时间: 2026-03-05T10:01:52.005261*
