# How we failed to notice a power failure

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-07T04:25:50Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Over on the Fediverse, I mentioned that <a href="https://mastodon.social/@cks/116021709012505023">we once missed noticing
that there had been a power failure</a>. Naturally there
is a story there (and this is the expanded version of what I said
in the Fediverse thread). A necessary disclaimer is that this was
all some time ago and I may be mangling or mis-remembering some of
the details.</p>

<p><a href="https://www.cs.toronto.edu/">My department</a> is spread across
multiple buildings, one of which has <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MyDesk">my group's offices</a>
and <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MachineRoomArchaeology">our ancient machine room</a> (which I
believe has been there since <a href="https://exhibits.library.utoronto.ca/exhibits/show/recollections/introduction">the building burned down and was
rebuilt</a>).
But for various reasons, this building doesn't have any of the
department's larger meeting rooms.
Once upon a time we had a weekly meeting of all the system
administrators (and our manager), both <a href="https://support.cs.toronto.edu/">my group</a> and all of <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/CSDeptSupportModel">the
Points of Contact</a>, which amounted to a dozen
people or so and needed one of the larger meeting rooms, which was
of course in a different building than our machine room.</p>

<p>As I was sitting in the meeting room during one weekly meeting,
fiddling around, I tried to get my Linux laptop on either our
wireless network or <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/CSLabNetworkLayout">our wired laptop network</a>
(it's been long enough that I can't remember which). This was back
in the days when networking on Linux laptops wasn't a 100% reliable
thing, especially wireless, so I initially assumed that my inability
to get on the network was the fault of my laptop and its software.
Only after a bit of time and also failing on both wired and wireless
networking did I ask to see if anyone else (with a more trustworthy
laptop) could get on the network. As a ripple of "no, not me"
spread around the room, we realized that something was wrong.</p>

<p>(This was in the days before smartphones were pervasive, and
also it must have been before the university-wide wireless
network was available in that meeting room.)</p>

<p>What was wrong turned out to be a short power failure that had been
isolated to the building that our machine room was in. Had people
been in their offices, the problem would have been immediately
obvious; we'd have seen all networking fail, and the people in the
building would have seen the lights go out and so on. But because
the power issue hit at exactly the time that we were all in our
weekly meeting in a different building, we missed it.</p>

<p>(My memory is that by the time we'd reached the machine room the
power was coming back, but obviously we had a variety of work to
do to clean the situation up so that was it for the meeting.)</p>

<p>For extra irony, <a href="https://exhibits.library.utoronto.ca/exhibits/show/engineering-buildings/dl-pratt-building/past-and-present-views">the building we were meeting in</a>
was right next to our machine room's building, and the meeting room
had a window that literally looked across the alleyway at our
building. At least that made it quick and easy to get to the machine
room, because we could just walk across the bridge that connects
the two buildings.</p>

<p>PS: In <a href="https://support.cs.toronto.edu/">our</a> environment, this
is such a rare collection of factors that it's not worth trying to
set up some sort of alerting for it, especially today in a world
with pervasive smartphones (where people outside the meeting room
can easily send some of us messages, even with the network down).</p>

<p>(Also, these days we don't normally have such big meetings any more
and if we did, they'd be virtual meetings and we'd definitely notice
bits of the network going down, one way or another.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/NotNoticingPowerFailure

---

*ID: 6dcedb70256b92ab*
*抓取时间: 2026-03-12T13:49:26.048403*
