# The FreeBSD 15 version of PF has basically caught up to OpenBSD

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-16T04:06:22Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>When <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/FreeBSDInterestAndOpenBSD">we initially became interested in FreeBSD</a> a year ago, I said that
FreeBSD's version of PF was close enough to an older version of
OpenBSD PF (in syntax and semantics) that we could deal with it.
Indeed, <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OpenBSDToFreeBSDMove">as we've moved firewalls from OpenBSD to FreeBSD</a> we found that most of our rules
moved over without trouble and things certainly performed well
(better than they had on OpenBSD). Things have gotten even better
with the recent release of FreeBSD 15, as covered in <a href="https://www.netgate.com/blog/updates-to-the-pf-packet-filter-in-freebsd-and-pfsense-software">Updates to
the pf packet filter in FreeBSD and pfSense software</a>.
To quote the important bit:</p>

<blockquote><p>Over the years this difference between OpenBSD and FreeBSD was
a common point of discussion, often in overly generalised (and
as a result, deeply inaccurate) terms. Thanks to recent efforts
by <a href="https://www.sigsegv.be/blog/">Kristof Provost</a> and Kajetan
Staszkiewicz focused on aligning FreeBSD’s pf with the one in
OpenBSD, that discussion can be put to rest.</p>
</blockquote>

<p>A change that's important for us in FreeBSD 15.0 is that OpenBSD
style integrated NAT rules are now supported in the FreeBSD PF.
Last year as we were exploring FreeBSD, I wrote about <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/PFAddrTransOnOpenBSDAndFreeBSD">OpenBSD
versus FreeBSD syntax for NAT</a>,
where a single OpenBSD rule that both passed traffic and NAT'd it
had to be split into two FreeBSD rules in the basic version.  With
FreeBSD 15, we can write NAT rules using the OpenBSD version of
syntax.</p>

<p>(I'm talking about syntax here because I don't care about how it's
implemented behind the scenes. PF already performs some degree of
ruleset transformations, so if the syntax works and the semantics
don't change, we're happy even if a peek under the hood would show
two rules. But I believe that the FreeBSD 15 changes mean that
FreeBSD now has the OpenBSD implementation of this too.)</p>

<p>So far <a href="https://support.cs.toronto.edu/">we</a>'ve converted two
firewall rulesets to the old PF NAT syntax, one a simple case that's
now in production and a second, more complex one that's not yet in
production. We were holding off on our most complex PF NAT firewall,
which is complex partly because it uses some stuff that's close to
<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/FreeBSDPolicyRoutingWithPF">policy based routing</a>. The release
of FreeBSD 15 will make it easier to migrate this firewall (in the
new year, we don't make big firewall changes shortly before our
winter break).</p>

<p>In general, I'm quite happy that FreeBSD and OpenBSD have reached
close to parity in their PF as of FreeBSD 15, because that makes
it easier to chose between them based on what other aspects of them
you like.</p>

<p>(I say 'close to' based on <a href="https://www.sigsegv.be/blog/">Kristof Provost</a>'s comment about the
situation on <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OpenBSDToFreeBSDMove">this entry</a>. The
situation will get even better (ie, closer) in future FreeBSD
versions.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/FreeBSDPFHasCaughtUp

---

*ID: 5fa9136073a252ed*
*抓取时间: 2026-03-12T13:49:26.048973*
