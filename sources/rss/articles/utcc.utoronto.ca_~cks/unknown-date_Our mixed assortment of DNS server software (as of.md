# Our mixed assortment of DNS server software (as of December 2025)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-07T04:12:06Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Without deliberately planning it, we've wound up running an assortment
of DNS server software on an assortment of DNS servers. A lot of
this involves history, so I might as well tell the story of that
history in the process. This starts with our three sets of DNS
servers: our internal DNS master (with a duplicate) that holds both
<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/BinatAndSplitHorizonDNS">the internal and external views of our zones</a>,
our resolving DNS servers (which use our internal zones), and our
public authoritative DNS server (carrying our external zones, <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DNSServerReferencesCanLinger">along
with various relics of the past</a>).
These days we also have an additional resolving DNS server that
resolves from outside our networks and so gives the people who can
use it an external view of our zones.</p>

<p>In the beginning we ran Bind on everything, as was the custom in
those days (and I suspect we started out without a separation between
the three types of DNS servers, but that predates my time <a href="https://support.cs.toronto.edu/">here</a>), and I believe all of the DNS
servers were Solaris. Eventually we moved the resolving DNS servers
and the public authoritative DNS server to OpenBSD (and the internal
DNS master to Ubuntu), still using Bind. Then OpenBSD switched which
nameservers they liked from Bind to Unbound and NSD, so we went
along with that. Our authoritative DNS server had a relatively easy
NSD configuration, but <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/UnboundZoneRefreshProblem">our resolving DNS servers presented some
challenges</a> and we wound up with a complex
Unbound plus NSD setup. Recently <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/UsingBindNowForResolvers">we switched our internal resolvers
to using Bind on Ubuntu</a>, and then we
switched our public authoritative DNS server from OpenBSD to Ubuntu
but kept it still with NSD, since we already had a working NSD
configuration for it.</p>

<p>This has wound up with us running the following setups:</p>

<ul><li>Our internal DNS masters run Bind in a somewhat complex split horizon
configuration.<p>
</li>
<li>Our internal DNS resolvers run Bind in a simpler configuration where
they act as internal authoritative secondary DNS servers for our own
zones and as general resolvers.<p>
</li>
<li>Our public authoritative DNS server (and its hot spare) run NSD as an
authoritative secondary, doing zone transfers from our internal DNS
masters.<p>
</li>
<li>We have an external DNS resolver machine that runs Unbound in an
extremely simple configuration. We opted to build this machine with
Unbound because we didn't need it to act as anything other than a
pure resolver, and Unbound is simple to set up for that.</li>
</ul>

<p>At one level, this is splitting our knowledge and resources among
three DNS servers rather than focusing on one. At another level,
two out of the three DNS servers are being used in quite simple
setups (and we already had the NSD setup written from prior use).
Our only complex configurations are all Bind based, and we've
explicitly picked Bind for complex setups because we feel we
understand it fairly well from long experience with it.</p>

<p>(Specifically, I can configure a simple Unbound resolver faster and
easier than I can do the same with Bind. I'm sure there's a simple
resolver-only Bind configuration, it's just that I've never built
one and I have built several simple and not so simple Unbound
setups.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OurMixedDNSServers?showcomments#comments">7 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OurMixedDNSServers

---

*ID: e594bd88cb6afcbf*
*抓取时间: 2026-03-12T13:49:26.049067*
