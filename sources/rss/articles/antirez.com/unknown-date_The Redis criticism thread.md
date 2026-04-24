# The Redis criticism thread

> 来源: antirez.com  
> 发布时间: Tue, 10 Dec 2013 00:53:03 +0100  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

A few days ago I tried to do an experiment by running some kind of “call for critiques” in the Redis mailing list:
<br />
<br />https://groups.google.com/forum/#!topic/redis-db/Oazt2k7Lzz4
<br />
<br />The thread has reached 89 posts so far, probably one of the biggest threads in the history of the Redis google group.
<br />The main idea was that critiques are a mix of pointless attacks, and truth, so to extract the truth from critiques can be a good exercise, it means to have some seed idea for future improvements from the part of the population that is not using or is not happy with your system.
<br />
<br />There were a lot of arguments possible: threading, persistence model, API, security, and so forth, however the argument that received the most attention was Redis Cluster design and its tradeoffs. There are people that are not convinced by the proposed design since it does not provide strong Consistency nor Availability (“C” and “A” of CAP, not any random consistency or availability).
<br />
<br />Instead it only provides some form of weaker consistency and some failure resistance. In this blog post I want to clarify why this is in my opinion the right choice for Redis.
<br />
<br />Strong consistency requires synchronous replication, and depending on the failure models you want to handle, it also requires to fsync data on disk at every write, in order to cover failures like all the nodes in a single data center rebooting for a power outage.
<br />Redis is what it is because the performance and latency characteristics, so a model like the above would not be Redis.
<br />
<br />So Redis Cluster trades Consistency for performance. The tradeoff is that there are well defined failure modes where it is possible to lose writes, however the system is designed in order to minimize lost writes under certain assumptions.
<br />
<br />The other property we give away is availability, because being available means, in order to have a decent consistency story, to merge values when partitions heals. Redis data model is not merge-friendly, Redis uses the fact that data representation is in memory to get an advantage and export rich data structures to the user that have practically no limits in the size of every single value, if not the available memory. So there are Redis deployments with just a few keys, with sorted set values of many million of elements, to implement leader boards of Facebook games, and stuff like that.
<br />
<br />Merging huge and complex values is extremely hard and not very practical. Implementing the values in a way that makes merging more manageable would mean instead to forget the current performance at all.
<br />
<br />So we trade Availability for a more powerful data model. We still have some degree of resistance to failures. Nodes can stop working and partitions can happen, and as long as there is the majority of master nodes up and at least a replica for each hash slot, the system is able to accept queries from clients.
<br />
<br />I believe this is a perfectly acceptable design and is able to provide great performances with consistency and availability guarantees that are reasonable for many class of applications. To get an idea about how it is possible to lose writes you can read the Redis Cluster tutorial here: http://redis.io/topics/cluster-tutorial
<br />
<br />Note that in the meantime Redis unstable got an implementation of synchronous replication. It is not capable of providing strong consistency alone, but it is able to improve the consistency guarantees that the system is able to provide for certain writes (less / hard to trigger failure modes). However I believe that most users want Redis for very high loads, so this feature will likely be not very used.
<br />
<br />Why Redis Cluster?
<br />===
<br />
<br />The real goal of Redis Cluster is not to provide the coolest consistent or available system, its goal was to provide what Redis is, but distributed in many nodes with *automatic sharding*. That was the real trigger: users can’t reinvent again and again client-side sharding, something that can do this for you is very useful, especially if it is designed in a way that 100 nodes will provide the performances of a single instance multiplied by 100.
<br />
<br />This is the main reason I want to see it working and deployed, because I believe it can make a huge difference for the Redis users.
<br />Being it a distributed system it should also be operational friendly (that was another design goal), provide some resistance to failure, and easy to predict failure modes. So consistency and availability are automatically concerns and huge part of the tradeoffs to make of course.
<br />
<br />I’m excited about Redis Cluster. I truly believe it will benefit many users.
<br />
<br />Redis became what it is, this strange tool that many developers learned to live and to solve problems with, because I tried to never be dogmatic about the development process and the tradeoffs, sometimes extreme, to take.
<br />For example the fact that Redis is probably the only top-used database system developed mostly by a single individual currently (at our max we were Pieter half-time and I full-time) is the result of this choices: I’m not magic, the only way to do it is to realize your limits and design and plan for them.
<br />
<br />So, as long as there are users doing good work with it, the Redis experiment is here to stay. Ended the thread I’ll start with my usual routine, grab a coffee in the morning, sit in the front of my computer, and do the only thing I’m really good at: write some code.
<br />
<br />Thanks everybody that took part to the thread. Probably I would not do it again, since it was more stressful than useful honestly, however sometimes odd things must be tried, and it feels great to don’t fear the critiques.
<br />
<br />Write code and be free.
<a href="http://antirez.com/news/67">Comments</a>

## 链接

http://antirez.com/news/67

---

*ID: c783e399bd7a273f*
*抓取时间: 2026-03-05T10:02:11.704847*
