# Distribution source packages and whether or not to embed in the source code

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-10T03:46:05Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>When I described <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/MyIdealSourcePackageFormat">my current ideal Linux source package format</a>, I said that it should be embedded in
the source code of the software being packaged. In a comment,
<a href="https://bitprophet.org/">bitprophet</a> had a perfectly reasonable
and good preference the other way:</p>

<blockquote><p>Re: other points: all else equal I think I vaguely prefer the Arch
"repo contains just the extras/instructions + a reference to the
upstream source" approach as it's cleaner overall, and makes it easier
to do "more often than it ought to be" cursed things like "apply
some form of newer packaging instructions against an older upstream
version" (or vice versa).</p>
</blockquote>

<p>The Arch approach is isomorphic to the source RPM format, which has
various extras and instructions plus a pre-downloaded set of upstream
sources. It's not really isomorphic to the Debian source format
because you don't normally work with the split up version; the split
up version is just a package distribution thing (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes">as dgit shows</a>).</p>

<p>(I believe the Arch approach is also how the FreeBSD and OpenBSD
ports trees work. Also, the source package format you work in is
not necessarily how you bundle up and distribute source packages,
again as shown by Debian.)</p>

<p>Let's call these two packaging options the <em>inline</em> approach (Debian)
and the <em>out of line</em> approach (Arch, RPM). My view is that which
one you want depends on what you want to do with software and
packages. The out of line approach makes it easier to build unmodified
packages, and as <a href="https://bitprophet.org/">bitprophet</a> comments it's easy to do weird build
things. If you start from a standard template for the type of build
and install the software uses, you can practically write the packaging
instructions yourself. And the files you need to keep are quite
compact (and if you want, it's relatively easy to put a bunch of
them into a single VCS repository, each in its own subdirectory).</p>

<p>However, the out of line approach makes modifying upstream software
much more difficult than a good version of the inline approach (such
as, for example, <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes">dgit</a>). To modify upstream
software in the out of line approach you have to go through some
process similar to what you'd do in the inline approach, and then
turn your modifications into patches that your packaging instructions
apply on top of the pristine upstream. Moving changes from version
to version may be painful in various ways, and in addition to those
nice compact out of line 'extras/instructions' package repos, you
may want to keep around your full VCS work tree that you built the
patches from.</p>

<p>(Out of line versus inline is a separate issue from whether or not
the upstream source code should include packaging instructions in
any form; <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/UpstreamPackagingProblem">I think that generally the upstream should not</a>.)</p>

<p>As a system administrator, <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/MyIdealSourcePackageFormat">I'm biased toward easy modification
of upstream packages and thus upstream source</a>
because that's most of why I need to build my own packages. However,
these days I'm not sure if that's what a Linux distribution should
be focusing on. This is especially true for 'rolling' distributions
that mostly deal with security issues and bugs not by patching their
own version of the software but by moving to a new upstream version
that has the security fix or bug fix. If most of what a distribution
packages is unmodified from the upstream version, optimizing for
that in your (working) source package format is perfectly sensible.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/SourcePackagesEmbedSourceOrNot

---

*ID: 637aafc1953575a1*
*抓取时间: 2026-03-12T13:49:26.048710*
