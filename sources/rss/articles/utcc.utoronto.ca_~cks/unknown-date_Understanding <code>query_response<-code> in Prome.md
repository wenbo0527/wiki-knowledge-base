# Understanding <code>query_response</code> in Prometheus Blackbox's tcp prober

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-24T02:54:48Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p><a href="https://github.com/prometheus/blackbox_exporter">Prometheus Blackbox</a>
is <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxNotes">somewhat complicated to understand</a>.
One of its fundamental abstractions is a 'prober', a generic way
of probing some service (such as making HTTP requests or DNS
requests). One prober is the 'tcp' prober, which makes a TCP
connection and then potentially conducts a conversation with
the service to verify its health.
For example, here's a ClamAV daemon health check, which connects,
sends a line with "PING", and expects to receive "PONG":</p>

<blockquote><pre style="white-space: pre-wrap;">
  clamd_pingpong:
    prober: tcp
    tcp:
      query_response:
        - send: "PING\n"
        - expect: "PONG"
</pre>
</blockquote>

<p>The conversation with the service is detailed in the <code>query_response</code>
configuration block (in YAML). For a long time I thought that this
was what it looks like here, a series of entries with one directive
per entry, such as 'send', 'expect', or 'starttls' (to switch to
TLS after, for example, you send a 'STARTTLS' command to the SMTP
or IMAP server).</p>

<p>However, <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/YamlSyntaxSurprise">much like an earlier case with Alertmanager</a>, this is not actually what the YAML syntax is.
In reality each step in the <code>query_response</code> YAML array can have
multiple things. To quote the documentation:</p>

<pre style="white-space: pre-wrap;">
 [ - [ [ expect: &lt;string> ],
       [ expect_bytes: &lt;string> ],
       [ labels:
         - [ name: &lt;string>
             value: &lt;string>
           ], ...
       ],
       [ send: &lt;string> ],
       [ starttls: &lt;boolean | default = false> ]
     ], ...
 ]
</pre>

<p>When there are multiple keys in a single step, Blackbox handles
them in almost the order listed here: first <code>expect</code>, then <code>labels</code>
if the <code>expect</code> matched, then <code>expect_bytes</code>, then <code>send</code>, then
<code>starttls</code>. Normally you wouldn't have both <code>expect</code> and <code>expect_bytes</code>
in the same step (and combining them is tricky). This order is not
currently documented, so you have to read <a href="https://github.com/prometheus/blackbox_exporter/blob/master/prober/query_response.go">prober/query_response.go</a>
to determine it.</p>

<p>One reason to combine <code>expect</code> and <code>send</code> together in a single step
is that then <code>send</code> can use regular expression match groups from
the <code>expect</code> in its text. There's an example of this in <a href="https://github.com/prometheus/blackbox_exporter/blob/master/blackbox.yml">the example
blackbox.yml file</a>:</p>

<blockquote><pre style="white-space: pre-wrap;">
  irc_banner:
    prober: tcp
    tcp:
      query_response:
      - send: "NICK prober"
      - send: "USER prober prober prober :prober"
      - expect: "PING :([^ ]+)"
        # cks: note use of ${1}, from PING
        send: "PONG ${1}"
      - expect: "^:[^ ]+ 001"
</pre>
</blockquote>

<p>The 'labels:' key is something added in <a href="https://github.com/prometheus/blackbox_exporter/releases/tag/v0.26.0">v0.26.0</a>, in
<a href="https://github.com/prometheus/blackbox_exporter/pull/1284">#1284</a>.
As shown in <a href="https://github.com/prometheus/blackbox_exporter/blob/master/blackbox.yml">the example blackbox.yml file</a>, it can be used to
do things like extract SSH banner information into labels on a
metric:</p>

<blockquote><pre style="white-space: pre-wrap;">
  ssh_banner_extract:
    prober: tcp
    timeout: 5s
    tcp:
      query_response:
      - expect: "^SSH-2.0-([^ -]+)(?: (.*))?$"
        labels:
        - name: ssh_version
          value: "${1}"
        - name: ssh_comments
          value: "${2}"
</pre>
</blockquote>

<p>This creates a metric that looks like this:</p>

<blockquote><pre style="white-space: pre-wrap;">
probe_expect_info {ssh_comments="Ubuntu-3ubuntu13.14", ssh_version="OpenSSH_9.6p1"} 1
</pre>
</blockquote>

<p>At the moment there are some undocumented restrictions on the
'<code>labels</code>' key (or action or whatever you want to call it). First,
it only works if you use it in a step that has an '<code>expect</code>'. Even
if all you want to do is set constant label values (for example to
record that you made it to a certain point in your steps), you need
to <code>expect</code> something; you can't use '<code>labels</code>' in a step that
otherwise only has, say, '<code>send</code>'. Second, you can only have one
<code>labels</code> in your entire <code>query_response</code> section; if you have
more than one, <a href="https://github.com/prometheus/blackbox_exporter/issues/1526">you'll currently experience a Go panic when checking
reaches the second</a>.</p>

<p>This is unfortunate because <a href="https://github.com/prometheus/blackbox_exporter/issues/1528">Blackbox is currently lacking good
ways to see how far your <code>query_response</code> steps got if the probe
fails</a>.
Sometimes it's obvious where your probe failed, or irrelevant, but
<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxOutsideSMTP">sometimes it's both relevant and not obvious</a>. If you could use multiple <code>labels</code>,
you could progressively set fixed labels and tell how far you got
by what labels were visible in the scrape metrics.</p>

<p>(And of course you could also record various pieces of useful
information that you don't get all at once.)</p>

<h3>Sidebar: On (not) condensing <code>expect</code> and <code>send</code> together</h3>

<p>My personal view is that I normally don't want to condense '<code>expect</code>'
and '<code>send</code>' together into one step entry unless I have to, because
most of the time it inverts the relationship between the two. In
most protocols and protocol interactions, you send something and
expect a response; you don't receive something and then send a
response to it. In my opinion this is more naturally written in the
style:</p>

<blockquote><pre style="white-space: pre-wrap;">
      query_response:
      - expect: "something"
      - send: "my request"
      - expect: "reply to my request"
      - send: "something else"
      - expect: "reply to something else"
</pre>
</blockquote>

<p>Than as:</p>
<blockquote><pre style="white-space: pre-wrap;">
      query_response:
      - expect: "something"
        send: "my request"
      - expect: "reply to my request"
        send: "something else"
      - expect: "reply to something else"
</pre>
</blockquote>

<p>What look like pairs (an expect/send in the same step) are not actually
pairs; the 'expect' is for a previous 'send' and then 'send' pairs with
the next 'expect' in the next step. So it's clearer to write them all as
separate steps, which doesn't create any expectations of pairing.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusBlackboxQueryResponse

---

*ID: ee56bf16360c9372*
*抓取时间: 2026-03-12T13:49:26.048565*
