# Some notes on using systemd-run or systemd-cat for logging program output

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-09T03:44:45Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>In response to <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdScriptsEasyLogCapture">yesterday's entry on using systemd (service) units
for easy capturing of log output</a>, a
commentator drew my attention to <a href="https://www.freedesktop.org/software/systemd/man/251/systemd-run.html">systemd-run</a> and
<a href="https://www.freedesktop.org/software/systemd/man/251/systemd-cat.html">systemd-cat</a>.  I
spent a bit of time poking at both of them and so I've wound up
with some things to remember and some opinions.</p>

<p>(The short summary is that you probably want to use systemd-run with
a specific unit name that you pick.)</p>

<p><a href="https://www.freedesktop.org/software/systemd/man/251/systemd-cat.html">Systemd-cat</a> is
very roughly the systemd equivalent of <a href="https://www.man7.org/linux/man-pages/man1/logger.1.html">logger</a>. As you'd
expect, things that it puts in the systemd journal flow through to
anywhere that regular journal entries would, including <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/GrafanaLokiWhatILikeItFor">things
that directly get fed from the journal</a> and syslog (including
<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/CentralizeSyslog">remote syslog destinations</a>). The
most convenient way to use systemd-cat is to just have it run a
command, at which point it will capture all of the output from the
command and put it in the journal. However, there is a little issue
with using just 'systemd-cat /some/command', which is that the
journal log identifiers that systemd-cat generates in this case
will be the direct name of whatever program produced the output.
If /some/command is a script that runs a variety of programs that
produce output (perhaps it echos some status information itself
then runs a program, which produces output on its own), you'll
get a mixture of identifier names in the resulting log:</p>

<blockquote><pre style="white-space: pre-wrap;">
your-script[...]: >>> Frobulating the thing
some-prog[...]: Frobulation results: 23 processed, 0 errors
</pre>
</blockquote>

<p>Journal logs written by systemd-cat also inherit whatever unit it
was in (a session unit, cron.service, etc), and the combination can
make it hard to clearly see all of the logs from running your script.
To do better you need to give systemd-cat an explicit identifier,
'systemd-cat -t &lt;something> /some/command', which point everything
is logged with that name, but still in whatever systemd unit
systemd-cat ran in.</p>

<p>Generally you want your script to report all its logs under a single
unit name, so you can find them and sort them out from all of the
other things your system is logging. To do this you need to use
<a href="https://www.freedesktop.org/software/systemd/man/251/systemd-run.html">systemd-run</a> with an explicit unit name:</p>

<blockquote><pre style="white-space: pre-wrap;">
systemd-run -u myscript --quiet --wait -G /some/script
</pre>
</blockquote>

<p>I believe you can then hook this into any systemd service unit
infrastructure you want, such as <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdTimersMailNotes">sending email if the unit fails</a> (if you do, you probably want to add
'--service-type=oneshot').  Using systemd-run this way gets you the
best of both systemd-cat worlds; all of the output from /some/script
will be directly labeled with what program produced it, but you can
find it all using the unit name.</p>

<p>Systemd-run will refuse to activate a unit with a name that duplicates
an existing unit, including existing systemd-run units. In many
cases this is a feature for script use, since you basically get
'run only one copy' locking for free (although the error message
is noisy, so you may want to do your own quiet locking). If you
want to always run your program even if another instance is running,
you'll have to generate non-constant unit names (or let systemd-run
do it for you).</p>

<p>Systemd-cat has some features that systemd-run doesn't offer, such
as setting the priority of messages (and setting a different priority
for standard error output). If these features are important to you,
I'd suggest nesting systemd-cat (with no '-t' argument) inside
systemd-run, so you get both the searchable unit name and the
systemd-cat features. If you're already in an environment with a
useful unit name and you just need to divert log messages from
wherever else the environment wants to send them into the system
journal, bare systemd-cat will do the job.</p>

<p>(Arguably this is the case for things run from cron, if you're
content to look for all of them under cron.service (or crond.service,
depending on your Linux distribution). Running things under systemd-cat
puts their output in the journal instead of having them send you
email, which may be good enough and saves you having to invent and
then remember a bunch of unit names.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdCatAndRunForLogging?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdCatAndRunForLogging

---

*ID: 98da13011a65641e*
*抓取时间: 2026-03-12T13:49:26.049044*
