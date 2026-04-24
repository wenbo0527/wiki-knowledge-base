# Early notes about using dgit on Ubuntu (LTS)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-23T04:25:34Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I recently read Ian Jackson's <a href="https://diziet.dreamwidth.org/20436.html">Debian’s git transition</a> (<a href="https://mastodon.me.uk/@Diziet/115760139095772594">via</a>) and
<a href="https://mastodon.social/@cks/115764239718631049">had a reaction</a>:</p>

<blockquote><p>I would really like to be able to patch and rebuild Ubuntu packages
from a git repository with our local changes (re)based on top of
upstream git. It would be much better than quilt'ing and debuild'ing
.dsc packages (I have non-complimentary opinions on the Debian source
package format). This news gives me hope that it'll be possible
someday, but especially for Ubuntu I have no idea how soon or how well
documented it will be.</p>

<p>(It could even be better than RPMs.)</p>
</blockquote>

<p>The subsequent discussion got me to try out <a href="https://manpages.debian.org/testing/dgit/dgit.1.en.html">dgit</a>, especially
since it had an attractive <a href="https://manpages.debian.org/testing/dgit/dgit-user.7.en.html">dgit-user(7)</a>
manual page that gave very simple directions on how to make a local
change to an upstream package. It turns out that things aren't
entirely smooth on Ubuntu, but they're workable.</p>

<p>The starting point is 'dgit clone', but on Ubuntu you currently get
to use special arguments that aren't necessary on Debian:</p>

<blockquote><pre style="white-space: pre-wrap;">
dgit clone -d ubuntu dovecot jammy,-security,-updates
</pre>
</blockquote>

<p>(You don't have to do this on a machine running 'jammy' (Ubuntu
22.04); it may be more convenient to do it from another one, perhaps
with a more up to date <a href="https://manpages.debian.org/testing/dgit/dgit.1.en.html">dgit</a>.)</p>

<p>The latest Ubuntu package for something may be in either their
&lt;release>-security or their &lt;release>-updates 'suite', so you need
both. I think this is equivalent to what 'apt-get source' gets you,
but you might want to double check. Once you've gotten the source
in a Git repository, you can modify it and commit those modifications
as usual, for example through <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/MagitPraise">Magit</a>.
If you have an existing locally patched version of the package that
you did with <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PatchingRPMsWithQuilt">quilt</a>, you can import all
of the quilt patches, either one by one or all at once and then
<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GitSelectiveCommitWithMagit">using Magit's selective commits to sort things out</a>.</p>

<p>Having made your modifications, whether tentative or otherwise,
you can now automatically modify debian/changelog:</p>

<blockquote><pre style="white-space: pre-wrap;">
gbp dch --since dgit/dgit/jammy,-security,-updates --local .cslab. --ignore-branch --commit
</pre>
</blockquote>

<p>(You might want to use -S for snapshots when testing modifications
and builds, I don't know. <a href="https://support.cs.toronto.edu/">Our</a>
practice is to use --local to add a local suffix on the upstream
package number, so we can keep our packages straight.)</p>

<p>The special bit is the 'dgit/dgit/&lt;whatever you used in dgit clone>',
which tells <a href="https://manpages.debian.org/testing/git-buildpackage/gbp-dch.1.en.html">gbp-dch</a>
(part of the <a href="https://manpages.debian.org/testing/git-buildpackage/gbp.1.en.html">gbp</a> suite
of stuff) where to start the changelog from. Using --commit is
optional; what I did was to first run 'gbp dch' without it, then
use 'git diff' to inspect the resulting debian/changelog changes,
and then 'git restore debian/changelog' and re-run it with a better
set of options until eventually I added the '--commit'.</p>

<p>You can then install build-deps (if necessary) and build the binary
packages with the <a href="https://manpages.debian.org/testing/dgit/dgit-user.7.en.html">dgit-user(7)</a> recommended 'dpkg-buildpackage
-uc -b'. Normally I'd say that you absolutely want to build source
packages too, but since you have a Git repository with the state
frozen that you can rebuild from, I don't think it's necessary here.</p>

<p>(After the build finishes you can admire 'git status' output that
will tell you just how many files in your source tree the Debian
or Ubuntu package building process modified. One of the nice things
about using Git and building from a Git repository is that you can
trivially fix them all, rather than the usual set of painful
workarounds.)</p>

<p>The <a href="https://manpages.debian.org/testing/dgit/dgit-user.7.en.html">dgit-user(7)</a> manual page suggests but doesn't confirm that
if you're bold, you can build from a tree with uncommitted changes.
Personally, even if I was in the process of developing changes I'd
commit them and then make liberal use of rebasing, <a href="https://github.com/tummychow/git-absorb">git-absorb</a>, <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GitUpdatingLocalChangesWithMore">and so on</a> to keep updating
my (committed) changes.</p>

<p>It's not clear to me how to integrate upstream updates (for example,
a new Ubuntu update to the Dovecot package) with your local changes.
It's possible that '<a href="https://manpages.debian.org/testing/dgit/dgit.1.en.html">dgit</a> pull' will automatically rebase your
changes, or give you the opportunity to do that. If not, you can
always do another 'dgit clone' and then <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GitMovingChangesEasyWay">manually import your Git
changes as patches</a>.</p>

<p>(A disclaimer: at this point I've only cloned, modified, and built
one package, although it's a real one we use. Still, I'm sold; the
ability to reset the tree after a build is valuable all by itself,
never mind having a better way than quilt to handle making changes.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes

---

*ID: f325db71569b99e4*
*抓取时间: 2026-03-12T13:49:26.048899*
