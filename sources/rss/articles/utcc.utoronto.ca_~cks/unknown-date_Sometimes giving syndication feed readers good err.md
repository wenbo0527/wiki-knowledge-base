# Sometimes giving syndication feed readers good errors is a mistake

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-16T03:56:00Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Yesterday I wrote about <a href="https://utcc.utoronto.ca/~cks/space/blog/web/FeedReaderErrorsProblem">the problem of giving feed readers error
messages that people will actually see</a>,
because you can't just give them HTML text; in practice you have
to wrap your HTML text up in a stub, single-entry syndication feed
(and then serve it with a HTTP 200 success code). In many situations
you're going to want to do this by replying to the initial feed
request with a <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/302">HTTP 302 temporary redirection</a>
that winds up on your stub syndication feed (instead of, say, a
general HTML page explaining things, such as "this resource is out
of service but you might want to look at ...").</p>

<p>Yesterday I put this into effect for certain sorts of problems,
including <a href="https://utcc.utoronto.ca/~cks/space/blog/web/OldBrowsersCrawlerProblem">claimed HTTP User-Agents that are for old browser</a>. Then several people reported that this
had caused Feedly to start presenting my feed as the special 'your
feed reader is (claiming to be) a too-old browser' single entry
feed. The apparent direct cause of this is that Feedly made some
syndication feed requests with <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">HTTP User-Agent</a>
headers of old versions of Chrome and Firefox, which wound up getting
a series of HTTP 302 temporary redirections to my new 'your feed
reader is a too-old browser' stub feed. Feedly then decided to
switch its main feed fetcher over to directly using this new URL
for various feeds, despite the HTTP redirections being temporary
(and not served for its main feed fetcher, which uses "Feedly/1.0"
for its User-Agent).</p>

<p>Feedly has been making these fake browser User-Agent syndication
feed fetch attempts for some time, and for some time they've been
getting HTTP 302 redirections. However, up until late yesterday,
what Feedly wound up on was <a href="https://utcc.utoronto.ca/~cks/cspace-old-browser.html">a regular HTML web page</a>. I have to assume that since this
wasn't a valid syndication feed, Feedly ignored it. Only when I did
the right thing to give syndication feed readers a good, useful
error result did Feedly receive a valid syndication feed and go
over the cliff.</p>

<p>Providing a stub syndication feed to communicate errors and problems
to syndication feed fetchers is clearly the technically correct
answer. However, I'm now somewhat less convinced that it's the
most useful answer in practice. In practice, plenty of syndication
feed fetchers keep fetching and re-fetching these stub feeds from
me, suggesting that people either aren't seeing them or aren't doing
anything about it. And now I've seen a feed reader malfunction
spectacularly and in a harmful way because I gave it a valid
syndication feed result at the end of a temporary HTTP redirection.</p>

<p>(I will probably stick to the current situation, partly because <a href="https://utcc.utoronto.ca/~cks/space/blog/web/WeShouldBlockForSocialReasons">I
no longer feel like accepting bad behavior from web agents</a>.)</p>

<p>PS: If you're a feed fetching system, please give your feeds IDs
that you put in the User-Agent, so that when they all wind up shifted
to the same URL through some misfortune, the website involved can
sort them out and redirect them back to the proper URLs.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/web/FeedReaderErrorsProblemII?showcomments#comments">3 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/FeedReaderErrorsProblemII

---

*ID: 88c21f6a9c470406*
*抓取时间: 2026-03-12T13:49:26.048305*
