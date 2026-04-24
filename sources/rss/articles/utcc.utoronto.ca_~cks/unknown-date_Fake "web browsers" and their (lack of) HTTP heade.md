# Fake "web browsers" and their (lack of) HTTP headers: some notes

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-18T03:34:24Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>It's hopefully not news to people that there is a plague of disguised
web crawlers that are imitating web browsers (and not infrequently
crawling from residential IPs, through various extremely questionable
methods). However, many of these crawlers have only a skin-deep
imitation of browsers, primarily done through their <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">HTTP User-Agent
header</a>.
This creates a situation where some of these crawlers can currently
be detected (and blocked) because they either lack entirely or have
non-browser values for other HTTP headers. I've been engaged in a
little campaign to reduce the crawler presence here on <a href="https://utcc.utoronto.ca/~cks/space/blog/">Wandering
Thoughts</a>, so I've been experimenting with a number of HTTP
header checks.</p>

<p>Headers I'm currently looking at include:</p>

<ul><li>The <code>CF-Worker</code> header is set for all requests from Cloudflare Workers.
<a href="https://anubis.techaro.lol/">Anubis</a> blocks all requests with
this header set by default (<a href="https://anubis.techaro.lol/docs/admin/policies/">cf</a>), and I decided
to copy it. This occasionally blocks things trying to scrape
<a href="https://utcc.utoronto.ca/~cks/space/blog/">Wandering Thoughts</a>.<p>
</li>
<li><a href="https://utcc.utoronto.ca/~cks/space/blog/web/XForwardedForOutThere">As I discovered, you can't block requests with X-Forwarded-For
headers</a> because people really do set these
headers on real, non-malicious requests.<p>
</li>
<li>The <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-Fetch-Mode">Sec-Fetch-Mode</a>
header is sent by every modern browser and is sent by almost no
bad crawlers. However, checking things claiming to be Safari is
a little bit complicated, since Sec-Fetch-Mode support was only
added in early 2023 (in 16.4) and there are still older Safari
versions out there (including earlier 16.x versions). This is
a quite effective check in my environment.<p>
(I got this trick from <a href="https://come-from.mad-scientist.club/@algernon/statuses/01KA7ADJ7XPXFYSZA2W7ST81ZS">here</a>,
although <a href="https://blog.sicuranext.com/sec-fetch-and-client-hints-a-powerful-tool-against-automation/">apparently there may be trouble with mobile WebView
interfaces</a>,
which might come about through in-app navigation if someone sends a
URL around.)<p>
</li>
<li>Every mainstream browser sends an <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Encoding">Accept-Encoding</a>
header and has for a long time. If it's missing for a fetch of a
regular HTML page, you have an imposter.
Unless you like maintaining a list of old browsers and other programs
that don't send Accept-Encoding, you probably want to limit requiring
the header to things claiming to be at least a bit like mainstream
browsers.<p>
</li>
<li>Some bad bots are sending an <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Encoding">Accept-Encoding</a> of 'identity' in what is
apparently an attempt to avoid being fed compression bombs by
people (I can't find my source for this). No mainstream browser
should do this and in general most things fetching web pages from
you should accept compressed responses if they advertise an
Accept-Encoding at all.<p>
Sadly, the exception to this is syndication feed fetchers, some of
which refuse to do compression. Whether you keep supporting such
feed fetchers is up to you. <a href="https://utcc.utoronto.ca/~cks/space/blog/">Wandering Thoughts</a> still does
so far, although it's getting tempting to say that enough is enough,
especially with the size of syndication feeds here.<p>
</li>
<li>Some or perhaps many bad crawlers set a HTTP <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept">Accept</a>
header of '*/*' on HTML requests, which isn't something that
real browsers do (<a href="https://kitsunemimi.pw/notes/posts/how-twitter-is-probably-crawling-the-internet-for-ai.html">source</a>).
Unfortunately, browser-based syndication feed fetchers will send
this value, so you can only do this check on HTML pages, and also
bingbot and Googlebot (at least) will sometimes also send this
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept">Accept</a> value. Some things seem to not end an <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept">Accept</a> header
at all, too.<p>
Based on monitoring the results so far, there may be something
funny going on; I've seen the same IP and User-Agent making an
initial request that is fine and then one or more re-requests
for the same URL that have '<code>Accept: */*</code>' and fail<p>
</li>
<li>A number of bad crawlers make HTTP/1.0 requests while claiming to
be mainstream browsers, all of which have supported HTTP/1.1 for
a very long time, and <a href="https://utcc.utoronto.ca/~cks/space/blog/web/HTTP10BlockQuestion">these days I block such requests</a>. Although it's tempting to reject all
HTTP/1.0 requests, some text-mode browsers still make them (the
ones I know of are Lynx and w3m, including inside GNU Emacs). The
HTTP version isn't really a HTTP header, but close enough.</li>
</ul>

<p>Some of these checks overlap with each other. For example, <a href="https://kitsunemimi.pw/notes/posts/how-twitter-is-probably-crawling-the-internet-for-ai.html">the
crawler with a bad Accept: HTTP header</a>
wasn't sending Sec-Fetch-Mode either.</p>

<p>Many of these HTTP headers are only sent by relatively mainstream
browsers and environments that have added support for recent HTTP
headers. For example, people still use text-based browsers and most
of them don't send headers like <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-Fetch-Mode">Sec-Fetch-Mode</a>; other programs
that make HTTP requests through various packages and libraries
probably won't either.</p>

<p>There are probably other useful header differences between crawlers
imitating mainstream browsers and actual browsers (and, apparently,
between headless browsers being driven by automation and real ones
being used by people). You could probably discover some of them by
collecting enough of a data set of request headers and then doing
some sort of statistical analysis to discover correlations and
clusters.</p>

<p>PS: The big offenders for requesting uncompressed syndication feeds
appear to be Tiny Tiny RSS, Selfoss, and Nextcloud-News. Some browser
based syndication feed readers also appear to do it, as do some
curl-based syndication feed fetching that people are doing here.</p>

<h3>Sidebar: What is a (mainstream) browser-like User-Agent?</h3>

<p>It depends on how restrictive you want to be. There are a lot of options:</p>

<ul><li>Just look for "Mozilla/5.0 (" at the start of the User-Agent.</li>
<li>Also look for " Chrome/", " Firefox/", or " AppleWebKit/" in the User-Agent</li>
<li>Try to specifically match a Firefox or Webkit based browser User-Agent
format, which will cause you to learn a lot about what Webkit-based user
agents appear in your logs.<p>
</li>
<li>Potentially exclude things that mark themselves as robots or crawlers,
for example by having 'compatible;' in their User-Agent, or 'robot',
or a URL. Anything with these markers is not trying to exactly be a
browser User-Agent, although they may be looking generally like one.</li>
</ul>

<p>I use different versions of these for different checks in <a href="https://utcc.utoronto.ca/~cks/space/dwiki/DWiki">DWiki</a>'s
steadily growing pile of hacks to detect bad crawlers. Currently
the most specific matching is reserved for <a href="https://utcc.utoronto.ca/~cks/cspace-cloud-browser.html">blocking claimed
browsers from cloud/server space</a>,
which catches a significant amount even with a limited selection
of cloud and VPS provider space that it applies to.</p>

<p>(<a href="https://utcc.utoronto.ca/~cks/space/blog/web/DoYouNeedCloudRequests">Some cloud space is blocked entirely</a>;
blocking only things that claim to be browsers is a lesser step.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/web/FakeBrowsersAndHTTPHeaders?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/FakeBrowsersAndHTTPHeaders

---

*ID: 6db190e2de4f1285*
*抓取时间: 2026-03-12T13:49:26.048951*
