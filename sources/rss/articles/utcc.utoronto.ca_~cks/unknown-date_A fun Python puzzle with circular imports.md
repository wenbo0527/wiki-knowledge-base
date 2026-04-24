# A fun Python puzzle with circular imports

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-10T04:12:25Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p><a href="https://mastodon.social/@bmispelon">Baptiste Mispelon</a> asked <a href="https://mastodon.social/@bmispelon/116041593220352595">an
interesting Python quiz</a>
(<a href="https://mastodon.social/@treyhunner/116041923791357383">via</a>,
via <a href="https://mastodon.social/@glyph">@glyph</a>):</p>

<blockquote><p>Can someone explain this #Python import behavior? <br />
I'm in a directory with 3 files:</p>

<p>a.py contains `A = 1; from b import *` <br />
b.py contains `from a import *; A += 1` <br />
c.py contains `from a import A; print(A)` <br />
</p>

<p>Can you guess and explain what happens when you run `python c.py`?</p>
</blockquote>

<p>I encourage you to guess which of the options in <a href="https://mastodon.social/@bmispelon/116041593220352595">the original
post</a> is
the actual behavior before you read the rest of this entry.</p>

<p>There are two things going on here. The first thing is <a href="https://utcc.utoronto.ca/~cks/space/blog/python/FromImportBindingIssue">what
actually happens when you do '<code>from module import ...</code>'</a>. The short version is that this copies
<a href="https://utcc.utoronto.ca/~cks/space/blog/python/WhatVariablesMean">the current bindings of names</a> from one module
to another. So when module b does '<code>from a import *</code>', it copies
the binding of a.A to b.A and then the <code>+=</code> changes that binding.
The behavior would be the same if we used '<code>from a import A</code>' and
'<code>from b import A</code>' in the code, and if we did we could describe
what each did in isolation as starting with '<code>A = 1</code>' (in a), then
'<code>A = a.A; A += 2</code>' (in b), and then '<code>A = b.A</code>' (back in a)
successively (and then in c, '<code>A = a.A</code>').</p>

<p>The second thing going on is that you can import incomplete modules
(this is true in both Python 2 and Python 3, which return the same
results here). To see how this works we need to combine <a href="https://docs.python.org/3/reference/simple_stmts.html#the-import-statement">the
description of '<code>import</code>' and '<code>from</code>'</a>
and <a href="https://docs.python.org/3/reference/import.html#loading">the approximation of what happens during loading a module</a>, although
neither is completely precise. To summarize, when a module is being
loaded, the first thing that happens is that a module namespace is
created and is added to <a href="https://docs.python.org/3/library/sys.html#sys.modules"><code>sys.modules</code></a>; then the
code of the module is executed in that namespace. When Python
encounters a '<code>from</code>', if there is an entry for the module in
<code>sys.modules</code>, Python immediately imports things from it; it
implicitly assumes that the module is already fully loaded.</p>

<p>At first I was surprised by this behavior, but the more I think
about it the more it seems a reasonable choice. It avoids having
to explicitly detect circular imports and it makes circular imports
work in the simple case (where you do '<code>import b</code>' and then don't
use anything from b until all imports are finished and the program
is running). It has the cost that if you have circular name uses
you get an unhelpful error message about 'cannot import name' (or
'NameError: name ... is not defined' if you use '<code>from module
import *</code>'):</p>

<blockquote><pre style="white-space: pre-wrap;">
$ cat a.py
from b import B; A = 10 + B
$ cat b.py
from a import A; B = 20 + A
$ cat c.py
from a import A; print(A)
$ python c.py
[...]
ImportError: cannot import name 'A' from 'a' [...]
</pre>
</blockquote>

<p>(Python 3.13 does print a nice stack trace the points to the whole set
of 'from ...' statements.)</p>

<p>Given all of this, here is what I believe is the sequence of execution
in <a href="https://mastodon.social/@bmispelon/116041593220352595">Baptiste Mispelon's example</a>:</p>

<ol><li>c.py does '<code>from a import A</code>', which initiates a load of the '<code>a</code>'
module.</li>
<li>an '<code>a</code>' module is created and added to <code>sys.modules</code></li>
<li>that module begins executing the code from a.py, which creates an
'<code>a.A</code>' name (bound to 1) and then does '<code>from b import *</code>'.</li>
<li>a '<code>b</code>' module is created and added to <code>sys.modules</code>.</li>
<li>that module begins executing the code from b.py. This code starts
by doing '<code>from a import *</code>', which finds that
'<code>sys.modules["a"]</code>' exists and copies the a.A name binding,
creating <code>b.A</code> (bound to 1).</li>
<li>b.py does '<code>A += 1</code>', which mutates the <code>b.A</code> binding (but not the
separate <code>a.A</code> binding) to be '2'.</li>
<li>b.py finishes its code, returning control to the code from a.py,
which is still part way through '<code>from b import *</code>'. This import
copies all names (and their bindings) from <code>sys.modules["b"]</code> into
the 'a' module, which means the <code>b.A</code> binding (to 2) overwrites
the old <code>a.A</code> binding (to 1).</li>
<li>a.py finishes and returns control to c.py, where '<code>from a import A</code>' 
can now complete by copying the <code>a.A</code> name and its binding into 'c',
make it the equivalent of 'import a; A = a.A; del a'.</li>
<li>c.py prints the value of this, which is 2.</li>
</ol>

<p>At the end of things, there is all of c.A, a.A, and b.A, and they
are bindings to the same object. The order of binding was 'b.A =
2; a.A = b.A; c.A = a.A'.</p>

<p>(There's also <a href="https://mastodon.social/@bmispelon/116041651512905642">a bonus question</a>, where <a href="https://mastodon.social/@cks/116043764923637178">I
have untested answers</a>.)</p>

<h3>Sidebar: A related circular import puzzle and the answer</h3>

<p>Let's take a slightly different version of my error message example
above, that simplifies things by leaving out c.py:</p>

<blockquote><pre style="white-space: pre-wrap;">
$ cat a.py
from b import B; A = 10 + B
$ cat b.py
from a import A; B = 20 + A
$ python a.py
[...]
ImportError: cannot import name 'B' from 'b' [...]
</pre>
</blockquote>

<p>When I first did this I was quite puzzled until the penny dropped.
What's happening is that running '<code>python a.py</code>' isn't creating
an 'a' module but instead a <code>__main__</code> module, so b.py doesn't
find a <code>sys.modules["a"]</code> when it starts and instead creates one
and starts loading it. That second version of a.py, now in an "a"
module, is what tries to refer to b.B and finds it not there (yet).</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/python/PythonCircularImportPuzzle

---

*ID: ca674375225ef9ac*
*抓取时间: 2026-03-12T13:49:26.048371*
