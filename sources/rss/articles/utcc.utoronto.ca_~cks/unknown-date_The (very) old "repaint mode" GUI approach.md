# The (very) old "repaint mode" GUI approach

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-14T04:34:18Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Today I ran across another article that talked in passing about
"retained mode" versus "immediate mode" GUI toolkits (<a href="https://tritium.legal/blog/desktop">this one</a>, <a href="https://lobste.rs/s/misukt/thanks_for_all_frames_rust_gui">via</a>), and
gave some code samples. As usual when I read about <a href="https://en.wikipedia.org/wiki/Immediate_mode_(computer_graphics)">immediate mode</a>
GUIs and see source code, I had a pause of confusion because the
code didn't feel right. That's because I keep confusing "immediate
mode" as used here with a much older approach, which I will call
<em>repaint mode</em> for lack of a better description.</p>

<p>A modern immediate mode system generally uses double buffering; one
buffer is displayed while the entire window is re-drawn into the
second buffer, and then the two buffers are flipped. I believe that
modern <a href="https://en.wikipedia.org/wiki/Retained_mode">retained mode</a>
systems also tend to use double buffering to avoid <a href="https://en.wikipedia.org/wiki/Screen_tearing">screen tearing</a> and other issues
(and I don't know if they can do partial updates or have to re-render
the entire new buffer). In the old days, the idea of having two
buffers for your program's window was a decided luxury. You might
not even have one buffer and instead be drawing directly onto screen
memory. I'll call this <em>repaint mode</em>, because you directly repainted
some or all of your window any time you needed to change anything
in it.</p>

<p>You could do an immediate mode GUI without double buffering, in
this repaint mode, but it would typically be slow and look bad. So
instead people devoted a significant amount of effort to not
repainting everything but instead identifying what they were changing
and repainting only it, along with any pixels from other elements
of your window that had been '<a href="https://www.x.org/releases/X11R7.5/doc/damageproto/damageproto.txt">damaged</a>' from
prior activity. If you did do a broader repaint, you (or the OS)
typically set clipping regions so that you wouldn't actually touch
pixels that didn't need to be changed.</p>

<p>(The OS's display system typically needed to support clipping regions
in any situation where windows partially overlapped yours, because
it couldn't let you write into their pixels.)</p>

<p>One reason that old display systems worked this way is that <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/XServerBackingStoreOptional">it
required as little memory as possible</a>, which was an important
consideration back in the day (which was more or less the 1980s to
the early to mid 1990s). People could optimize their repaint code
to be efficient and do as little work as possible, but they couldn't
materialize RAM that wasn't there. Today, RAM is relatively plentiful
and we care a lot more about non-tearing, coherent updates.</p>

<p>The typical code style for a repaint mode system was that many UI
elements would normally only issue drawing commands to update or
repaint themselves when they were altered. If you had a slider or
a text field and its value was updated as a result of input, the
code would typically immediately call its repaint function, which
could lead to a relatively tight coupling of input handling to the
rendering code (a coupling that I believe <a href="https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller">Model-view-controller</a> was
designed to break). Your system had to be capable of a full window
repaint, but if you wanted to look good, it wasn't a common operation.
A corollary of this is that your code might spend a significant
amount of effort working out what was the minimal amount of repainting
you needed to do in order to correctly get between two states (and
this code could be quite complicated).</p>

<p>(Some of the time this was hidden from you in widget and toolkit
internals, although they didn't necessarily give you minimal repaints
as you changed widget organization. Also, because a drawing operation
was issued right away didn't mean that it took effect right away.
In X, <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/XRenderingVsWaylandRendering">server side drawing operations</a> might be batched up to be
sent to the X server only when your program was about to wait for
more X events.)</p>

<p>Because I'm used to this repaint mode style, modern immediate mode
code often looks weird to me. There's no event handler connections,
no repaint triggers, and so on, but there is an explicit display
step. Alternately, you aren't merely configuring widgets and then
camping out in the toolkit's main loop, letting it handle events
and repaints for you (the widgets approach is the classical style
for X applications, including PyTk applications such as <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ToolsPyhosts">pyhosts</a>).</p>

<p>These days, I suspect that any modern toolkit that still looks like
a repaint mode system is probably doing double buffering behind the
scenes (unless you deliberately turn that off). Drawing directly
to what's visible right now on screen is decidedly out of fashion
because of issues like <a href="https://en.wikipedia.org/wiki/Screen_tearing">screen tearing</a>, and it's not how modern
display systems like <a href="https://en.wikipedia.org/wiki/Wayland_(protocol)">Wayland</a> want to operate.
I don't know if toolkits implement this with a full repaint on the
new buffer, or if they try to copy the old buffer to the new one
and selectively repaint parts of it, but I suspect that the former
works better with modern graphics hardware.</p>

<p>PS: My view is that even the widget toolkit version of repaint mode
isn't a variation of retained mode because the philosophy was
different. The widget toolkit might batch up operations and defer
redoing layout and repainting things until you either returned to
its event loop or asked it to update the display, but you expected
a more or less direct coupling between your widget operations and
repaints. But you can see it as a continuum that leads to retained
mode when you decouple and abstract things enough.</p>

<p>(Now that I've written this down, perhaps I'll stop having that
weird 'it's wrong somehow' reaction when I see immediate mode GUI
code.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/RepaintModeGUI?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/RepaintModeGUI

---

*ID: 83b657a0c4e88af9*
*抓取时间: 2026-03-12T13:49:26.048327*
