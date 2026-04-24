# I prefer to pass secrets between programs through standard input

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-04T04:12:04Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>There are a variety of ways to pass secrets from one program to
another on Unix, and many of them may expose your secrets under
some circumstances. A secret passed on the command line is visible
in process listings; a secret passed in the environment can be found
in the process's environment (which can usually be inspected by
outside parties). When I've had to deal with this in administrative
programs in <a href="https://support.cs.toronto.edu/">our environment</a>, I
have reached for an old Unix standby: pass the secret between
programs through file descriptors, specifically standard input and
standard output. This can even be used and done in shell scripts.
However, there are obviously some cautions, both in general and in
shell scripts.</p>

<p>Although Bourne shell script variables look like environment
variables, they aren't exported into the environment until you ask
for this with '<code>export</code>'. Naturally you should never do this for
the environment variables that hold secrets. Also, these days 'echo'
is a built-in in any version of the Bourne shell you want to use,
so '<code>echo $somesecret</code>' does not actually run a process that has
the secret visible in its command line arguments. However, you have
to be careful what commands you use here, because potentially
convenient ones like <a href="https://www.gnu.org/software/coreutils/printf"><code>printf</code></a> aren't builtin and
can't be used like this.</p>

<p>As a general caution, you need to either limit the characters that
are allowed in secrets or encode the secret somehow (you might as
well use base64). If you need to pass more than one thing between
your programs this way, you'll need to define a very tiny protocol,
if only so that you write down the order that things are sent between
programs (and if they are, for example, newline-delimited).</p>

<p>One advantage of passing secrets this way is that it's easy to pass
them from machine to machine through mechanisms like SSH (if you
have passwordless SSH). Instead of 'provide-secret | consume-secret',
you can simply change to 'provide-secret | ssh remote consume-secret'.</p>

<p>In the right (Unix) environment it's possible to pass secrets this
way to programs that want to read them from a file, using features
like Bash's '&lt;(...)' notation or the underlying Unix features that
enable that Bash feature (specifically, /dev/fd).</p>

<p>Passing secrets between programs this way can seem a little janky
and improper, but I can testify that it works. We have a number of
things that move secrets around this way, including across machines,
and they've been doing it for years without problems.</p>

<p>(There are fancy ways to handle this on Linux for some sorts of
secrets, generally static secrets, but I don't know of any other
generally usable way of doing this for dynamic secrets that are
generated on the fly, especially if some of the secrets consumers
are shell scripts. But you probably could write a D-Bus based system
to do this with all sorts of bells and whistles, if you had to do
it a lot and wanted something more professional looking.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/PassingSecretsViaStdin?showcomments#comments">5 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/PassingSecretsViaStdin

---

*ID: 2157fa9dca8f5ad9*
*抓取时间: 2026-03-12T13:49:26.048436*
