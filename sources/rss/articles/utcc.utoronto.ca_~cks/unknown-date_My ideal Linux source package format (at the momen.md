# My ideal Linux source package format (at the moment)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-31T04:25:50Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I've written recently on <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PackagesWhyComplicated">why source packages are complicated</a> and <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PackagingShouldBeDeclarative">why packages should be declarative</a> (in contrast to Arch style shell
scripts), but I haven't said anything about what I'd like in a
source package format, which will mostly be from the perspective
of a system administrator who sometimes needs to modify upstream
packages or package things myself.</p>

<p>A source package format is a compromise. After my recent experiences
with <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes">dgit</a>, I now feel that the best
option is that a source package is a VCS repository directory tree
(Git by default) with special control files in a subdirectory.
Normally this will be the upstream VCS repository with packaging
control files and any local changes merged in as VCS commits. You
perform normal builds in this checked out repository, which has the
advantage of convenience and the disadvantage that you have to clean
up the result, possibly with liberal use of 'git clean' and 'git
reset'. Hermetic builds are done by some tool that copies the checked
out files to a build area, or clones the repository, or some other
option. If a binary package is built in an environment where this
information is available, its metadata should include the exact
current VCS commit it was built from, and I would make binary
packages not build if there were uncommitted changes.</p>

<p>(Making the native source package a VCS tree with all of the source
code makes it easy to work on but mingles package control files
with the program source. In today's environment with good distributed
VCSes I think this is the right tradeoff.)</p>

<p>The control files should be as declarative as possible, and they
should directly express major package metadata such as version
numbers (unlike the Debian package format, where the version number
is derived from debian/changelog). There should be a changelog but
it should be relatively free-form, like RPM changelogs. Changelogs
are especially useful for local modifications because they go along
with the installed binary package, which means that you can get an
answer to 'what did we change in this locally modified package'
without having to find your source. The main metadata file that
controls everything should be kept simple; I would go as far as to
say it should have a format that doesn't allow for multi-line
strings, and anything that requires multi-line strings should go
in additional separate files (including the package description).
You could make it TOML but I don't think you should make it YAML.</p>

<p>Both the build time actions, such as configuring and compiling
the source, and the binary package install time actions should by
default be declarative; you should be able to say 'this is an
autoconf based program and it should have the following additional
options', and the build system will take care of everything else.
Similarly you should be able to directly express that the binary
package needs certain standard things done when it's installed,
like adding system users and enabling services. However, this will
never be enough so you should also be able to express additional
shell script level things that are done to prepare, build, install,
upgrade, and so on the package. Unlike RPM and Debian source packages
but somewhat like Arch packages, these should be separate files in
the control directory, eg 'pkgmeta/build.sh'. Making these separate
files makes it much easier to do things like run shellcheck on them
or edit them in syntax-aware editor environments.</p>

<p>(It should be possible to combine standard declarative prepare and
build actions with additional shell or other language scripting.
We want people to be able to do as much as possible with standard,
declarative things. Also, although I used '.sh', you should be able
to write these actions in other languages too, such as Python or
Perl.)</p>

<p>I feel that like RPMs, you should have to at least default to
explicitly declaring what files and directories are included in the
binary package. Like RPMs, these installed files should be analyzed
to determine the binary package dependencies rather than force you
to try to declare them in the (source) package metadata (although
you'll always have to declare build dependencies in the source
package metadata). Like build and install scripts, these file lists
should be in separate files, not in the main package metadata file.
The RPM collection of magic ways to declare file locations is complex
but useful so that, for example, you don't have to keep editing
your file lists when the Python version changes. I also feel that
you should have to specifically mark files in the file lists with
unusual permissions, such as setuid or setgid bits.</p>

<p>The natural way to start packing something new in this system would
be to clone its repository and then start adding the package control
files. The packaging system could make this easier by having
additional tools that you ran in the root of your just-cloned
repository and looked around to find indications of things like the
name, the version (based on repository tags), the build system in
use, and so on, and then wrote out preliminary versions of the
control files. More tools could be used incrementally for things
like generating the file lists; you'd run the build and 'install'
process, then have a tool inventory the installed files for you
(and in the process it could recognize places where it should change
absolute paths into specially encoded ones for things like 'the
current Python package location').</p>

<p>This sketch leaves a lot of questions open, such as what 'source
packages' should look like when published by distributions. One
answer is to publish the VCS repository but that's potentially quite
heavyweight, so you might want a more minimal form. However, once
you create a 'source only' minimal form without the VCS history,
you're going to want a way to disentangle your local changes from
the upstream source.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/MyIdealSourcePackageFormat?showcomments#comments">6 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/MyIdealSourcePackageFormat

---

*ID: 965ce4e419f7b3b9*
*抓取时间: 2026-03-12T13:49:26.048817*
