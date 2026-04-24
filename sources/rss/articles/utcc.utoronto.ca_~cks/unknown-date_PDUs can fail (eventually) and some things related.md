# PDUs can fail (eventually) and some things related to this

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-22T23:23:37Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Early last Tuesday <a href="https://mastodon.social/@cks/116084506995715846">there was a widespread power outage at work</a>, which took out
power to our machine rooms for about four hours. Most things came
back up when the power was restored, but not everything. One of the
things that had happened was that one of our <a href="https://en.wikipedia.org/wiki/Power_distribution_unit">rack PDUs</a> had failed.
Fixing this took a surprising amount of work.</p>

<p>We don't normally think about our PDUs very much. They sit there,
acting as larger and often smarter versions of power bars, and just,
well, work. But both power bars and PDUs can fail eventually, and
in our environment rack PDUs tend to last long enough to reach that
point. We may replace servers in the racks in our machine rooms,
but we don't pull out and replace entire racks all that often. The
result is that a rack's initial PDU is likely to stay in the rack
until it fails.</p>

<p>(This isn't universal; there are plenty of places that install and
remove entire racks at a time. If you're turning over an entire
rack, you might replace the PDU at the same time you're replacing
all of the rest of it. Whole rack replacement is certainly going
to keep your wiring neater.)</p>

<p>A rack PDU failing not a great thing for the obvious reason; it's
going to take out much or all of the servers in the rack unless you
have dual power supplies on your servers, each connected to a
separate PDU. For racks that have been there for a while and gone
through a bunch of changes, often it will turn out to be hard to
remove and replace the PDU. Maintaining access to remove PDUs is
often not a priority either in placing racks in your machine room
or in wiring things up, so it's easy for things to get awkward and
encrusted. This was one of the things that happened with our failed
PDU on last Tuesday; it took quite some work to extract and replace
it.</p>

<p>(Some people might have pre-deployed spare PDUs in each rack, but
we don't. And if those spare PDUs are already connected to power
and turned on, they too can fail over time.)</p>

<p>We're fortunate that we already had spare (smart) PDUs on hand, and
we had also pre-configured a couple of them for emergency replacements.
If we'd had to order a replacement PDU, things would obviously have
been more of a problem. There are probably some research groups
around <a href="https://support.cs.toronto.edu/">here</a> with their own racks
who don't have a spare PDU, because it's an extra chunk of money
for an unlikely or uncommon contingency, and they might choose to
accept a rack being down for a while.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PDUsCanFailEventually

---

*ID: 80aeaf9b791f0d8f*
*抓取时间: 2026-03-12T13:49:26.048224*
