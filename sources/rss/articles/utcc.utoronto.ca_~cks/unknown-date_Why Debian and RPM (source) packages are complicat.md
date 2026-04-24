# Why Debian and RPM (source) packages are complicated

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-28T02:44:17Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>A commentator on <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes">my early notes on dgit</a>
mentioned that they found packaging in Debian overly complicated
(and I think perhaps RPMs as well) and would rather build and ship
a container. On the one hand, this is in a way fair; my impression
is that the process of specifying and building a container is rather
easier than for source packages. On the other hand, Debian and RPM
source packages are complicated for good reasons.</p>

<p>Any reasonably capable source package format needs to contain a
number of things. A source package needs to supply the original
upstream source code, some amount of distribution changes, instructions
for building and 'installing' the source, a list of (some) dependencies
(for either or both build time and install time), a list of files
and directories it packages, and possibly additional instructions
for things to do when the binary package is installed (such as
creating users, enabling services, and so on). Then generally you
need some system for <a href="https://rpm-software-management.github.io/mock/feature-hermetic-builds.html">'hermetic' builds</a>,
ones that don't depend on things in your local (Linux) login
environment. You'll also want some amount of metadata to go with
the package, like a name, a version number, and a description. Good
source package formats also support building multiple binary packages
from a single source package, because sometimes you want to split
up the built binary files to reduce the amount of stuff some people
have to install. A built binary package contains a subset of this;
it has (at least) the metadata, the dependencies, a file list, all
of the files in the file list, and those install and upgrade time
instructions.</p>

<p>Built containers are a self contained blob plus some metadata. You
don't need file lists or dependencies or install and removal actions
because all of those are about interaction with the rest of the
system and by design containers don't interact with the rest of the
system. To build a container you still need some of the same
information that a source package has, but you need less and it's
deliberately more self-contained and freeform. Since the built
container is a self contained artifact you don't need a file list,
I believe it's uncommon to modify upstream source code as part of
the container build process (instead you patch it in advance in
your local repository), and your addition of users, activation of
services, and so on is mostly free form and at container build time;
once built the container is supposed to be ready to go. And my
impression is that in practice people mostly don't try to do things
like multiple UIDs in a single container.</p>

<p>(You may still want or need to understand what things you install
where in the container image, but that's your problem to keep track
of; the container format itself only needs a little bit of information
from you.)</p>

<p>Containers have also learned from source packages in that they can
be layered, which is to say that you can build your container by
starting from some other container, either literally or by sticking
another level of build instructions on the end. Layered source
packages don't make any sense when you're thinking like a distribution,
but they make a lot of sense for people who need to modify the
distribution's source packages (this is what <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes">dgit makes much
easier</a>, partly because Git is effectively
a layering system; that's one way to look at a sequence of Git
commits).</p>

<p>(My impression of container building is that it's a lot more ad-hoc
than package building. Both Debian and RPM have tried to standardize
and automate a lot of the standard source code building steps, like
running autoconf, but the cost of this is that each of them has a
bespoke set of 'convenient' automation to learn if you want to build
a package from scratch. With containers, you can probably mostly
copy the upstream's shell-based build instructions (or these days,
their Dockerfile).)</p>

<p>Dgit based building of (potentially modified) Debian packages can
be surprisingly close to the container building experience. Like
containers, you first prepare your modifications in a repository
and then you run some relatively simple commands to build the
artifacts you'll actually use. Provided that your modifications
don't change the dependencies, files to be packaged, and so on, you
don't have to care about how Debian defines and manipulates those,
plus you don't even need to know exactly how to build the software
(the Debian stuff takes care of that for you, which is to say that
the Debian package builders have already worked it out).</p>

<p>In general I don't think you can get much closer to the container
build experience other than the dgit build experience or the general
RPM experience (if you're starting from scratch). <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PackagingTakesWork">Packaging takes
work</a> because packages aren't isolated, self
contained objects; they're objects that need to be integrated into
a whole system in a reversible way (ie, you can uninstall them, or
upgrade them even though the upgraded version has a somewhat different
set of files). You need more information, more understanding, and
a more complicated build process.</p>

<p>(Well, I suppose there are <a href="https://en.wikipedia.org/wiki/Flatpak">flatpaks</a> (and snaps). But these
mostly don't integrate with the rest of your system; they're
explicitly designed to be self-contained, standalone artifacts that
run in a somewhat less isolated environment than containers.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PackagesWhyComplicated?showcomments#comments">4 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/PackagesWhyComplicated

---

*ID: e22d962646e3a68f*
*抓取时间: 2026-03-12T13:49:26.048848*
