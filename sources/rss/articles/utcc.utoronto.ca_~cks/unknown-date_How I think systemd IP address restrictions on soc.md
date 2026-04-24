# How I think systemd IP address restrictions on socket units works

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-06T04:43:52Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Among the <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html">systemd resource controls</a>
are <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html#IPAddressAllow=ADDRESS%5B/PREFIXLENGTH%5D%E2%80%A6"><code>IPAddressAllow=</code> and <code>IPAddressDeny=</code></a>,
which allow you to limit what IP addresses your systemd thing can
interact with. This is <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdAndConnectToAny">implemented with eBPF</a>.
A limitation of these as applied to systemd .service units is that
they restrict all traffic, both inbound connections and things your
service initiates (like, say, DNS lookups), while <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdPortFirewallWish">you may want
only a simple inbound connection filter</a>.
However, you can also set these on <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html">systemd.socket</a>
units. If you do, your IP address restrictions apply only to the socket (or
sockets), not to the service unit that it starts. To quote the
documentation:</p>

<blockquote><p>Note that for socket-activated services, the IP access list configured
on the socket unit applies to all sockets associated with it directly,
but not to any sockets created by the ultimately activated services
for it.</p>
</blockquote>

<p>So if you have a systemd socket activated service, you can control
who can access the socket without restricting who the service itself
can talk to.</p>

<p>In general, systemd IP access controls are done through eBPF programs
set up on cgroups. If you set up IP access controls on a socket,
such as ssh.socket in Ubuntu 24.04, you do get such eBPF programs
attached to the ssh.socket cgroup (and there is a ssh.socket cgroup,
perhaps because of the eBPF programs):</p>

<blockquote><pre style="white-space: pre-wrap;">
# pwd
/sys/fs/cgroup/system.slice
# bpftool cgroup list ssh.socket
ID  AttachType      AttachFlags  Name
12  cgroup_inet_ingress   multi  sd_fw_ingress
11  cgroup_inet_egress    multi  sd_fw_egress
</pre>
</blockquote>

<p>However, if you look there are no processes or threads in the
ssh.socket cgroup, which is not really surprising but also means
there is nothing there for these eBPF programs to apply to. And if
you dump the eBPF program itself (with 'ebpftool dump xlated id
12'), it doesn't really look like it checks for the port number.</p>

<p>What I think must be going on is that the eBPF filtering program
is connected to the SSH socket itself. Since I can't find any
relevant looking uses in the systemd code of the `<code>SO_ATTACH_*</code>'
BPF related options from <a href="https://www.man7.org/linux//man-pages/man7/socket.7.html">socket(7)</a> (which
would be used with <a href="https://www.man7.org/linux//man-pages/man2/setsockopt.2.html">setsockopt(2)</a> to
directly attach programs to a socket), I assume that what happens
is that if you create or perhaps start using a socket within a
cgroup, that socket gets tied to the cgroup and its eBPF programs,
and this attachment stays when the socket is passed to another
program in a different cgroup.</p>

<p>(I don't know if there's any way to see what eBPF programs are
attached to a socket or a file descriptor for a socket.)</p>

<p>If this is what's going on, it unfortunately means that there's no
way to extend this feature of socket units to get <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdPortFirewallWish">per-port IP
access control in .service units</a>. Systemd
isn't writing special eBPF filter programs for socket units that
only apply to those exact ports, which you could in theory reuse
for a service unit; instead, it's arranging to connect (only)
specific sockets to its general, broad IP access control eBPF
programs. Programs that make their own listening sockets won't be
doing anything to get eBPF programs attached to them (and only
them), so we're out of luck.</p>

<p>(One could experiment with relocating programs between cgroups,
with the initial cgroup in which the program creates its listening
sockets restricted and the other not, but I will leave that up to
interested parties.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdSocketIPRestrictions

---

*ID: 6965b69ebf060995*
*抓取时间: 2026-03-12T13:49:26.048103*
