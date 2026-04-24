# The importance of limiting syndication feed requests in some way

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-22T01:27:33Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>People sometimes wonder why I care so much about <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Conditional_requests">HTTP conditional
GETs</a>
and rate limiting for syndication feed fetchers. There are multiple
reasons, including <a href="https://utcc.utoronto.ca/~cks/space/blog/web/WeShouldBlockForSocialReasons">social reasons to establish norms</a>, but one obvious one is transfer
volumes. To illustrate that, I'll look at the statistics for yesterday
for feed fetches of the main syndication feed for <a href="https://utcc.utoronto.ca/~cks/space/blog/">Wandering
Thoughts</a>.</p>

<p>Yesterday there were 7492 feed requests that got HTTP 200 responses,
9419 feed requests that got HTTP 304 Not Modified responses, and
11941 requests that received <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/429">HTTP 429</a>
responses. The HTTP 200 responses amounted to about 1.26 GBytes,
with the average response size being 176 KBytes. This average
response size is actually a composite; typical compressed syndication
feed responses are on the order of 160 KBytes, while uncompressed
ones are on the order of 540 KBytes (but there look to have been
only 313 of them, which is fortunate; even still they're 12% of the
transfer volume).</p>

<p>If feed readers didn't do any conditional GETs and I didn't have
any rate limiting (and all of the requests that got HTTP 429s would
still have been made), the additional feed requests would have
amounted to about another 3.5 GBytes of responses sent out to people.
Obviously feed readers did do conditional GETS, and 66% of their
non rate limited requests were successful conditional GETs.  A HTTP
200 response ratio of 44% is probably too pessimistic once we include
rate limited requests, so as an extreme approximation we'll guess
that 33% of the rate limited requests would have received HTTP 200
responses with a changed feed; that would amount to another 677
MBytes of response traffic (which is less than I expected). If we
use the 44% HTTP 200 ratio, it's still only 903 MBytes more.</p>

<p>(This 44% rate may sound high but my syndication feed changes any
time someone leaves a comment on a recent entry, because the
syndication feed of entries includes a comment count for every
entry.)</p>

<p>Another statistic is that 41% of syndication feed requests yesterday
got HTTP 429 responses. The most prolific single IP address received
950 HTTP 429s, <a href="https://utcc.utoronto.ca/~cks/space/blog/web/WebRequestTotalsToRequestRates">which maps to an average request interval of less
than two minutes between requests</a>.
Another prolific source made 779 requests, which again amounts to
an interval of just less than two minutes. There are over 20 single
IPs that received more than 96 HTTP 429 responses (which corresponds
to an average interval of 15 minutes). There is a lot of syndication
feed fetching software out there that is fetching quite frequently.</p>

<p>(Trying to figure out how many HTTP 429 sources did conditional
requests is too complex with my current logs, since I don't directly
record that information.)</p>

<p>You can avoid the server performance impact of lots of feed fetching
by arranging to serve syndication feeds from static files instead
of a dynamic system (and then you can limit how frequently you
update those files, effectively forcing a maximum number of HTTP
200 fetches per time interval on anything that does conditional
GETs). You can't avoid the bandwidth effects, and serving from
static files generally leaves you with only modest tools for rate
limiting.</p>

<p>PS: The syndication feeds for <a href="https://utcc.utoronto.ca/~cks/space/blog/">Wandering Thoughts</a> are so big
because I've opted to default to 100 entries in them, but I maintain
you should be able to do this sort of thing without having your
bandwidth explode.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/web/FeedLimitingImportance?showcomments#comments">7 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/FeedLimitingImportance

---

*ID: 3f20d9b09674aefa*
*抓取时间: 2026-03-12T13:49:26.048235*
