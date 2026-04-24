# Pitfalls in using Prometheus Blackbox to monitor external SMTP

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-23T04:15:09Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>The news of the day is that Microsoft had a significant outage
inside their Microsoft 365 infrastructure. <a href="https://support.cs.toronto.edu/">We</a> noticed when we stopped being
able to deliver email to the university's institutional email system,
<a href="https://mastodon.social/@cks/115940637649055921">which was a bit mysterious in the usual way of today's Internet</a>:</p>

<blockquote><p>The joys of modern email: "Has Microsoft decided to put all of our
email on hold or are they having a global M365 inbound SMTP email
incident?"</p>

<p>(For about the last hour and a half, if it's an incident someone is
having a bad day.)</p>
</blockquote>

<p>We didn't find out immediately when this happened (and if our systems
had been working right, we wouldn't have found out when I did, but
that's another story). Initially I was going to write an entry about
whether or not we should use <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusGrafanaSetup-2019">our monitoring system</a> to monitor external services that
other people run, but it turns out that we do try to monitor whether
we can do a SMTP conversation to the university's M365-hosted
institutional email. There were several things that happened with
this monitoring.</p>

<p>The first thing that happened is that the alerts related to it
rotted. The university once had a fixed set of on-premise MX targets
and we monitored our ability to talk to them and alerted on it.
Then the university moved their MX targets to M365 and our old
alerts stopped applying, so we commented them out and never added
any new alerts for any new checking we were doing.</p>

<p>One of the reasons for that is that we were doing this monitoring
through <a href="https://github.com/prometheus/blackbox_exporter">Prometheus Blackbox</a>, and Blackbox is
not ideal for monitoring Microsoft 365 MX targets. The way M365
does redundancy in their inbound mail servers for your domain is
not by returning multiple DNS MX records, but by returning one MX
record for a hostname that has multiple IP addresses (and the IP
addresses may change). What a mailer will do is try all of the IP
addresses until one responds. What Blackbox does is it picks one
IP address and then it probes the IP address; if the address fails,
there is no attempt to check the other IP addresses. Failing if
one IP of many is not responding is okay for casual checks, but you
don't necessarily want to alert on it.</p>

<p>(I believe that Blackbox picks the first IP address in the DNS A
record, but this depends on how the Go standard library and possibly
your local resolver behaves. If either sort the results, you get
the first A record in the sorted result.)</p>

<p>The final issue is that we weren't necessarily checking enough of
the SMTP conversation. For various reasons, we decided that all we
could safely and confidently check was that the university's mail
system accepted a testing SMTP MAIL FROM from our subdomain; we
didn't check that it also accepted a SMTP RCPT TO. I believe that
during part of this Microsoft 365 incident, the inbound M365 SMTP
servers would accept our SMTP MAIL FROM but report an error at the
RCPT TO (although I can't be sure). Certainly if we want to have a
more realistic check of 'is email to M365 working', we should go
as far as a SMTP RCPT TO.</p>

<p>(During parts of the incident, DNS lookups didn't succeed for the
MX target. Without detailed examination I can't be sure of what
happened in the other cases.)</p>

<p>Overall, Blackbox is probably the wrong tool to check an external
mail target like M365 if we're serious about it and want to do a
good job. At the moment it's not clear to me if we should go to the
effort to do better, since it is an external service and there's
nothing we can do about problems (although we can let people know,
which has some value, but that's another entry).</p>

<p>PS: You can get quite elaborate in a mail deliverability test, but
to some degree the more elaborate you get the more pieces of
infrastructure you're testing, and you may want a narrow test for
better diagnostics.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxOutsideSMTP

---

*ID: 8f19561f5c094275*
*抓取时间: 2026-03-12T13:49:26.048576*
