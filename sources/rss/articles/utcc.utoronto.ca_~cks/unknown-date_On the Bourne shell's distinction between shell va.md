# On the Bourne shell's distinction between shell variables and exported ones

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-28T03:44:18Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of the famous things that people run into with the Bourne shell
is that it draws a distinction between plain <em>shell variables</em> and
special <em>exported shell variables</em>, which are put into the environment
of processes started by the shell. This distinction is a source of
frustration when you set a variable, run a program, and the program
doesn't have the variable available to it:</p>

<blockquote><pre style="white-space: pre-wrap;">
$ GODEBUG=...
$ go-program
[doesn't see your $GODEBUG setting]
</pre>
</blockquote>

<p>It's also a source of mysterious failures, because more or less all
of the environment variables that are present automatically become
exported shell variables. So whether or not '<code>GODEBUG=..; echo
running program; go-program</code>' works can depend on whether $GODEBUG
was already set when your shell started. The environment variables
of regular shell sessions are usually fairly predictable, but the
environment variables present when shell scripts get run can be
much more varied.  This makes it easy to write a shell script that
only works right for you, because in your environment it runs with
certain environment variables set and so they automatically become
exported shell variables.</p>

<p>I've told you all of that because despite these pains, I believe
that the Bourne shell made the right choice here, in addition to a
pragmatically necessary choice at the time it was created, in V7
(Research) Unix. So let's start with the pragmatics.</p>

<p>The Bourne shell was created along side <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/V7GaveUsEnvironmentVariables">environment variables
themselves</a>, and on the comparatively
small machines that V7 ran on, you didn't have much room for the
combination of program arguments and the new environment. If either
grew too big, you got <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ExecEnvironmentIssue">'argument list too long'</a>
when you tried to run programs. This made it important to minimize
and control the size of the environment that the shell gave to new
processes. If you want to do that without limiting the use of shell
variables so much, a split between plain shell variables and exported
ones makes sense and requires only a minor bit of syntax (in the
form of 'export').</p>

<p>Both machines and exec() size limits are much larger now, so you
might think that getting rid of the distinction is a good thing.
The Bell Labs Research Unix people thought so, so they did do this
in <a href="https://en.wikipedia.org/wiki/Rc_(Unix_shell)">Tom Duff's <code>rc</code> shell for V10 Unix and Plan 9</a>. Having used both
the Bourne shell and <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/WhyISwitchedToRc">a version of <code>rc</code></a> for
many years, I both agree and disagree with them.</p>

<p>For interactive use, having no distinction between shell variables
and exported shell variables is generally great. If I set $GODEBUG,
$PYTHONPATH, or any number of any other environment variables that
I want to affect programs I run, I don't have to remember to do a
special '<code>export</code>' dance; it just works. This is a sufficiently
nice (and obvious) thing that it's an option for the POSIX 'sh',
in the form of '<a href="https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html#set"><code>set -a</code></a>'
(and this set option is present in more or less all modern Bourne
shells, including Bash).</p>

<p>('Set -a' wasn't in <a href="https://www.tuhs.org/cgi-bin/utree.pl?file=V7/usr/man/man1/sh.1">the V7 sh</a>, but
I haven't looked to see where it came from. I suspect that it may
have come from ksh, since POSIX took a lot of the specification for
their 'sh' from ksh.)</p>

<p>For shell scripting, however, not having a distinction is messy and
sometimes painful. If I write an rc script, every shell variable
that I use to keep track of something will leak into the environment
of programs that I run. The shell variables for intermediate results,
the shell variables for command line options, the shell variables
used for <code>for</code> loops, you name it, it all winds up in the environment
unless I go well out of my way to painfully scrub them all out. For
shell scripts, it's quite useful to have the Bourne shell's strong
distinction between ordinary shell variables, which are local to
your script, and exported shell variables, which you deliberately
act to make available to programs.</p>

<p>(This comes up for shell scripts and not for interactive use because
you commonly use a lot more shell variables in shell scripts than
you do in interactive sessions.)</p>

<p>For a new Unix shell today that's made primarily or almost entirely
for interactive use, automatically exporting shell variables into
the environment is probably the right choice. If you wanted to be
slightly more selective, you could make it so that shell variables
with upper case names are automatically exported and everything
else can be manually exported. But for a shell that's aimed at
scripting, you want to be able to control and limit variable scope,
only exporting things that you explicitly want to.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/BourneShellExportGoodAndBad?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/BourneShellExportGoodAndBad

---

*ID: 3884b33e34299bb0*
*抓取时间: 2026-03-12T13:49:26.048169*
