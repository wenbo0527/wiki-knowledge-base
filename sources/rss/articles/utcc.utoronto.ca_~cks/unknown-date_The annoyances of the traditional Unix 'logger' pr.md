# The annoyances of the traditional Unix 'logger' program

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-13T04:10:44Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>The venerable 'logger' command has been around so long it's part
of the Single Unix Specification (really, <a href="https://pubs.opengroup.org/onlinepubs/9799919799/utilities/logger.html">logger — log messages</a>).
Although <a href="https://www.tuhs.org/cgi-bin/utree.pl?file=4.2BSD/usr/man/man3/syslog.3">syslog(3)</a>
is in 4.2 BSD (along with <a href="https://www.tuhs.org/cgi-bin/utree.pl?file=4.2BSD/usr/man/man8/syslog.8">syslog(8)</a>,
the daemon), it doesn't seem to have been until 4.3 BSD that we got
<a href="https://www.tuhs.org/cgi-bin/utree.pl?file=4.3BSD/usr/man/man1/logger.1">logger(1)</a>,
with more or less the same arguments as the POSIX version.
Unfortunately, if you want to do more than throw messages into your
syslog and actually create <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/SyslogWellFormedEntryPieces">well-formed, useful syslog messages</a>, '<code>logger</code>' has some annoyances and
flaws.</p>

<p>The flaw is front and center in the manual page and <a href="https://pubs.opengroup.org/onlinepubs/9799919799/utilities/logger.html">the POSIX
specification</a>,
if you read the description of the -i option carefully:</p>

<blockquote><p><code>-i</code>: Log the process ID <strong>of the <code>logger</code> process</strong> with each
message.</p>
</blockquote>

<p>(Emphasis mine.)</p>

<p>In shell scripts where you want to report the script's activities
to syslog, it's not unusual to want to report more than one thing.
In <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/SyslogWellFormedEntryPieces">well-formed syslog messages</a>,
these would all have the same PID, so that you can tell that they
all came from the same invocation of your script. Logger doesn't
support this; if you run logger several times over the course of
your script and use '-i', every log message will have a different
PID. In some environments (such as FreeBSD and Linux with systemd),
logger usually puts in its own PID whether you like it or not.</p>

<p>(The traditional fake for this was to not use '-i' and then embed
your script's PID into your syslog identifier (FreeBSD even recommends
this in their <a href="https://man.freebsd.org/cgi/man.cgi?logger(1)">logger(1)</a>
manual page). This worked okay when syslog identifiers were nothing
more than what got stuck on the front of the message in your log
files, but these days it's not necessarily ideal even if your
'logger' environment doesn't add a PID itself. If you're sending
syslog to a log aggregation system, the identifier can be meaningful
and important and you want it to be a constant for a given message
source so you can search on it.)</p>

<p>Since it's a front end to syslog, logger inherits the traditional
syslog issues that you have to select a meaningful syslog facility,
priority, and identifier (traditionally, the <a href="https://man.freebsd.org/cgi/man.cgi?basename(1)"><code>basename</code></a> of your script).
On the positive side, you can easily vary these from message to
message; on the not so great side, you have to supply them for every
logger invocation and it's on you to make sure all of your uses of
logger use the same ones. Logger doesn't insist that you provide
these and it doesn't have any mechanism (such as a set of environment
variables) for you to provide defaults. This was a bigger issue in
the days before shell functions, since these days you can write a
'logit' function for your shell script that invokes logger correctly
(for your environment). This function is also a good place to
automatically embed your script's PID in the logged message (perhaps
as 'pid=... &lt;supplied message>').</p>

<p>Out of the three of these, the syslog identifier is the easiest to
do a good job of (since you should be picking a meaningful name for
your script anyway) but the traditional syslog environment makes
the identifier relatively meaningless.</p>

<p>It's possible to send all of the output of your script to syslog,
or <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/PipingJustStderr">with a bunch of work</a> you can send just
standard error to syslog (and perhaps repeat it again). But doing
either of these requires wrapping the body of your script up and
feeding all of it to <code>logger</code>:</p>

<blockquote><pre style="white-space: pre-wrap;">
(
... script stuff ...
) 2>&amp;1 | logger -i -t "$(basename "$0")" -pX.Y
</pre>
</blockquote>

<p>(Everything will have the same facility and priority, but if it's
really important to log things at a different priority you can put
in direct 'logger' invocations in the body of the script.)</p>

<p>I suspect that people who used <code>logger</code> a lot probably wrote a
wrapper script (you could call it 'stderr-to-syslog') and ran all
of the real scripts under it.</p>

<p>All of this adds up to a collection of small annoyances. It's not
impossible to use logger in scripts to push things into syslog, but
generally it has to be relatively important to capture the information.
There's nothing off the shelf that makes it easy. And if you want
to have portable logging for your scripts, this basic <code>logger</code> use
is all you get.</p>

<p>(Linux with systemd has <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdCatAndRunForLogging">an entire separate system for this</a> and <a href="https://www.man7.org/linux/man-pages/man1/logger.1.html">the standard Linux
<code>logger</code></a>
has additional options even for syslog logging. But <a href="https://man.openbsd.org/logger.1">OpenBSD
logger(1)</a> is quite minimal and
<a href="https://man.freebsd.org/cgi/man.cgi?logger(1)">FreeBSD logger(1)</a>
is in between, with its own additional features that don't overlap
with the Linux version.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/LoggerItsAnnoyances?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/LoggerItsAnnoyances

---

*ID: 7a0e12d33fb40ef7*
*抓取时间: 2026-03-12T13:49:26.049004*
