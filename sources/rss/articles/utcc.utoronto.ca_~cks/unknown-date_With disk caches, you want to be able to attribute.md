# With disk caches, you want to be able to attribute hits and misses

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-26T03:06:01Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Suppose that you have a disk or filesystem cache in memory (which
you do, since pretty much everything has one these days). Most disk
caches will give you simple hit and miss information as part of
their basic information, but if you're interested in the performance
of your disk cache (or in improving it), you want more information.
The problem with disk caches is that there are a lot of different
sources and types of disk IO, and you can have hit rates that are
drastically different between them. Your hit rate for reading data
from files may be modest, while <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/KernelNameCachesWhy">your hit rate on certain sorts
of metadata may be extremely high</a>.
Knowing this is important because it means that your current good
performance on things involving that metadata is critically dependent
on that hit rate.</p>

<p>(Well, it may be, depending on what storage media you're using and
what its access speeds are like. A lot of my exposure to this dates
from the days of slow HDDs.)</p>

<p>This potential vast difference is why you want more detailed
information in both cache metrics and IO traces. The more narrowly
you can attribute IO and the more you know about it, the more useful
things you can potentially tell about the performance of your system
and what matters to it. This is not merely 'data' versus 'metadata',
and synchronous versus asynchronous; ideally you want to know the
sort of metadata read being done, and whether the file data being
read is synchronous or not, and whether this is a prefetching read
or a 'demand' read that really needs the data.</p>

<p>A lot of the times, operating systems are not set up to pass this
information down through all of the layers of IO from the high level
filesystem code that knows what it's asking for to the disk driver
code that's actually issuing the IOs. Part of the reason for this
is that it's a lot of work to pass all of this data along, which
means extra CPU and memory on what is an increasingly hot path
(especially with modern NVMe based storage). These days you may get
some of this fine grained details in metrics and perhaps IO traces
(eg, <a href="https://utcc.utoronto.ca/~cks/space/blog/solaris/ZFSUnderstandingARCHits">for (Open)ZFS</a>), but
probably not all the way to types of metadata.</p>

<p>Of course, disk and filesystem caches (and IO) aren't the only place
that this can come up. Any time you have a cache that stores different
types of things that are potentially queried quite differently, you
can have significant divergence in the types of activity and the
activity rates (and cache hit rates) that you're experiencing.
Depending on the cache, you may be able to get detailed information
from it or you may need to put more detailed instrumentation into
the code that queries your somewhat generic cache.</p>

<p>Modern general observability features in operating systems can
sometimes let you gather some of this detailed attribute yourself
(if the OS doesn't already provide them). However, it's not a certain
thing and there are limits; for example, you may have trouble tracing
and tracking IO once it gets dispatched asynchronously inside the OS
(and most OSes turn IO into asynchronous operations before too long).</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/DiskCacheHitMissWantDetails

---

*ID: 38a260d8d122434f*
*抓取时间: 2026-03-12T13:49:26.048191*
