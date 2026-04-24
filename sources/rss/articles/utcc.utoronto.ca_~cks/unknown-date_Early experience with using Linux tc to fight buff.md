# Early experience with using Linux tc to fight bufferbloat latency

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-11T03:52:52Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Over on the Fediverse <a href="https://mastodon.social/@cks/115850659871840908">I mentioned something recently</a>:</p>

<blockquote><p>Current status: doing extremely "I don't know what I'm really doing,
I'm copying from a website¹" things with Linux tc to see if I can
improve my home Internet latency under load without doing too much
damage to bandwidth or breaking my firewall rules. So far, it seems to
work and things² claim to like the result.</p>

<p>¹ <a href="https://www.bufferbloat.net/projects/codel/wiki/Cake/#configuring-cake">&lt;documentation link></a> <br />
² <a href="https://bufferbloat.libreqos.com/">https://bufferbloat.libreqos.com/</a> via <a href="https://hachyderm.io/@davecb">@davecb</a></p>
</blockquote>

<p>What started this was <a href="https://fosstodon.org/@LibreQoS/115848718757642436">running into a Fediverse post about the
bufferbloat test</a>,
trying it, and discovering that (as expected) my home DSL link
performed badly, with significant increased latency during downloads,
uploads, or both. My memory is that reported figures went up to the
area of 400 milliseconds.</p>

<p>Conveniently for me, my Linux home desktop is also my DSL router;
it speaks PPPoE directly through my DSL modem. This means that doing
traffic shaping on my Linux desktop should cover everything, without
any need to wrestle with a limited router OS environment. And <a href="https://www.bufferbloat.net/projects/codel/wiki/Cake/#configuring-cake">there
was some more or less cut and paste directions on the site</a>.</p>

<p>So my outbound configuration was simple and obviously not harmful:</p>

<blockquote><pre style="white-space: pre-wrap;">
tc qdisc add root dev ppp0 cake bandwidth 7.6Mbit
</pre>
</blockquote>

<p>The bandwidth is a guess, although one informed by checking both
my raw DSL line rate and what testing sites told me.</p>

<p>The inbound configuration was copied from the documentation and
it's where I don't understand what I'm doing:</p>

<blockquote><pre style="white-space: pre-wrap;">
ip link add name ifb4ppp0 type ifb
tc qdisc add dev ppp0 handle ffff: ingress
tc qdisc add dev ifb4ppp0 root cake bandwidth 40Mbit besteffort
ip link set ifb4ppp0 up
tc filter add dev ppp0 parent ffff: matchall action mirred egress redirect dev ifb4ppp0
</pre>
</blockquote>

<p>(This order follows <a href="https://www.bufferbloat.net/projects/codel/wiki/Cake/#configuring-cake">the documentation</a>.)</p>

<p>Here is what I understand about this. As covered in the <a href="https://www.man7.org/linux/man-pages/man8/tc.8.html">tc</a> manual page,
traffic shaping and scheduling happens only on 'egress', which is
to say for outbound traffic. To handle inbound traffic, we need a
level of indirection to a special <a href="http://linux-ip.net/gl/tc-filters/tc-filters-node3.html">ifb (Intermediate Functional
Block)</a>
(<a href="https://wiki.linuxfoundation.org/networking/ifb">also</a>) device,
that is apparently used only for our (inbound) tc qdisc.</p>

<p>So we have two pieces. The first is the actual traffic shaping on
the IFB link, ifb4ppp0, and setting the link 'up' so that it will
actually handle traffic instead of throw it away. The second is
that we have to push inbound traffic on ppp0 through ifb4ppp0 to
get its traffic shaping. To do this we add a special 'ingress' qdisc
to ppp0, which applies to inbound traffic, and then we use a tc
filter that <a href="https://www.man7.org/linux/man-pages/man8/tc-matchall.8.html">matches all (ingress) traffic</a> and
<a href="https://www.man7.org/linux/man-pages/man8/tc-mirred.8.html">redirects it to ifb4ppp0 as 'egress' traffic</a>. Since
it's now egress traffic, the tc shaping on ifb4ppp0 will now apply
to it and do things.</p>

<p>When I set this up I wasn't certain if it was going to break my
non-trivial firewall rules on the ppp0 interface. However, everything
seems to fine, and the only thing the tc redirect is affecting is
traffic shaping. My firewall blocks and NAT rules are still working.</p>

<p>Applying these tc rules definitely improved my latency scores on
<a href="https://bufferbloat.libreqos.com/">the test site</a>; my link went
from an F rating to an A rating (and a C rating for downloads and
uploads happening at once).  Does this improve my latency in practice
for things like interactive SSH connections while downloads and
uploads are happening? It's hard for me to tell, partly because I
don't do such downloads and uploads very often, especially while I'm
doing interactive stuff over SSH.</p>

<p>(Of course partly this is because I've sort of conditioned myself
out of trying to do interactive SSH while other things are happening
on my DSL link.)</p>

<p>The most I can say is that this probably improves things, and that
since my DSL connection has drifted into having relatively bad
latency to start with (by my standards), it probably helps to
minimize how much worse it gets under load.</p>

<p>I do seem to get slightly less bandwidth for transfers than I did
before; experimentation says that how much less can be fiddled with
by adjusting the tc 'bandwidth' settings, although that also changes
latency (more bandwidth creates worse latency). Given that I rarely
do large downloads or uploads, I'm willing to trade off slightly
lower bandwidth for (much) less of a latency hit. One reason that
my bandwidth numbers are approximate anyway is that <a href="https://www.bufferbloat.net/projects/codel/wiki/Cake/#extensive-framing-compensation-for-dsl-atm-pppoe">I'm not sure
how much PPPoE DSL framing compensation I need</a>.</p>

<p>(The Arch wiki has a page on <a href="https://wiki.archlinux.org/title/Advanced_traffic_control">advanced traffic control</a> that
has some discussion of tc.)</p>

<h3>Sidebar: A rewritten command order for ingress traffic</h3>

<p>If my understanding is correct, we can rewrite the commands to set
up inbound traffic shaping to be more clearly ordered:</p>

<blockquote><pre style="white-space: pre-wrap;">
# Create and enable ifb link
ip link add name ifb4ppp0 type ifb
ip link set ifb4ppp0 up

# Set CAKE with bandwidth limits for
# our actual shaping, on ifb link.
tc qdisc add dev ifb4ppp0 root cake bandwidth 40Mbit besteffort

# Wire ifb link (with tc shaping) to inbound
# ppp0 traffic.
tc qdisc add dev ppp0 handle ffff: ingress
tc filter add dev ppp0 parent ffff: matchall action mirred egress redirect dev ifb4ppp0
</pre>
</blockquote>

<p>The 'ifb4ppp0' name is arbitrary but conventional, set up as
'ifb4&lt;whatever>'.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/TcBufferbloatEarlyExperience?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/TcBufferbloatEarlyExperience

---

*ID: 151613785c8a4f2d*
*抓取时间: 2026-03-12T13:49:26.048700*
