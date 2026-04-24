# WAIT: synchronous replication for Redis

> 来源: antirez.com  
> 发布时间: Thu, 05 Dec 2013 10:50:33 +0100  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

Redis unstable has a new command called "WAIT". Such a simple name, is indeed the incarnation of a simple feature consisting of less than 200 lines of code, but providing an interesting way to change the default behavior of Redis replication.
<br />
<br />The feature was extremely easy to implement because of previous work made. WAIT was basically a direct consequence of the new Redis replication design (that started with Redis 2.8). The feature itself is in a form that respects the design of Redis, so it is relatively different from other implementations of synchronous replication, both at API level, and from the point of view of the degree of consistency it is able to ensure.
<br />
<br />Replication: synchronous or not?
<br />===
<br />
<br />Replication is one of the main concepts of distributed systems. For some state to be durable even when processes fail or when there are network partitions making processes unable to communicate, we are forced to use a simple but effective strategy, that is to take the same information “replicated” across different processes (database nodes).
<br />
<br />Every kind of system featuring strong consistency will use a form of replication called synchronous replication. It means that before some new data is considered “committed”, a node requires acknowledge from other nodes that the information was received. The node initially proposing the new state, when the acknowledge is received, will consider the information committed and will reply to the client that everything went ok.
<br />
<br />There is a price to pay for this safety: latency. Systems implementing strong consistency are unable to reply to the client before receiving enough acknowledges. How many acks are “enough”? This depends on the kind of system you are designing. For example in the case of strong consistent systems that are available as long as the majority of nodes are working, the majority of the nodes should reply back before some data is considered to be committed. The result is that the latency is bound to the slowest node that replies as the (N/2+1)th node. Slower nodes can be ignored once the majority is reached.
<br />
<br />Asynchronous replication
<br />===
<br />
<br />This is why asynchronous replication exists: in this alternative model we reply to the client confirming its write BEFORE we get acknowledges from other nodes.
<br />If you think at it from the point of view of CAP, it is like if the node *pretends* that there is a partition and can’t talk with the other nodes. The information will eventually be replicated at a latter time, exactly like an eventually consistent DB would do during a partition. Usually this latter time will be a few hundred microseconds later, but if the node receiving the write fails before propagating the write, but after it already sent the reply to the client, the write is lost forever even if it was acknowledged.
<br />
<br />Redis uses asynchronous replication by default: Redis is designed for performances and low, easy to predict, latency. However if possible it is nice for a system to be able to adapt consistency guarantees depending on the kind of write, so some form of synchronous replication could be handy even for Redis.
<br />
<br />WAIT: call me synchronous if you want.
<br />===
<br />
<br />The way I depicted synchronous replication above, makes it sound simpler than it actually is.
<br />
<br />The reality is that usually synchronous replication is “transactional”, so that a write is propagated to the majority of nodes (or *all* the nodes with some older algorithm), or none, in one way or the other not only the node proposing the state change must wait for a reply from the majority, but also the other nodes need to wait for the proposing node to consider the operation committed in order to, in turn, commit the change. Replicas require in one way or the other a mechanism to collect the write without applying it, basically.
<br />
<br />This means that nothing happens during this process, everything is blocked for the current operation, and later you can process a new one, and so forth and so forth.
<br />
<br />Because synchronous replication can be very costly, maybe we can do with a bit less? We want a way to make sure some write propagated across the replicas, but at the same time we want other clients to go at light speed as usually sending commands and receiving replies. Clients waiting in a synchronous write should never block any other client doing other synchronous or non-synchronous work.
<br />
<br />There is a tradeoff you can take: WAIT does not allow to rollback an operation that was not propagated to enough slaves. It only offers, merely, a way to inform the client about what happened.
<br />The information, specifically, is the number of replicas that your write was able to reach, all this encapsulated into a simple to use blocking command.
<br />
<br />This is how it works:
<br />
<br />redis 127.0.0.1:9999> set foo bar
<br />OK
<br />redis 127.0.0.1:9999> incr mycounter
<br />(integer) 1
<br />redis 127.0.0.1:9999> wait 5 100
<br />(integer) 7
<br />
<br />Basically you can send any number of commands, and they’ll be executed, and replicated as usually.
<br />As soon as you call WAIT however the client stops until all the writes above are successfully replicated to the specified number of replicas (5 in the example), unless the timeout is reached (100 milliseconds in the example).
<br />
<br />Once one of the two limits is reached, that is, the master replicated to 5 replicas, or the timeout was reached, the command returns, sending as reply the number of replicas reached. If the return value is less than the replicas we specified, the request timed out, otherwise the above commands were successfully replicated to the specified number of replicas.
<br />
<br />In practical terms this means that you have to deal with the condition in which the command was accepted by less replicas you specified in the amount of time you specified. More about that later.
<br />
<br />How it works?
<br />===
<br />
<br />The WAIT implementation is surprisingly simple. The first thing I did was to take the blocking code of BLPOP & other similar operations and make it a generic primitive of Redis internal API, so now implementing blocking commands is much simpler.
<br />
<br />The rest of the implementation was trivial because 2.8 introduced the concept of master replication offset, that is, a global offset that we increment every time we send something to the slaves. All the salves receive exactly the same stream of data, and remember the offset processed so far as well.
<br />
<br />This is very useful for partial resynchronization as you can guess, but moreover slaves acknowledge the amount of replication offset processed so far, every second, with the master, so the master has some idea about how much they processed.
<br />
<br />Every second sucks right? We can’t base WAIT on an information available every second. So when WAIT is used by a client, it sets a flag, so that all the WAIT callers in a given event loop iteration will be grouped together, and before entering the event loop again we send a REPLCONF GETACK command into the replication stream. Slaves will reply ASAP with a new ACK.
<br />
<br />As soon as the ACKs received from slaves is enough to unblock some client, we do it. Otherwise we unblock the client on timeout.
<br />
<br />Not considering the refactoring needed for the block operations that is technically not part of the WAIT implementation, all the code is like 170 lines of code, so very easy to understand, modify, and with almost zero effects on the rest of the code base.
<br />
<br />Living with the indetermination
<br />===
<br />
<br />WAIT does not offer any “transactional” feature to commit a write to N nodes or nothing, but provides information about the degree of durability we achieved with our write, in an easy to use form that does not slow down operations of other clients.
<br />
<br />How this improves consistency in Redis land? Let’s look at the following pseudo code:
<br />
<br />    def save_payment(payment_id)
<br />        redis.set(payment_id,”confirmed”)
<br />    end
<br />
<br />We can imagine that the function save_payment is called every time an user payed for something, and we want to store this information in our database. Now imagine that there are a number of clients processing payments, so the function above gets called again and again.
<br />
<br />In Redis 2.6 if there was an issue communicating with the replicas, while running the above code, it was impossible to sense the problem in time. The master failing could result in replicas missing a number of writes.
<br />
<br />In Redis 2.8 this was improved by providing options to stop accepting writes if there are problems communicating with replicas. Redis can check if there are at least N replicas that appear to be alive (pinging back the master) in this setup. With this option we improved the consistency guarantees a bit, now there is a maximum window to write to a master that is not backed by enough replicas.
<br />
<br />With WAIT we can finally considerably improve how much safe are our writes, since I can modify the code in the following way:
<br />
<br />    def save_payment(payment_id)
<br />        redis.set(payment_id,”confirmed”)
<br />        if redis.wait(3,1000) >= 3 then
<br />            return true
<br />        else
<br />            return false
<br />    end
<br />
<br />In the above version of the program we finally gained some information about what happened to the write, even if we actually did not changed the outcome of the write, we are now able to report back this information to the caller.
<br />However what to do if wait returns less than 3? Maybe we could try to revert our write sending redis.del(payment_id)?  Or we can try to set the value again in order to succeed the next time?
<br />
<br />With the above code we are exposing our system to too much troubles. In a given moment if only two slaves are accepting writes all the transactions will have to deal with this inconsistency, whatever it is handled. There is a better thing we can do, modifying the code in a way so that it actually does not set a value, but takes a list of events about the transaction, using Redis lists:
<br />
<br />    def save_payment(payment_id)
<br />        redis.rpush(payment_id,”in progress”) # Return false on exception
<br />        if redis.wait(3,1000) >= 3 then
<br />            redis.rpush(payment_id,”confirmed”) # Return false on exception
<br />            if redis.wait(3,1000) >= 3 then
<br />                return true
<br />            else
<br />                redis.rpush(payment_id,”cancelled”)
<br />                return false
<br />            end
<br />        else
<br />            return false
<br />    end
<br />
<br />Here we push an “in progress” state into the list for this payment ID before to actually confirming it. If we can’t reach enough replicas we abort the payment, and it will not have the “confirmed” element. In this way if there are only two replicas getting writes the transactions will fail one after the other. The only clients that will have the deal with inconsistencies are the clients that are able to propagate “in progress” to 3 or more replicas but are not able to do the same with the “confirmed” write. In the above code we try to deal with this issue with a best-effort “cancelled” write, however there is still the possibility of a race condition:
<br />
<br />1) We send “in progress”
<br />2) We send “confirmed”, it only reaches 2 slaves.
<br />3) We send “cancelled” but at this point the master crashed and a failover elected one of the slaves.
<br />
<br />So in the above case we returned a failed transaction while actually the “confirmed” state was written.
<br />
<br />You can do different things to deal better with this kind of issues, that is, to mark the transaction as “broken” in a strong consistent and highly available system like Zookeeper, to write a log in the local client, to put it in the hands of a message queue that is designed with some redundancy, and so forth.
<br />
<br />Synchronous replication and failover: two close friends
<br />===
<br />
<br />Synchronous replication is important per se because it means, there are N copies of this data around, however to really exploit the improved data safety, we need to make sure that when a master node fails, and a slave is elected, we get the best slave.
<br />
<br />The new implementation of Sentinel already elects the slave with the best replication offset available, assuming it publishes its replication offset via INFO (that is, it must be Redis 2.8 or greater), so a good setup can be to run an odd number of Redis nodes, with a Redis Sentinel installed in every node, and use synchronous replication to write to the majority of nodes. As long as the majority of the nodes is available, a Sentinel will be able to win the election and elect a slave with the most updated data.
<br />
<br />Redis cluster is currently not able to elect the slave with the best replication offset, but will be able to do that before the stable release. It is also conceivable that Redis Cluster will have an option to only promote a slave if the majority of replicas for a given hash slot are reachable.
<br />
<br />I just scratched the surface of synchronous replication, but I believe that this is a building block that we Redis users will be able to exploit in the future to stretch Redis capabilities to cover new needs for which Redis was traditionally felt as inadequate.
<a href="http://antirez.com/news/66">Comments</a>

## 链接

http://antirez.com/news/66

---

*ID: e5b65f7ebc14972e*
*抓取时间: 2026-03-05T10:02:11.704850*
