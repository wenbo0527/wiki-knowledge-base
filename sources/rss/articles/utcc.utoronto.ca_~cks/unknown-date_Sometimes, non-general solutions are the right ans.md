# Sometimes, non-general solutions are the right answer

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-05T03:33:13Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>I have a Python program that calculates and prints various pieces
of Linux memory information on a per-cgroup basis.  In the beginning,
its life was simple; cgroups had a total memory use that was split
between 'user' and '(filesystem) cache', so the program only needed
to display either one field or a primary field plus a secondary
field.  Then I discovered that <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/CgroupsMemoryUsageAccountingII">there was additional important
(ie, large) kernel memory use in cgroups</a> and added the ability to
report it as an additional option for the secondary field. However,
this wasn't really ideal, because now I had a three-way split and
I might want to see all three things at once.</p>

<p>A while back I wrote up <a href="https://utcc.utoronto.ca/~cks/space/blog/python/NamedStringFormattingFlexibility">my realization about flexible string
formatting with named arguments</a>.
This sparked all sorts of thoughts about writing a general solution
for my program that could show any number of fields. Recently I
took a stab at implementing this and rapidly ran into problems
figuring out how I wanted to do it. I had multiple things that could
be calculated and presented, I had to print not just the values but
also a header with the right field names, I'd need to think about
how I structured argparse argument groups in light of <a href="https://utcc.utoronto.ca/~cks/space/blog/python/ArgparseAndNestedGroups">argparse
not supporting nested groups</a>, and so on.
At a minimum this wasn't going to be a quick change; I was looking
at significantly rewriting how the program printed its output.</p>

<p>The other day, I had an obvious realization: while it would be nice
to have a fully general solution that could print any number of
additional fields, which would meet my needs now and in the future,
all that I needed right now was an additional three-field version
with the extra fields hard-coded and the whole thing selected through
a new command line argument. And this command line argument could
drop right into the existing <a href="https://docs.python.org/3/library/argparse.html">argparse</a> exclusive group
for choosing the second field, even though this feels inelegant.</p>

<p>(The fields I want to show are added with '-c' and '-k' respectively
in the two field display, so the morally correct way to select both
at once would be '-ck', but currently they're exclusive options,
which is <a href="https://docs.python.org/3/library/argparse.html#mutual-exclusion">enforced by argparse</a>. So
I added a third option, literally '-b' for 'both'.)</p>

<p>Actually implementing this hard-coded version was a bit annoying
for structural reasons, but I put the whole thing together in not
very long; certainly it was much faster than a careful redesign and
rewrite (in an output pattern I haven't used before, no less). It's
not necessarily the right answer for the long term, but it's
definitely the right answer for now (and I'm glad I talked myself
into doing it).</p>

<p>(I'm definitely tempted to go back and restructure the whole output
reporting to be general. But now there's no rush to it; it's not
blocking a feature I want, it's a cleanup.)</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/python/HardcodingCanBeTheRightAnswer

---

*ID: 3b1fcc60c9c78ba2*
*抓取时间: 2026-03-12T13:49:26.048114*
