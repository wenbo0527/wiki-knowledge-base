# Unicode Explorer using binary search over fetch() HTTP range requests

> 来源: simonwillison.net  
> 发布时间: 2026-02-27T17:50:54+00:00  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><strong><a href="https://tools.simonwillison.net/unicode-binary-search">Unicode Explorer using binary search over fetch() HTTP range requests</a></strong></p>
Here's a little prototype I built this morning from my phone as an experiment in HTTP range requests, and a general example of using LLMs to satisfy curiosity.</p>
<p>I've been collecting <a href="https://simonwillison.net/tags/http-range-requests/">HTTP range tricks</a> for a while now, and I decided it would be fun to build something with them myself that used binary search against a large file to do something useful.</p>
<p>So I <a href="https://claude.ai/share/47860666-cb20-44b5-8cdb-d0ebe363384f">brainstormed with Claude</a>. The challenge was coming up with a use case for binary search where the data could be naturally sorted in a way that would benefit from binary search.</p>
<p>One of Claude's suggestions was looking up information about unicode codepoints, which means searching through many MBs of metadata.</p>
<p>I had Claude write me a spec to feed to Claude Code - <a href="https://github.com/simonw/research/pull/90#issue-4001466642">visible here</a> - then kicked off an <a href="https://simonwillison.net/2025/Nov/6/async-code-research/">asynchronous research project</a> with Claude Code for web against my <a href="https://github.com/simonw/research">simonw/research</a> repo to turn that into working code.</p>
<p>Here's the <a href="https://github.com/simonw/research/tree/main/unicode-explorer-binary-search#readme">resulting report and code</a>. One interesting thing I learned is that Range request tricks aren't compatible with HTTP compression because they mess with the byte offset calculations. I added <code>'Accept-Encoding': 'identity'</code> to the <code>fetch()</code> calls but this isn't actually necessary because Cloudflare and other CDNs automatically skip compression if a <code>content-range</code> header is present.</p>
<p>I deployed the result <a href="https://tools.simonwillison.net/unicode-binary-search">to my tools.simonwillison.net site</a>, after first tweaking it to query the data via range requests against a CORS-enabled 76.6MB file in an S3 bucket fronted by Cloudflare.</p>
<p>The demo is fun to play with - type in a single character like <code>ø</code> or a hexadecimal codepoint indicator like <code>1F99C</code> and it will binary search its way through the large file and show you the steps it takes along the way:</p>
<p><img alt="Animated demo of a web tool called Unicode Explore. I enter the ampersand character and hit Search. A box below shows a sequence of HTTP binary search requests made, finding in 17 steps with 3,864 bytes transferred and telling me that ampersand is U+0026 in Punctuation other, Basic Latin" src="https://static.simonwillison.net/static/2026/unicode-explore.gif" />


    <p>Tags: <a href="https://simonwillison.net/tags/algorithms">algorithms</a>, <a href="https://simonwillison.net/tags/http">http</a>, <a href="https://simonwillison.net/tags/research">research</a>, <a href="https://simonwillison.net/tags/tools">tools</a>, <a href="https://simonwillison.net/tags/unicode">unicode</a>, <a href="https://simonwillison.net/tags/ai">ai</a>, <a href="https://simonwillison.net/tags/generative-ai">generative-ai</a>, <a href="https://simonwillison.net/tags/llms">llms</a>, <a href="https://simonwillison.net/tags/ai-assisted-programming">ai-assisted-programming</a>, <a href="https://simonwillison.net/tags/vibe-coding">vibe-coding</a>, <a href="https://simonwillison.net/tags/http-range-requests">http-range-requests</a></p>

## 链接

https://simonwillison.net/2026/Feb/27/unicode-explorer/#atom-everything

---

*ID: d2ef8b38b7246b45*
*抓取时间: 2026-03-05T10:01:51.143475*
