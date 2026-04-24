# Systemd resource controls on user.slice and system.slice work fine

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-25T03:54:52Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>We have a number of systems where we traditionally set <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/LinuxVMOvercommit">strict
overcommit handling</a>, and <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdMemoryLimitVsOvercommit">for some time this
has caused us some heartburn</a>. Some
years ago I speculated that <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdMemoryLimitVsOvercommit">we might want to use resource controls
on user.slice or systemd.slice if they worked</a>, and then recently in a comment
<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/StrictOvercommitVsOOM">here</a> I speculated that this was the way to
(relatively) safely limit memory use if it worked.</p>

<p>Well, it does (as far as I can tell, without deep testing). If you
want to limit how much of the system's memory people who log in can
use so that system services don't explode, you can set <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html#MemoryMin=bytes,%20MemoryLow=bytes"><code>MemoryMin=</code></a>
on system.slice to guarantee some amount of memory to it and all
things under it. Alternately, you can set <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html#MemoryMax=bytes"><code>MemoryMax=</code></a>
on user.slice, collectively limiting all user sessions to that
amount of memory. In either case my view is that you might want to
set <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html#MemorySwapMax=bytes"><code>MemorySwapMax=</code></a>
on user.slice so that user sessions don't spend all of their time
swapping. Which one you set things on depends on which is easier
and you trust more; my inclination is MemoryMax, although that
means you need to dynamically size it depending on this machine's
total memory.</p>

<p>(If you want to limit user memory use you'll need to make sure that
things like <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdCronUserSlices">user cron jobs are forced into user sessions</a>, rather than running under cron.service in
system.slice.)</p>

<p>Of course this is what you should expect, given systemd's documentation
and <a href="https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files">the kernel documentation</a>.
On the other hand, the Linux kernel cgroup and memory system is
sufficiently opaque and ever changing that I feel the need to verify
that things actually do work (in our environment) as I expect them
to. Sometimes there are surprises, or settings that nominally work
but don't really affect things the way I expect.</p>

<p>This does raise the question of how much memory you want to reserve
for the system. It would be nice if you could use <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd-cgtop.html">systemd-cgtop</a>
to see how much memory your system.slice is currently using, but
unfortunately the number it will show is potentially misleadingly
high. This is because <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/CgroupsMemoryUsageAccountingII">the memory attributed to any cgroup includes
(much) more than program RAM usage</a>.
For example, on <a href="https://support.cs.toronto.edu/">our</a> it seems
typical for system.slice to be using under a gigabyte of 'user' RAM
but also several gigabytes of filesystem cache and other kernel
memory. You probably want to allow for some of that in what memory
you reserve for system.slice, but maybe not all of the current
usage.</p>

<p>(You can get the current version of the 'memdu' program I use
as <a href="https://www.cs.toronto.edu/~cks/software/memdu/memdu.py">memdu.py</a>.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdUserAndSystemSliceLimits

---

*ID: 18f2dc18c99eadbb*
*抓取时间: 2026-03-12T13:49:26.048202*
