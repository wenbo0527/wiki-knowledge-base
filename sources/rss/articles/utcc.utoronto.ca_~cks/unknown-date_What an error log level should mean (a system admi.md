# What an error log level should mean (a system administrator's view)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-17T03:08:34Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Over on the Fediverse, <a href="https://mastodon.social/@cks/115696867071346159">I had a grumpy reaction to one program's
new logging behavior</a>:</p>

<blockquote><p>Tell me you don't look at your logs without telling me that you
don't look at your logs: arrange to log perfectly routine events as
'level=ERROR' reports.</p>

<p>Thank you, Prometheus Blackbox version 0.28.0, you have been voted off
the island. We will not be upgrading to you from 0.27.0. Maybe there
will be a 0.28.1, one can hope. (Yes, <a href="https://github.com/prometheus/blackbox_exporter/issues/1510">reported</a>.)</p>
</blockquote>

<p>Then I had <a href="https://mastodon.social/@cks/115730558592210621">an additional hot take</a> that's today's
subject:</p>

<blockquote><p>Today's hot take on log levels: if it's not something that has to be
fixed, it's not an error, it's a warning (at most).</p>

<p>(This assumes an error/warning/info/debug set of logging levels
instead of something more fine grained, but that's how many things are
these days.)</p>
</blockquote>

<p>In system logs (and thus in anything that's expected to feed into
them), an 'error' should mean that something is wrong and it needs
to be fixed. By extension, it should be something that people can
fix. Since we're talking about system logs, this should generally
be things that affect the operation of the program that's doing the
logging, not simply things wrong somewhere else. If a SMTP mailer
trying to send email to somewhere logs 'cannot contact port 25 on
&lt;remote host>', that is not an error in the local system and should
not be logged at level 'error'. The 'error' log level is for 'I'm
not working right, help', things such as 'configuration file error',
'my memory allocation failed', 'unexpected failure to read a data
file', and so on.</p>

<p>(If people can't fix the 'error' condition, either it's not really an
error or people are going to have to abandon your program because it
has an unfixable problem in their environment.)</p>

<p>Or to put it another way, a program that's working properly as
designed and configured should not be logging 'error' level messages.
Error level messages should be a reliable sign that something is
actually wrong. If error level messages are not such a sign, I can
assure you that most system administrators will soon come to ignore
all messages from your program rather than try to sort out the mess,
and any actual errors will be lost in the noise and never be noticed
in advance of actual problems becoming obvious.</p>

<p>When implementing logging, it's important to distinguish between
an error from the perspective of an individual operation and an
error from the perspective of the overall program or system.
Individual operations may well experience errors that are not error
level log events for the overall program. You could say that an
operation error is anything that prevents an operation from completing
successfully, while a program level error is something that prevents
the program as a whole from working right. <a href="https://github.com/prometheus/blackbox_exporter/issues/1510">As Prometheus Blackbox
illustrates</a>,
treating operation level error events as program level error events
is not necessarily useful for people operating your program.</p>

<p>(It can be interesting to know about operation level problems and
errors, so you might log them as 'warn' or 'info'. But not 'error'
if you intend 'error' to be useful when operating your program and
for people to look at your logs other than when they're debugging
your program. And if your logs are only for debugging, you should
provide an option to turn them off entirely so people don't have
to pollute their system logs with your debugging output.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/ErrorsShouldRequireFixing?showcomments#comments">7 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/ErrorsShouldRequireFixing

---

*ID: 042e0f1eeda474a8*
*抓取时间: 2026-03-12T13:49:26.048962*
