# tldraw issue: Move tests to closed source repo

> 来源: simonwillison.net  
> 发布时间: 2026-02-25T21:06:53+00:00  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><strong><a href="https://github.com/tldraw/tldraw/issues/8082">tldraw issue: Move tests to closed source repo</a></strong></p>
It's become very apparent over the past few months that a comprehensive test suite is enough to build a completely fresh implementation of any open source library from scratch, potentially in a different language.</p>
<p>This has worrying implications for open source projects with commercial business models. Here's an example of a response: tldraw, the outstanding collaborative drawing library (see <a href="https://simonwillison.net/2023/Nov/16/tldrawdraw-a-ui/">previous coverage</a>), are moving their test suite to a private repository - apparently in response to <a href="https://blog.cloudflare.com/vinext/">Cloudflare's project to port Next.js to use Vite in a week using AI</a>.</p>
<p>They also filed a joke issue, now closed to <a href="https://github.com/tldraw/tldraw/issues/8092">Translate source code to Traditional Chinese</a>:</p>
<blockquote>
<p>The current tldraw codebase is in English, making it easy for external AI coding agents to replicate. It is imperative that we defend our intellectual property.</p>
</blockquote>
<p>Worth noting that tldraw aren't technically open source - their <a href="https://github.com/tldraw/tldraw?tab=License-1-ov-file#readme">custom license</a> requires a commercial license if you want to use it in "production environments".</p>
<p><strong>Update</strong>: Well this is embarrassing, it turns out the issue I linked to about removing the tests was <a href="https://github.com/tldraw/tldraw/issues/8082#issuecomment-3964650501">a joke as well</a>:</p>
<blockquote>
<p>Sorry folks, this issue was more of a joke (am I allowed to do that?) but I'll keep the issue open since there's some discussion here. Writing from mobile</p>
<ul>
<li>moving our tests into another repo would complicate and slow down our development, and speed for us is more important than ever</li>
<li>more canvas better, I know for sure that our decisions have inspired other products and that's fine and good</li>
<li>tldraw itself may eventually be a vibe coded alternative to tldraw</li>
<li>the value is in the ability to produce new and good product decisions for users / customers, however you choose to create the code</li>
</ul>
</blockquote>

    <p><small></small>Via <a href="https://twitter.com/steveruizok/status/2026581824428753211">@steveruizok</a></small></p>


    <p>Tags: <a href="https://simonwillison.net/tags/open-source">open-source</a>, <a href="https://simonwillison.net/tags/cloudflare">cloudflare</a>, <a href="https://simonwillison.net/tags/ai-ethics">ai-ethics</a></p>

## 链接

https://simonwillison.net/2026/Feb/25/closed-tests/#atom-everything

---

*ID: 9b7e65115cb0012f*
*抓取时间: 2026-03-05T10:01:51.143491*
