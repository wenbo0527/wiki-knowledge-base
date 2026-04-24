# Our problem with finding good 10G-T Ethernet switches (in 2025)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-21T02:35:50Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p><a href="https://support.cs.toronto.edu/">We</a> have essentially standardized
our <a href="https://en.wikipedia.org/wiki/10-Gigabit_Ethernet">10G Ethernet</a>
networking on <a href="https://en.wikipedia.org/wiki/10_Gigabit_Ethernet#10GBASE-T">10G-T</a>, which
runs over relatively conventional copper network cables. The pragmatic
advantage of 10G-T is that it provides for easy interoperability
between 1G and 10G-T equipment. You can make all of your new in-wall
cabling 10G-T rated and then plug 1G equipment and switches into
it because those offices or rooms or whatever don't need 10G (yet),
you can ship servers with 10G-T ports and not worry about people
who are still at 1G, and so on. It's quite flexible and enables
slow, piece by piece upgrades to 10G (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/Why10GTWillWin">which can be an important
thing</a>). However, we've run into a problem with our
10G-T environment, and that is finding good 10G-T switches that
don't have a gigantic number of ports.</p>

<p>Our preference in Ethernet switches is ones that have around 24
ports. In <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OurThreeNetworkImplementations">our current network implementation</a>, we try to make as
many switches as possible be 'dumb' switches that carry only <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/CSLabNetworkImplementation">a
single (internal) network</a>,
and we also <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/RackSwitches">put switches into each machine room rack</a>. All of this means that 24 ports per
switch is about right for most switches; we rarely want to connect
up more than that many things on one network to a single switch in
a single place. We can live with 16-port or 10-port switches, but
that starts to get expensive because we have to buy (a lot) more
switches.</p>

<p>Unfortunately, 24-port 10G-T switches appear to be an increasingly
unpopular thing, as far as we can tell. At one point there were a
reasonable number of inexpensive sources for good ones, but recently
many of those seem to have gotten out of the business (and there's
a few that have products that have thermals that don't work for
us). You can probably get 24-port 10G-T switches from the 'enterprise'
switch vendors but you'll pay 'enterprise' prices for them, there's
a reasonable number of sources for 48-port 10G-T switches that are
too big for us, and a certain amount of smaller 10G-T switches, but
the middle seems to have gone mostly missing.</p>

<p>My suspicion is that this has to do with the shifts in the server
market from plenty of relatively low (rack) density on-premise sales
to an increasing amount of large cloud or high-density datacenter
sales. A fully populated rack likely needs more than 24 ports of
local connections, and you're buying the whole rack's worth at once,
making incremental upgrades much less compelling. And 10G-T itself
has drawbacks in high-density situations; the cables are physically
bulkier than fiber, the ports (still) use more heat, SFP+ ports
have a lot of flexibility, and increasingly people want datacenter
networking that runs faster than 10G, even for individual machines.</p>

<p>At the same time, a 24-port 10G-T switch is awkwardly large for a
lot of other situations. Most people don't have a use for that many
10G ports at home or in smaller offices, and on top of that 10G-T
ports use enough power and are hot enough that the switch will need
decent fans, which will make it noisy (and so not something you
want to have out in the open). At most you might put such a 24-port
switch in a local wiring closet, assuming that the wiring closet has
enough air flow that a relatively hot switch doesn't cook itself.</p>

<p>(It's possible that there are good 24 port 10G-T switches out there
that we haven't found. We know of TP-Link's offerings, but for local
reasons we prefer to avoid them. Similarly, I believe that 16 or
24 port SFP+ switches with 10G-T SFP+ modules are likely to be
decidedly too expensive for us, once we buy all the SFP+ modules
needed.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/Our10GTSwitchFindingProblem?showcomments#comments">3 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/Our10GTSwitchFindingProblem

---

*ID: 9c801e001b80352a*
*抓取时间: 2026-03-12T13:49:26.048920*
