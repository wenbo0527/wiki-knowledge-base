# Systemd and blocking connections to localhost, including via 'any'

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-09T04:21:16Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I recently discovered <a href="https://utcc.utoronto.ca/~cks/space/blog/web/LocalhostSurpriseAccessViaAny">a surprising path to accessing localhost
URLs and services</a>, where
instead of connecting to 127.0.0.1 or the IPv6 equivalent, you
connected to 0.0.0.0 (or the IPv6 equivalent). In that entry I
mentioned that I didn't know if <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html#IPAddressAllow=ADDRESS%5B/PREFIXLENGTH%5D%E2%80%A6">systemd's IPAddressDeny</a>
would block this. I've now tested this, and the answer is that
systemd's restrictions do block this. If you set
'IPAddressDeny=localhost', the service or whatever is blocked from
the 0.0.0.0 variation as well (for both outbound and inbound
connections). This is exactly the way it should be, so you might
wonder why I was uncertain and felt I needed to test it.</p>

<p>There are a variety of ways at different levels that you might
implement access controls on a process (or a group of processes)
in Linux, for IP addresses or anything else. For example, you might
create an eBPF program that filtered the system calls and system
call arguments allowed and attach it to a process and all of its
children using <a href="https://www.man7.org/linux/man-pages/man2/seccomp.2.html">seccomp(2)</a>.
Alternately, for filtering IP connections specifically, you might
use <a href="https://docs.ebpf.io/linux/program-type/BPF_PROG_TYPE_CGROUP_SOCK_ADDR/">a cgroup socket address eBPF program</a>
(<a href="https://eunomia.dev/tutorials/cgroup/">also</a>), which are among
the <a href="https://docs.ebpf.io/linux/program-type/">the cgroup program types</a>
that are available. Or perhaps you'd prefer to use <a href="https://docs.ebpf.io/linux/program-type/BPF_PROG_TYPE_CGROUP_SKB/">a cgroup socket
buffer program</a>.</p>

<p>How a program such as systemd implements filtering has implications
for what sort of things it has to consider and know about when doing
the filtering. For example, if we reasonably conclude that the
kernel will have mapped 0.0.0.0 to 127.0.0.1 by the time it invokes
cgroup socket address eBPF programs, such a program doesn't need
to have any special handling to block access to localhost by people
using '0.0.0.0' as the target address to connect to. On the other
hand, if you're filtering at the system call level, the kernel has
almost certainly not done such mapping at the time it invokes you,
so your connect() filter had better know that '0.0.0.0' is equivalent
to 127.0.0.1 and it should block both.</p>

<p>This diversity is why I felt I couldn't be completely sure about
systemd's behavior without actually testing it. To be honest, I
didn't know what the specific options were until I researched them
for this entry. I knew systemd used eBPF for <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html#IPAddressAllow=ADDRESS%5B/PREFIXLENGTH%5D%E2%80%A6">IPAddressDeny</a>
(because it mentions that in the manual page in passing), but I vaguely
knew there are a lot of ways and places to use eBPF and I didn't know if
systemd's way needed to know about 0.0.0.0 or if systemd did know.</p>

<h3>Sidebar: What systemd uses</h3>

<p>As I found out through use of '<a href="https://man.archlinux.org/man/bpftool.8.en">bpftool</a> <a href="https://man.archlinux.org/man/bpftool-cgroup.8.en">cgroup</a> list
/sys/fs/cgroup/&lt;relevant thing>' on a systemd service that I knew
uses systemd IP address filtering, systemd uses <a href="https://docs.ebpf.io/linux/program-type/BPF_PROG_TYPE_CGROUP_SKB/">cgroup socket
buffer programs</a>, and
is presumably looking for good and bad IP addresses and netblocks
in those programs. This unfortunately means that it would be hard for
systemd to have different filtering for inbound connections as opposed
to outgoing connections, because at the socket buffer level it's all
packets.</p>

<p>(You'd have to go up a level to more complicated filters on <a href="https://docs.ebpf.io/linux/program-type/BPF_PROG_TYPE_CGROUP_SOCK_ADDR/">socket
address operations</a>.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdAndConnectToAny

---

*ID: 74cc766bd740338d*
*抓取时间: 2026-03-12T13:49:26.048382*
