# What ZFS people usually mean when they talk about "ZFS metadata"

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-22T04:14:37Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Recently I read <a href="https://klarasystems.com/articles/understanding-zfs-scrubs-and-data-integrity/">Understanding ZFS Scrubs and Data Integrity</a>
(<a href="https://news.ycombinator.com/item?id=46622090">via</a>), which is
a perfectly good article and completely accurate, bearing in mind
some qualifications which I'm about to get into. One of the things
this article says in the preface is:</p>

<blockquote><p>In this article, we will walk through what scrubs do, how the Merkle
tree layout lets ZFS validate metadata and data from end to end, [...]</p>
</blockquote>

<p>This is both completely correct and misleading, because what ZFS
people mean we talk about "metadata" is probably not what ordinary
people (who are aware of filesystems) think of as "metadata". This
misunderstanding leads people (which once upon a time included me)
to believe that ZFS scrubs check much more than <a href="https://utcc.utoronto.ca/~cks/space/blog/solaris/ZFSScrubLimitsII">they actually do</a>.</p>

<p>Specifically, in normal use "ZFS metadata" is different from
"filesystem metadata", like directories. A core ZFS concept is <em>DMU
objects (dnodes)</em>, which are a basic primitive of ZFS's structure;
a DMU object stores data in a more or less generic way. As covered
in more detail in <a href="https://utcc.utoronto.ca/~cks/space/blog/solaris/ZFSBroadDiskStructure">my broad overview on how ZFS is structured on
disk</a>, filesystem objects like directories,
files, ACLs, and so on are all DMU objects that are stored in the
filesystem's <em>(DMU) object set</em> and are referred to (for examine
in filesystem directories) by object number (the equivalent of an
inode number). At this level, filesystem metadata is ZFS data.</p>

<p>What ZFS people and ZFS scrubs mean by "ZFS metadata" are things
such as each filesystem's DMU object set (which is itself a DMU
object, because in ZFS it's turtles most of the way down), the
various DSL (Dataset and Snapshot Layer) objects, the various DMU
objects used to track and manage free space in the ZFS pool, and
so on. All of this ZFS metadata is organized in a tree that's rooted
in the uberblock and the pool's <em>Meta Object Set</em> (MOS) that the
uberblock points to. It is this tree that is guarded and verified
by checksums and ZFS scrubs, from the very top down to the leaves.</p>

<p>As far as I know, all filesystem level files, directories, symbolic
links, ACLs, and so on are leaves of this tree of ZFS metadata;
they are merely ZFS data. While they make up a logical filesystem
tree (we hope), they aren't a tree at the level of ZFS objects;
they're merely DMU objects in the filesystem's object set. Only at
the ZFS filesystem layer (ZPL, the "ZFS POSIX Layer") does ZFS look
inside these various filesystem objects and maintain structural
relationships, such as a filesystem's directory tree or <a href="https://utcc.utoronto.ca/~cks/space/blog/solaris/ZFSPathLookupTrick">parent
information</a> (some of which is maintained using
generic ZFS facilities like <a href="https://people.freebsd.org/~gibbs/zfs_doxygenation/html/db/d47/zap_8h.html#_details">ZAP objects</a>).</p>

<p>Scrubs must go through the tree of ZFS metadata in order to find
everything that's in use in order to verify its checksum, but <a href="https://utcc.utoronto.ca/~cks/space/blog/solaris/ZFSScrubLimitsII">they
don't have to go through the filesystem's directory tree</a>. To verify the checksum of everything in a
filesystem, all a scrub has to do is go through the filesystem's
DMU object set, which contains every in-use object in the filesystem
regardless of whether it's a regular file, a directory, a symbolic
link, an ACL, or whatever.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/solaris/ZFSMetadataMeaning

---

*ID: 95bfbad2af95b1e3*
*抓取时间: 2026-03-12T13:49:26.048586*
