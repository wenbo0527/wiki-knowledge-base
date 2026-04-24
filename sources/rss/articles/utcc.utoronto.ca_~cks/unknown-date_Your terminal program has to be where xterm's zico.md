# Your terminal program has to be where xterm's ziconbeep feature is handled

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-07T03:26:47Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I recently wrote about <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/XTermWhyAttached">things that make me so attached to xterm</a>. One of those things is <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/XtermZiconbeep">xterm's ziconbeep
feature</a>, which causes xterm to visibly
and perhaps audibly react when it's iconified or minimized and gets
output. A commentator suggested that this feature should ideally
be done in the window manager, where it could be more general.
Unfortunately we can't do the equivalent of ziconbeep in the window
manager, or at least we can't do all of it.</p>

<p>A window manager can sound an audible alert when a specific type
of window changes its title in a certain way. This would give us
the 'beep' part of ziconbeep in a general way, although we're
treading toward a programmable window manager. But then, Gnome Shell
now does a lot of stuff in JavaScript and its extensions are written
in JS and the whole thing doesn't usually blow up. So we've got
prior art for writing an extension that reacts to window title
changes and does stuff.</p>

<p>What the window manager can't really do is reliably detect when the
window has new output, in order to trigger any beeping and change
the visible window title. As far as I know, neither X nor Wayland
give you particularly good visibility into whether the program is
rendering things, and <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/RepaintModeGUI">in some ways of building GUIs, you're always
drawing things</a>. In theory, a program might
opt to detect that it's been minimized and isn't visible and so not
render any updates at all (although it will be tracking what to
draw for when it's not minimized), but in practice I think this is
unfashionable because it gets in the way of various sorts of live
previews of minimized windows (where you want the window's drawing
surface to reflect its current state).</p>

<p>Another limitation of this as a general window manager feature is
that the window manager doesn't know what changes in the appearance
of a window are semantically meaningful and which ones are happening
because, for example, you just changed some font preference and the
program is picking up on that. Only the program itself knows what's
semantically meaningful enough to signal for people's attention.
A terminal program can have a simple definition but other programs
don't necessarily; your mail client might decide that only certain
sorts of new email should trigger a discreet 'pay attention to me'
marker.</p>

<p>(Even in a terminal program you might want more control over this
than xterm gives you. For example, you might want the terminal
program to not trigger 'zicon' stuff for text output but instead
to do it when the running program finishes and you return to the
shell prompt. This is best done by being able to signal the terminal
program through escape sequences.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/XTermHasToDoZiconbeep

---

*ID: b698d51f0176673d*
*抓取时间: 2026-03-12T13:49:26.048092*
