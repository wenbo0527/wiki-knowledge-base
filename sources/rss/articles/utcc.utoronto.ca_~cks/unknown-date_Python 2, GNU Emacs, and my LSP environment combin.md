# Python 2, GNU Emacs, and my LSP environment combine to shoot me in the foot

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-26T21:50:14Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>So <a href="https://mastodon.social/@cks/115772410046643299">I had a thing happen</a>:</p>

<blockquote><p>This is my angry face that GNU Emacs appears to have re-indented my
entire Python file to a different standard without me noticing and I
didn't catch it in time. And also it appears impossible in GNU Emacs
to FIX this. I do not want four space no tabs, this is historical code
that all files should be eight spaces with tabs (yes, Python 2).</p>
</blockquote>

<p>That 'Python 2' bit turns out to be load-bearing. The specific
problem turned out to be that if I hit TAB with a region selected
or M-q when GNU Emacs point was outside a comment, the entire file
was reformatted to modern 4-space indents (and long expressions got
linewrapped, and some other formatting changes). I'm not sure which
happened to trigger the initial reformatting that I didn't notice
in time, but I suspect I was trying to use M-q to reflow a file
level comment block and had my cursor (point) in the wrong spot.
<a href="https://mastodon.social/@cks/115778377555998716">My TAB and M-q bindings are standard</a>, and when I
investigated deeply enough I discovered that this was LSP related.</p>

<p>The first thing I learned is that just 'turning off' LSP mode with
'lsp-mode' (or 'M-: (lsp-mode -1))' isn't enough to actually turn
off LSP based indentation handling. This is discussed in <a href="https://github.com/emacs-lsp/lsp-mode/issues/824">lsp-mode
issue #824</a>, and
apparently the solution is some combination of deactivating an
additional minor mode, invoking <code>lsp-disconnect</code> through M-x (or
using the 's-l w D' key binding if you have Super available), or
setting <code>lsp-enable-indentation</code> to 'nil' (probably as a buffer-local
variable, although tastes may differ).</p>

<p>The second thing I discovered is that in my environment this doesn't
happen for Python 3 code. With my normal Python 3 GNU Emacs LSP
environment, using <a href="https://pypi.org/project/python-lsp-server/">python-lsp-server (pylsp)</a> (<a href="https://utcc.utoronto.ca/~cks/space/blog/python/PythonPylspNotes">also</a>),
the LSP environment will make no changes and report 'No formatting
changes provided'. My problem only happens in Python 2 buffers, and
that's because in Python 2 buffers I wasn't using pylsp (which only
officially supports Python 3 code) but instead the older and now
unsupported <a href="https://emacs-lsp.github.io/lsp-mode/page/lsp-pyls/">pyls</a>.
Either pyls has always behaved differently than pylsp when the LSP
server asks it to do formatting stuff, or at some point the LSP
protocol and expectations around formatting actions changed and
pyls (which has been unmaintained since 2020) didn't change to keep
up.</p>

<p>My immediate fix was to set <code>lsp-enable-indentation</code> to nil in my
GNU Emacs lsp-mode hook for python-mode. As a longer term thing I'm
going to experiment with using pylsp even for Python 2 code, to see
how it goes. Otherwise I may wind up disabling LSP for Python 2
code and buffers, although that's somewhat tricky since there's no
explicit separate settings for Python 2 versus Python 3. Another
immediate fix is that in the future I may be editing this particular
code base more in vi(m) or perhaps <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/SamWhyILikeIt">sam</a>
than GNU Emacs.</p>

<p>(My Python 2 code is mostly or entirely written using tabs for
indentation, so the presence of leading tabs is a reliable way
of detecting 'Python 2' code.)</p>

<p>PS: This particular Python 2 program is <a href="https://utcc.utoronto.ca/~cks/space/dwiki/DWiki">DWiki</a>, the wiki engine
underlying <a href="https://utcc.utoronto.ca/~cks/space/blog/">Wandering Thoughts</a>, so <a href="https://utcc.utoronto.ca/~cks/space/blog/python/DWikiPython3Someday">while it will move
to Python 3 someday</a> and <a href="https://utcc.utoronto.ca/~cks/space/blog/python/DWikiAndPython3">I once got a hacked
version vaguely running that way</a>, it's not going
to happen any time soon for multiple reasons.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/python/Python2EmacsLSPProblems?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/python/Python2EmacsLSPProblems

---

*ID: 4ca78a5c2e42250d*
*抓取时间: 2026-03-12T13:49:26.048858*
