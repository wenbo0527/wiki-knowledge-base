# Lingering bad DNS traffic to our authoritative DNS server

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-10T03:53:48Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I recently wrote about <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DNSServerReferencesCanLinger">how getting out of being people's secondary
authoritative DNS server is hard</a>.
In the process of that I said that there was a background Internet
radiation of external machines throwing random DNS queries at us.
Now that we've reduced the number of DNS zones that were improperly
still pointing at us for historical reasons, I think I can finally
see enough from <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OurMixedDNSServers">our public authoritative DNS server's</a> traffic to say something about that.</p>

<p>The rejected DNS queries we're seeing so far are a mixture of three
types of queries. The first sort of query is for one of those DNS
zones that used to be pointing to us but haven't been for long
enough that people's DNS caches should have timed out by now. My
best guess is that some systems simply hold on to DNS nameserver
information for well over any listed TTLs for it. The amount of
these queries has been going down for some time so it seems that
eventually people do refresh their DNS information and stop poking
us.</p>

<p>The second sort of query is for more or less random DNS names that
have definitely never pointed at us, not infrequently in well known
domains such as 'google.com' or 'googleapis.com', or a well known
name like 'chrome.cloudflare-dns.com'. The source IPs for these
queries are all over and they're generally low volume.  Some IPs
may be probing to see if we have any sort of open recursive resolver
behavior, but others seem much more random, enough so that I wonder
if the remote machines are experiencing some sort of corruption in
the DNS server IP that they want to query (or perhaps their DNS
lookup software or resolving DNS software is copying the NS record
from one entry over to another).</p>

<p>(Sometimes people even make queries for things in the RFC 1918
portion of in-addr.arpa.)</p>

<p>The third and largest source of bad traffic is queries for what
look like internal domains within at least one top level domain
(and I'm going to name it, it's koenigmetall.com). On spot checking
so far, all of the queries come from IP addresses that seem to be
located in Romania. What I suspect here is a version of <a href="https://utcc.utoronto.ca/~cks/space/blog/spam/BadAddressSpamComedy">people
using our 128.100/16 as internal IP address space</a>. Our public authoritative DNS server
is at the IP address 128.100.1.1, which is a very attractive IP to
put something important on if you're using 128.100/16 internally.
So I suspect that if someone were to inspect the internal DNS of
the company in question, they'd find errant DNS NS and A records
that said an internal DNS server for these internal zones was found
at 128.100.1.1. Then queries theoretically to that internal DNS
server are leaking onto the public Internet and reaching us, likely
in a process similar to <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DNSDynamicUpdatesToUs">how people keep sending dynamic DNS updates
to us</a> (that entry is from 2021 but it's all
still going on).</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DNSServerLingeringTraffic?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DNSServerLingeringTraffic

---

*ID: a31738e9bd131bda*
*抓取时间: 2026-03-12T13:49:26.049034*
