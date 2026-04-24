# Two challenges of incremental backups

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-18T04:25:12Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Roughly speaking, there are two sorts of backups that you can make,
<em>full backups</em> and <em>incremental backups</em>. At the abstract level,
full backups are pretty simple; you save everything that you find.
Incremental backups are more complicated because they save only the
things that changed since whatever they're relative to. People want
incremental backups despite the extra complexity because they save
a lot of space compared to backing up everything all the time.</p>

<p>There are two general challenges that make incremental backups more
complicated than full backups. The first challenge is reliably
finding everything that's changed, in the face of all of the stuff
that can change in filesystems (or other sources of data). Full
backups only need to be able to traverse all of the filesystem (or
part of it), or in general the data source, and this is almost
always a reliable thing because all sorts of things and people use
it. Finding everything that has changed has historically been more
challenging because it's not something that people do often outside
of incremental backups.</p>

<p>(And when people do it they may not notice if they're missing some
things, the way they absolutely will notice if a general traversal
skips some files.)</p>

<p>The second challenge is handling things that have gone away. Once
you have a way to find everything that's changed it's not too
difficult to build a backup system that will faithfully reproduce
everything that definitely was there as of the incremental. All you
need to do is save every changed file and then unpack the sequence
of full and incremental backups on top of each other, with the
latest version of any particular file overwriting any previous one.
But people often want their incremental restore to reflect the state
of directories and so on as of the incremental, which means removing
things that have been deleted (both files and perhaps entire directory
trees). This means that your incrementals need some way to pass on
information about things that were there in earlier backups but
aren't there now, so that the restore process can either not restore
them or remove them as it restores the sequence of full and incremental
backups.</p>

<p>While there are a variety of ways to tackle the first challenge,
backup systems that want to run quickly are often constrained by
what features operating systems offer (and also what features your
backup system thinks it can trust, which isn't always the same
thing). You can checksum everything all the time and keep a checksum
database, but that's usually not going to be the fastest thing.
The second challenge is much less constrained by what the operating
system provides, which means that in practice it's much more on you
(the backup system) to come up with a good solution. Your choice
of solution may interact with how you solve the first challenge,
and there are tradeoffs in various approaches you can pick (for
example, do you represent deletions explicitly in the backup format
or are they implicit in various ways).</p>

<p>There is no single right answer to these challenges. I'll go as far
as to say that the answer depends partly on what sort of data and
changes you expect to see in the backups and partly where you want
to put the costs between creating backups and handling restores.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/IncrementalBackupsTwoChallenges?showcomments#comments">9 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/IncrementalBackupsTwoChallenges

---

*ID: 3066ee87480ac044*
*抓取时间: 2026-03-12T13:49:26.048284*
