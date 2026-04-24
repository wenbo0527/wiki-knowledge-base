# Moving to make many of my SSH logins not report things on login

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-11T04:32:49Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I've been logging in to Unix machines for what is now quite a long
time. When I started, it was traditional for your login process to
be noisy. The login process itself would tell you last login details
and the 'message of the day' ('motd'), and people often made their
shell
.profile or .login report more things, so you could see things like:</p>

<blockquote><pre style="white-space: pre-wrap;">
Last login: Tue Feb 10 22:16:14 2026 from 128.100.X.Y
 22:22:42 up 1 day, 11:22,  3 users,  load average: 0.40, 2.95, 3.30
cks cks cks
[output from fortune elided]
: &lt;host> ;
</pre>
</blockquote>

<p>(There is no motd shown here but it otherwise hits the typical high
points, including <a href="https://en.wikipedia.org/wiki/Fortune_(Unix)">a quote from fortune</a>. People didn't always
use 'fortune' itself but printing a randomly selected quote on login
used to be common.)</p>

<p>Many years ago I modified my shell environment on <a href="https://support.cs.toronto.edu/">our</a> servers so that it wouldn't report
the currently logged in users, show the motd, or tell me my last
login. But I kept the '<code>uptime</code>' line:</p>

<blockquote><pre style="white-space: pre-wrap;">
$ ssh cs.toronto.edu
 22:26:05 up 209 days,  5:26, 167 users,  load average: 0.47, 0.51, 0.60
: apps0.cs ;
</pre>
</blockquote>

<p>Except, I typically didn't see that. I see this only on full login
sessions, and when I was in the office I typically used <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ToolsRxterm">special
tools</a> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ToolsPyhosts">also</a>, <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ToolsXrun">also</a>,
<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/RemoteXWhatIMiss">also</a>) that didn't actually start a
login session and so didn't show me this greeting banner. Only when
I was at home did I do SSH logins (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ToolsSshterm">with tooling</a>)
and so see this, and I didn't do that very much (because I didn't
normally work from home, so I had no reason to be routinely opening
windows on our servers).</p>

<p>As a long term result of <a href="https://en.wikipedia.org/wiki/COVID-19_pandemic">that 2020 thing</a> I work from home
a lot more these days and so I open up a lot more SSH logins than
I used to. Recently I was thinking about how to make this feel
nicer, and it struck me that one of the things I found quietly
annoying was that line from 'uptime' (to the point that sometimes
my first action on login was to run 'clear', so I had a clean
window). It was the one last thing cluttering up 'give me a new
window on host X' and making the home experience visibly different
from the office experience.</p>

<p>So far I've taken only a small step forward. I've made it so that
I skip running 'uptime' if I'm logging in from home and the load
on the machine I'm logging in to is sufficiently low to be uninteresting
(which is often the case). As I get used to (or really, accept)
this little change, I'll probably slowly move to silence 'uptime'
more often.</p>

<p>When I think about it, making this change feels long overdue.
Printing out all sorts of things on login made sense in a world
where I logged in to places relatively infrequently. But that's not
the case in my world any more. <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MySemiTransience">My terminal windows are mostly
transient</a> and I mostly work on servers that I
have to start new windows on, and right from very early I made my
office environment not treat them as login sessions, with the full
output and everything (if I cared about routinely seeing the load
on a server, that's what <code>xload</code> was for (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MyBoringDesktop">cf</a>)).</p>

<p>(<a href="https://mastodon.social/@cks/116037349248581999">I'm bad about admitting to myself that my usage has shifted and
old settings no longer make sense</a>.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MovingToSilentLogins?showcomments#comments">3 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MovingToSilentLogins

---

*ID: 6a569ef96a4229d8*
*抓取时间: 2026-03-12T13:49:26.048360*
