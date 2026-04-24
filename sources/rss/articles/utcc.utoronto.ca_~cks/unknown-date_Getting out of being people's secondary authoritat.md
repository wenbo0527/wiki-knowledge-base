# Getting out of being people's secondary authoritative DNS server is hard

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-06T03:28:40Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Many, many years ago, <a href="https://support.cs.toronto.edu/">my department</a>
operated one of the university's secondary authoritative DNS servers,
which was used by most everyone with a university subdomain and as
a result was listed as one of their DNS NS records. This DNs server
was also the authoritative DNS server for our own domains, because
this was in the era where servers were expensive and it made perfect
sense to do this. At the time, departments who wanted a subdomain
pretty much needed to have a Unix system administrator and probably
run their own primary DNS server and so on. Over time, the university's
DNS infrastructure shifted drastically, with central IT offering
more and more support, and more than half a decade ago our authoritative
DNS server stopped being a university secondary, after a lot of notice
to everyone.</p>

<p>Experienced system administrators can guess what happened next. Or
rather, what didn't happen next. References to our DNS server
lingered in various places for years, both in the university's root
zones as DNS glue records and in people's own DNS zone files as
theoretically authoritative records. As late as the middle of last
year, when I started grinding away on this, I believe that roughly
half of our authoritative DNS server's traffic was for old zones
we didn't serve and was getting DNS 'Refused' responses. The situation
is much better today, after several rounds of finding other people's
zones that were still pointing to us, but it's still not quite over
and it took a bunch of tedious work to get this far.</p>

<p>(Why I care about this is that it's hard to see if your authoritative
DNS server is correctly answering everything it should if things
like tcpdumps of DNS traffic are absolutely flooded with bad traffic
that your DNS server is (correctly) rejecting.)</p>

<p>In theory, what we should have done when we stopped being a university
secondary authoritative DNS server was to switch the authoritative
DNS server for our own domains to another name and another IP
address; this would have completely cut off everyone else when we
turned the old server off and removed its name from our DNS. In
practice the transition was not clearcut, because for a while we
kept on being a secondary for some other university zones that have
long-standing associations with <a href="https://www.cs.toronto.edu/">the department</a>. Also, I think we were optimistic
about how responsive people would be (and how many of them we could
reach).</p>

<p>(Also, there's a great deal of history tied up in the specific name
and IP address of our current authoritative DNS server. It's been
there for a very long time.)</p>

<p>PS: Even when no one is incorrectly pointing to us, there's clearly
a background Internet radiation of external machines throwing random
DNS queries at us. But that's another entry.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DNSServerReferencesCanLinger?showcomments#comments">4 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DNSServerReferencesCanLinger

---

*ID: 8315333254ec569e*
*抓取时间: 2026-03-12T13:49:26.049077*
