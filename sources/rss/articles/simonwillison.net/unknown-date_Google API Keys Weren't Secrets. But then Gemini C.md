# Google API Keys Weren't Secrets. But then Gemini Changed the Rules.

> 来源: simonwillison.net  
> 发布时间: 2026-02-26T04:28:55+00:00  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><strong><a href="https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules">Google API Keys Weren&#x27;t Secrets. But then Gemini Changed the Rules.</a></strong></p>
Yikes! It turns out Gemini and Google Maps (and other services) share the same API keys... but Google Maps API keys are designed to be public, since they are embedded directly in web pages. Gemini API keys can be used to access private files and make billable API requests, so they absolutely should not be shared.</p>
<p>If you don't understand this it's very easy to accidentally enable Gemini billing on a previously public API key that exists in the wild already.</p>
<blockquote>
<p>What makes this a privilege escalation rather than a misconfiguration is the sequence of events. </p>
<ol>
<li>A developer creates an API key and embeds it in a website for Maps. (At that point, the key is harmless.) </li>
<li>The Gemini API gets enabled on the same project. (Now that same key can access sensitive Gemini endpoints.) </li>
<li>The developer is never warned that the keys' privileges changed underneath it. (The key went from public identifier to secret credential).</li>
</ol>
</blockquote>
<p>Truffle Security found 2,863 API keys in the November 2025 Common Crawl that could access Gemini, verified by hitting the <code>/models</code> listing endpoint. This included several keys belonging to Google themselves, one of which had been deployed since February 2023 (according to the Internet Archive) hence predating the Gemini API that it could now access.</p>
<p>Google are working to revoke affected keys but it's still a good idea to check that none of yours are affected by this.

    <p><small></small>Via <a href="https://news.ycombinator.com/item?id=47156925">Hacker News</a></small></p>


    <p>Tags: <a href="https://simonwillison.net/tags/api-keys">api-keys</a>, <a href="https://simonwillison.net/tags/google">google</a>, <a href="https://simonwillison.net/tags/security">security</a>, <a href="https://simonwillison.net/tags/gemini">gemini</a></p>

## 链接

https://simonwillison.net/2026/Feb/26/google-api-keys/#atom-everything

---

*ID: 1ae46fb7e56c4419*
*抓取时间: 2026-03-05T10:01:51.143484*
