# Some notes on using the Sec-CH-UA HTTP headers that Chrome supports

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-25T02:39:10Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>A while back, Chrome proposed and implemented what are called <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Client_hints#user_agent_client_hints">user
agent hints</a>,
which are <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers#user_agent_client_hints">a collection of Sec-CH-UA HTTP headers</a>
that can provide you with additional information about the browser
beyond what the HTTP <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent</a>
header provides. As mentioned, only Chrome and browsers derived
from Chromium (or if you prefer, 'Blink') support these headers,
and only since early 2021 (for Chrome; later for some others).
However, Chrome is what a lot of people use. More to the point,
Chrome is what a lot of bad crawlers claim to be in their User-Agent
header. As has been written up by other people, <a href="https://blog.sicuranext.com/sec-fetch-and-client-hints-a-powerful-tool-against-automation/">you can use these
headers to detect inconsistencies that give away crawlers</a>.</p>

<p>In an ideal world, it would be enough to detect a recent enough
Chrome version and then require it to be consistent between the
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent</a>, the platform from <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA-Platform">Sec-CH-UA-Platform</a>,
and the version information from <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA">Sec-CH-UA</a>.
We don't live in an ideal world. The first issue is that some
versions of Chrome don't send these <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Client_hints#user_agent_client_hints">user agent hints</a> by default
(I've seen this specifically from Android Pixel devices). To get
them to do so, you must reply with a <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/307">HTTP 307</a>
redirection that includes <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-CH">Accept-CH</a>
and <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Critical-CH">Critical-CH</a>
headers for the Sec-CH-UA headers you care about. I'm not sure if
you can redirect the browser to the current URL; I opt to redirect
to the URL with a special query parameter added, which then redirects
back to the original version of the URL.</p>

<p>(One advantage of this is that in my HTTP request handling, I can
reject a request with the special query parameter if it still doesn't
including the Sec-CH-UA headers I ask for. This avoids infinite
redirect loops and lets me log definite failures. Chrome browser
setups that refuse to provide them even when requested are currently
redirected to <a href="https://utcc.utoronto.ca/~cks/cspace-sec-ch-mismatch.html">an error page explaining the situation</a>.)</p>

<p>Cross checking the browser version from <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA">Sec-CH-UA</a> against the
'browser version' in the <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent</a> is complicated by the
question of <a href="https://utcc.utoronto.ca/~cks/space/blog/web/BrowserVersionsComplicated">what is a browser version</a>.
This is especially the case because the 'brand names' used in
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA">Sec-CH-UA</a> aren't necessarily the '&lt;whatever>/&lt;ver>' names used
in the User-Agent; for example, Microsoft Edge will report itself
as 'Microsoft Edge' in <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA">Sec-CH-UA</a> but 'Edg/' in the User-Agent.
Some browsers based on Chrome will report a Chrome version that is
the same as their brand name version (this appears to be true for
Edge, for example), but others definitely won't, so you may need a
mapping table from brand name to User-Agent name if you want to go
that far. Sometimes the best you can do is verify the claimed
'Chromium' version against the 'Chrome/' version from the User-Agent.</p>

<p>Platform names definitely require a mapping from the <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA-Platform">Sec-CH-UA-Platform</a>
value to what appears in the <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent</a>. On top of that, sometimes
browsers will change their User-Agent platform name without changing
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA-Platform">Sec-CH-UA-Platform</a>. One case I know of is that some versions
of Android Opera (and perhaps Chrome) will change their User-Agent
to say they're on Linux if you have them ask for the 'desktop'
version of a site, but still report the Android values in their
Sec-CH-UA headers (and say that they aren't a mobile device in
<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA-Mobile">Sec-CH-UA-Mobile</a>,
which is fair enough). It's hard to object to this behavior in a
world where User-Agent sniffing is one way that websites decide on
regular versus 'mobile' versions.</p>

<p>My use of Sec-CH-UA checks so far here on <a href="https://utcc.utoronto.ca/~cks/space/blog/">Wandering Thoughts</a> has turned up several sorts of bad behavior in crawlers (so
far). As I sort of expected, the most common behavior is crawlers
that claim to be Chrome in their <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent</a> (or something derived
from it) but don't supply any Sec-CH-UA headers; <a href="https://utcc.utoronto.ca/~cks/space/blog/web/BrowserLikeUserAgentBadIdeaNow">this is now a
straightforward bad idea</a> even if
you mention your crawler in your User-Agent. Some crawlers report
one Chrome version in Sec-CH-UA but another one in their <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent">User-Agent</a>,
usually with the User-Agent version being older. I suspect that
these crawlers are based on Chromium and periodically update their
Chromium version, but statically configure their User-Agent and
don't update it. Some of these crawlers also report a different
platform between Sec-CH-UA-Platform and their User-Agent (so far
all of them have been running on macOS but saying they were Windows
10 or 11 machines in their User-Agent).  The third case is things
that report they are headless Chrome in their <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA">Sec-CH-UA</a> header
(and I reject them).</p>

<p>(This is where <a href="https://mastodon.social/@cks/115759106642448477">the Internet Archive gets a dishonorable mention</a>; currently their
crawling often has mismatched User-Agent and Sec-CH-UA headers.
Sometimes they have a special marker in the User-Agent and sometimes
it's just mismatched Chrome information.)</p>

<p>I've also seen some weird cases so far where a crawler provided
Sec-CH-UA headers despite claiming to be Firefox in its User-Agent.
My data so far is incomplete, but some of these have had mismatches
between Sec-CH-UA-Platform and the User-Agent, while another claimed
to be Chrome 88 (which in theory is before Chrome supported them)
while saying it was Firefox 120 in its User-Agent. I've improved
my logging and error reporting so I may get slightly better data
on this in a while.</p>

<p>At the same time, checking Sec-CH-UA headers (and checking them
against User-Agent headers) will definitely not defeat all bad
crawlers. Some crawlers are clearly using either real browsers or
software that fakes everything together properly. I suspect the
latter because the most recent case involves a horde of IPs claiming
to be Chrome 142 on macOS 10.15.7, which I doubt is so universal a
configuration (especially on datacenter VPSes and servers). As with
email spam, all of this is a constant race of heuristics against
the bad actors.</p>

<p>(It's hard to judge my new Sec-CH-UA checks compared to <a href="https://utcc.utoronto.ca/~cks/space/blog/web/FakeBrowsersAndHTTPHeaders">my existing
header checks</a> because of check ordering.
If I was sufficiently energetic I'd try to do all of the checks
before rejecting anything and log all failed checks, but as it is
I do checks one by one and reject (or redirect with <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Critical-CH">Critical-CH</a>)
at the first failed one.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/HTTPSecCHUAHeaderNotes

---

*ID: 685186b1755014b0*
*抓取时间: 2026-03-12T13:49:26.048879*
