# Sending DMARC reports is somewhat hazardous

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-03T03:10:34Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p><a href="https://en.wikipedia.org/wiki/DMARC">DMARC</a> has a feature where
you can request that other mail systems send you <a href="https://en.wikipedia.org/wiki/DMARC#Aggregate_reports">aggregate reports</a> about the
DMARC results that they observed for email claiming to be from you.
If you're <a href="https://www.utoronto.ca/">a large institution</a> with a
sprawling, complex, multi-party mail environment and you're considering
trying to make your DMARC policy stricter, it's very useful to get
as many DMARC reports from as many people as possible. Especially,
'you' (in a broad sense) probably want to get as much information
from mail systems run by sub-units as possible, and if you're a
sub-unit, you want to report DMARC information up to the organization
so they have as much visibility into what's going on as possible.</p>

<p>In related news, I've been looking into making <a href="https://support.cs.toronto.edu/">our</a> mail system send out DMARC reports,
and <a href="https://mastodon.social/@cks/115652216099034053">I had what was in retrospect a predictable learning experience</a>:</p>

<blockquote><p>Today's discovery: if you want to helpfully send out DMARC reports to
people who ask for them and you operate even a moderate sized email
system, you're going to need to use a dedicated sending server and
you probably don't want to. Because a) you'll be sending a lot of
email messages and b) a lot of them will bounce because people's DMARC
records are inaccurate and c) a decent number of them will camp out in
your mail queue because see b, they're trying to go to non-responsive
hosts.</p>

<p>Really, all of this DMARC reporting nonsense was predictable from
first (Internet) principles, but I didn't think about it and was just
optimistic when I turned our reporting on for local reasons. Of course
people are going to screw up their DMARC reporting information (or for
spammers, just make it up), they screw everything up and DMARC data
will be no exception.</p>

<p>(Or they take systems and email addresses out of service without
updating their DMARC records.)</p>
</blockquote>

<p>If you operate even a somewhat modest email system that gets a wide
variety of email, as <a href="https://support.cs.toronto.edu/">we</a> do, it
doesn't take very long to receive email from hundreds of From:
domains that have DMARC records in DNS that request reports. When
you generate your DMARC reports (whether once a day or more often),
you'll send out hundreds of email messages to those report addresses.
If you send them through your regular outgoing email system, you'll
have a sudden influx of a lot of messages and you may trigger any
anti-flood ratelimits you have. Once your reporting system has
upended those hundreds of reports into your mail system, your mail
system has to process through them; some of them will be delivered
promptly, some of them will bounce (either directly or inside the
remote mail system you hand them off to), and some of them will be
theoretically destined for (currently) non-responsive hosts and
thus will clog up your mail queue with repeated delivery attempts.
If you're sending these reports through a general purpose mail
system, your mail queue probably has a long timeout for stalled
email, which is not really what you want in this case; your DMARC
reports are more like 'best effort one time delivery attempt and
then throw the message away' email. If this report doesn't get
through and the issue is transient, you'll keep getting email with
that From: domain and eventually one of your reports will go through.
DMARC reports are definitely not 'gotta deliver them all' email.</p>

<p>So in my view, you're almost certainly going to have to be selective
about what domains you send DMARC reports for. If you're considering
this and you can, it may help to trawl your logs to see what domains
are failing DMARC checks and pick out the ones you care about (such
as, say, your organization's overall domain or domains). It's
somewhat useful to report even successful DMARC results (where the
email passes DMARC checks), but if you're considering acting on
DMARC results, it's important to get false negatives fixed. If you
want to send DMARC reports to everyone, you'll want to set up a
custom mail system, perhaps on the DMARC local machine, which blasts
everything out, efficiently handles potentially large queues and
fast submission rates, and discards queued messages quickly (and
obviously doesn't send you any bounces).</p>

<p>(Sending through a completely separate mail system also avoids the
possibility that someone will decide to put your regular system on
a blocklist because of your high rate of DMARC report email.)</p>

<p>PS: Some of those hundreds of From: domains with DMARC records that
request reports will be spammer domains; I assume that putting a
'rua=' into your DMARC record makes it look more legitimate to
(some) receiving systems. Spammers sending from their own domains
can DKIM sign their messages, but having working reporting addresses
requires extra work and extra exposure. And of course spammers
often rotate through domains rapidly.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/spam/DMARCSendingReportsProblems?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/spam/DMARCSendingReportsProblems

---

*ID: fcfd7521208f32c9*
*抓取时间: 2026-03-12T13:49:26.049107*
