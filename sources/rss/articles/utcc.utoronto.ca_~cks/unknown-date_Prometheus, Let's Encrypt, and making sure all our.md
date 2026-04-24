# Prometheus, Let's Encrypt, and making sure all our TLS certificates are monitored

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-06T03:11:03Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I recently wrote about <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/TLSCertificateUsageReporting">the complexities of getting programs to
report the TLS certificates they use</a>,
where I theorized about writing a script to scrape this information
out of places like the Apache configuration files, and then today
<a href="https://mastodon.social/@cks/115844675099295774">I realized the obvious specific approach for our environment</a>:</p>

<blockquote><p>Obvious realization is obvious: since we universally use Let's
Encrypt with certbot and follow standard naming, I can just look in
/etc/letsencrypt/live to find all live TLS certificates and (a) host
name for them, for cross-checking against our monitoring.</p>
</blockquote>

<p>Our TLS certificates usually have multiple names associated with
them, only one of which is the directory name in /etc/letsencrypt/live.
However, we usually monitor the TLS certificate under what we think
of as the primary name, and in any case we can make this our standard
Prometheus operating procedure.</p>

<p>In our Prometheus environment we create <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusAddHostnameLabel">a standard label for the
'host' being monitored</a>, including for
metrics obtained through Blackbox. Given that <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxTLSExpiry">Blackbox exposes
TLS certificate metrics</a>, we can use
things like <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusQueryWithCurl">direct <code>curl</code> queries to Prometheus</a>
to verify that we have TLS certificate monitoring for everything
in /etc/letsencrypt/live. The obvious thing to check is that we
have a probe_ssl_earliest_cert_expiry metric with the relevant
'host' value for each Let's Encrypt primary name.</p>

<p>If we want to, we can go further by looking at
probe_ssl_last_chain_info. This Blackbox metric directly exposes
labels for the TLS 'subject' and 'subjectalternative', so we can
in theory search them for either the primary name that Let's Encrypt
will be using or for what we consider an important name to be
covered. It appears that this wouldn't be needed to cover any
additional TLS certificates for us, as we're already checking
everything under its primary name.</p>

<p>(Well, we are after I found one omission in a manual check today.)</p>

<p>With <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ToolsOneach">the right tools</a> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ToolsOneachII">also</a>), I
don't need to make this a pre-written shell script that runs on
each machine; instead, I can do this centrally by hand every so
often. On the one hand this isn't as good as automating it, but on
the other hand every bit of locally built automation is another bit
of automation we have to maintain ourselves. We mostly haven't
had a problem with tracking TLS certificates, and <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdTimersMailNotes">we have other
things to notice failures</a>.</p>

<p>(I should probably write a personal script to do this, just
to capture the knowledge.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusLetsEncryptTLSChecking?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusLetsEncryptTLSChecking

---

*ID: 5b6856b0749349db*
*抓取时间: 2026-03-12T13:49:26.048751*
