# String formatting with named format arguments and format flexibility

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-14T03:43:38Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Suppose, not entirely hypothetically, that you have a tool that
prints out records (one per line) and each record has a bunch of
information associated with it, which you print out in columns.
You'd like to provide a way for people to control which columns of
information are printed for the records. If there's only a few
options, maybe you can do this with a few different format strings
using the traditional <code>"%s %s %s"</code> approach of positional formatting
(because you're old fashioned and haven't really updated to the
modern world of <a href="https://docs.python.org/3/library/string.html">string formatting</a>), but this doesn't
really scale up very well; you rapidly get into a massive explosion
of options and formatting.</p>

<p>As I was contemplating exactly this issue for a tool of mine, it
belatedly occurred to me that the solution I wanted was named format
arguments, instead of positional ones. Named format arguments have
two great advantages here. First, you can shuffle the order that
they occur in within the format string without having to change the
arguments. Second, you don't have to use all of them; Python is
perfectly happy if you supply extra named arguments to your string
formatting that aren't used.</p>

<p>This means that you can simply build up a big dictionary of all of
your available information for a given record (perhaps even in
multiple formats, for example if you have an option to print numbers
precisely or abbreviate them to K, M, G, and so on), and then either
pick a formatting string or assemble it from pieces based on what
columns you want to print (and how). Then you can just do the actual
formatting with:</p>

<blockquote><pre style="white-space: pre-wrap;">
outstr = fmtstr.format_map(datadict)
</pre>
</blockquote>

<p>It doesn't matter that you supplied (way) more information in your
datadict than your assembled or chosen format string uses, or what
order your format string puts things. Everything just works.</p>

<p>(You can use '<code>fmtstr % datadict</code>' instead if you want to. I'm
not sure which I'll use, but a bit of me feels that I should switch
to modern Python string formatting instead of sticking with the old
printf style of '%', even if it allows named arguments too.)</p>

<p>This feels like something that I should have realized long ago,
back when named ('keyword') format arguments were added to Python,
but for some reason it never clicked until now. Several of my
programs are probably going to start providing a lot more options
for formatting their output.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/python/NamedStringFormattingFlexibility?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/python/NamedStringFormattingFlexibility

---

*ID: 94d354828fb6ebe8*
*抓取时间: 2026-03-12T13:49:26.048993*
