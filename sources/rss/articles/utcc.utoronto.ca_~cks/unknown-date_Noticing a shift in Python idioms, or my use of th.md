# Noticing a shift in Python idioms, or my use of them

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-11T03:15:11Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>For <a href="https://mastodon.social/@cks/115682316364518333">reasons outside the scope of this entry</a>, I was recently
reminded of some very old entries here where I compared <a href="https://utcc.utoronto.ca/~cks/space/blog/python/PythonDNSQueries">some
Python code</a> with <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/PerlDNSQueries">some Perl code to do the same
thing</a>. One of the things that stood
out to me is that way back then I said:</p>

<blockquote><p>For example, I <em>could</em> have written '<code>print "\n".join(rr.strings)</code>' in
Python, but it doesn't feel right; I would rather write the <code>for</code> loop
explicitly instead.</p>
</blockquote>

<p>At some point between back then and now, my views on this changed
without me noticing. Today I would unhesitatingly print a multi-line
list of text (ie a list of lines) using the .join() version, and
in fact I have; I can easily find little utility programs of mine
that use this idiom (some of them a significant number of years old
by now, so I don't think this is a recent shift).</p>

<p>What I don't know is if this was a shift in my personal views or
if Python in general shifted its view of this idiom. <a href="https://utcc.utoronto.ca/~cks/space/blog/python/DangerousUnicodeConversions">At least
some Python code seems to have been using this a long time ago</a>, so it's entirely possible that I'm
what changed and this was always considered idiomatic Python.</p>

<p>(My suspicion today is that '<code>"\n".join()</code>' probably always was
idiomatic Python, at least in Python 2 and later. It's not quite
as clear as a <code>for</code> loop but it's much more compact.)</p>

<p>There are probably lots of other Python idioms where either I or
Python as a whole has shifted our views on over time. But for various
reasons I rarely get my attention shoved into them the way I did
this time. <a href="https://support.cs.toronto.edu/">We</a> do have a certain
amount of old Python code that we're still using, but because it's
old and reliable, I generally don't have any reason to look at it
and think about the idioms it uses.</p>

<p>All of this makes me wonder what Python idioms I'm currently not
using and thinking about that I'll consider perfectly natural and
automatic in five or ten years. I should probably be using <a href="https://docs.python.org/3/library/dataclasses.html">dataclasses</a>, and then
there's <a href="https://utcc.utoronto.ca/~cks/space/blog/python/TypeHintsDifferentLanguage">copious use of typing annotations</a>
(which would probably feel more natural to me if I used them
frequently).</p>

<p>(I have <a href="https://utcc.utoronto.ca/~cks/space/blog/python/TwelveYearOldPythonProgram">a very old</a> and <a href="https://utcc.utoronto.ca/~cks/space/blog/python/AbandoningOldGoodCode">now abandoned</a> Python program, but I'm not energetic enough
to pick through its code. Also, it would probably be slightly
depressing.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/python/PythonAnIdiomShiftForMe?showcomments#comments">3 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/python/PythonAnIdiomShiftForMe

---

*ID: e0f6681b86d49365*
*抓取时间: 2026-03-12T13:49:26.049024*
