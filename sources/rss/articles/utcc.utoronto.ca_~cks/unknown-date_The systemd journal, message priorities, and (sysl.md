# The systemd journal, message priorities, and (syslog) facilities

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-15T03:27:20Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>If you use <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdScriptsEasyLogCapture">systemd units</a> or
<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdCatAndRunForLogging">systemd-run</a> to conveniently capture
output from scripts and programs into the systemd journal, one of
the things that it looks like you don't get is message priorities
and (syslog) facilities. Fortunately, systemd's journal support is
a bit more sophisticated than that.</p>

<p>When you print out regular output and systemd captures it into the
journal, systemd assigns it a default priority that's set with
<a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#SyslogLevel="><code>SyslogLevel=</code></a>;
this is normally 'info', which is a good default choice. Similarly,
you can pick the syslog facility associated with your unit or your
<a href="https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html">systemd-run</a>
invocation with <a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#SyslogFacility="><code>SyslogFacility=</code></a>.
Systemd defaults to 'daemon', which may not entirely be what you
want. On the other hand, the choice of syslog facility matters less
if you're primarily working with <a href="https://www.freedesktop.org/software/systemd/man/latest/journalctl.html">journalctl</a>,
where what you usually care about is the systemd unit name.</p>

<p>(You can use journalctl to select messages by <a href="https://www.freedesktop.org/software/systemd/man/latest/journalctl.html#-p">priority</a>
or <a href="https://www.freedesktop.org/software/systemd/man/latest/journalctl.html#--facility=">syslog facility</a>
with the -p and --facility options. You can also select by <a href="https://www.freedesktop.org/software/systemd/man/latest/journalctl.html#-t">syslog
identifier</a>
with the -t option. This is probably going to be handy for searching
the journal for messages from some of our programs that use syslog
to report things.)</p>

<p>If you know that you're logging to systemd (or you don't care that
your regular output looks a bit weird in spots), you can also print
messages with special priority markers, as covered in <a href="https://www.freedesktop.org/software/systemd/man/latest/sd-daemon.html">sd-daemon(3)</a>.
Now that I know about this, I may put it to use in some of our
scripts and programs. Sadly, unlike the normal Linux <a href="https://www.man7.org/linux/man-pages/man1/logger.1.html">logger</a> and its
--prio-prefix option, you can't change the syslog facility this
way, but if you're doing pure journald logging you probably don't
care about that.</p>

<p>(It's possible that <a href="https://www.freedesktop.org/software/systemd/man/latest/sd-daemon.html">sd-daemon(3)</a> actually supports the <a href="https://www.man7.org/linux/man-pages/man1/logger.1.html">logger</a>
behavior of changing the syslog facility too, but if so it's not
documented and you shouldn't count on it. Instead you should assume
that you have to control the syslog facility through setting
<a href="https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#SyslogFacility="><code>SyslogFacility=</code></a>, which unfortunately means you can't log just
authentication things to 'auth' and everything else to 'daemon' or
some other appropriate facility.)</p>

<p>PS: Unfortunately, as far as I know journalctl has no way to augment
its normal syslog-like output with some additional fields, such as
the priority or the syslog facility. Instead you have to go all the
way to a verbose dump of information in <a href="https://www.freedesktop.org/software/systemd/man/latest/journalctl.html#--output-fields=">one of the supported
formats for field selection</a>.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdJournalPriorityEtc

---

*ID: e02cac6543d523ad*
*抓取时间: 2026-03-12T13:49:26.048983*
