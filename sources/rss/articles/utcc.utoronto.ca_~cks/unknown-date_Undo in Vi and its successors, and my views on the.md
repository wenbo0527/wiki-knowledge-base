# Undo in Vi and its successors, and my views on the mess

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-12T04:19:15Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>The original Bill Joy vi famously only had a single level of undo
(which is part of what makes it <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ViIsAProductOfItsTime">a product of its time</a>). The 'u' command either undid your latest
change or it redid the change, undo'ing your undo. When POSIX and
the Single Unix Specification wrote vi into the standard, they
required this behavior; the <a href="https://pubs.opengroup.org/onlinepubs/9799919799/utilities/vi.html">vi</a>
specification requires 'u' to work the same as it does in <a href="https://pubs.opengroup.org/onlinepubs/9799919799/utilities/ex.html">ex</a>, where
it is specified as:</p>

<blockquote><p>Reverse the changes made by the last command that modified the
contents of the edit buffer, including undo.</p>
</blockquote>

<p>This is one particular piece of POSIX compliance that I think
everyone should ignore.</p>

<p><a href="https://en.wikipedia.org/wiki/Vim_(text_editor)">Vim</a> and its
derivatives ignore the POSIX requirement and implement multi-level
undo and redo in the usual and relatively obvious way. The vim
'u' command only undoes changes but it can undo lots of them, and
to redo changes you use Ctrl-r ('r' and 'R' were already taken).
Because 'u' (and Ctrl-r) are regular commands they can be used with
counts, so you can undo the last 10 changes (or redo the last 10
undos). Vim can be set to <a href="https://vimhelp.org/undo.txt.html#undo-two-ways">vi compatible behavior</a> if you want.
I believe that vim's multi-level undo and redo is the default
even when it's invoked as 'vi' in an unconfigured environment,
but I can't fully test that.</p>

<p><a href="https://en.wikipedia.org/wiki/Nvi">Nvi</a> has opted to remain POSIX
compliant and operate in the traditional vi way, while still
supporting multi-level undo. To get multi-level undo in nvi, you
extend the first 'u' with '.' commands, so 'u..' undoes the most
recent three changes. The 'u' command can be extended with '.'
in either of its modes (undo'ing or redo'ing), so 'u..u..' is
a no-op. The '.' operation doesn't appear to take a count in nvi,
so there is no way to do multiple undos (or redos) in one action;
you have to step through them by hand. I'm not sure how nvi reacts
if you want do things like move your cursor position during an undo
or redo sequence (my limited testing suggests that it can perturb
the sequence, so that '.' now doesn't continue undoing or redoing
the way vim will continue if you use 'u' or Ctrl-r again).</p>

<p>The vi emulation package <a href="https://github.com/emacs-evil/evil">evil</a>
for GNU Emacs inherits GNU Emacs' multi-level undo and nominally
binds undo and redo to 'u' and Ctrl-r respectively. However, I don't
understand its actual stock undo behavior. It appears to do multi-level
undo if you enter a sequence of 'u' commands and accepts a count
for that, but it feels not vi or vim compatible if you intersperse
'u' commands with things like cursor movement, and I don't understand
redo at all (evil has <a href="https://evil.readthedocs.io/en/latest/settings.html#miscellaneous">some customization settings for undo behavior</a>,
especially <a href="https://evil.readthedocs.io/en/latest/settings.html#elispobj-evil-undo-system"><code>evil-undo-system</code></a>).
I haven't investigated Evil extensively and this undo and redo stuff
makes me less likely to try using it in the future.</p>

<p>The <a href="https://en.wikipedia.org/wiki/BusyBox">BusyBox</a> implementation
of vi is minimal but it can be built with support for 'u' and
multi-level undo, which is done by repeatedly invoking 'u'. It
doesn't appear to have any redo support, which makes a certain
amount of sense in an environment when your biggest concern may be
reverting things so they're no worse than they started out. The
Ubuntu and Fedora versions of busybox appear to be built this way,
but your distance may vary on other Linuxes.</p>

<p>My personal view is that the vim undo and redo behavior is the best
and most human friendly option. Undo and redo are predictable and
you can predictably intersperse undo and redo operations with other
operations that don't modify the buffer, such as moving the cursor,
searching, and yanking portions of text. The nvi behavior essentially
creates a special additional undo mode, where you have to remember
that you're in a sequence of undo or redo operations and you can't
necessarily do other vi operations in the middle (such as cursor
movement, searches, or yanks). This matters a lot to me because I
routinely use multi-level undo when I'm writing text to rewind my
buffer to a previous state and yank out some wording that I've
decided I like better than its replacement.</p>

<p>(For additional vi versions, <a href="https://mastodon.social/@cks/116054998873679043">on the Fediverse</a>, I was also
<a href="https://snac.bsd.cafe/r1w1s1/p/1770859710.601320">pointed to</a>
<a href="https://github.com/kyx0r/nextvi">nextvi</a>, which appears to use
vim's approach to undo and redo; I believe <a href="https://github.com/aligrudi/neatvi">neatvi</a> also does this but I can't
spot any obvious documentation on it. There are vi-inspired editors
such as <a href="https://invisible-island.net/vile/">vile</a> and <a href="https://github.com/martanne/vis">vis</a>, but they're not things people
would normally use as a direct replacement for vi. I believe that
vile follows the nvi approach of 'u.' while vis follows the vim
model of 'uu' and Ctrl-r.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ViUndoMyViews?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/ViUndoMyViews

---

*ID: 57341d0cd729cb10*
*抓取时间: 2026-03-12T13:49:26.048349*
