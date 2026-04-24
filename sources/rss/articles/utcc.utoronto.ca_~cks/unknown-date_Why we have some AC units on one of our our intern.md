# Why we have some AC units on one of our our internal networks

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-07T03:13:18Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I mentioned on the Fediverse a while back that <a href="https://mastodon.social/@cks/115613882168849189">we have air
conditioners on our internal network</a>. Well, technically
what we have on the internal network is separate (and optional)
controller devices that connect to the physical AC units themselves,
but as they say, this is close enough. Of course <a href="https://mastodon.social/@cks/115613887986675852">there's a story
here</a>:</p>

<blockquote><p>Why do we have networked AC controllers? Well, they control portable
AC units that are in our machine rooms for emergency use, and having
their controllers on our internal network means we can possibly turn
them on from home if the main room AC stops working out of hours, on
weekends, etc.</p>

<p>(It would still be a bad time, just maybe a little less bad.)</p>
</blockquote>

<p>Our machine rooms are old (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MachineRoomArchaeology">cf</a>) and so
are their normal AC units. Over the years we've had enough problems
with these AC units that we've steadily accumulated emergency
measures. A couple of years ago, these emergency measures reached
the stage of pre-deploying wheeled portable AC units with their
exhaust hoses connected up to places where they could vent hot air
that would take it outside of the machine room.</p>

<p>Like most portable ACs, these units are normally controlled in
person from their front panels (well, top panels). However, these
are somewhat industrial AC units and you could get optional
network-accessible controllers for them; after thinking about it,
we did and then hooked the controllers (and thus the ACs) up to our
internal management network. As I mentioned, the use case for
networked control of these AC units is to turn them on from home
during emergencies. They don't have anywhere near enough cooling
power to cover all of the systems we normally have running in our
machine rooms, but we might be able to keep a few critical systems
up rather than being completely down.</p>

<p>(We haven't had serious AC issues since we put these portable AC
units into place, so we aren't sure how well they'd perform and how
much we'd be able to keep up.)</p>

<p>These network controllers can get status information (including
temperatures) from the ACs and have some degree of support for SNMP,
so we could probably pull information from them for <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusGrafanaSetup-2019">metrics
purposes</a> if we wanted to. Right now
we haven't looked into this, partly because we have our own temperature
monitoring and partly because I'm not sure I trust the SNMP server
implementation to be free of bugs, memory leaks, and other things
that might cause problems for the overall network controller.</p>

<p>(Like most little things, these network controllers are probably
running some terrifyingly ancient Linux kernel and software stack.
A quick look at the HTTP server headers says that it's running a
clearly old version of nginx on Ubuntu, although it's slightly more
recent than I expected.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/NetworkedACUnits

---

*ID: 1ce32b66dad65c18*
*抓取时间: 2026-03-12T13:49:26.048741*
