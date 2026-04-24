# ChangeTheHeaders

> 来源: daringfireball.net  
> 发布时间: 2026-03-02T21:10:50Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p>During <a href="https://daringfireball.net/thetalkshow/2026/02/28/ep-442">the most recent episode of The Talk Show</a>, Jason Snell brought up a weird issue that I started running into last year. On my Mac, sometimes I’d drag an image out of a web page in Safari, and I’d get an image in <a href="https://en.wikipedia.org/wiki/WebP">WebP</a> format. Sometimes I wouldn’t care. But usually when I download an image like that, it’s because I want to publish (or merely host my own copy of) that image on Daring Fireball. And I don’t publish WebP images — I prefer PNG and JPEG for compatibility.</p>

<p>What made it weird is when I’d view source on the original webpage, the original image was usually in PNG or JPEG format. If I opened the image in a new tab — just the image — I’d get it in PNG or JPEG format. But when I’d download it by dragging out of the original webpage, I’d get a WebP. This was a total WTF for me.</p>

<p>I turned to my friend <a href="https://lapcatsoftware.com/articles/">Jeff Johnson</a>, author of, <a href="https://underpassapp.com/">among other things</a>, the excellent Safari extension <a href="https://underpassapp.com/StopTheMadness/">StopTheMadness</a>. Not only was Johnson able to explain what was going on, he actually made a new Safari extension called ChangeTheHeaders that fixed the problem for me. Johnson, announcing ChangeTheHeaders last year:</p>

<blockquote>
  <p>After some investigation, I discovered that the difference was the
<a href="https://developer.mozilla.org/docs/Web/HTTP/Reference/Headers/Accept">Accept HTTP request header</a>, which specifies what types of
response the web browser will accept. Safari’s default Accept
header for images is this:</p>

<p><code>Accept:
image/webp,image/avif,image/jxl,image/heic,image/heic-sequence,video/*;q=0.8,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5</code></p>

<p>Although <code>image/webp</code> appears first in the list, the order
actually doesn’t matter. The <a href="https://developer.mozilla.org/docs/Glossary/Quality_values">quality value</a>, specified by
the <code>;q=</code> suffix, determines the ranking of types. The range of
values is 0 to 1, with 1 as the default value if none is
specified. Thus, <code>image/webp</code> and <code>image/png</code> have equal
precedence, equal quality value 1, leaving it up to the web site
to decide which image type to serve. In this case, the web site
decided to serve a WebP image, despite the fact that the image
URL has a <code>.png</code> suffix. In a URL, unlike in a file path, the
“file extension”, if one exists, is largely meaningless. A very
simple web server will directly match a URL with a local file
path, but a more complex web server can do almost anything it
wants with a URL.</p>
</blockquote>

<p>This was driving me nuts. Thanks to Johnson, I now understand why it was happening, and I had a simple set-it-and-forget-it tool to fix it. Johnson writes:</p>

<blockquote>
  <p>What can you do with ChangeTheHeaders? I suspect the biggest
selling point will be to spoof the User-Agent. The extension
allows you to customize your User-Agent by URL domain. For
example, you can make Safari pretend that it’s Chrome on Google
web apps that give special treatment to Chrome. You can also
customize the <a href="https://developer.mozilla.org/docs/Web/HTTP/Reference/Headers/Accept-Language">Accept-Language</a> header if you don’t like the
default language handling of some website, such as YouTube.</p>
</blockquote>

<p>Here’s the custom rule I applied a year ago, when I first installed ChangeTheHeaders (<a href="https://daringfireball.net/misc/2026/02/changetheheaders-no-webp.png">screenshot</a>):</p>

<p>Header: <code>Accept</code> <br />
Value: <code>image/avif,image/jxl,image/heic,image/heic-sequence,video/*;q=0.8,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5</code> <br />
URL Domains: «<em>leave blank for all domains</em>» <br />
URL Filter: «<em>leave blank for all URLs</em>» <br />
Resource Types: <code>image</code></p>

<p>I haven’t seen a single WebP since.</p>

<p>ChangeTheHeaders works everywhere Safari does — Mac, iPhone, iPad, Vision Pro — and <a href="https://apps.apple.com/us/app/changetheheaders-for-safari/id6743129567">you can get it for just $7 on the App Store</a>.</p>

<div>
<a href="https://daringfireball.net/linked/2026/03/02/changetheheaders" title="Permanent link to ‘ChangeTheHeaders’">&nbsp;★&nbsp;</a>
</div>

## 链接

https://underpassapp.com/news/2025/3/4.html

---

*ID: c8a8883b01bb5c61*
*抓取时间: 2026-03-05T10:01:55.507097*
