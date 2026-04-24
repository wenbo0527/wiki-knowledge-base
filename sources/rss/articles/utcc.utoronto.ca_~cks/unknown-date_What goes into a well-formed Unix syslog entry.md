# What goes into a well-formed Unix syslog entry

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-12T04:54:47Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>In a <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdScriptsEasyLogCapture">recent entry</a>, I said
in passing that the venerable <a href="https://man.freebsd.org/cgi/man.cgi?logger(1)"><code>logger</code></a> utility had some
amount of annoyances associated with it. In order to explain those
annoyances, I need to first talk about what goes into a well-formed,
useful Unix syslog entry in a traditional Unix syslog environment.</p>

<p>(This is 'well-formed' in a social sense, not in a technical sense
of simply conforming to the syslog message format. There are a lot
of ways to produce technically 'correct' syslog messages that are
neither well formed nor useful.)</p>

<p>A well-formed syslog entry is made up from a number of pieces:</p>

<ul><li>A timestamp, the one thing that you don't have to worry about because
your syslog environment should automatically generate it for you.<p>
(Your syslog environment will also assign a hostname, which you
also don't worry about.)<p>
</li>
<li>An appropriate syslog <em>facility</em>, chosen from the assorted options
that you generally find listed in your local <a href="https://man.freebsd.org/cgi/man.cgi?syslog(3)">syslog(3)</a> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SyslogLogEverythingSomewhere">the available
facilities vary from Unix to Unix</a>). Your program may
need to log to multiple different facilities depending on what
the messages are about; for example, a network daemon that does
authentication should probably send authentication related messages
to 'auth' or 'authpriv' and general things to 'daemon'.<p>
(I know <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SyslogToOnePlace">I've said to throw every syslog facility together in
one place</a>, but having a correct
facility still matters.)<p>
</li>
<li>An appropriate syslog <em>level</em> (aka priority), where you need to at
least distinguish between informational reports ('info'), things
only of interest during debugging problems ('debug', and probably
normally not logged), and active errors that need attention
('error'). Using more levels is useful if they make sense in your
program.<p>
(<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SyslogPrioritiesGivingUp">This doesn't work out in practice</a> but I'm describing how things
should be.)<p>
</li>
<li>A meaningful and unique <em>identifier</em> ('tag' in <a href="https://man.freebsd.org/cgi/man.cgi?logger(1)"><code>logger</code></a>) that
identifies your program as the source of the syslog entry and
groups all of its syslog entries together. This is normally
expected to be the name of your program or perhaps your system.
All syslog entries from your program should have this identifier.<p>
</li>
<li>Your process ID (PID), to uniquely identify this instance of your
program. Your syslog entries should include a PID even if only
one instance of your program is ever running at a time, because
that lets system administrators match your syslog messages up
with other PID-based information and also tell if and when your
program was restarted.<p>
(Under normal circumstances, all messages logged by a single
instance of your program should use the same PID, because that's
how people match up messages to get all of the ones this particular
instance generated.)<p>
</li>
<li>A meaningful message that is more or less readable plain text.
<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PlaintextNotGreatLogFormat">Plain text is not a great format for logs</a>, but syslog message text
that people can read without too much effort is the Unix tradition,
even if it means not including a certain amount of available
metadata (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/StructuredLogFormatsVsPlaintext">structured log formats are not 'plain text'</a>).</li>
</ul>

<p>The text and importance of your message text should match the syslog
level of the syslog entry; if your text says 'ERROR' but you logged
at level 'info', this isn't really a well-formed syslog entry. This
goes double if you're using a semi-structured message text format,
so that you actually logged 'level=error ...' at level 'info' (or
the other way around).</p>

<p>All of this is in service to letting people find your program's
syslog entries, pick out the important ones, understand them, and
categorize both your syslog entries and syslog entries from other
programs. If a busy sysadmin wants to see an overview of all
authentication activity, they should be able to look at where they're
sending 'auth' logs. If they want to look for problems, they can
look for 'error' or higher priority logs. And the syslog facility
your program uses should be sensible in general, although there
aren't many options these days (and you should probably allow the
local system administrators to pick what facility you normally use,
so they can assign you a unique local one to collect just your logs
somewhere).</p>

<p>A good library or tool for making syslog entries should make it as
easy as possible to create well-formed, useful syslog entries.  I
will note in passing that the traditional <a href="https://man.freebsd.org/cgi/man.cgi?syslog(3)">syslog(3)</a> API is not
ideal for this, because it assumes that your program will log all
entries in a single facility, which is not necessarily true for
programs that do authentication and something else.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/SyslogWellFormedEntryPieces?showcomments#comments">3 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/SyslogWellFormedEntryPieces

---

*ID: 37444ec47818c62d*
*抓取时间: 2026-03-12T13:49:26.049014*
