# What 24 hours of traffic looks like to our main web server in January 2026

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-08T03:54:53Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of the services <a href="https://support.cs.toronto.edu/">we</a> operate
for <a href="https://www.cs.toronto.edu/">the department</a> is a traditional
Apache-based shared web server, with things like people's home pages
(<a href="https://www.cs.toronto.edu/~cks/">eg</a>), pages for various groups,
and so on (we call this our departmental web server). This web
server has been there for a very long time and its URLs have spread
everywhere, and <a href="https://mastodon.social/@cks/115851872715237648">in the process it's become quite popular for some
things</a>. These
days there are a lot of things crawling everything in sight, and
our server has no general defenses against them (we don't even have
much of a robots.txt).</p>

<p>(Technically our perimeter firewall has <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/OpenBSDPfMaxNotes">basic HTTP and HTTPS
brute-force connection rate limits</a>, but
people typically have to really work to trigger them and they mostly
don't. Although now that I look at yesterday, more IPs wound up
listed than I expected, although listings normally last at most
five minutes.)</p>

<p>The first, very noticeable thing that we have is people who do very
slow downloads from us. Our server rolls over the logs at midnight,
but Apache only writes a log record when a HTTP request completes,
possibly to the old log file. Yesterday (Tuesday), the last log
record was written at 05:24, for a request that started at 22:44.
Over the 24 hours that requests were initiated in, we saw 1.2 million
requests.</p>

<p>The two most active User-Agents were (in somewhat rounded numbers):</p>

<blockquote><pre style="white-space: pre-wrap;">
426000 "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
424000 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0 Safari/537.36"
</pre>
</blockquote>

<p>The most active thing that was willing to admit it wasn't a human
with a browser was "ChatGPT-User", with just under 20,000 requests.
After that came "GoogleOther" and "Amazonbot", at about 12,000
requests each, then "Googlebot" with 10,000 and bingbot with about
6,000. Of course, some of those could be people impersonating the
real Googlebot and bingbot.</p>

<p>To my surprise, the most popular HTTP result code by far was <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/301">HTTP
301 Moved Permanently</a>,
at 844,000 responses (HTTP 200s were 347,000, everything else was
small by comparison). And most of the requests by the those two
most active User-Agents got HTTP 301 responses (roughly 418,000
each). I don't know what's going on there, but someone seems to
have latched on to a lot of URLs that require redirects (which
include things like directory URLs without the '/' on the end). On
the positive side, most of those requests will have been pretty
cheap for Apache to handle.</p>

<p>A single DigitalOcean IP claiming to be running Chrome 61 on 'Windows
NT 10.0' made 11,000 requests, most of which got HTTP 404 errors
because it was requesting URLs like '/wp-login.php'. There's no
point complaining to hosting providers about this sort of thing,
it's just background noise. No other single IP stood out to that
degree (well, <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusGrafanaSetup-2019">our monitoring system</a> made over 10,000 requests,
but that's expected). Google mostly crawled from a few IPs, with
large counts, but other crawlers were more spread out.</p>

<p>To find out more traffic information, we need to go to looking at
<a href="https://en.wikipedia.org/wiki/Autonomous_system_%28Internet%29">Autonomous System Numbers (ASNs)</a>,
using <a href="https://utcc.utoronto.ca/~cks/space/blog/web/ToolsToSeeVolumeSources">asncounter</a>. This reports:</p>

<pre style="white-space: pre-wrap;">
 count   percent ASN     AS
 463536  36.55   210906  BITE-US, LT
 152237  12.0    212286  LONCONNECT, GB
 65064   5.13    3257    GTT-BACKBONE GTT, US
 53927   4.25    7385    ABUL-14-7385, US
 45255   3.57    8075    MICROSOFT-CORP-MSN-AS-BLOCK, US
 32557   2.57    7029    WINDSTREAM, US
 32101   2.53    55286   SERVER-MANIA, CA
 30037   2.37    15169   GOOGLE, US
 24412   1.92    239     UTORONTO-AS, CA
 21745   1.71    7015    COMCAST-7015, US
 16311   1.29    64200   VIVIDHOSTING, US
 [...]
</pre>

<p>And then for prefixes:</p>

<pre style="white-space: pre-wrap;">
 count   percent prefix  ASN     AS
 64312   5.07    138.226.96.0/20 3257    GTT-BACKBONE GTT, US
 43459   3.43    85.254.128.0/22 210906  BITE-US, LT
 43161   3.4     185.47.92.0/22  210906  BITE-US, LT
 43111   3.4     45.131.216.0/22 212286  LONCONNECT, GB
 43040   3.39    45.145.136.0/22 212286  LONCONNECT, GB
 42998   3.39    45.138.248.0/22 212286  LONCONNECT, GB
 42870   3.38    185.211.96.0/22 210906  BITE-US, LT
 32365   2.55    85.254.112.0/22 210906  BITE-US, LT
 26937   2.12    66.249.64.0/20  15169   GOOGLE, US
 23785   1.88    128.100.0.0/16  239     UTORONTO-AS, CA
 23088   1.82    45.154.148.0/22 212286  LONCONNECT, GB
 21767   1.72    85.254.42.0/23  210906  BITE-US, LT
 [and then five more BITE-US prefixes at the same
  volume level, then many more prefixes]
</pre>

<p>Given that we have two extremely prolific User-Agents, let's look
at where those requests came from in specific, and you will probably
not be surprised at the results:</p>

<pre style="white-space: pre-wrap;">
 count   percent ASN     AS
 462925  54.37   210906  BITE-US, LT
 152155  17.87   212286  LONCONNECT, GB
 64321   7.55    3257    GTT-BACKBONE GTT, US
 53649   6.3     7385    ABUL-14-7385, US
 32287   3.79    7029    WINDSTREAM, US
 31955   3.75    55286   SERVER-MANIA, CA
 21710   2.55    7015    COMCAST-7015, US
 16304   1.92    64200   VIVIDHOSTING, US
 [...]
</pre>

<p>If you have the ability to block traffic by ASN and <a href="https://utcc.utoronto.ca/~cks/space/blog/web/DoYouNeedCloudRequests">you don't
need to accept requests from clouds</a> and
your traffic is anything like this, you can probably drop a lot of
it quite easily.</p>

<p>I can ask a different question: if we exclude those two popular
User-Agents and look only at successful requests (HTTP 200
responses), where do they come from?</p>

<pre style="white-space: pre-wrap;">
 count   percent ASN     AS
 38821   11.61   8075    MICROSOFT-CORP-MSN-AS-BLOCK, US
 25510   7.63    15169   GOOGLE, US
 16968   5.07    239     UTORONTO-AS, CA
 12816   3.83    14618   AMAZON-AES, US
 11529   3.45    396982  GOOGLE-CLOUD-PLATFORM, US
 [...]
</pre>

<p>(There are about 334,000 of these in total.)</p>

<p>The 'UTORONTO-AS' listing includes our own monitoring, with its
10,000 odd requests. Much of Google's requests come from their
66.249.64.0/20 prefix, which is mostly or entirely used by various
Google crawlers.</p>

<p>Around 138,000 requests were for <a href="https://www.cs.toronto.edu/~kriz/cifar.html">a set of commonly used ML training
data</a>, and they probably
account for most of the bandwidth used by this web server (which
typically averages 40 Mbytes/sec of outgoing bandwidth all of the
time on weekdays).</p>

<p>(I've previously done <a href="https://utcc.utoronto.ca/~cks/space/blog/web/HTTP2OurWebServerHowMuch-2025">HTTP/2 stats for this server as of mid 2025</a>.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/web/OurWebServer24Hours-2026?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/OurWebServer24Hours-2026

---

*ID: 86fa2f2fa2a76c01*
*抓取时间: 2026-03-12T13:49:26.048730*
