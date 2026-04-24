# Turning to systemd units for easy capturing of log output

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-08T03:17:29Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Suppose, <a href="https://utcc.utoronto.ca/~cks/space/blog/spam/DMARCSendingReportsProblems">not hypothetically</a>,
that you have a third party tool that you need to run periodically.
This tool prints things to standard output (or standard error) that
are potentially useful to capture somehow. You want this captured
output to be associated with the program (or your general system
for running the program) and timestamped, and it would be handy if
the log output wound up in all of the usual places in your systems
for output. Unix has traditionally had some solutions for this, such
as <a href="https://www.man7.org/linux/man-pages/man1/logger.1.html">logger</a>
for sending things to syslog, but they all have a certain amount of
annoyances associated with them.</p>

<p>(If you directly run your script or program from cron, you will
automatically capture the output in a nice dated form, but you'll
also get email all the time. Let's assume we want a quieter experience
than email from cron, because you don't need to regularly see the
output, you just want it to be available if you go looking.)</p>

<p>On modern Linux systems, the easy and lazy thing to do is to run
your script or program from a systemd service unit, because systemd
will automatically do this for you and send the result into the
systemd journal (and anything that pulls data from that) and, if
configured, into whatever overall systems you have for handling
syslog logs. You want a unit like this:</p>

<blockquote><pre style="white-space: pre-wrap;">
[Unit]
Description=Local: Do whatever
ConditionFileIsExecutable=/root/do-whatever

[Service]
Type=oneshot
ExecStart=/root/do-whatever
</pre>
</blockquote>

<p>Unlike the usual setup for running scripts as systemd services, we
don't set '<code>RemainAfterExit=True</code>' because we want to be able to
repeatedly trigger our script with, for example, 'systemctl start
local-whatever.service'. <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdTimersMailNotes">You can even arrange to get email if
this unit (ie, your script) fails</a>.</p>

<p>You can run this directly from cron through suitable /etc/cron.d
files that use 'systemctl start', or set up a systemd timer unit
(possibly with <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdTimerMethodsUsed">a randomized start time</a>).
The advantage of a systemd timer unit is that you definitely won't
ever get email about this unless you specifically configure it.  If
you're setting up <a href="https://utcc.utoronto.ca/~cks/space/blog/spam/DMARCSendingReportsProblems">a relatively unimportant and throwaway thing</a>, it being reliably silent is
probably a feature.</p>

<p>(Setting up a systemd timer unit also keeps everything within the
systemd ecosystem rather than worrying about various aspects of
running 'systemctl start' from scripts or crontabs or etc.)</p>

<p>On the one hand, it feels awkward to go all the way to a systemd
service unit simply to get easy to handle logs; it feels like there
should be a better solution somewhere. On the other hand, it works
and it only needs one extra file over what you'd already need (the
.service).</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdScriptsEasyLogCapture?showcomments#comments">4 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdScriptsEasyLogCapture

---

*ID: 763b96e7da92e2eb*
*抓取时间: 2026-03-12T13:49:26.049056*
