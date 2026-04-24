# Why Linux wound up with system package managers

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-29T04:37:48Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Yesterday I discussed <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/PackageManagersTwoTypesIII">the two sorts of program package managers</a>, <em>system package managers</em> that
manage the whole system and <em>application package managers</em> that
mostly or entirely manage third party programs. <a href="https://mastodonapp.uk/@JdeBP/115971958570664653">Commercial Unix
got application package managers in the very early 1990s</a>, but <a href="https://nesbitt.io/2025/11/15/package-manager-timeline.html">Linux's
first program managers were system package managers</a>, in
dpkg and RPM (or at least those seem to be the first Linux package
managers).</p>

<p>The <a href="https://nesbitt.io/2026/01/27/the-c-shaped-hole-in-package-management.html">abstract way to describe why</a>
is to say that Linux distributions had to assemble a whole thing
from separate pieces; the kernel came from one place, libc from
another, coreutils from a third, and so on. The concrete version
is to think about what problems you'd have without a package manager.
Suppose that you assembled a directory tree of all of the source
code of the kernel, libc, coreutils, GCC, and so on. Now you need
to build all of these things (or rebuild, let's ignore bootstrapping
for the moment).</p>

<p>Building everything is complicated partly because everything goes
about it differently. The kernel has its own configuration and build
system, a variety of things use autoconf but not necessarily with
the same set of options to control things like features, GCC has a
multi-stage build process, Perl has its own configuration and
bootstrapping process, X is frankly weird and vaguely terrifying,
and so on. Then not everyone uses 'make install' to actually install
their software, so you have another set of variations for all of
this.</p>

<p>(The less said about the build processes for either TeX or GNU
Emacs in the early to mid 1990s, the better.)</p>

<p>If you do this at any scale, you need to keep track of all of this
information (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MyConfigureSolution">cf</a>) and you want
a uniform interface for 'turn this piece into a compiled and ready
to unpack blob'. That is, you want <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PackagesWhyComplicated">a source package</a> (which encapsulates all of the 'how to do
it' knowledge) and a command that takes a source package and does
a build with it. Once you're building things that you can turn into
blobs, <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PatchesAndPackaging">it's simpler to always ship a new version of the blob
whenever you change anything</a>.</p>

<p>(You want the 'install' part of 'build and install' to result in a
blob rather than directly installing things on your running system
because until it finishes, you're not entirely sure the build and
install has fully worked. Also, this gives you an easy way to split
overall system up into multiple pieces, some of which people don't
have to install. And in the very early days, <a href="https://en.wikipedia.org/wiki/Softlanding_Linux_System#Series">to split them across
multiple floppy disks, as SLS did</a>.)</p>

<p>Now you almost have a system package manager with source packages
and binary packages. You're building all of the pieces of your Linux
distribution in a standard way from something that looks a lot like
source packages, and you pretty much want to create binary blobs
from them rather than dump everything into a filesystem. People
will obviously want a command that takes a binary blob and 'installs'
it by unpacking it on their system (and possibly extra stuff),
rather than having to run 'tar whatever' all the time themselves,
and they'll also want to automatically keep track of which of your
packages they've installed rather than having to keep their own
records. Now you have all of the essential parts of a system package
manager.</p>

<p>(Both dpkg and RPM also keep track of which package installed what
files, which is important for upgrading and removing packages, along
with things having versions.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/WhySystemPackageManagers

---

*ID: 4b42b89393856217*
*抓取时间: 2026-03-12T13:49:26.048504*
