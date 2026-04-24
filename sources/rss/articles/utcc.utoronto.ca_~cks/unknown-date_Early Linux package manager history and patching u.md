# Early Linux package manager history and patching upstream source releases

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-01T03:19:38Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of the important roles of <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/WhySystemPackageManagers">Linux system package managers like
dpkg and RPM</a> is providing a single
interface to building programs from source even though the programs
may use a wide assortment of build processes. One of the source
building features that both dpkg and RPM included (I believe from
the start) is patching the upstream source code, as well as providing
additional files along with it. My impression is that today this is
considered much less important in package managers, and some may make
it at least somewhat awkward to patch the source release on the fly.
Recently I realized that there may be a reason for this potential
oddity in dpkg and RPM.</p>

<p>Both dpkg and RPM are very old (by Linux standards). As covered in
Andrew Nesbitt's <a href="https://nesbitt.io/2025/11/15/package-manager-timeline.html">Package Manager Timeline</a>, both
date from the mid-1990s (dpkg in January 1994, RPM in September
1995). Linux itself was quite new at the time and the Unix world
was still dominated by commercial Unixes (partly because <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/MarchOfTheCheap">the march
of x86 PCs</a> was only just starting). As a
result, Linux was a minority target for a lot of general Unix free
software (although obviously not for Linux specific software). I
suspect that this was compounded by limitations in early Linux libc,
where apparently it had some issues with standards (see eg <a href="http://freesoftwaremagazine.com/articles/history_of_glibc_and_linux_libc/">this</a>,
<a href="https://web.archive.org/web/20040411191201/http://people.redhat.com/~sopwith/old/glibc-vs-libc5.html">also</a>,
<a href="https://www.man7.org/linux/man-pages/man7/libc.7.html">also</a>,
<a href="https://en.wikipedia.org/wiki/Glibc#Fork_and_variant">also</a>).</p>

<p>As a minority target, I suspect that Linux regularly had problems
compiling upstream software, and for various reasons not all upstreams
were interested in fixing (or changing) that (especially if it
involved accepting patches to cope with a non standards compliant
environment; one reply was to tell Linux to get standards compliant).
This probably left early Linux distributions regularly patching
software in order to make it build on (their) Linux, leading to
first class support for patching upstream source code in early
package managers.</p>

<p>(I don't know for sure because <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/IndyDown">at that time</a> I
wasn't using Linux or x86 PCs, and I might have been vaguely in the
incorrect <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/LinuxIsAUnix">'Linux isn't Unix'</a> camp. <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/MyFirstLinux">My first Linux</a> came somewhat later.)</p>

<p>These days things have changed drastically. Linux is much more
standards compliant and of course it's a major platform. Free
software that works on non-Linux Unixes but doesn't build cleanly
on Linux is a rarity, so it's much easier to imagine (or have) a
package manager that is focused on building upstream source code
unaltered and where patching is uncommon and not as easy (or trivial)
as dpkg and RPM make it.</p>

<p>(You still need to be able to patch upstream releases to handle
security patches and so on, since projects don't necessarily publish
new releases for them. I believe some projects simply issue patches
and tell you to apply them to their current release. And you may
have to backport a patch yourself if you're sticking on an older
release of the project that they no longer do patches for.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/PatchingUpstreamsOnceNeeded

---

*ID: 22ac060cbe1eb1b6*
*抓取时间: 2026-03-12T13:49:26.048468*
