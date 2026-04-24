# Testing Linux memory limits is a bit of a pain

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-13T04:23:09Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>For reasons outside of the scope of this entry, I want to test how
various <a href="https://www.freedesktop.org/software/systemd/man/systemd.resource-control.html">systemd memory resource limits</a>
work and interact with each other (which means that I'm really
digging into <a href="https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html#usage-guidelines">cgroup v2 memory controls</a>).
When I started trying to do this, it turned out that I had no good
test program (or programs), although I had some ones that gave me
partial answers.</p>

<p>There are two complexities in memory usage testing programs in a
cgroups environment. First, you may be able to allocate more memory
than you can actually use, depending on your system's settings for
<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/LinuxVMOvercommit">strict overcommit</a>. So it's not enough to see
how much memory you can allocate using the mechanism of your choice
(I tend to use <a href="https://www.man7.org/linux/man-pages/man2/mmap.2.html">mmap()</a> rather than
go through language allocators). After you've either determined how
much memory you can allocate or allocated your target amount, you
have to at least force the kernel to materialize your memory by
writing something to every page of it. Since the kernel can probably
swap out some amount of your memory, you may need to keep repeatedly
reading all of it.</p>

<p>The second issue is that if you're not in strict overcommit (and
<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/StrictOvercommitCanOOM">sometimes even if you are</a>), the kernel
can let you allocate more memory than you can actually use and then
you try to use it, hit you with the OOM killer. For my testing, I
care about the actual usable amount of memory, not how much memory
I can allocate, so I need to deal with this somehow (and this is
where my current test programs are inadequate). Since the OOM killer
can't be caught by a process (that's sort of the point), the simple
approach is probably to have my test program progressively report
on how much memory its touched so far, so I can see how far it got
before it was OOM-killed. A more complex approach would be to do
the testing in a child process with progress reports back to the
parent so it could try to narrow in on how much it could use rather
than me guessing that I wanted progress reports every, say, 16
MBytes or 32 MBytes of memory touching.</p>

<p>(Hopefully the OOM killer would only kill the child and not the
parent, but with the OOM killer you can never be sure.)</p>

<p>I'm probably not the first person to have this sort of need, so I
suspect that other people have written test programs and maybe even
put them up somewhere. I don't expect to be able to find them in
today's ambient Internet search noise, plus this is very close to
the much more popular issue of testing your RAM memory.</p>

<p>(Will I put up my little test program when I hack it up? Probably
not, it's too much work to do it properly, with actual documentation
and so on. And these days I'm not very enthused about putting more
repositories on Github, so I'd need to find some alternate place.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/MemoryLimitTestingPain?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/MemoryLimitTestingPain

---

*ID: 68356291907142f1*
*抓取时间: 2026-03-12T13:49:26.048338*
