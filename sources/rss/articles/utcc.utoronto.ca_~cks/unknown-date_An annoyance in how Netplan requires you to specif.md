# An annoyance in how Netplan requires you to specify VLANs

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-12T04:27:24Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p><a href="https://netplan.io/">Netplan</a> is Canonical's more or less mandatory
method of specifying networking on Ubuntu. Netplan has a collection of
limitations and irritations, and recently I ran into a new one, which
is how VLANs can and can't be specified. To explain this, I can start
with <a href="https://netplan.readthedocs.io/en/stable/netplan-yaml/">the YAML configuration language</a>. To quote
the top level version, it looks like:</p>

<blockquote><pre style="white-space: pre-wrap;">
network:
  version: NUMBER
  renderer: STRING
  [...]
  ethernets: MAPPING
  [...]
  vlans: MAPPING
  [...]
</pre>
</blockquote>

<p>To translate this, you specify VLANs separately from your Ethernet or
other networking devices. On the one hand, this is nicely flexible. On
the other hand it creates a problem, because here is what you have
to write for <a href="https://netplan.readthedocs.io/en/stable/netplan-yaml/#properties-for-device-type-vlans">VLAN properties</a>:</p>

<blockquote><pre style="white-space: pre-wrap;">
network:
  vlans:
    vlan123:
      id: 123
      link: enp5s0
      addresses: &lt;something>
</pre>
</blockquote>

<p>Every VLAN is on top of some networking device, and because VLANs
are specified as a separate category of top level devices, you have
to name the underlying device in every VLAN (which gets very annoying
and old very fast if you have ten or twenty VLANs to specify). Did
you decide to switch from a 1G network port to a 10G network port
for the link with all of your VLANs on it? Congratulations, you get
to go through every 'vlans:' entry and change its 'link:' value.
We hope you don't overlook one.</p>

<p>(Or perhaps you had to move the system disks from one model of 1U
server to another model of 1U server because the hardware failed.
Or you would just like to write generic install instructions with
a generic block of YAML that people can insert directly.)</p>

<p>The best way for Netplan to deal with this would be to allow you
to also specify VLANs as part of other devices, especially Ethernet
devices. Then you could write:</p>


<blockquote><pre style="white-space: pre-wrap;">
network:
  ethernet:
    enp5s0: 
      vlans:
        vlan123:
          id: 123
          addresses: &lt;something>
</pre>
</blockquote>

<p>Every VLAN specified in enp5s0's configuration would implicitly use
enp5s0 as its underlying link device, and you could rename all of
them trivially. This also matches how I think most people think of
and deal with VLANs, which is that (obviously) they're tied to some
underlying device, and you want to think of them as 'children' of
the other device.</p>

<p>(You can have an approach to VLANs where they're more free-floating
and the interface that delivers any specific VLAN to your server
can change, for load balancing or whatever. But you could still do
this, since Netplan will need to keep supporting the separate
'vlans:' section.)</p>

<p>If you want to work around this today, you have to go for the far
less convenient approach of artificial network names.</p>

<blockquote><pre style="white-space: pre-wrap;">
network:
  ethernet:
    vlanif0:
      match:
        name: enp5s0

  vlans:
    vlan123:
      id: 123
      link: vlanif0
      addresses: &lt;something>
</pre>
</blockquote>

<p>This way you only need to change one thing if your VLAN network
interface changes, but at the cost of doing a non-standard way of
setting up the base interface. (Yes, Netplan accepts it, but it's
not how the Ubuntu installer will create your netplan files and who
knows what other Canonical tools will have a problem with it as a
result.)</p>

<p>We have one future Ubuntu server where we're going to need to set
up a lot of VLANs on one underlying physical interface. I'm not
sure which option we're going to pick, but the 'vlanif0' option
is certainly tempting. If nothing else, it probably means we can
put all of the VLANs into a separate, generic Netplan file.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/NetplanVlanAnnoyance

---

*ID: f9e4a69302c2f42a*
*抓取时间: 2026-03-12T13:49:26.048690*
