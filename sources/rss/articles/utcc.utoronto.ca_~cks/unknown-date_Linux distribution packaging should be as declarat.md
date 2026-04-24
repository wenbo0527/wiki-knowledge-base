# Linux distribution packaging should be as declarative as possible

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-30T01:49:05Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>A commentator on <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PackagesWhyComplicated">my entry on why Debian and RPM (source) packages
are complicated</a> suggested looking at Arch
Linux packaging, where most of the information is in a single file
as more or less a shell script (<a href="https://gitlab.archlinux.org/archlinux/packaging/packages/dovecot/-/blob/main/PKGBUILD?ref_type=heads">example</a>).
Unfortunately, I'm not a fan of this sort of shell script or shell
script like format, ultimately because it's only declarative by
convention (although I suspect Arch enforces some of those conventions).
One reason that declarative formats are important is that you can
analyze and understand what they do without having to execute code.
Another reason is that such formats naturally standardize things,
which makes it much more likely that any divergence from the standard
approach is something that matters, instead of a style difference.</p>

<p>Being able to analyze and manipulate declarative (source) packaging
is useful for large scale changes within a distribution. The <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DebianAndRPMSourcePackages">RPM
source package format</a> uses standard,
more or less declarative macros to build most software, which I
understand has made it relatively easy to build a lot of software
with special C and C++ hardening options. You can inject similar
things into a shell script based environment, but then you wind up
with ad-hoc looking modifications in some circumstances, <a href="https://gitlab.archlinux.org/archlinux/packaging/packages/dovecot/-/blob/main/PKGBUILD?ref_type=heads#L108">as we
see in the Dovecot example</a>.</p>

<p>Some things about declarative source packages versus Arch style
minimalism are issues of what could be called 'hygiene'. RPM packages
push you to list and categorize what files will be included in the
built binary package, rather than simply assuming that everything
installed into a scratch hierarchy should be packaged. This can be
frustrating (and there are shortcuts), but it does give you a chance
to avoid accidentally shipping unintended files. You could do this
with shell script style minimal packaging if you wanted to, of
course. Both RPM and Debian packages have standard and relatively
declarative ways to modify a pristine upstream package, and while
you can do that in Arch packages, it's not declarative, which hampers
various sorts of things.</p>

<p>Basically my feeling is that at scale, you're likely to wind up
with something that's essentially as formulaic as a declarative
source package format without having its assured benefits. There
will be standard templates that everyone is supposed to follow and
they mostly will, and you'll be able to mostly analyze the result,
and that 'mostly' qualification will be quietly annoying.</p>

<p>(On the positive side, the Arch package format does let you run
shellcheck on your shell stanzas, which isn't straightforward to
do in the RPM source format.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PackagingShouldBeDeclarative?showcomments#comments">4 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/PackagingShouldBeDeclarative

---

*ID: 85fbfa30d49e3b86*
*抓取时间: 2026-03-12T13:49:26.048827*
