# The two subtypes of one sort of package managers, the "program manager"

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-28T02:08:55Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I've written before that one of the complications of talking about
package managers and package management is that <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/PackageManagersTwoTypes">there are two
common types of package managers</a>, <em>program
managers</em> (which manage installed programs on a system level) and
<em>module managers</em> (which manage package dependencies for your project
within a language ecosystem or maybe a broader ecosystem). Today I
realized that there is a further important division within program
managers.  I will call this division <em>application (package) managers</em>
and <em>system (package) managers</em>.</p>

<p>A system package manager is what almost all Linux distributions
have (in the form of Debian's dpkg and its set of higher level
tools, Fedora's RPM and its set of higher level tools, Arch's
<a href="https://wiki.archlinux.org/title/Pacman">pacman</a>, and so on). It
manages everything installed by the distribution on the system,
from the kernel all the way up to the programs that people run to
get work done, but certainly including what we think of as system
components like the core C library, basic POSIX utilities, and so
on. In modern usage, <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PatchesAndPackaging">all updates to the system are done by shipping
new package versions</a>, rather than
by trying to ship 'patches' that consist of only a few changed files
or programs.</p>

<p>(Some Linux distributions are moving some high level programs
like Chrome to an application package manager.)</p>

<p>An application package manager doesn't manage the base operating
system; instead it only installs, manages, and updates additional
(and optional) software components. Sometimes these are actual
applications, but at other times, especially historically, these
were things like <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/PackagingHistory">the extra-cost C compiler from your commercial
Unix vendor</a>. On Unix, files from these
application packages were almost always installed outside of the
core system areas like /usr/bin; instead they might go into
/opt/&lt;something> or /usr/local or various other things.</p>

<p>(Sometimes vendor software comes with its own internal application
package manager, because the vendor wants to ship it in pieces and
let you install only some of them while managing the result. And if
you want to stretch things a bit, browsers have their own internal
'application package management' for addons.)</p>

<p>A system package manager can also be used for 'applications' and
routinely is; many Linux systems provide undeniable applications
like Firefox and LibreOffice through the system package manager
(not all of them, though). This can include third party packages
that put themselves in non-system places like /opt (on Unix) if
they want to. I think this is most common on Linux systems, where
there's no common dedicated application package manager that's
widely used, so third parties wind up building their own packages
for the system package manager (which is sure to be there).</p>

<p>For relatively obvious reasons, it's very hard to have multiple
system package managers in use on the same system at once; they
wind up fighting over who owns what and who changes what in the
operating system. It's relatively straightforward to have multiple
application package managers in use at once, provided that they
keep to their own area so that they aren't overwriting each other.</p>

<p>For the most part, the *BSDs have taken a <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/LinuxBSDBaseHistory">base system plus
application manager approach</a>, with
things like their 'ports' system being their application manager.
Where people use third party program managers, including <a href="https://www.pkgsrc.org/">pkgsrc</a> on multiple Unixes, Homebrew on macOS,
and so on, these are almost always application managers that don't
try to also take over and manage the core ('base') operating system
programs, libraries, and so on.</p>

<p>(As a result, the *BSDs ship system updates as 'patches', not
as new packages, cf <a href="https://man.openbsd.org/syspatch">OpenBSD's syspatch</a>. I've heard some rumblings that
FreeBSD may be working to change this.)</p>

<p>I believe that Microsoft Windows has some degree of system package
management, in that it has components that you might or might not
install and that can be updated or restored independently, but I
don't have much exposure to the Windows world. I will let macOS
people speak up in the comments about how that system operates (as
people using macOS experience, not as how it's developed; as developed
there are a bunch of different parts to macOS, as one can see from
the various open source repositories that Apple publishes).</p>

<p>PS: The Linux <a href="https://en.wikipedia.org/wiki/Flatpak">flatpak</a>
movement is mostly or entirely an application manager, and so usually
separate from the system package manager (<a href="https://en.wikipedia.org/wiki/Snap_(software)">Snap</a> is the same thing
but I ignore Canonical's not-invented-here pet projects as much as
possible). You can also see containers as an extremely overweight
application 'package' delivery model.</p>

<p>PPS: In my view, to count as package management a system needs to
have multiple 'packages' and have some idea of what packages are
installed. It's common but not absolutely required for the package
manager to keep track of what files belong to what package. Generally
this goes along with a way to install and remove packages. A system
can be divided up into components without having package management,
for example if there's no real tracking of what components you've
installed and they're shipped as archives that all get unpacked in
the same hierarchy with their files jumbled together.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/PackageManagersTwoTypesIII?showcomments#comments">7 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/PackageManagersTwoTypesIII

---

*ID: d5f51c33d0260038*
*抓取时间: 2026-03-12T13:49:26.048515*
