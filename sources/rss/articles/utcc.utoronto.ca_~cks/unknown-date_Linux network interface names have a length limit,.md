# Linux network interface names have a length limit, and Netplan

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-15T02:19:11Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Over on the Fediverse, <a href="https://mastodon.social/@cks/115895841326615811">I shared a discovery</a>:</p>

<blockquote><p>This is my (sad) face that Linux interfaces have a maximum
name length. What do you mean I can't call this VLAN interface
'vlan22-matterlab'?</p>

<p>Also, this is my annoyed face that <a href="https://netplan.io/">Canonical Netplan</a> doesn't check
or report this problem/restriction. Instead your VLAN interface just
doesn't get created, and you have to go look at system logs to find
systemd-networkd telling you about it.</p>

<p>(This is my face about Netplan in general, of course. The sooner it
gets yeeted the better.)</p>
</blockquote>

<p>Based on both some Internet searches and looking at kernel headers,
I believe the limit is 15 characters for the primary name of an
interface. In headers, you will find this called <code>IFNAMSIZ</code> (the
kernel) or <code>IF_NAMESIZE</code> (glibc), and it's defined to be 16 but
that includes the trailing zero byte for C strings.</p>

<p>(I can be confident that the limit is 15, not 16, because
'vlan22-matterlab' is exactly 16 characters long without a trailing
zero byte. Take one character off and it works.)</p>

<p>At the level of <a href="https://www.man7.org/linux/man-pages/man8/ip.8.html">ip</a>
commands, the error message you get is on the unhelpful side:</p>

<blockquote><pre style="white-space: pre-wrap;">
# ip link add dev vlan22-matterlab type wireguard
Error: Attribute failed policy validation.
</pre>
</blockquote>

<p>(I picked the type for illustration purposes.)</p>

<p>Systemd-networkd gives you a much better error message:</p>

<blockquote><p>/run/systemd/network/10-netplan-vlan22-matterlab.netdev:2: Interface name is not valid or too long, ignoring assignment: vlan22-matterlab</p>
</blockquote>

<p>(Then you get some additional errors because there's no name.)</p>

<p>As mentioned in <a href="https://mastodon.social/@cks/115895841326615811">my Fediverse post</a>, Netplan tells
you nothing. One direct consequence of this is that in any context
where you're writing down your own network interface names, such
as <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/NetplanVlanAnnoyance">VLANs</a> or <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/NetplanWireGuardWorksBut">WireGuard interfaces</a>, simply having 'netplan try' or 'netplan
apply' succeed without errors does not mean that your configuration
actually works. You'll need to look at error logs and perhaps
inventory all your network devices.</p>

<p>(<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/NetplanWireGuardOneFileOnly">This isn't the first time I've seen Netplan behave this way</a>, and it remains just as dangerous.)</p>

<p>As covered in the <a href="https://www.man7.org/linux/man-pages/man8/ip-link.8.html">ip link</a> manual
page, network interfaces can have either or both of aliases and
'altname' properties. These alternate names can be (much) longer
than 16 characters, and the 'ip link property' altname property can
be used in various contexts to make things convenient (I'm not sure
what good aliases are, though). However this is somewhat irrelevant
for people using Netplan, because <a href="https://netplan.readthedocs.io/en/latest/netplan-yaml/">the current Netplan YAML</a> doesn't
allow you to set interface altnames.</p>

<p>You can set altnames in networkd .link files, as covered in the
<a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html">systemd.link</a>
manual page. The direct thing you want is <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html#AlternativeName="><code>AlternativeName=</code></a>,
but apparently you may also want to set a blank alternative names
policy, <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html#AlternativeNamesPolicy="><code>AlternativeNamesPolicy=</code></a>.
Of course this probably only helps if you're using systemd-networkd
directly, instead of through Netplan.</p>

<p>PS: Netplan itself has the notion of Ethernet interfaces having
symbolic names, such as 'vlanif0', but this is purely internal to
Netplan; it's not manifested as an actual interface altname in the
'rendered' systemd-networkd control files that Netplan writes out.</p>

<p>(Technically this applies to all <a href="https://netplan.readthedocs.io/en/latest/netplan-yaml/#properties-for-physical-device-types">physical device types</a>.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/NetworkInterfaceNameLengthLimit?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/NetworkInterfaceNameLengthLimit

---

*ID: 4694782433701ae5*
*抓取时间: 2026-03-12T13:49:26.048659*
