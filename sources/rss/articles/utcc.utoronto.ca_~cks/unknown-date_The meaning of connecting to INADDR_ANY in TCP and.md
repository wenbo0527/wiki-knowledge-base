# The meaning of connecting to INADDR_ANY in TCP and UDP

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-05T02:55:11Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>An interesting change to IP behavior landed in FreeBSD 15, <a href="https://github.com/golang/go/issues/77411">as I
discovered by accident</a>.
To quote from <a href="https://www.freebsd.org/releases/15.0R/relnotes/#network-general">the general networking section of the FreeBSD 15
release notes</a>:</p>

<blockquote><p>Making a connection to <code>INADDR_ANY</code>, i.e., using
it as an alias for <code>localhost</code>, is now disabled by
default. This functionality can be re-enabled by setting the
<code>net.inet.ip.connect_inaddr_wild sysctl</code> to 1. <a href="https://cgit.freebsd.org/src/commit/?id=cd240957d7ba">cd240957d7ba</a></p>
</blockquote>

<p><a href="https://cgit.freebsd.org/src/commit/?id=cd240957d7ba">The change's commit message</a> has a bit
of a different description:</p>

<blockquote><p>Previously connect() or sendto() to INADDR_ANY reached some socket
bound to some host interface address. Although this was intentional it
was an artifact of a different era, and is not desirable now.</p>
</blockquote>

<p>This is connected to <a href="https://cgit.freebsd.org/src/commit/?id=417b35a97b76">an earlier change</a>
and <a href="https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=280705">FreeBSD bugzilla #28075</a>, which has
some additional background and motivation for the overall change (as
well as the history of this feature in 4.x BSD).</p>

<p>The (current) Linux default behavior matches the previous FreeBSD
behavior. If you had something listening on localhost (in IPv4,
specifically 127.0.0.1) or listening on INADDR_ANY, connecting
to INADDR_ANY would reach it and give the source of your
connection a localhost address (either 127.0.0.1 or ::1 depending
on IPv4 versus IPv6). Obviously the current FreeBSD default behavior
has now changed, and the Linux behavior may change at some point
(or at least become something that can be changed by a sysctl).</p>

<p>(Linux specifically restricts you to connecting to 127.0.0.1;
you can't reach a port listening on, eg, 127.0.0.10, although
that is also a localhost address.)</p>

<p>One of the tricky API issues here is that higher level APIs can
often be persuaded or tricked into using INADDR_ANY by default
when they connect to something. For example, in Go's <a href="https://pkg.go.dev/net">net</a> package, if you leave the hostname blank,
you currently get INADDR_ANY (which is convenient behavior for
listening but not necessarily for connecting). In other APIs, your
address variable may start with an initial zero value for the target
IP address, which is INADDR_ANY for IPv4; if your code never
sets it (perhaps because the 'host' is a blank string), you get a
connection to INADDR_ANY and thus to localhost. In top of that,
a blank host name to connect to may have come about through accident
or through an attacker's action (perhaps they can make decoding or
parsing the host name fail, leaving the 'host name' blank on you).</p>

<p>I believe that what's happening with Go's tests is that the <a href="https://pkg.go.dev/net">net</a>
package guarantees that things like <a href="https://pkg.go.dev/net#Dial">net.Dial("tcp", ":&lt;port>")</a> connect to localhost, so of course
the net package has tests to insure that this stays working.
Currently, Go's net package implements this behavior by mapping a
blank host to INADDR_ANY, which has traditionally worked and
been the easiest way to get the behavior Go wants. It also means
that Go can use uniform parsing of 'host:port' for both listening,
where ':port' is required to mean listening on INADDR_ANY, and
for connecting, where the host has to be localhost. Since this is
a high level API, Go can change how the mapping works, and it pretty
much has to in order to fully work as documented on FreeBSD 15 in
a stock configuration.</p>

<p>(Because that would be a big change to land right before the release
of Go 1.26, I suspect that the first bugfix that will land is to
skip these tests on FreeBSD, or maybe only on FreeBSD 15+ if that's
easy to detect.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/SocketConnectToAnyMeaning?showcomments#comments">6 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/SocketConnectToAnyMeaning

---

*ID: 54adc000e3788416*
*抓取时间: 2026-03-12T13:49:26.048425*
