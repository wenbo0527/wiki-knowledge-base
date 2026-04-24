# The long painful history of (re)using <code>login</code> to log people in

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-21T03:36:34Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>The news of the time interval is that <a href="https://www.openwall.com/lists/oss-security/2026/01/20/2">Linux's usual telnetd has
had a giant security vulnerability for a decade</a>. As
people on the Fediverse observed, we've been here before; Solaris
apparently had a similar bug 20 or so years ago (which was
CVE-2007-0882, <a href="https://blog.erratasec.com/2007/02/trivial-remote-solaris-0day-disable.html?m=1">cf</a>,
<a href="https://chaos.social/@ck/115929639137303281">via</a>), and AIX in
the mid 1990s (CVE-1999-0113, <a href="https://infosec.exchange/@phreakmonkey/115929406277759333">source</a>, <a href="https://www.exploit-db.com/exploits/19348">also</a>)), and also apparently
SGI Irix, and no doubt many others (<a href="https://seclists.org/bugtraq/1994/Aug/3">eg</a>). It's not necessarily
telnetd at fault, either, as I believe it's sometimes been <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/BSDRcmdsAndPrivPorts">rlogind</a>.</p>

<p>All of these bugs have a simple underlying cause; in a way that
root cause is people using Unix correctly and according to its
virtue of modularity, where each program does one thing and you
string programs together to achieve your goal. Telnetd and rlogind
have the already complicated job of talking a protocol to the
network, setting up ptys, and so on, so obviously they should leave
the also complex job of logging the user in to <code>login</code>, which already
exists to do that. In theory this should work fine.</p>

<p>The problem with this is that from more or less the beginning, login
has had several versions of its job. From no later than V3 in 1972,
<a href="https://www.tuhs.org/cgi-bin/utree.pl?file=V3/man/man1/login.1">login</a>
could also be used to switch from one user to another, not just log
in initially. In 4.2 BSD, <a href="https://www.tuhs.org/cgi-bin/utree.pl?file=4.2BSD/usr/man/man1/login.1">login</a>
was modified and reused to become part of rlogind's authentication
mechanism (really; .rhosts is checked in <a href="https://www.tuhs.org/cgi-bin/utree.pl?file=4.2BSD/usr/src/bin/login.c">the 4.2BSD login.c</a>,
not in rlogind). Later, various versions of login were modified to
support 'automatic' logins, without challenging for a password (see
eg <a href="https://man.freebsd.org/cgi/man.cgi?query=login">FreeBSD login(1)</a>,
<a href="https://man.openbsd.org/login.1">OpenBSD login(1)</a>, and <a href="https://www.man7.org/linux/man-pages/man1/login.1.html">Linux
login(1)</a>;
use of -f for this appears to date back to around <a href="https://www.tuhs.org/cgi-bin/utree.pl?file=4.3BSD-Tahoe/usr/src/man/man1/login.1">4.3 Tahoe</a>).
Sometimes this was explicitly for the use of things that were running
as root and had already authenticated the login.</p>

<p>In theory this is all perfectly Unixy. In practice, login figured
out which of these variations of its basic job it was being used
for based on a combination of command line arguments and what UID
it was running as, which made it <em>absolutely critical</em> that programs
running as root that reused login never allowed login to be invoked
with arguments that would shift it to a different mode than they
expected. Telnetd and rlogind have traditionally run as root,
creating this exposure.</p>

<p>People are fallible, programmers included, and attackers are very
ingenious. Over the years any number of people have found any number
of ways to trick network daemons running as root into running login
with 'bad' arguments.</p>

<p>The one daemon I don't think has ever been tricked this way is
OpenSSH, because from very early on sshd refused to delegate logging
people in to login. Instead, sshd has its own code to log people
in to the system. This has had its complexities but has also shielded
sshd from all of these (login) context problems.</p>

<p>In my view, this is one of the unfortunate times when the ideals
of Unix run up against the uncomfortable realities of the world.
Network daemons delegating logging people in to <code>login</code> is the
correct Unix answer, but in practice it has repeatedly gone wrong
and the best answer is OpenSSH's.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/LoginProgramReuseFootgun?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/LoginProgramReuseFootgun

---

*ID: 9ef63ed5d4039505*
*抓取时间: 2026-03-12T13:49:26.048597*
