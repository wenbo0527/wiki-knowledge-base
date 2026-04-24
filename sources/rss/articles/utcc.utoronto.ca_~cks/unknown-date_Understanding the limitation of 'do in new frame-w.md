# Understanding the limitation of 'do in new frame/window' in GNU Emacs

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-17T03:09:55Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>GNU Emacs has a core model for how it operates, and some of its
weird seeming limitations are easier to understand if you internalize
that model. One of them is what you have to do in GNU Emacs to get
the perfectly sensible operation of 'do &lt;X> in a new frame or
window'. For instance, one of the things I periodically want to do
in <a href="https://www.gnu.org/software/emacs/manual/html_mono/mh-e.html">MH-E</a>
is 'open a folder in a new frame', so that I can go through it while
keeping my main MH-E environment on my inbox to process incoming
email.</p>

<p>If you dig through existing GNU Emacs ELisp functions, you won't
find a 'make-frame-do-operation' function, which is a bit frustrating.
GNU Emacs has <a href="https://www.gnu.org/software/emacs/manual/html_node/emacs/Creating-Frames.html">a whole collection of operations for making a new
frame</a>,
and I can run <code>mh-visit-folder</code> in the context of this frame, so
it seems like there should be a simple function I could invoke to
do this and create my own 'C-x 5 v' binding for 'visit MH-E folder
in other frame'.</p>

<p>The clue to what's going on is in the description of C-x 5 5 from
the <a href="https://www.gnu.org/software/emacs/manual/html_node/emacs/Creating-Frames.html">Creating Frames</a>
page of the manual, with the emphasis mine:</p>

<blockquote><p>A more general prefix command that affects the buffer displayed
by a subsequent command invoked after this prefix command
(<code>other-frame-prefix</code>). It requests <strong>the buffer to be displayed by a
subsequent command</strong> to be shown in another frame.</p>
</blockquote>

<p>GNU Emacs frames (and windows) don't run commands and show their
output, they display (GNU Emacs) buffers. In order to create a
frame, you must have some buffer to display on that frame, and GNU
Emacs must know what it is. GNU Emacs has some relatively complex
and magical code to implement the 'C-x 5 5' and 'C-x 4 4' prefix
commands, but it's all still fundamentally starting from having
some buffer to display, not from running a command. The code basically
assumes you're running a command that will at some point try to
display a buffer, and it hooks into that 'please display this buffer'
operation to make the new frame or window and then display the
buffer in it.</p>

<p>(Buffers can be created to show files, but they can also be created
for a lot of other purposes, including non-file buffers created by
ELisp commands that want to present text to you. All of <a href="https://www.gnu.org/software/emacs/manual/html_mono/mh-e.html">MH-E</a>'s
buffers are non-file ones, as are things like <a href="https://magit.vc/">Magit</a>'s
information displays.)</p>

<p>The corollary of this is that the most straightforward way to write
our own ELisp code to run a command in a new frame is to start out
by <a href="https://www.gnu.org/software/emacs/manual/html_node/elisp/Switching-Buffers.html#index-switch_002dto_002dbuffer_002dother_002dframe">switching to some buffer in another frame</a>,
such as '<code>*scratch*</code>', and then run our command. In an extremely
minimal form, this looks like:</p>

<blockquote><pre style="white-space: pre-wrap;">
(defun mh-visit-folder-other-frame (folder &amp;optional argp)
  "...."
  (interactive [...])
  (switch-to-buffer-other-frame "*scratch*")
  (mh-visit-folder folder argp))
</pre>
</blockquote>

<p>If you know that your command displays a specific buffer, ideally
you'll check to see if that buffer exists already and switch to it
instead of to some scratch buffer that you're only using because
you need to tell Emacs to display some buffer (any buffer) in the
new frame.</p>

<p>(In normal GNU Emacs environments you can be pretty confident that
there's a <code>*scratch*</code> buffer sitting around. GNU Emacs normally
creates it on startup and most people don't delete it. And if you're
writing your own code, you can definitely not delete it yourself.)</p>

<p>Now that I've written this entry, maybe I'll remember 'C-x 5 5' and
also stop feeling vaguely irritated every time I do the equivalent
by hand ('C-x 5 b', pick <code>*scratch*</code>, and then run my command in
the newly created frame).</p>

<p>PS: It's probably possible to write a general ELisp function to run
another function and make any buffers it wants to show come up on
another frame, using the machinery that 'C-x 5 5' does. I will leave
writing this function as an exercise for my readers (although maybe
it already exists somewhere).</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/EmacsNewWhateverLimitation?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/EmacsNewWhateverLimitation

---

*ID: d7340d2a04821fcd*
*抓取时间: 2026-03-12T13:49:26.048295*
