# Safely querying Spamhaus DNSBLs in Exim

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-14T02:53:51Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>When querying Spamhaus DNS blocklists, either their public mirrors
or through a DQS account, the DNS blocklists can potentially return
<a href="https://www.spamhaus.org/resource-hub/dnsbl/using-our-public-mirrors-check-your-return-codes-now/">error codes in 127.255.255.0/24</a>
(<a href="https://docs.spamhaus.com/datasets/docs/source/70-access-methods/data-query-service/040-dqs-queries.html#return-codes">also</a>).
Although Exim has a variety of DNS blocklist features, it doesn't yet
let you match return codes based on CIDR netblocks. However, it does have
a magic way of doing this.</p>

<p>The magic way is to stick '!&amp;0.255.255.0' on the end of the DNS
blocklist name. This is a <a href="https://exim.org/exim-html-current/doc/html/spec_html/ch-access_control_lists.html#SECID205">negated DNS (blocklist) matching
conditions</a>,
specifically a negated bitmask (a 'bitwise-and'). The whole thing
looks like:</p>


<blockquote><pre style="white-space: pre-wrap;">
deny dnslists = zen.spamhaus.org!&amp;0.255.255.0
</pre>
</blockquote>

<p>What this literally means is to consider the lookup to have failed
if the resulting IP address matches '*.255.255.*'. Because
Exim already requires successful lookup results to be in 127.0.0.0/8,
this implicitly constrains the entire result to not match
127.255.255.*, which is what we want.</p>

<p>As covered in <a href="https://exim.org/exim-html-current/doc/html/spec_html/ch-access_control_lists.html#SECTaddmatcon">Additional matching conditions for DNS lists</a>,
Exim can match DNS blocklist results by a specific IP or a <em>bitmap</em>,
the latter of which is written as, eg, '&amp;0.255.255.0'.  When you
match by bitmap, the IP address is anded with the bitmap and the
result must be the same as the bitmap (meaning that all bits set
in the bitmask are set in the IP address):</p>

<blockquote><p>(ip &amp; bitmask) == bitmask</p>
</blockquote>

<p>(You can consider both the IP and the bitmask as 32-bit numbers,
or you can consider each octet separately in both, whichever makes
it easier.)</p>

<p>There's no way to say that the match succeeds if the result of
and'ing the IP and the bitmask is non-zero (has any bits set).  For
small number of bits, you can sort of approximate that by using
multiple bitmasks. For example, to succeed if either of the two
lowest bits are set:</p>

<blockquote><p>a.example&amp;0.0.0.1,0.0.0.2</p>
</blockquote>

<p>(The 'lowest bit' here is the lowest bit of the rightmost octet.)</p>

<p>If you negate a bitmask condition by writing it as '!&amp;', the lookup
is considered to have failed if the '&amp;&lt;bitmask>' match is successful,
which is to say that the IP address anded with the bitmask is the
same as the bitmask.</p>

<p>This is why '!&amp;0.255.255.0' does what we want.  '&amp;0.255.255.0'
successfully matches if the IP address is exactly *.255.255.*,
because both middle octets have all their bits set in the mask so
they have to have all their bits set in the IP address, and because
the first and last octets in the mask are 0, their value in the IP
address isn't looked at. Then we negate this, so the lookup is
considered to have failed if the bitmask matched, which would mean
that Spamhaus returned results in 127.255.255.0/24.</p>

<p>I'm writing all of that out in detail because here is what the
current Exim documentation says about negated DNS bitmask conditions:</p>

<blockquote><p>Negation can also be used with a bitwise-and restriction. The dnslists
condition with only be true if a result is returned by the lookup
which, anded with the restriction, is all zeroes.</p>
</blockquote>

<p>This is not how Exim behaves. If it was how Exim behaves, Spamhaus
DBL lookups would not work correctly with '!&amp;0.255.255.0'. DBL
lookups return results in 127.0.1.0/24; if you bitwise-and that
with 0.255.255.0, you get '0.0.1.0', which is not all zeroes.</p>

<p>(It could be useful to have a version of '&amp;' that succeeded if any of
the bits in the result were non-zero, but that's not what Exim has
today, as discussed above.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/EximSafeSpamhausQueries?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/EximSafeSpamhausQueries

---

*ID: 0a88e9959f835032*
*抓取时间: 2026-03-12T13:49:26.048669*
