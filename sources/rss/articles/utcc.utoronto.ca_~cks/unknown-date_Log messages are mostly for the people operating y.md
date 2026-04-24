# Log messages are mostly for the people operating your software

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-03T04:48:37Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I recently read Evan Hahn's <a href="https://evanhahn.com/the-two-kinds-of-error/">The two kinds of error</a> (<a href="https://lobste.rs/s/3cq649/two_kinds_error">via</a>), which talks very
briefly in passing about logging, and it sparked a thought. I've
previously written <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/ErrorsShouldRequireFixing">my system administrator's view of what an error
log level should mean</a>, but that entry
leaves out something fundamental about log messages, which is that
under most circumstances, <strong>log messages are for the people operating
your software</strong> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/GoodKernelMessages">I've sort of said this before in a different
context</a>). When you're about to add a
non-debug log message, one of the questions you should ask is what
does someone running your program get out of seeing the message.</p>

<p>Speaking from my own experience, it's very easy to write log messages
(and other messages) that are aimed at you, the person developing
the program, script, or what have you. They're useful for debugging
and for keeping track of the state of the program, and it's natural
to write them that way since you're immersed in the program and
have all of the context (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ContextInErrorMessages">this is especially a problem for infrequent
error messages</a>, which I've
learned to make as verbose as possible, and a similar thing applies
for <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/LoggingForLocalModifications">infrequently logged messages</a>). But if your software
is successful (especially if it gets distributed to other people),
most of the people running it won't be the developers, they'll only
be operating it.</p>

<p>(This can include a future version of you when you haven't touched
this piece of software for months.)</p>

<p>If you want your log messages to be useful for anything other than
being mailed to you as part of a 'can you diagnose this' message,
they need to be useful for the people operating the software. This
doesn't mean 'only report errors that they can fix and need to',
although that's part of it. It also means making the information
you provide through logs be things that are useful and meaningful
to people operating your software, and that they can understand
without <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/UselessKernelMessages">a magic decoder ring</a>.</p>

<p>If people operating your software won't get anything out of seeing
a log message, you probably shouldn't log it by default in the first
place (or you need to reword it so that people will get something
from it). In Evan Hahn's terminology, this apply to the log messages
for both expected errors and unexpected errors, although if the
program aborts, it should definitely tell system administrators why
it did.</p>

<p>For a system administrator, log messages about expected errors let
us diagnose what went wrong to cause something to fail, and how
interested we are in them depends partly on how common they are.
However, how common they are isn't the only thing. <a href="https://en.wikipedia.org/wiki/Message_transfer_agent">MTAs</a> often have
what would be considered relatively verbose logs of message processing
and will log every expected error like 'couldn't do a DNS lookup'
or 'couldn't connect to a remote machine', even though they can
happen a lot. This is very useful because one thing we sometimes
care a lot about is what happened to and with a specific email
message.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/LogMessagesAreForOperation?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/LogMessagesAreForOperation

---

*ID: 8cc66375d1ecaab3*
*抓取时间: 2026-03-12T13:49:26.048137*
