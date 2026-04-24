# Browser version numbers are a bit complicated (for server code)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-22T04:15:53Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Suppose, not entirely hypothetically, that you're writing code that
for some reason wants to determine a 'browser version' from something
and then cross-check it against other sources of browser version
information. Possibly <a href="https://utcc.utoronto.ca/~cks/space/blog/web/BrowserLikeUserAgentBadIdeaNow">you also want to notice when you're not
working with real browsers</a> and not
apply your version consistency checks to them. When you're starting
out, it looks like what your code should do is return a browser
name and version number. Unfortunately, this is a naive view, partly
because of all of the browsers based on Chrome (or Chromium) and
partly because of mobile device <a href="https://en.wikipedia.org/wiki/WebView">WebViews</a>, which reuse a browser
engine without being the browser.</p>

<p>The theoretically correct and maximally flexible approach would be
to parse all possible version indicators of everything from whatever
source of information you're using, such as the browser <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent</a>
or <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Client_hints#user_agent_client_hints">user agent client hints</a>,
and return them as a big map, possibly augmented with your best
guess at what the 'browser' as such is. If applied to a User-Agent
string such as this:</p>

<blockquote><pre style="white-space: pre-wrap;">
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 OPR/125.0.0.0
</pre>
</blockquote>

<p>Parsing this might give you identifiers and versions of AppleWebKit
537.36, Chrome 141, Safari 537.36, and OPR 125, and you'd guess
that the browser is Opera and it's based on Chromium 141 (which is
potentially important for what features and behavior should be
present). There are complications in parsing this, because sometimes
you'll see "Mobile Safari/537.36", and sometimes you'll see mysterious
additions like 'Version/4.0' or 'ABB/133.0.6943.51' (and I haven't
even gone into what you might see on iOS). Simply fully parsing the
User-Agent string is complicated (although there are projects that
do this for you, such as the <a href="https://github.com/ua-parser">User Agent String Parser</a> and the Python <a href="https://pypi.org/project/user-agents/">user-agents</a> package).</p>

<p>(For instance, did you know that Firefox reports its Gecko version
in at least two ways? On desktop Firefox, it's always 'Gecko/20100101'.
On Android Firefox, it can be 'Gecko/146.0', perhaps always matching
the Firefox/ version.)</p>

<p>One problem is that a giant map is not necessarily entirely useful
to code that wants to use browser version information, especially
since the browser names in data may not match the common names you
know them by. For example, on iOS devices Firefox reports 'FxiOS'
and Chrome reports 'CriOS', which is in one sense accurate because
these two iOS browsers don't have the behavior of their regular
counterparts since they're built on top of Apple's WebKit, not their
own browser engines (and as a result Chrome on iOS doesn't report
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Client_hints#user_agent_client_hints">user agent client hints</a>). Do you want to treat FxiOS as a
different browser from Firefox or not? That depends.</p>

<p>Currently, the minimum information I think you want to provide is
the name and version of both the browser engine and the 'browser'
itself. Given WebViews, Chromium, and other similar situations, you
may not be able to reliably determine the browser, and sometimes
you won't have either. When parsing the User-Agent string for Chrome,
you don't get an explicit version for Chromium, so you have to
assume it's the same as the Chrome version; for Chrome derived
browsers I think you can assume that the 'Chrome/...' version
reported is the version of their underlying Chromium. If present,
the HTTP <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA">Sec-CH-UA</a>
header can give you the Chromium version directly and also perhaps
tell you if you have a genuine Chrome or another brand where you
(or your User-Agent parser) don't recognize their User-Agent marker.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/BrowserVersionsComplicated

---

*ID: 26f004ec3c27fc5b*
*抓取时间: 2026-03-12T13:49:26.048910*
