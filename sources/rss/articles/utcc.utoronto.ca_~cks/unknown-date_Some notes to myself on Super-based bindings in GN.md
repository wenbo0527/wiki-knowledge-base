# Some notes to myself on Super-based bindings in GNU Emacs

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-05T03:11:59Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p><a href="https://utcc.utoronto.ca/~cks/space/blog/python/Python2EmacsLSPProblems">I recently had to deal with GNU Emacs lsp-mode in a context where I
cared a bit about its keybindings</a>,
and in the process of that ran across mention of what one could call
its leader prefix, s-l. People who use GNU Emacs a lot will know what
this specific 's-' notation means, but I'm not one of them, so it took
me a bit of research to work it out. This is GNU Emacs' notation for
'Super', one of the theoretical extra key modifiers that you can have
on keyboards.</p>

<p>(I suspect that lsp-mode uses s-l as its prefix on its key bindings
because everything else good is taken.)</p>

<p>My impression is that it's normal for Unix desktop environments to
have a key mapped to 'Super', often the left 'Microsoft' key; this
is the case in my unusual X desktop environment. On Windows and
macOS machines, you can apparently set up mappings in GNU Emacs
itself as covered by <a href="http://xahlee.info/emacs/emacs/emacs_hyper_super_keys.html">Xah Lee in "Emacs Keys: Super Hyper"</a> (<a href="https://irreal.org/blog/?p=6645">via</a>). This gives me a working Super
key (if I remember it, which I hopefully will now) when I'm using
a GUI GNU Emacs that has <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/KeysAndCharacters">direct access to relatively raw key
information</a>, either locally or on a
server with X forwarding.</p>

<p>However, things aren't so good for me if I'm using GNU Emacs in any
sort of terminal window. <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/TerminalEmulatorsAndAlt">Unlike Alt, for which there's a standard
way to handle it in terminals</a>,
there appears to be no special handling for Super in either xterm
or Gnome-Terminal. Super plus a regular character gives me the
regular character, both locally and over SSH connections. In this
environment, the only way to access Super-based bindings is with
the special and awkward <a href="https://www.gnu.org/software/emacs/manual/html_node/emacs/Modifier-Keys.html">GNU Emacs way to add Super (and Hyper)
to key sequences</a>.
For Super, this is 'C-x @ s ...', and you can see why I'm not
enthused about typing it all that often. In practice, I'm more
likely to invoke obscure (to me) lsp-mode things through M-x and
<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/EmacsUnderstandingOrderless">orderless</a>.</p>

<p>Fortunately, I think lsp-mode is the only thing that has Super
bindings in my usual GNU Emacs environment, which means this is
something I mostly won't need to care about. Given the challenges
in using Super, I'll avoid any temptation to bind my own things
with it. I also suspect that there's pretty much no hope for (Unix)
terminal emulators and the terminal environment to add support for
it, which will probably discourage other Emacs addons from using
it.</p>

<p>(I did a crude search of all of the .el files I use and no obvious
Super bindings turned up other than lsp-mode's.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/EmacsSuperNotes?showcomments#comments">6 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/EmacsSuperNotes

---

*ID: 4f9a26f1a7ab2ee6*
*抓取时间: 2026-03-12T13:49:26.048761*
