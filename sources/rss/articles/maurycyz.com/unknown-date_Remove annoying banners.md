# Remove annoying banners

> 来源: maurycyz.com  
> 发布时间: Tue, 03 Mar 2026 00:00:00 +0000  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<!-- mksite: start of content -->
<p>

This is a small javascript snippet that removes most annoying website elements:
</p>

<pre>
function cleanup(node) {
        var style = getComputedStyle(node);
        // Bad styles
        var bad = (a)=&gt;(["fixed","sticky","hidden","clip"].includes(a));

        // Removes "dick bars" and the such
        if (bad(style.position))
                node.parentNode.removeChild(node);

        // Shows hidden content
        if (bad(style.overflow))  node.style.overflow  = "visible";
        if (bad(style.overflowX)) node.style.overflowX = "visible";
        if (bad(style.overflowY)) node.style.overflowY = "visible";
}

// Run for everything on the page
document.querySelectorAll('*').forEach(cleanup)
</pre>
<p>
<!-- snip -->
</p>
<p>
It's really simple: removing anything that doesn't scroll with the page, and enabling scrolling if it's been disabled. 
This gets rid of cookie popups/banners, recommend&shy;ation sidebars, 
those annoying headers that follow you down the page, etc, etc.
</p><p>
<em>If you don't want to mess around with the JS console</em>, you can drag this link into your bookmark bar, and run it by clicking the bookmark:
</p><p>
<a href="">Cleanup Site</a>
</p><p>
If you need to manually create the bookmark, here's the URL:
</p>
<pre>
javascript:function%20cleanup(node)%7Bvar%20style%3DgetComputedStyle(node)%3Bvar%20bad%3D(a)%3D%3E(%5B%22fixed%22%2C%22sticky%22%2C%22hidden%22%2C%22clip%22%5D.includes(a))%3Bif(bad(style.position))node.parentNode.removeChild(node)%3Bif(bad(style.overflow))node.style.overflow%3D%22visible%22%3Bif%20(bad(style.overflowX))node.style.overflowX%3D%22visible%22%3Bif%20(bad(style.overflowY))node.style.overflowY%3D%22visible%22%3B%7Ddocument.querySelectorAll(%27*%27).forEach(cleanup)
</pre>
<p>
<em>This is a typical website before the script</em>:
</p><p>
<img src="https://maurycyz.com/projects/fixsite/before.png" />
</p><p>
... and after:
</p><p>
<img src="https://maurycyz.com/projects/fixsite/after.png" />
</p><p>
One click to get all your screen space back.
It even works on very complex sites like social media &mdash;
great for when you want to read a longer post without constant distractions.
</p><p>
<em>As a bonus, I made these to fix bad color schemes:</em>
</p><p>
<a href="">
Force dark mode
</a>
</p><p>
<pre>
javascript:function%20colorize(a)%7Ba.style.color%3D%22white%22%3Ba.style.backgroundColor%3D%22black%22%3B%7Ddocument.querySelectorAll(%27*%27).forEach(colorize)
</pre>
</p><p>
... and ...
</p><p>
<a href="">
Force light mode
</a>
</p><p>
<pre>
javascript:function%20colorize(a)%7Ba.style.color%3D%22black%22%3Ba.style.backgroundColor%3D%22white%22%3B%7Ddocument.querySelectorAll(%27*%27).forEach(colorize)
</pre>
</p>
<!-- mksite: end of content -->

## 链接

https://maurycyz.com/projects/fixsite/

---

*ID: 3b048b61c6a771d0*
*抓取时间: 2026-03-05T10:02:14.134464*
