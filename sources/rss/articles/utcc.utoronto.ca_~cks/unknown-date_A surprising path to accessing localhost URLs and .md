# A surprising path to accessing localhost URLs and HTTP services

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-06T03:43:36Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of the classic challenges in web security is <a href="https://en.wikipedia.org/wiki/DNS_rebinding">DNS rebinding</a>. The simple version
is that you put some web service on localhost in order to keep
outside people from accessing it, and then some joker out in the
world makes 'evil.example.org' resolve to 127.0.0.1 and arranges
to get you to make requests to it. Sometimes this is through
JavaScript in a browser, and sometimes this is by getting you to
fetch things from URLs they supply (because you're running a service
that fetches and processes things from external URLs, for example).</p>

<p>One way people defend against this is by screening out 127.0.0.0/8,
IPv6's ::1, and other dangerous areas of IP address space from DNS
results (either in the DNS resolver or in your own code). And you
can also block URLs with these as explicit IP addresses, or 'localhost'
or the like. Sometimes you might add extra security restrictions to a
process or an environment through means like Linux eBPF to screen out
which IP addresses you're allowed to connect to (<a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html#IPAddressAllow=ADDRESS%5B/PREFIXLENGTH%5D%E2%80%A6">cf</a>,
and I don't know whether systemd's restrictions would block this).</p>

<p>As I discovered the other day, <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/SocketConnectToAnyMeaning">if you connect to INADDR_ANY,
you connect to localhost</a>
(which any number of people already knew). Then in a comment <a href="https://phrye.com/">Kevin
Lyda</a> reminded me that INADDR_ANY is also
known as 0.0.0.0, and '0' is often accepted as a name that will
turn into it, resulting in 'ssh 0' working and also (in some browsers)
'http://0:&lt;port>/'. The IPv6 version of INADDR_ANY is also an
all-zero address, and '::0' and '::' are both accepted as names for
it, and then of course it's easy to create DNS records that resolve
to either the IPv4 or IPv6 versions. <a href="https://mastodon.social/@cks/116019553552602780">As I said on the Fediverse</a>:</p>

<blockquote><p>Surprise: blocking DNS rebinding to localhost requires screening out
more than 127/8 and ::1 answers. This is my face.</p>
</blockquote>

<p>It turns out that this came up in mid 2024 in the browser context,
as '0.0.0.0 Day' (<a href="https://mastodon.social/@cks/116019713829679330">cf</a>).
Modern versions of Chrome and Safari apparently explicitly block
requests to 0.0.0.0 (and presumably also the IPv6 version), while
Firefox will still accept it. And of course your URL-fetching
libraries will almost certainly also accept it, especially through
DNS lookups of ordinary looking but attacker controlled hostnames.</p>

<p>In my view, it's not particularly anyone's fault that this slipped
through the cracks, both in browsers and in tools that handle
fetching content from potentially hostile URLs. The reality of life
is that how IP behaves in practice is complicated and some of it
is <a href="https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=280705">historical practice that's been carried forward</a> and isn't
necessarily obvious or well known (and certainly isn't standardized).
Then URLs build on top of this somewhat rickety foundation and
surprises happen.</p>

<p>(This is related to the issue of <a href="https://utcc.utoronto.ca/~cks/space/blog/web/BrowsersAndLocalIPs">browsers being willing to talk
to 'local' IPs</a>, which <a href="https://utcc.utoronto.ca/~cks/space/blog/web/ChromePrivateNetBlocks">Chrome once attempted
to start blocking</a> (and I believe that shipped,
but <a href="https://utcc.utoronto.ca/~cks/space/blog/web/ChromeWalkingAwayII">I don't use Chrome any more</a> so I don't know
what the current state is).)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/web/LocalhostSurpriseAccessViaAny?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/LocalhostSurpriseAccessViaAny

---

*ID: 134e9ea961c620f8*
*抓取时间: 2026-03-12T13:49:26.048414*
