# TCP, UDP, and listening only on a specific IP address

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-20T02:33:59Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of the surprises of TCP and UDP is that when your program listens
for incoming TCP connections or UDP packets, you can chose to listen
only on a specific IP address instead of all of the IP addresses
that the current system has. This behavior started as <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/TCPAndUDPPartiallyImplicit">a de-facto
standard</a> but is now explicitly
required for TCP in <a href="https://www.ietf.org/rfc/rfc9293.html#section-3.9.1.1">RFC 9293 section 3.9.1.1</a>. There are
at least two uses of this feature; to restrict access to your
listening daemon, and to run multiple daemons on the same port.</p>

<p>The classical case of restricting access to a listening daemon is
a program that listens only on the loopback IP address (IPv4 or
IPv6 or both). Since loopback addresses can't be reached from outside
the machine, only programs running on the machine can reach the
daemon. On a machine with multiple IP addresses that are accessible
from different network areas, you can also listen on only one IP
address (perhaps an address 'inside' a firewall) to shield your
daemon from undesired connections.</p>

<p>(Except in the case of the loopback IP address, this shielding isn't
necessarily perfect. People on any of your local networks can always
throw packets at you for any of your IP addresses, if they know
them. In some situations, listening only on RFC 1918 private addresses
can be reasonably safe from the outside world.)</p>

<p>The other use is to run multiple daemons that are listening on the
same port but on different IP addresses. For example, you might run
a public authoritative DNS server for some zones that is listening
on port 53 (TCP and UDP) on your non-localhost IPs and a private
resolving DNS server that is listening on localhost:53. Or you could
have a 'honeypot' IP address that is running a special SSH server
to look for Internet attackers, while still running your regular
SSH server (to allow regular access) on your normal IP addresses.
Broadly, this can be useful any time you want to have different
configurations on the same port for different IP addresses.</p>

<p>Using restricted listening for access control has a lot of substitutes.
Your daemon can check incoming connections and drop them depending
on the local or remote IPs, or your host could have some simple
firewall rules, or <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/SystemdPortFirewallWish">some additional software layer could give you
a hand</a>. Also, as mentioned, if
you listen on anything other than localhost, you need to be sure
that your overall configuration makes that safe enough. The other
options are more complex but also more sure, or at least more
obviously sure (or flawed).</p>

<p>Using restricted listening to have different things listening on
the same TCP or UDP port doesn't have any good substitutes in current
systems. Even if the operating system allows multiple things to
listen generally on the same port, it has no idea which instance
should get which connection or packet. To do this steering today,
you'd need either a central 'director' daemon that received all
packets or connection attempts and then somehow passed them to the
right other program, or you'd have programs listen on different
ports and then use OS firewall rules to (re)direct traffic to the
right instance.</p>

<p>You can imagine an API that allows all of the programs to tell the
operating system which connections they're interested in and which
ones they aren't. One simple form of that API is 'listen on a
specific IP address instead of all of them', and it conveniently
also allows the OS to trivially detect conflicts between programs
(<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/WhyPortBindingRestriction">even if some of them initially seem artificial</a>).</p>

<p>(It would be nice if OSes gave programs nice APIs for choosing what
incoming connections and packets they wanted and what they didn't,
but mostly we deal with the APIs we have, not the ones we want.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/TCPUDPListeningOnAddress?showcomments#comments">6 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/TCPUDPListeningOnAddress

---

*ID: 5e2b62761c2e52cf*
*抓取时间: 2026-03-12T13:49:26.048607*
