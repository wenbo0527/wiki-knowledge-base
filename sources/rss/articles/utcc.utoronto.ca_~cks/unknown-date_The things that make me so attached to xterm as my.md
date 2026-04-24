# The things that make me so attached to xterm as my terminal program

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-02T04:27:43Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I've said before in various contexts (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ViIsAProductOfItsTime">eg</a>)
that I'm very attached to the venerable <code>xterm</code> as my terminal
(emulator) program, and I'm not looking forward to the day that I
may have to migrate away from it due to Wayland (although I probably
can keep running it under XWayland, now that I think about it). But
I've never tried to write down a list of the things that make me
so attached to it over other alternatives like urxvt, much less
more standard ones like gnome-terminal. Today I'm going to try to
do that, although my list is probably going to be incomplete.</p>

<ul><li><a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/XtermZiconbeep">Xterm's ziconbeep feature</a>, which
I use heavily. <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/UrxvtNotes">Urxvt can have an equivalent</a> but
I don't know if other terminal programs do.<p>
</li>
<li>I routinely use <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/XTermLargeSelections">xterm's very convenient way of making large
selections</a>, which is supported in urxvt
but not in gnome-terminal (and it can't be since gnome-terminal
uses mouse button 3 for its own purposes).<p>
</li>
<li>The ability to turn off all terminal colours, because <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/TerminalColoursNotTheSame">they
often don't work in my preferred terminal colours</a>. Other terminal programs have somewhat
different and sometimes less annoying colours, but it's still far
to easy for programs to display things in unreadable colours.<p>
Yes, I can set my shell environment and many programs to not use
colours, but I can't set all of them; some modern programs simply
always use colours on terminals. Xterm can be set to completely
ignore them.<p>
</li>
<li>I'm very used to xterm's specific behavior when it comes to what
is a 'word' for double-click selection. You can read the full
details in <a href="https://invisible-island.net/xterm/manpage/xterm.html#h2-CHARACTER-CLASSES">the xterm manual page's section on character classes</a>.
I'm not sure if it's possible to fully emulate this behavior in other
terminal programs; <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/UrxvtNotes">I once made an incomplete attempt in urxvt</a>, while gnome-terminal is quite different and has little
or no options for customizing that behavior (in the Gnome way).
Generally the modern double click selection behavior is too broad for
me.<p>
(For instance, I'm extremely attached to double-click selecting
only individual directories in full paths, rather than the entire
thing. I can always swipe to select an entire path, but if I
can't pick out individual path elements with a double click my
only choice is character by character selection, which is a giant
pain.)<p>
Based on a quick experiment, I think I can make KDE's konsole
behave more or less the way I want by clearing out its entire set
of "Word characters" in profiles. I think this isn't quite how
xterm behaves but it's probably close enough for my reflexes.<p>
</li>
<li>Xterm doesn't treat text specially because of its contents, for
example by underlining URLs or worse, hijacking clicks on them to
do things. I already have well evolved systems for dealing with
things like URLs and I don't want my terminal emulator to provide
any 'help'. I believe that KDE's konsole can turn this off, but
gnome-terminal doesn't seem to have any option for it.<p>
</li>
<li>Many of xterm's behaviors can be controlled from command line
switches. Some other terminal emulators (like gnome-terminal)
force you to bundle these behaviors together as 'profiles' and
only let you select a profile. Similarly, a lot of xterm's behavior
can be temporarily changed on the fly through its context menus,
without having to change the profile's settings (and then change
them back).<p>
</li>
<li>Every xterm window is a completely separate program that starts
from scratch, and xterm is happy to run on remote servers without
complications; this isn't something I can say for all other
competitors. Starting from scratch also means things like not
deciding to place yourself where your last window was, which is
konsole's behavior (and infuriates me).</li>
</ul>

<p>Of these, the hardest two to duplicate are probably xterm's double
click selection behavior of what is a word and xterm's large selection
behavior. The latter is hard because it requires the terminal program
to not use mouse button 3 for a popup menu.</p>

<p>I use some other xterm features, like <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/XtermKeybinding">key binding</a>,
including <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/XTermDuplicatingWindows">duplicating windows</a>, but I
could live without them, especially if the alternate terminal program
directly supports <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/XtermModernCutAndPaste">modern cut and paste</a>
in addition to xterm's traditional style. And I'm accustomed to <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/OddControlCharacters">a
few of xterm's special control characters</a>,
especially Ctrl-space, but I think this may be pretty universally
supported by now (Ctrl-space is in gnome-terminal).</p>

<p>There are probably things that other terminal programs like konsole,
gnome-terminal and so on do that I don't want them to (and that
xterm doesn't). But since I don't use anything other than xterm
(and a bit of gnome-terminal and once in a while a bit of urxvt),
I don't know what those undesired features are. Experimenting with
konsole for this entry taught me some things I definitely don't
want, such as it automatically placing itself where it was before
(including placing a new konsole window on top of one of the existing
ones, if you have multiple ones).</p>

<p>(This elaborates on <a href="https://lobste.rs/s/2omooc/original_vi_is_product_its_time_its_time#c_cwnwgp">a comment I made elsewhere</a>.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/XTermWhyAttached?showcomments#comments">5 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/XTermWhyAttached

---

*ID: 8e9d1957a9b5b68b*
*抓取时间: 2026-03-12T13:49:26.048147*
