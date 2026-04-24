# The complexities of getting programs to report the TLS certificates they use

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-03T03:17:45Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of the practical reasons that <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/ExpiryTimesAreDangerous">TLS certificates have dangerous
expiry times</a> is that in most
environments, it's up to you to remember to add monitoring for each
TLS certificate that you use, either <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusMultipurposeMonitoring">as part of general purpose
monitoring of the service</a> or
specific monitoring for certificate expiry. <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MonitoringTooHard">It would be nice if
programs that used TLS certificates inherently monitored their
expiry</a>, but that's a fairly big change (for
example, you have to decide how to send alerts about that information).
A nominally easier change would be for programs routinely to be
able to report what TLS certificates they're using, either as part
of normal metrics and log messages or through some additional command
line switch.</p>

<p>(If your program uses TLS certificates and it has some sort of built
in way of reporting metrics, it would be very helpful to system
administrators if it reported basic TLS certificate metrics like
the 'notAfter' time.)</p>

<p>In a lot of programs, this would be relatively straightforward (in
theory). A common pattern is for programs to read in all of the
TLS certificates they're going to use on startup, before they drop
privileges, which means that these programs reliably know what all
of those certificates are (and some programs will abort if some TLS
certificates can't be read). They could then report the TLS certificate
file paths on startup, either as part of their regular startup or
in a special 'just report configuration information' mode. In many
cases, one could write your own script that scanned the program's
configuration files and did a reasonably good job of finding all
of the TLS certificate filenames (and you could then make it report
the names those TLS certificates were for, and cross-check this
against your existing monitoring).</p>

<p>(I should probably write such a script for our Apache environment,
because adding TLS based virtual hosts and then forgetting to monitor
them is something we could definitely do.)</p>

<p>However, not all programs are straightforward this way. There are
some programs that can at least potentially generate the TLS
certificate file name on the fly at runtime (for example, <a href="https://www.exim.org/">Exim</a>'s settings for TLS certificate file names
are 'expanded strings' that might depend on connection parameters).
And even usually straightforward programs like Apache can have
conditional use of TLS certificates, although this probably will
only leave you doing some extra monitoring of unused TLS certificates
(let's assume you're not using <a href="https://httpd.apache.org/docs/current/mod/mod_ssl.html#sslcertificatefile">SSLCertificateFile token identifiers</a>).
These programs would probably need to log TLS certificate filenames
on their first use, assuming that they cache loaded TLS certificates
rather than re-read them from scratch every time they're necessary.</p>

<p>There's also no generally obvious and good way to expose this
information, which means that logging it or printing it out is only
the first step and not necessarily deeply useful by itself. If
programs put it into logs, people have to pull it out of logs; if
programs report it from the command line, people need to write
additional tooling. If a program has built in metrics that it exposes
in some way, exposing metrics for any TLS certificates it uses is
great, but most programs don't have their own metrics and statistics
systems.</p>

<p>(Still, it would be nice if programs supported this first step.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/TLSCertificateUsageReporting?showcomments#comments">3 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/TLSCertificateUsageReporting

---

*ID: 99e575662473b54e*
*抓取时间: 2026-03-12T13:49:26.048782*
