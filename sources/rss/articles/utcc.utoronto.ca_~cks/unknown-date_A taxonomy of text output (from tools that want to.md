# A taxonomy of text output (from tools that want to be too clever)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-04T01:41:02Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of my long standing gripes with Debian and Ubuntu is, well,
<a href="https://mastodon.social/@cks/115415433547543468">I'll quote myself on the Fediverse</a>:</p>

<blockquote><p>I understand that Debian wants me to use 'apt' instead of apt-get,
but the big reason I don't want to is because you can't turn off that
progress bar at the bottom of your screen (or at least if you can
it's not documented). That curses progress bar is something that I
absolutely don't want (and it would make some of our tooling explode,
yes we have tooling around apt-get).</p>
</blockquote>

<p>Over time, I've developed opinions on what I want to see tools do
for progress reports and other text output, and what I feel is
increasingly too clever in tools that makes them more and more
inconvenient for me. Today I'm going to try to run down that taxonomy,
from best to worst.</p>

<ol><li>Line by line output in plain text with no colours.</li>
<li>Represent progress by printing successive dots (or other characters) on
the line until finally you print a newline. This is easy to capture and
process later, since the end result is a newline terminated line with
no control characters.<p>
</li>
<li>Reporting progress by printing dots (or other characters) and then
backspacing over them to erase them later. Pagers like <a href="https://www.man7.org/linux/man-pages/man1/less.1.html"><code>less</code></a> have some
ability to handle backspaces, but this will give you heartburn in
your own programs.<p>
</li>
<li>Reporting progress by repeatedly printing a line, backspacing over
it, and reprinting it (as apt-get does). This produces a lot more
output, but I think <code>less</code> and anything that already deals with
backspacing over things will generally be able to handle this.
I believe apt-get does this.<p>
</li>
<li>Any sort of line output with colours (which don't work in my environment,
and when they do work they're usually unreadable). Any sort of
terminal codes in the output make it complicated to capture the
output with tools like <a href="https://www.man7.org/linux/man-pages/man1/script.1.html"><code>script</code></a> and then
look over them later with pagers like <a href="https://www.man7.org/linux/man-pages/man1/less.1.html"><code>less</code></a>, although
<code>less</code> can process a limited amount of terminal codes, including
colours.<p>
</li>
<li>Progress bar animation on one line with cursor controls and other
special characters. This looks appealing but generates a lot more
output and is increasingly hard for programs like <code>less</code> to
display, search, or analyze and process. However, your terminal
program of choice is probably still going to see this as line by
line output and preserve various aspects of scrollback and so on.<p>
</li>
<li>Progress output that moves the cursor and the output from its
normal line to elsewhere on screen, such as at the bottom (as 'apt
autoremove' and other bits of 'apt' do). Now you have a full
screen program; viewing, reconstructing, and searching its output
later is extremely difficult, and its output will blow up
increasingly spectacularly if it's wrong about your window size
(including if you resize things while it's running) or what
terminal sequences your window responds to. Terminal programs
and terminal environments such as tmux or screen may well throw
up their hands at doing anything smart with the output, since
you look much like a full screen editor, a pager, or programs
like <code>top</code>. In some environments this may damage or destroy
terminal scrollback.<p>
An additional reason I dislike this style is that it causes output
to not appear at the current line. When I run your command line
program, I want your program to print its output right below where
I started it, in order, because that's what everything else does.
I don't want the output jumping around the screen to random other
locations. The only programs I accept that from are genuine full
screen programs like <code>top</code>. Programs that insist on displaying
things at random places on the screen are not really command line
programs, they are TUIs <a href="https://en.wikipedia.org/wiki/Cosplay">cosplaying</a> being CLIs.<p>
</li>
<li>Actual full screen output, as a text UI, with the program clearing the
screen and printing status reports all over the place. Fortunately
I don't think I've seen any 'command line' programs do this; anything
that does tends to be clearly labeled as a TUI program, and people
mostly don't provide TUIs for command line tools (partly because it's
usually more work).</li>
</ol>

<p>My strong system administrator's opinion is that if you're tempted
to do any of these other than the first, you should provide a command
line switch to turn these off. Also, you should detect unusual
settings of the <code>$TERM</code> environment variable, like 'dumb' or perhaps
'vt100', and automatically disable your smart output. And you should
definitely disable your smart output if <code>$TERM</code> isn't set or you're
not outputting to a (pseudo-)terminal.</p>

<p>(Programs that insist on fancy output no matter what make me
<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/FedoraDnf5SmartOutputCurse">very unhappy</a>.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ProgramTextOutputTaxonomy?showcomments#comments">5 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ProgramTextOutputTaxonomy

---

*ID: 475feea009221e03*
*抓取时间: 2026-03-12T13:49:26.048125*
