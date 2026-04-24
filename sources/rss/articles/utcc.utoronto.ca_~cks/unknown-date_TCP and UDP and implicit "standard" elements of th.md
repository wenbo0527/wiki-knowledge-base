# TCP and UDP and implicit "standard" elements of things

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-16T02:34:36Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Recently, <a href="http://verisimilitudes.net/">Verisimilitude</a> left a
comment on <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/UnboundListenAllInterfaces">this entry of mine</a>
about binding TCP and UDP ports to a specific address. That got me
thinking about features that have become standard elements of things
despite not being officially specified and required.</p>

<p>TCP and UDP are more or less officially specified in various RFCs
and are implicitly specified by what happens on the wire. As far
as I know, nowhere in these standards (or wire behavior) does
anything require that a multi-address host machine allow you to
listen for incoming TCP or UDP traffic on a specific port on only
a restricted subset of those addresses. People talking to your host
have to use a specific IP, obviously, and established TCP connections
have specific IP addresses associated with them that can't be
changed, but that's it. Hosts could have an API where you simply
listened to a specific TCP or UDP port and then they provided you
with the local IP when you received inbound traffic; it would be
up to your program to do any filtering to reject addresses that
you didn't want used.</p>

<p>However, I don't think anyone has such an API, and anything that
did would likely be considered very odd and 'non-standard'. It's
become an implicit standard feature of TCP and UDP that you can opt
to listen on only one or a few IP addresses of a multi-address host,
including listening only on localhost, and connections to your (TCP)
port on other addresses are rejected without the TCP three-way
handshake completing. This has leaked through into the behavior
that TCP clients expect in practice; if a port is not available on
an IP address, clients expect to get a TCP layer 'connection refused',
not a successful connection and then an immediate disconnection.
If a host had the latter behavior, clients would probably not report
it as 'connection refused' and some of them would consider it a
sign of a problem on the host.</p>

<p>This particular (API) feature comes from a deliberately designed
element of the BSD sockets API, <a href="https://man.freebsd.org/cgi/man.cgi?bind(2)">the <code>bind()</code> system call</a>. Allowing you to
bind() local addresses to your sockets means that you can set the
outgoing IP address for TCP connection attempts and UDP packets,
which is important in some situations, but BSD could have provided
a different API for that. BSD's bind() API does allow you maximum
freedom with only a single system call; you can nail down <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/BindingOutgoingSockets">either
or both of the local IP and the local port</a>. Binding the local port (but not
necessarily the local IP) was important in BSD Unix because <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/BSDRcmdsAndPrivPorts">it
was part of a security mechanism</a>.</p>

<p>(This created an implicit API requirement for other OSes. If you
wanted your OS to have an rlogin client, you had to be able to force
the use of a low local port when making TCP connections, because
<a href="https://minnie.tuhs.org/cgi-bin/utree.pl?file=4.1cBSD/usr/src/ucb/netser/rlogin/rlogind.c">the BSD rlogind.c</a>
simply rejected connections from ports that were 1024 and above even
in situations where it would ask you for a password anyway.)</p>

<p>A number of people copied the BSD sockets API rather than design
their own. Even when people designed their own API for handling
networking (or IPv4 and later IPv6), my impression is that they
copied the features and general ideas of the BSD sockets API rather
than starting completely from scratch and deviating significantly
from the BSD API. My usual example of a relatively divergent API
is Go, which is significantly influenced by a quite different
networking history inside Bell Labs and AT&amp;T, but <a href="https://pkg.go.dev/net">Go's net package</a> still allows you to <a href="https://pkg.go.dev/net#Listen">listen selectively
on an IP address</a>.</p>

<p>(Of course Go has to work with the underlying BSD sockets API on
many of the systems it runs on; what it can offer is mostly constrained
by that, and people will expect it to offer more or less all of the
'standard' BSD socket API features in some form.)</p>

<p>PS: The BSD TCP API doesn't allow a listening program to make a
decision about whether to allow or reject an incoming connection
attempt, but this is turned out to be a pretty sensible design.
As we found out witn <a href="https://en.wikipedia.org/wiki/SYN_flood">SYN flood attacks</a>, TCP's design means that
you want to force the initiator of a connection attempt to prove
that they're present before the listening ('server') side spends
much resources on the potential connection.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/TCPAndUDPPartiallyImplicit?showcomments#comments">6 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/TCPAndUDPPartiallyImplicit

---

*ID: 5c2e4fe3657b3e36*
*抓取时间: 2026-03-12T13:49:26.048648*
