# Expiry times are dangerous, on "The dangers of SSL certificates"

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-29T03:48:07Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Recently I read Lorin Hochstein's <a href="https://surfingcomplexity.blog/2025/12/27/the-dangers-of-ssl-certificates/">The dangers of SSL certificates</a>
(<a href="https://lobste.rs/s/l9jl7h/dangers_ssl_certificates">via</a>, among
others), which talks about a Bazel build workflow outage caused by
an expired TLS certificate. I had some direct reactions to this but
after thinking about it I want to step back and say that in general,
it's clear that expiry times are dangerous, often more or less
regardless of where they appear. TLS certificate expiry times are
an obvious and commonly encountered instance of expiry times in
cryptography, but TLS certificates aren't the only case; in 2019,
Mozilla had an incident where the signing key for Firefox addons
expired (I believe the system used certificates, but not web PKI
TLS certificates). Another thing that expires is DNS data (not just
DNSSEC keys) and there have been incidents where expiring DNS data
caused problems. Does a system have caches with expiry times? Someone
has probably had an incident where things expired by surprise.</p>

<p>One of the problems with expiry times in general is that they're
usually implemented as an abrupt cliff. On one side of the expiry
time everything is fine and works perfectly, and one second later
on the other side of the expiry time everything is broken. There's
no slow degradation, no expiry equivalent of 'overload', and so on,
which means that there's nothing indirect to notice and detect in
advance. You must directly check and monitor the expiry time, and
if you forget, things explode. We're fallible humans so we forget
every so often.</p>

<p>This abrupt cliff of failure is a technology choice. In theory we
could begin degrading service some time before the expiry time, or
we could allow some amount of success for a (short) time after the
expiry time, but instead we've chosen to make things be a boolean
choice (which has made time synchronization across the Internet
increasingly important; your local system can no longer be all that
much out of step with Internet time if things are to work well).
This is especially striking because expiry times are most often a
heuristic, not a hard requirement. We add expiry times to limit
hypothetical damage, such as silent key compromise, or constrain
how long out of data DNS data is given to people, or similar things,
but we don't usually have particular knowledge that the key or data
cannot and must not be used after a specific time (for example,
because the data will definitely have changed at that point).</p>

<p>(Of course the mechanics of degrading the service around the
expiry time are tricky, especially in a way that the service
operator would notice or get reports about.)</p>

<p>Another problem, related to the abrupt cliff, is that generally
expiry times are invisible or almost invisible. Most APIs and user
interfaces don't really surface the expiry time until you fall over
the cliff; generally you don't even get warnings logged that an
expiry time is approaching (either in clients or in servers and
services). We implicitly assume that expiry times will never get
reached because something will handle the situation before then.
Invisible expiry times are fine if they're never reached, but if
they're hit as an abrupt cliff you have the worst of two worlds.
Again, this isn't a simple problem with an obvious solution; for
example, you might need things to know or advertise what is a
dangerously close expiry time (if you report the expiry time all
of the time, it becomes noise that is ignored; that's already
effectively the situation with TLS certificates, where tools will
give you all the notAfter dates you could ask for and no one bothers
looking).</p>

<p>Some protocols do without expiry times entirely; SSH keypairs are
one example (unless you use SSH certificates, but even then the key
that signs certificates has no expiry). This has problems and risks
that make it not suitable for all environments. If you're working
in an environment that has and requires expiry times, another option
is to simply set them as far in the future as possible. If you don't
expect the thing to ever expire and have no process for replacing
it, <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/TenYearsNotLongEnough">don't set its expiry time to ten years</a>. But not everything can work
this way; your DNS entries will change sooner or later, and often
in much less than ten years.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/ExpiryTimesAreDangerous

---

*ID: 2321291c9b421570*
*抓取时间: 2026-03-12T13:49:26.048838*
