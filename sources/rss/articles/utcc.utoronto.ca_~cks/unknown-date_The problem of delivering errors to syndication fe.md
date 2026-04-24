# The problem of delivering errors to syndication feed readers

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-15T04:30:32Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Suppose, not hypothetically, that there are some feed readers (or
at least things fetching your syndication feeds) that are misbehaving
or blocked for one reason or another. You could just serve these
feed readers <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/403">HTTP 403</a>
errors and stop there, but you'd like to be more friendly. For
regular web browsers, you can either serve a custom HTTP error page
that explains the situation or answer with a <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/302">HTTP 302 temporary
redirection</a> to
a regular HTML page with the explanation. Often the HTTP 302
redirection will be easier because you can use various regular means
to create the HTML pages (and even host them elsewhere if you want).
Unfortunately, this probably leaves syndication feed readers out
in the cold.</p>

<p>(This can also come up if, for example, you decommission a syndication
feed but want to let people know more about the situation than a
simple <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/404">HTTP 404</a>
would give them.)</p>

<p>As far as I know, most syndication feed readers expect that the
reply to their HTTP feed fetching request is in some syndication
feed format (Atom, RSS, etc), which they will parse, process, and
display to the person involved. If they get a reply in a different
format, such as text/html, this is an error and it won't be shown
to the person. Possible the HTML &lt;title> element will make it
through, or the HTTP status code response for an error, or maybe
both. But your carefully written HTML error page is unlikely to
be seen.</p>

<p>(Since syndication feed readers need to be able to display HTML in
general, they could do something to show people at least the basic
HTML text they got back. But I don't think this is very common.)</p>

<p>As a practical thing, if you want people using blocked syndication
feed readers to have a chance to see your explanation, you need to
reply with a syndication feed with an entry that is your (HTML)
message to them (either directly or through HTTP 302 redirections).
Creating this stub feed and properly serving it to appropriate
visitors may be anywhere from annoying to challenging. Also, you
can't reply with HTTP error statuses (and the feed) even though
that's arguably the right thing to do. If you want syndication feed
readers to process your stub feed, you need to provide it as part
of a HTTP 200 reply.</p>

<p>(Speaking from personal experience I can say that hand-writing stub
Atom syndication feeds is a pain, and it will drive you to put very
little HTML in the result. Which is okay, you can make it mostly a
link to your regular HTML page about whatever issue it is.)</p>

<p>If you're writing a syndication feed reader, I urge you to optionally
display the HTML of any HTTP error response or regular HTML page
that you receive. If I was writing some sort of blog system today,
I would make it possible to automatically generate a syndication
feed version of any special error page the software could serve to
people (probably through some magic HTTP redirection). That way
people can write each explanation only once and have it work in
both contexts.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/web/FeedReaderErrorsProblem?showcomments#comments">5 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/FeedReaderErrorsProblem

---

*ID: 30a80ca028eec125*
*抓取时间: 2026-03-12T13:49:26.048316*
