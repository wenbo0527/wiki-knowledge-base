# Something you don't want to do when using Spamhaus's DQS with Exim

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-13T04:16:48Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>For reasons outside the scope of this entry, <a href="https://support.cs.toronto.edu/">we</a> recently switched from <a href="https://spamhaus.org/">Spamhaus</a>'s traditional public DNS (what is now called
the 'public mirrors') to an account with their Data Query Service.
The DQS data can still be queried via DNS, which presents a problem:
DNS queries have no way to carry any sort of access key with them.
Spamhaus has solved this problem by embedding your unique access
key in the zone name you must use. Rather than querying, say,
zen.spamhaus.org, you query '&lt;key>.zen.dq.spamhaus.net'. Because
your DQS key is tied to your account and your account has query
limits, you don't want to spread your DQS key around for other
people to pick up and use.</p>

<p>We use the <a href="https://exim.org/">Exim</a> mailer (which is more of <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PostfixVsExim">a
mailer construction kit</a> out of the box). Exim has
<a href="https://exim.org/exim-html-current/doc/html/spec_html/ch-access_control_lists.html#SECTmorednslists">a variety of convenient features for using DNS (block) lists</a>.
One of them is that when Exim finds an entry in a DNS blocklist in
an <a href="https://exim.org/exim-html-current/doc/html/spec_html/ch-access_control_lists.html">ACL</a>,
it sets some (Exim) variables that you can use later in various
contexts, such as creating log messages. To more or less quote from
the Exim documentation on <a href="https://exim.org/exim-html-current/doc/html/spec_html/ch-string_expansions.html#SECTexpvar">(string) expansion variables</a>:</p>

<blockquote><p>$dnslist_domain <br />
$dnslist_matched <br />
$dnslist_text <br />
$dnslist_value</p>
<blockquote><p>When a DNS (black) list lookup succeeds, these variables are set to
contain the following data from the lookup: the list’s domain name,
the key that was looked up, the contents of any associated TXT record,
and the value from the main A record. [...]</p>
</blockquote>
</blockquote>

<p>To make life easier on yourself, it's conventional to use these
variables (among others) in things like SMTP error messages and
headers that you add to messages:</p>

<blockquote><pre style="white-space: pre-wrap;">
deny hosts = !+local_networks
     message = $sender_host_address is listed \
               at $dnslist_domain: $dnslist_text
     dnslists = rbl-plus.mail-abuse.example

warn dnslists = weird.example
     add_header = X-Us-DNSBL: listed in $dnslist_domain
</pre>
</blockquote>

<p>However, if you're using Spamhaus DQS, using $dnslist_domain
as these examples do is dangerous. The DNS list domain will be the
full domain, and that full domain will include your DQS access key,
which you will thus be exposing in message headers and SMTP error
messages. You probably don't want to do that.</p>

<p>(Certainly it feels like a bad practice to leak a theoretically
confidential value into the world, even if the odds are that no one
is going to pick it up and abuse it.)</p>

<p>You have two options. The first option is to simply hard code some
appropriate name for the list instead of using $dnslist_domain.
However, this only works if you're using a single DNS list in each
ACL condition, instead of something where you check multiple DNS
blocklists at once (with 'dnslists = a.example : b.example :
c.example'). It's also a bit annoying to have to repeat yourself.</p>

<p>(This is what I did to our Exim configuration when I realized the
problem.)</p>

<p>The second option is that Exim has <a href="https://exim.org/exim-html-current/doc/html/spec_html/ch-string_expansions.html">a comprehensive string expansion
language</a>,
so determined people can manipulate $dnslist_domain to detect
that it contains your DQS key and remove it. The brute force way
would be to use <code>${sg}</code> (from <a href="https://exim.org/exim-html-current/doc/html/spec_html/ch-string_expansions.html#SECTexpansionitems">expansion items</a>)
to replace your key with nothing, something like (this is untested):</p>

<blockquote><pre style="white-space: pre-wrap;">
${sg{$dnslist_domain}{&lt;DQS key>}{}}
</pre>
</blockquote>

<p>You could probably wrap this up in <a href="https://exim.org/exim-html-current/doc/html/spec_html/ch-the_exim_runtime_configuration_file.html#SECTmacrodefs">an Exim macro</a>,
call it '<code>DNSLIST_NAME</code>', and then write ACLs as, say:</p>

<blockquote><pre style="white-space: pre-wrap;">
deny hosts = !+local_networks
     message = $sender_host_address is listed \
               at DNSLIST_NAME
     dnslists = rbl-plus.mail-abuse.example
</pre>
</blockquote>

<p>(Because we're using ${sg}, we won't change the name of a DNSBL domain
that doesn't contain the DQS key.)</p>

<p>This isn't terrible and it does cope with a single Exim ACL condition
that checks multiple DNS blocklists.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/EximSpamhausDQSGotcha

---

*ID: da1a2d96954002a4*
*抓取时间: 2026-03-12T13:49:26.048679*
