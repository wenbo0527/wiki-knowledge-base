# How GNU Tar handles deleted things in incremental tar archives

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-19T04:10:50Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Suppose, not hypothetically, that you have a system that uses GNU
Tar for its full and incremental backups (such as <a href="https://en.wikipedia.org/wiki/Amanda_(software)">Amanda</a>).  Or maybe you
use GNU Tar directly for this. If you have an incremental backup
tar archive, you might be interested in one or both of two questions,
which are in some ways mirrors of each other: what files were deleted
between the previous incremental and this incremental, or what's
the state of the directory tree as of this incremental (if it and
all previous backups it depends on were properly restored).</p>

<p>(These questions are of deep interest to people who may have deleted
some amount of files but they're not sure exactly what files have
been deleted.)</p>

<p><a href="https://utcc.utoronto.ca/~cks/space/blog/tech/IncrementalBackupsTwoChallenges">Handling deleted files is one of the challenges of incremental
backups</a>, with various
approaches. How GNU Tar handles deleted files is sort of documented
in <a href="https://www.gnu.org/software/tar/manual/html_node/Incremental-Dumps.html">Using tar to perform incremental dumps</a>
and <a href="https://www.gnu.org/software/tar/manual/html_node/Dumpdir.html">Dumpdir</a>,
but the documentation doesn't explain it specifically. The simple
version is that GNU Tar doesn't explicitly record deletions; instead,
<strong>every incremental tar archive carries a full listing of the
directory tree</strong>, covering both things that are in this incremental
archive and things that come from previous ones. To deduce deleted
files, you have to compare two listings of the directory tree.</p>

<p>(As part of this full listing, an incremental tar archive records
every directory, even unchanged ones.)</p>

<p>You can get at these full listings with '<code>tar --list --incremental
--verbose --verbose --file ...</code>', but tar prints them in an
inconvenient format. You don't get a directory tree, the way you
do with plain 'tar -t'; instead you get the <a href="https://www.gnu.org/software/tar/manual/html_node/Dumpdir.html">Dumpdir</a> contents
of each directory printed out separately, and it's up to you to
post-process the results to assemble a directory tree with full
paths and so on. People have probably written tools to do this,
either from tar's output or by directly reading the GNU Tar incremental
tar archive format.</p>

<p>In my view, GNU Tar's approach is sensible and it comes with some
useful properties (although there are tradeoffs). Conveniently, you
can reconstruct the full directory tree as of that point in time
from any single incremental archive; you don't have to go through
a series of them to build up the picture. This probably also makes
things somewhat more resilient if you're missing some incremental
archives in the middle, since at least you know what's supposed to
be there but you don't have any copy of. Finding where a single
file was deleted is better than it would be if there were explicit
deletion records, since you can do a binary search across incrementals
to find the first one where it doesn't appear. The lack of explicit
deletion reports does make it inconvenient to determine everything
that was deleted between two successive incrementals, but on the
other hand you can determine what was deleted (or added) between
any two tar archives without having to go through every incremental
between them.</p>

<p>(You could say that GNU Tar incremental archives have a snapshot
of the directory tree state instead of carrying a journal of changes
to the state.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/GNUTarIncrementalDeletes?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/GNUTarIncrementalDeletes

---

*ID: 5ec038379c66ea3c*
*抓取时间: 2026-03-12T13:49:26.048273*
