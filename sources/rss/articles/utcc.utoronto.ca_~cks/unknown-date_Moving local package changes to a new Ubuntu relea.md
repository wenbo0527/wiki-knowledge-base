# Moving local package changes to a new Ubuntu release with dgit

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-23T23:55:32Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Suppose, not entirely hypothetically, that you've made local changes
to an Ubuntu package on one Ubuntu release, such as 22.04 ('jammy'),
and now you want to move to another Ubuntu release such as 24.04
('noble'). If you're working with straight 'apt-get source' Ubuntu
source packages, this is done by tediously copying all of your
patches over (hopefully the package uses <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/PatchingRPMsWithQuilt">quilt</a>)
to duplicate and recreate your 22.04 work.</p>

<p>If you're using <a href="https://manpages.debian.org/testing/dgit/dgit.1.en.html">dgit</a>, this is
much easier. Partly this is because dgit is based on Git, but partly
this is because dgit has an extremely convenient feature where it
can have several different releases in the same Git repository. So
here's what we want to do, assuming <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes">you have a dgit repository for
your package already</a>.</p>

<p>(For safety you may want to do this in a copy of your repository.
I make rsync'd copies of Git repositories all the time for stuff
like this.)</p>

<p>Our first step is to fetch the new 24.04 ('noble') version of the
package into our dgit repository as a new dgit branch, and then
check out the branch:</p>

<blockquote><pre style="white-space: pre-wrap;">
dgit fetch -d ubuntu noble,-security,-updates
</pre>

<pre style="white-space: pre-wrap;">
dgit checkout noble,-security,-updates
</pre>
</blockquote>

<p>We could do this in one operation but I'd rather do it in two, in
case there are problems with the fetch.</p>

<p>The Git operation we want to do now is to <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GitPickingRightApproach">cherry-pick</a> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GitRebaseVsCherrypick">also</a>) our changes to the 22.04
version of the package onto the 24.04 version of the package. If
this goes well the changes will apply cleanly and we're done.
However, there is a complication. If we've followed <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DgitOnUbuntuEarlyNotes">the usual
process for making dgit-based local changes</a>,
the last commit on our 22.04 version is an update to debian/changelog.
We don't want that change, because we need to do our own 'gbp dch'
on the 24.04 version after we've moved our own changes over to make
our own 24.04 change to debian/changelog (among other things, the
22.04 changelog change has the wrong version number for the 24.04
package).</p>

<p>In general, cherry-picking all our local changes is 'git cherry-pick
old-upstream..old-local'. To get all but the last change, we want
'old-local~' instead. Dgit has long and somewhat obscure branch
names; its upstream for our 22.04 changes is
'dgit/dgit/jammy,-security,-updates' (ie, the full 'suite' name we
had to use with 'dgit clone' and 'dgit fetch'), while our local
branch is 'dgit/jammy,-security,-updates'. So our full command,
with a 'git log' beforehand to be sure we're getting what we want,
is:</p>

<blockquote><pre style="white-space: pre-wrap;">
git log dgit/dgit/jammy,-security,-updates..dgit/jammy,-security,-updates~
</pre>

<pre style="white-space: pre-wrap;">
git cherry-pick dgit/dgit/jammy,-security,-updates..dgit/jammy,-security,-updates~
</pre>
</blockquote>

<p>(We've seen this dgit/dgit/... stuff before when doing 'gbp dch'.)</p>

<p>Then we need to make our debian/changelog update. Here, as an
important safety tip, don't blindly copy the command you used while
building the 22.04 package, using 'jammy,...' in the --since argument,
because that will try to create a very confused changelog of
everything between the 22.04 version of the package and the 24.04
version. Instead, you obviously need to update it to your new 'noble'
24.04 upstream, making it:</p>

<blockquote><pre style="white-space: pre-wrap;">
gbp dch --since dgit/dgit/noble,-security,-updates --local .cslab. --ignore-branch --commit
</pre>
</blockquote>

<p>('git reset --hard HEAD~' may be useful if you make a mistake here.
As they say, ask me how I know.)</p>

<p>If the cherry-pick doesn't apply cleanly, you'll have to resolve
that yourself. If the cherry-pick applies cleanly but the result
doesn't build or perhaps doesn't work because the code has changed
too much, you'll be <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GitUpdatingLocalChangesWithMore">using various ways to modify and update your
changes</a>. But at
least this is a bunch easier than trying to sort out and update a
quilt-based patch series.</p>

<h3>Appendix: Dealing with Ubuntu package updates</h3>

<p>Based on <a href="https://mastodon.social/@cks/115769365150522346">this</a>
<a href="https://mastodon.me.uk/@Diziet/115769377698929398">conversation</a>,
if Ubuntu releases a new version of the package, what I think I need
to do is to use 'dgit fetch' and then explicitly rebase:</p>

<blockquote><pre style="white-space: pre-wrap;">
dgit fetch -d ubuntu
</pre>
</blockquote>

<p>You have to use '-d ubuntu' here or 'dgit fetch' gets confused and
fails. There may be ways to fix this with git config settings, but
setting them all is exhausting and if you miss one it explodes, so
I'm going to have to use '-d ubuntu' all the time (unless dgit fixes
this someday).</p>

<p>Dgit repositories don't have an explicit Git upstream set, so I
don't think we can use <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GitRebaseUnderstanding">plain rebase</a>. Instead I think we need
the more complicated form:</p>

<blockquote><pre style="white-space: pre-wrap;">
git rebase dgit/dgit/jammy,-security,-updates dgit/jammy,-security,-updates
</pre>
</blockquote>

<p>(Until I do it for real, these arguments are speculative. I believe
they should work if I understand 'git rebase' correctly, but I'm not
completely sure. I might need the full three argument form and to make
the 'upstream' a commit hash.)</p>

<p>Then, as above, we need to drop our debian/changelog change and redo
it:</p>

<blockquote><pre style="white-space: pre-wrap;">
git reset --hard HEAD~
</pre>

<pre style="white-space: pre-wrap;">
gbp dch --since dgit/dgit/jammy,-security,-updates --local .cslab. --ignore-branch --commit
</pre>
</blockquote>

<p>(There may be a clever way to tell 'git rebase' to skip the last
change, or you can do an interactive rebase (with '-i') instead of
a non-interactive one and delete it yourself.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/DgitForwardPortingChanges

---

*ID: 370e752a271dcb69*
*抓取时间: 2026-03-12T13:49:26.048889*
