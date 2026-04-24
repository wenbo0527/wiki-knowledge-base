# The Amanda backup system and "dump promotion"

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-09T03:05:50Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>The <a href="https://en.wikipedia.org/wiki/Amanda_(software)">Amanda backup system</a> is what <a href="https://support.cs.toronto.edu/">we</a> use to handle our backups.  One
of Amanda's core concepts is a 'dump cycle', the amount of time
between normally scheduled full backups for filesystems. If you
have a dumpcycle of 7 days and Amanda does a full backup of a
filesystem on Monday, its normal schedule for the next full backup
is next Monday. However, Amanda can 'promote' a full backup ahead
of schedule if it believes there's room for the full backup in a
given backup run. Promoting full backups is a good idea in theory
because it reduces how much data you need to restore a filesystem.</p>

<p>The <a href="https://linux.die.net/man/5/amanda.conf">amanda.conf</a>
configuration file has a per-dumptype option that affects this:</p>

<blockquote><dl><dt><strong>maxpromoteday</strong> <em>int</em> </dt>
<dd>Default: 10000. The maximum number of day[s]
for a promotion, set it 0 if you don't want promotion, set it to 1
or 2 if your disks get overpromoted.</dd>
</dl>
</blockquote>

<p>As written, I find this a little bit opaque (to be polite).  What
<code>maxpromoteday</code> controls is the maximum of how many days ahead of
the normal schedule Amanda will promote a full backup. For example,
if you have a 7-day dump cycle, a <code>maxpromoteday</code> of 2, and did a
full dump of a filesystem on Monday, the earliest Amanda will
possibly schedule a 'promoted' full backup is two days before next
Monday, so the coming Saturday or Sunday. By extension, if you set
<code>maxpromoteday</code> to '0', Amanda will only consider promoting a full
backup of a filesystem zero days ahead of schedule, which is to say
'not at all'. Any value larger than your 'dumpcycle' setting has
no effect, because Amanda is already doing full backups that often
and so a larger value doesn't add any extra constraints on Amanda's
scheduling of full backups.</p>

<p>You might wonder why you'd want to set '<code>maxpromoteday</code>' down to
limit full backup promotions, and naturally there is a story here.</p>

<p>Amanda is a very old backup system, and although it's not necessarily
used with physical tapes and tape robots today (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DiskBackupSystemII">our 'tapes' are
HDDs</a>), many of its behaviors date back to that
era. While the modern version of Amanda can split up a single large
backup of a single (large) filesystem across multiple 'tapes', what it
refuses to do is to split such a backup across multiple Amanda runs. If
a filesystem backup can't be completely written out to tape in the
current Amanda run, any partially written amount is ignored; the entire
filesystem backup will be (re)written in the next run, using up the full
space. If Amanda managed to write 90% of your large filesystem to your
backup media today, that 90% is ignored because the last 10% couldn't be
written out.</p>

<p>The consequence of this is that if you're backing up large filesystems
with Amanda, you really don't want to run out of tape space during
a backup run because this can waste hundreds of gigabytes of backup
space (or more, if you have multi-terabyte filesystems). In
<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DiskBackupSystemII">environments like ours</a> where the 'tapes' are
artificial and we have a lot of them available to Amanda (our tapes
a partitions on HDDs and we have a dozen HDDs or more mounted on
each backup server at any given time), the best way to avoid running
out of tape space during a single Amanda run is to tell Amanda that
it can use a lot of tapes, way more tapes than it should ever
actually need.</p>

<p>(Even in theory, Amanda can't perfectly estimate how much space a
given full or incremental backup will actually use and so it can
run over the tape capacity you actually want it to use. In practice,
in many environments you may have to tell Amanda to use 'server
side estimates', where it guesses based on past backup behavior,
instead of the much more time-consuming 'client side estimates',
where it basically does an estimation pass over each filesystem to
be backed up.)</p>

<p>However, if you tell Amanda it can use a lot of tapes in a standard
Amanda setup, Amanda will see a vast expanse of available tape
capacity and enthusiastically reach the perfectly rational conclusion
that it should make use of that capacity by aggressively promoting
full backups of filesystems (both small and large ones). This is
very much not what you (we) actually want. We're letting Amanda use
tons of 'tapes' to insure that it never wastes tape space, not so
that it can do extra full backups; if Amanda doesn't need to use
the tape space we don't want it to touch that tape space.</p>

<p>The easiest way for us to achieve this is to set '<code>maxpromoteday
0</code>' in our Amanda configuration, at least for Amanda servers that
back up very large filesystems (where the wasted tape space of an
incompletely written backup could be substantial). Unfortunately I
think you'll generally want to set this for all dump types in a
particular Amanda server, because over-promotion of even small(er)
filesystems could eat up a bunch of tape space that you want to
remain unused.</p>

<p>(Amanda talks about 'dumps' because it started out on Unix systems
where <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/DumpHistory">for a long time the filesystem backup program was called
'dump'</a>. These days your Amanda filesystem
backups are probably done with GNU Tar, although I think people
still talk about things like 'database dumps' for backups.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/AmandaDumpPromotionIssue

---

*ID: 8d419d6864c81121*
*抓取时间: 2026-03-12T13:49:26.048720*
