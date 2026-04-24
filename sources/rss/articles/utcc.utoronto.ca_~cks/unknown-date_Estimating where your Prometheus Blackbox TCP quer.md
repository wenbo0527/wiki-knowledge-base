# Estimating where your Prometheus Blackbox TCP query-response check failed

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-02T04:20:27Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>As <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxQueryResponse">covered recently</a>, the normal
way to check simple services from outside in a Prometheus environment
is with <a href="https://github.com/prometheus/blackbox_exporter">Prometheus Blackbox</a>, which is <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxNotes">somewhat
complicated to understand</a>. One of its
abstractions is a <em>prober</em>, a generic way of checking some service
using HTTP, DNS queries, a TCP connection, and so on. The TCP prober
supports <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxQueryResponse">conducting a query-response dialog once you connect</a>, but currently (as of Blackbox
0.28.0) it doesn't directly expose metrics that tell you where your
TCP probe with a query-response set failed (and why), and <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxOutsideSMTP">sometimes
you'd like to know</a>.</p>

<p>A somewhat typical query-response probe looks like this:</p>

<blockquote><pre style="white-space: pre-wrap;">
  smtp_starttls:
    prober: tcp
    tcp:
      query_response:
        - expect: "^220"
        - send: "EHLO something\r"
        - expect: "^250-STARTTLS"
        - expect: "^250 "
        - send: "STARTTLS\r"
        - expect: "^220"
        - starttls: true
        - expect: "^220"
        - send: "QUIT\r"
</pre>
</blockquote>

<p>To understand what metrics we can look for on failure, we need to
both understand how each important option in a step can fail, and
what metrics they either set on failure or create when they succeed.</p>

<ul><li><code>starttls</code> will fail if it can't successfully negotiate a TLS connection
with the server, possibly including if the server's TLS certificate fails
to verify. It sets no metrics on failure, but on success it will set
various TLS related metrics such as the <code>probe_ssl_*</code> family and
<code>probe_tls_version_info</code>.<p>
</li>
<li><code>send</code> will fail if there is an error sending the line, such as the TCP
connection closing on you. It sets no metrics on either success or failure.<p>
</li>
<li><code>expect</code> reads lines from the TCP connection until either a line
matches your regular expression, it hits EOF, or it hits a network
error. If it hit a network error, including from the other end
abruptly terminating the connection in a way that raises a local
error, it sets no metrics. If it hit EOF, it sets the metric
<code>probe_failed_due_to_regex</code> to 1; if it matched a line, it sets
that metric to 0.<p>
One important case of 'network error' is if the check you're doing
times out. This is internally implemented partly by putting a
(Go) deadline on the TCP connection, which will cause an error
if it runs too long. Typical Blackbox module timeouts aren't very
long (how long depends on both configuration settings and how
frequent your checks are; they have to be shorter than the check
interval).<p>
If you have multiple '<code>expect</code>' steps and you check fails at one
of them, there's (currently) no way to find out which one it failed
at unless you can determine this from other metrics, for example
the presence or absence of TLS metrics.<p>
</li>
<li><code>expect_bytes</code> fails if it doesn't immediately read those bytes
from the TCP connection. If it failed because of an error or because
it read fewer bytes than required (including no bytes, ie an EOF), it
sets no metrics. If it read enough bytes it sets the
<code>probe_failed_due_to_bytes</code> metric to either 0 (if they matched)
or 1 (if they didn't).</li>
</ul>

<p>In many protocols, the consequences of how <code>expect</code> works means
that if the server at the other end spits out some error response
instead of the response you expect, your <code>expect</code> will skip over
it and then wait endlessly. For instance, if the SMTP server you're
probing gives you a SMTP 4xx temporary failure response in either
its greeting banner or its reply to your EHLO, your '<code>expect</code>' will
sit there trying to read another line that might start with '220'.
Eventually either your check will time out or the SMTP server will,
and probably it will be your check (resulting in a 'network error'
that leaves no traces in metrics).
Generally this means you can only see a <code>probe_failed_due_to_regex</code>
of 1 in a TCP probe based module if the other end cleanly closed
the connection, so that you saw EOF. This tends to be pretty rare.</p>

<p>(We mostly see it for SSH probes against overloaded machines, where
we connect but then the SSH daemon immediately closes the connection
without sending the banner, giving us an EOF in our '<code>expect</code>' for
the banner.)</p>

<p>If the probe failed because of a DNS resolution failure, I believe
that <code>probe_ip_addr_hash</code> will be 0 and I think <code>probe_ip_protocol</code>
will also be 0.</p>

<p>If the check involves TLS, the presence of the TLS metrics in the
result means that you got a connection and got as far as starting
TLS. In the example above, this would mean that you got almost all
of the way to the end.</p>

<p>I'm not sure if there's any good way to detect that the connection
attempt failed. You might be able to reasonably guess that from an
abnormally low <code>probe_duration_seconds</code> value. If you know the
relevant timeout values, you can detect a probe that failed due to
timeout by looking for a suitably high <code>probe_duration_seconds</code>
value.</p>

<p>If you have some use of <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxQueryResponse">the special <code>labels</code> action</a>, then the presence of a
<code>probe_expect_info</code> metric means that the check got to that step.
If you don't have any particular information that you want to capture
from an <code>expect</code> line, you can use <code>labels</code> (once) to mark that
you've succeeded at some <code>expect</code> step by using a constant value
for your label.</p>

<p>(Hopefully all of this will improve at some point and Blackbox will
provide, for example, a metric that tells you the step number that
a query-response block failed on. See <a href="https://github.com/prometheus/blackbox_exporter/issues/1528">issue #1528</a>, and
also <a href="https://github.com/prometheus/blackbox_exporter/issues/1527">issue #1527</a> where
I wish for a way to make an '<code>expect</code>' fail immediately and
definitely if it receives known error responses, such as a SMTP
4xx code.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxTCPQRMetrics?showcomments#comments">4 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxTCPQRMetrics

---

*ID: 18dfc3ef98ac1d31*
*抓取时间: 2026-03-12T13:49:26.048457*
