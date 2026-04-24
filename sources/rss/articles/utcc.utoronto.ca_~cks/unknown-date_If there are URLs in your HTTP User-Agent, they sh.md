# If there are URLs in your HTTP User-Agent, they should exist and work

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-09T02:18:01Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of the things people put in their HTTP User-Agent header for
non-browser software is a URL for their software, project, or
whatever (<a href="https://utcc.utoronto.ca/~cks/space/blog/web/UserAgentContentsView">I'm all for this</a>). This is a a
good thing, because it allows people operating web servers to check
out who and what you are and decide for themselves if they're going
to allow it. Increasingly (and partly <a href="https://utcc.utoronto.ca/~cks/space/blog/web/WeShouldBlockForSocialReasons">for social reasons</a>), I block many 'generic' User-Agent
values that come to my attention, for example through their volume.</p>

<p>(I don't block all of them, but if your User-Agent shows up and I
can't figure out what it is and whether or not it's legitimate and
used by real people, <a href="https://utcc.utoronto.ca/~cks/cspace-generic-ua.html">that's probably a block</a>.)</p>

<p>However, there's an important and obvious thing about any URLs in
your HTTP User-Agent, which is that they should actually work. The
domain or host should exist, the URL should exist in the web server,
and the URL's contents should actually explain the software, project,
or organization involved. Plus, if you use a HTTPS website, the TLS
certificate should be valid.</p>

<p>(A related thing is a generic URL that doesn't give me anything to
go on. For example, your URL on a code forge, and either it's not
obvious which one of your repositories is doing things or you don't
have any public repositories.)</p>

<p>For me, a non-working URL is much more suspicious than a missing
URL. HTTP User-Agents without URLs are reasonably common (especially
in feed readers), so I don't find them immediately suspicious.
Non-working URLs in mysterious User-Agents certainly look like
you're attempting to distract me with the appearance of a proper
web agent but without the reality of it. If a User-Agent with such
a non-working URL comes to my attention, I'm very likely to block
it in some way (unless it's very clear that it's a legitimate program
used by real people, and it merely has bad habits with its User-Agent).</p>

<p>You would think that people wouldn't make this sort of mistake, but
I regret to say that I've seen it repeatedly, in all of the variations.
One interesting version I've seen is User-Agent strings with the
various 'example.&lt;TLD>' domains in their URLs. I suspect that this
comes from software that has some sort of 'operator URL' setting
and provides a default value if you don't set one explicitly. I've
also seen .lan and .local URLs in User-Agents, which takes somewhat
more creativity.</p>

<p>As usual, my view is that software shouldn't provide this sort of
default value; instead, it should refuse to work until you configure
your own value. However, this makes it slightly more annoying to
use, so it will be less popular than more accommodating software.
Of course, we can change that calculation by blocking everything
that mentions 'example.com', 'example.org', 'example.net' and so
on in its User-Agent.</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/UserAgentURLsShouldExist

---

*ID: 43dc43a3c37acb04*
*抓取时间: 2026-03-12T13:49:26.048070*
