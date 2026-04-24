# It's now a bad idea to look like a browser in your HTTP User-Agent

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-20T03:34:16Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Once upon a time, something like the following was a perfectly decent
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent</a>
header string for a web crawler or a web fetching agent:</p>

<blockquote><pre style="white-space: pre-wrap;">
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 (compatible; Yourbot; +https://some/url)
</pre>
</blockquote>

<p>You weren't hiding, after all, you called yourself 'Yourbot', and
for the rest, you were asking for people to serve you pages like
you were Chrome. Well, I'm not too sad to say, those days are over.</p>

<p>They're over because an increasing number of websites are increasingly
requiring that anything that looks like a browser in its User-Agent
also act like a browser, in specific the browser and browser version
it's saying it is, and <a href="https://utcc.utoronto.ca/~cks/space/blog/web/FakeBrowsersAndHTTPHeaders">there are a lot of picky details around
other HTTP headers</a> (<a href="https://blog.sicuranext.com/sec-fetch-and-client-hints-a-powerful-tool-against-automation/">also</a>).
For example, often simply having 'Mozilla' in your User-Agent will
cause <a href="https://anubis.techaro.lol/">Anubis</a> to challenge your
crawler (<a href="https://anubis.techaro.lol/docs/admin/policies/">cf</a>).
And the version of Chrome being asserted here is new enough that
it should be reporting a <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA-Platform">Sec-CH-UA-Platform header</a>,
among other Sec-CH- headers.</p>

<p>(<a href="https://utcc.utoronto.ca/~cks/space/blog/web/OldBrowsersCrawlerProblem">Claiming to be a really old version of Chrome without those
features is likely to be worse</a>.)</p>

<p>Now, you can certainly pin your hopes on the idea that people who
are writing header checking code will pay attention to the presence
of the 'compatible;' and the URL in your User-Agent, and realize
that you're not actually a browser despite you having a fairly good
imitation of a Chrome User-Agent. However, <a href="https://utcc.utoronto.ca/~cks/space/blog/web/SmallCrawlersGettingFeedback">you're not Google(bot)</a>. People have to make exceptions for
Googlebot (to some degree), but they don't have to make exceptions
for you and they probably won't.</p>

<p>The User-Agent you should instead use today is something like, for
example:</p>

<blockquote><pre style="white-space: pre-wrap;">
Fedithing/4.5.1 (library/1.2.3; +https://some/url)
</pre>
</blockquote>

<p>You don't start with a superstitious invocation of 'Mozilla/5.0',
you don't claim to be be like any version of any browser, and you
put in the basics of identifying your software and yourself so no
one can accuse you of hiding. No one is going to match your User-Agent
against detectors for old versions of browsers, or things claiming
to be browser but lacking their headers, and so on, because you
haven't put in the names of any browsers.</p>

<p>PS: Googlebot and Bingbot and a few others still use User-Agent
strings very much like my first example, but they're Googlebot (and
Bingbot) and to a fair extent they do get their HTTP headers
relatively authentic.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/BrowserLikeUserAgentBadIdeaNow

---

*ID: 338b5f958a5ec7b2*
*抓取时间: 2026-03-12T13:49:26.048930*
