# Shooting myself in the foot with Git by accident

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-19T04:13:35Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Today <a href="https://mastodon.social/@cks/115741495131431212">I had a Git experience</a>:</p>

<blockquote><p>It has been '0' days since I hit a mysterious Git error out of
nowhere, during a completely routine 'git pull' in a repository that's
identical with upstream:</p>

<p>error: fetching ref refs/remotes/origin/master failed: incorrect old
value provided</p>

<p>What should I do? What's wrong? Good luck figuring it out. Fortunately
this is just a tracking repository, so maybe the correct answer is
'delete and re-clone'.</p>
</blockquote>

<p><a href="https://mastodon.social/@cks/115741986034855476">This turned out to be my own fault</a> (<a href="https://transfem.social/notes/agfbr0svx14q0aj1">as suggested
by a helpful Fediverse denizen</a>). I have copies
of <a href="https://github.com/openzfs/zfs">this repository</a> on several
hosts, and because I want to read every commit message in it, I try
to update all of those repositories at the same time, getting the
same new commits in each. This time around I accidentally opened
two windows on the same host and didn't notice, so when I ran 'git
pull' in each of them at the same time, they stepped on each other
somehow.</p>

<p>(I run the 'git pull' at the same time in each copy of the repository
to maximize the odds that they'll pull the same set of changes.
Pulling the same set of changes makes it easy to read all of the
commit messages only once. This is all a bit awkward but as far as
I know it's the easiest way to maintain multiple independent copies
of an upstream yet read all of the new commit messages only once.)</p>

<p>This isn't the first time I've accidentally done two overlapping
'git pull' operations on the same repository. I think it's the first
time I hit this error and also the first time I didn't notice what
the real problem was right away. Having <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SysadminAphorism">stubbed my toe</a> on this more than once, this time rather
vividly, hopefully in the future I'll remember to check for this
cause if I have weird things happen during Git operations.</p>

<p>Git has some locking around the Git index, which you can discover
if Git commands start complaining that an 'index.lock' file already
exists. I believe the general discussion of this is in <a href="https://git-scm.com/docs/api-lockfile">api-lockfile</a>, and if I'm reading it
right, 'index.lock' is not just the lock file, it's the new version
of the index file. Lock files are apparently also used for at least
<a href="https://git-scm.com/docs/commit-graph">the commit graph file</a>,
and <a href="https://git-scm.com/docs/git-config">the git-config manual page</a>
has a tantalizing list of various lock timeouts. However, there
evidently isn't enough locking to stop accidents completely,
especially for multi-step operations like 'git pull' (which is
actually 'git fetch' plus a fast-forward update done somehow).</p>

<p>(Based on <a href="https://stackoverflow.com/a/79382104">this</a>, I think
Git references like 'HEAD' can also be locked; <a href="https://git-scm.com/docs/git-config#Documentation/git-config.txt-corefilesRefLockTimeout">also</a>.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GitConcurrentUsageOops?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/GitConcurrentUsageOops

---

*ID: 5ed194c530128b0c*
*抓取时间: 2026-03-12T13:49:26.048941*
