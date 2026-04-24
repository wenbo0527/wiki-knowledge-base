# How to redirect a Bash process substitution into a <code>while</code> loop

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-27T03:37:47Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>In some sorts of shell scripts, you often find yourself wanting to
work through a bunch of input in the shell; some examples of this
for me are <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/RCStoMercurial">here</a> and <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ForcingSortOrder">here</a>. One of the tools for this is a
'<code>while read -r ...</code>' loop, using the shell's <a href="https://www.gnu.org/software/bash/manual/bash.html#index-read">builtin <code>read</code></a> to
pull in one or more fields of data (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ShellImportanceOfASpace">hopefully not making a mistake</a>).
Suppose, not hypothetically, that you have a situation where you
want to use such a '<code>while read</code>' loop to accumulate some information
from the input, setting shell variables, and then using them later.
The innocent and non-working way to write this is:</p>

<blockquote><pre style="white-space: pre-wrap;">
accum=""
sep=""
some-program |
while read -r avalue; do
   accum="$accum$sep$avalue"
   sep=" or "
done

# Now we want to use $accum
</pre>
</blockquote>

<p>(The recent script where I ran into this issue does much more complex
things in the while loop that can't easily be done in other ways.)</p>

<p>This doesn't work because the 'while' is actually happening in a
subshell, so the shell variables it sets are lost at the end. To
make this work we have to wrap everything from the 'while ...'
onward up into a subshell, with that part looking like:</p>

<blockquote><pre style="white-space: pre-wrap;">
some-program |
(
while read -r avalue; do
   accum="$accum$sep$avalue"
   sep=" or "
done
[...]
)
</pre>
</blockquote>

<p>(You can't get around this with '{ while ...; ... done; }', Bash
will still put the 'while' in a subshell.)</p>

<p>The way around this starts with how you can use a file redirection
with a while loop (it goes on the '<code>done</code>'):</p>

<blockquote><pre style="white-space: pre-wrap;">
some-program >/some/file
while read -r avalue; do
  [...]
done &lt;/some/file
# $accum is still set
</pre>
</blockquote>

<p>So far this is all generic Bourne shell things. Bash has a special
feature of <a href="https://www.gnu.org/software/bash/manual/bash.html#Process-Substitution-1">process substitution</a>,
which allows us to use a process instead of a file, using the
otherwise illegal syntax '&lt;(...)'. This is great and exactly what
we want to avoid creating a temporary file and then have to clean
it up. So the innocent and obvious way to try to write things is
this:</p>

<blockquote><pre style="white-space: pre-wrap;">
while read -r avalue; do
  [...]
done &lt;(some-program)
</pre>
</blockquote>

<p>If you try this, you will get the sad error message from Bash of:</p>

<blockquote><pre style="white-space: pre-wrap;">
line N: syntax error near unexpected token `&lt;(some-program)'
line N: 'done &lt;(some-program)'
</pre>
</blockquote>

<p>This is not a helpful error message. I will start by telling you
the cure, and then what is going on at a narrow technical level to
produce this error message. The cure is:</p>

<blockquote><pre style="white-space: pre-wrap;">
while read -r avalue; do
  [...]
done &lt; &lt;(some-program)
</pre>
</blockquote>

<p>Note that you must have a space between the two &lt;'s, writing this
as '&lt;&lt;(some-program)' will get you a similar syntax error.</p>

<p>The technical reason for this error is that although it looks like
redirection, <a href="https://www.gnu.org/software/bash/manual/bash.html#Process-Substitution-1">process substitution</a> is a form of substitution,
like '<code>$var</code>' (it's in the name, but you, like me, may not know
what Bash calls it off the top of your head). The result of process
substitution will be, for example, a /dev/fd/N name (and a subprocess
that is running our 'some-program' and feeding into the other end
of the file descriptor).  We can see this directly:</p>

<blockquote><pre style="white-space: pre-wrap;">
$ echo &lt;(cat /dev/null)
/dev/fd/63
</pre>
</blockquote>

<p>(Your number may vary.)</p>

<p>You can't write '<code>while ...; done /dev/fd/63</code>'. That's a syntax
error. Even though the pre-substitution version looks like
redirection, it's not, so it's not accepted.</p>

<p>That '&lt;(...)' is actually a substitution is why our revised version
works. Reading '&lt; &lt;(some-program)' right to left, the '&lt;(some-program)'
is <a href="https://www.gnu.org/software/bash/manual/bash.html#Process-Substitution-1">process substitution</a>, and it (along with other <a href="https://www.gnu.org/software/bash/manual/bash.html#Shell-Expansions">shell
expansions</a>) are
done first, before redirections. After substitution this looks like
'&lt; /dev/fd/NN', which is acceptable syntax. If we leave out the
space and write this as '&lt;&lt;(some-program)', the shell throws up its
hands at the '&lt;&lt;' bit.</p>

<p>(So from Bash's perspective, this is very similar to '<code>file=/some/file;
while ... ; done &lt; $file</code>', which is perfectly legal.)</p>

<p>PS: Before I wrote this entry, I didn't know how to get around the
'done &lt;(some-program)' syntax error. Until the penny dropped about
the difference between <a href="https://www.gnu.org/software/bash/manual/bash.html#Redirections">redirections</a>
and <a href="https://www.gnu.org/software/bash/manual/bash.html#Process-Substitution-1">process substitution</a>, I thought that Bash simply forbade
this to make its life easier.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/BashWhileWithProcessSubstitution?showcomments#comments">4 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/BashWhileWithProcessSubstitution

---

*ID: 3a1b6294dbabc2c7*
*抓取时间: 2026-03-12T13:49:26.048180*
