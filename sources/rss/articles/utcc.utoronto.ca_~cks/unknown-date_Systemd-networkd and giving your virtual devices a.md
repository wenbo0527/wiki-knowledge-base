# Systemd-networkd and giving your virtual devices alternate names

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-17T03:28:42Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Recently I wrote about <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/NetworkInterfaceNameLengthLimit">how Linux network interface names have a
length limit</a>, of 15 characters.
You can work around this limit by giving network interfaces an
'altname' property, as exposed in (for example) <a href="https://www.man7.org/linux/man-pages/man8/ip-link.8.html">'ip link'</a>. While
you can't work around this at all in <a href="https://netplan.io/">Canonical's Netplan</a>, it looks like you can have this for your
VLANs in systemd-networkd, since there's <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html#AlternativeName="><code>AlternativeName=</code></a>
in the <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html">systemd.link</a>
manual page.</p>

<p>Except, if you look at an actual VLAN configuration as materialized
by Netplan (or written out by hand), you'll discover a problem.
Your VLANs don't normally have .link files, only <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.netdev.html">.netdev</a>
and <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html">.network</a>
files (and even your normal Ethernet links may not have .link files).
The <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html#AlternativeName="><code>AlternativeName=</code></a> setting is only valid in .link files, because
networkd is like that.</p>

<p>(The <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html#AlternativeName="><code>AlternativeName=</code></a> is a '[Link]' section setting and
.network files also have a '[Link]' section, but they allow
completely different sets of '[Link]' settings. The .netdev file,
which is where you define virtual interfaces, doesn't have a '[Link]'
section at all, although settings like <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html#AlternativeName="><code>AlternativeName=</code></a> apply
to them just as much as to regular devices. Alternately, .netdev
files could support setting altnames for virtual devices in the
'[NetDev]' section along side the mandatory 'Name=' setting.)</p>

<p>You can work around this indirectly, because you can create a .link
file for a virtual network device and have it work:</p>


<blockquote><pre style="white-space: pre-wrap;">
[Match]
Type=vlan
OriginalName=vlan22-mlab

[Link]
AlternativeNamesPolicy=
AlternativeName=vlan22-matterlab
</pre>
</blockquote>

<p>Networkd does the right thing here even though 'vlan22-mlab' doesn't
exist when it starts up; when vlan22-mlab comes into existence, it
matches the .link file and has the altname stapled on.</p>

<p>Given how awkward this is (and that not everything accepts or sees
altnames), I think it's probably not worth bothering with unless
you have a very compelling reason to give an altname to a virtual
interface. In my case, this is clearly too much work simply to give
a VLAN interface its 'proper' name.</p>

<p>Since I tested, I can also say that this works on a Netplan-based
Ubuntu server where the underlying VLAN is specified in Netplan.
You have to hand write the .link file and stick it in /etc/systemd/network,
but after that it cooperates reasonably well with <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/NetplanVlanAnnoyance">a Netplan VLAN
setup</a>.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdNetworkdVirtualAltnames

---

*ID: 7cec85767dbf8cab*
*抓取时间: 2026-03-12T13:49:26.048638*
