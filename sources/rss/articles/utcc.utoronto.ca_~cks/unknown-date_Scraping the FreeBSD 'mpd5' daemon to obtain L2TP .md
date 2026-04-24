# Scraping the FreeBSD 'mpd5' daemon to obtain L2TP VPN usage data

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-26T04:00:33Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p><a href="https://support.cs.toronto.edu/">We</a> have a collection of VPN
servers, some OpenVPN based and some L2TP based. They used to be
based on OpenBSD, but <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OpenBSDToFreeBSDMove">we're moving from OpenBSD to FreeBSD</a> and the VPN servers recently
moved too. We also have <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SelectingUsefulMetrics">a system for collecting Prometheus metrics
on VPN usage</a>, which worked by
<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OurOpenBSDMonitoring">parsing the output of things</a>.
For OpenVPN, our scripts just kept working when we switched to
FreeBSD because the two OSes use basically the same OpenVPN setup.
This was not the case for our L2TP VPN server.</p>

<p>OpenBSD does L2TP using <a href="https://man.openbsd.org/npppd">npppd</a>,
which supports a handy command line control program, <a href="https://man.openbsd.org/npppctl.8">npppctl</a>, that can readily extract and
report status information. On FreeBSD, we wound up using <a href="https://man.freebsd.org/cgi/man.cgi?query=mpd5">mpd5</a>. Unfortunately,
mpd5 has no equivalent of npppctl. Instead, as covered (sort of)
in <a href="https://mpd.sourceforge.net/doc5/mpd.html">its user manual</a>
you get your choice of <a href="https://mpd.sourceforge.net/doc5/mpd16.html">a TCP based console</a> that's clearly intended
for interactive use and <a href="https://mpd.sourceforge.net/doc5/mpd41.html">a web interface</a> that is also sort of
intended for interactive use (and isn't all that well documented).</p>

<p>Fortunately, one convenient thing about the web interface is that
it uses HTTP Basic authentication, which means that you can easily
talk to it through tools like <a href="https://man.freebsd.org/cgi/man.cgi?query=curl">curl</a>. To do status
scraping through the web interface, first you need to turn it on
and then you need an unprivileged mpd5 user you'll use for this:</p>

<blockquote><pre style="white-space: pre-wrap;">
set web self 127.0.0.1 5006
set web open

set user metrics &lt;some-password> user
</pre>
</blockquote>

<p>At this point you can use <code>curl</code> to get responses from the mpd5
web server (from the local host, ie your VPN server itself):</p>

<blockquote><pre style="white-space: pre-wrap;">
curl -s -u metrics:... --basic 'http://localhost:5006/&lt;something>'
</pre>
</blockquote>

<p>There are two useful things you can ask the web server interface
for. First, you can ask it for a complete dump of its status in
JSON format, by asking for 'http://localhost:5006/json' (although
the documentation claims that the information returned is what 'show
summary' in the console would give you, it is more than that). If
you understand mpd5 and like parsing and processing JSON, this is
probably a good option. We did not opt to do this.</p>

<p>The other option is that you can ask the web interface to run console
(interface) commands for you, and then give you the output in either
a 'pleasant' HTML page or in a basic plain text version. This is
done by requesting either '/cmd?&lt;command>' or '/bincmd?&lt;command>'
respectively. For statistics scraping, the most useful version is
the 'bincmd' one, and the command we used is '<code>show session</code>':</p>

<blockquote><pre style="white-space: pre-wrap;">
curl -s -u metrics:... --basic 'http://localhost:5006/bincmd?show%20session'
</pre>
</blockquote>

<p>This gets you output that looks like:</p>

<blockquote><pre style="white-space: pre-wrap;">
ng1  172.29.X.Y  B2-2 9375347-B2-2  L2-2  2  9375347-L2-2  someuser  A.B.C.D
RESULT: 0
</pre>
</blockquote>

<p>(I assume 'RESULT: 0' would be something else if there was some
sort of problem.)</p>

<p>Of these, the useful fields for us are the first, which gives the
local network device, the second, which gives the internal VPN IP
of this connection, and the last two, which give us the VPN user
and their remote IP. The others are internal MPD things that we
(hopefully) don't have to care about. The internal VPN IP isn't
necessary for (our) metrics but may be useful for log correlation.</p>

<p>To get traffic volume information, you need to extract the usage
information from each local network device that a L2TP session is
using (ie, 'ng1' and its friends). As far as I know, the only tool
for this in (base) FreeBSD is <a href="https://man.freebsd.org/cgi/man.cgi?netstat">netstat</a>. Although you can
invoke it interface by interface, probably the better thing to do
(and what we did) is to use '<code>netstat -ibn -f link</code>' to dump
everything at once and then pick through the output to get the lines
that give you packet and byte counts for each L2TP interface, such
as ng1 here.</p>

<p>(I'm not sure if dropped packets is relevant for these interfaces;
if you think it might be, you want '<code>netstat -ibnd -f link</code>'.)</p>

<p>FreeBSD has a general system, 'libxo', for producing output from
many commands in a variety of handy formats. As covered in
<a href="https://man.freebsd.org/cgi/man.cgi?query=xo_options">xo_options</a>,
this can be used to get this netstat output in JSON if you find
that more convenient. I opted to get the plain text format and use
field numbers for the information I wanted for our VPN traffic
metrics.</p>

<p>(Partly this was because I could ultimately reuse a lot of my metrics
generation tools from the OpenBSD npppctl parsing. Both environments
generated two sets of line and field based information, so a
significant amount of the work was merely shuffling around which
field was used for what.)</p>

<p>PS: Because of how mpd5 behaves, my view is that you don't want to
let anyone but system staff log on to the server where you're using
it. It is an old C code base and I would not trust it if people can
hammer on its TCP console or its web server. I certainly wouldn't
expose the web server to a non-localhost network, even apart from
the bit where it definitely doesn't support HTTPS.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/FreeBSDScrapingMpd5ForL2TP

---

*ID: 29da205d46fcef26*
*抓取时间: 2026-03-12T13:49:26.048545*
