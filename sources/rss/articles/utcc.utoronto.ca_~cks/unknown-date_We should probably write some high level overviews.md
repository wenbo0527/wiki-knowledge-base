# We should probably write some high level overviews of our environment

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-26T03:28:12Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Over on the Fediverse, <a href="https://mastodon.social/@cks/115776155428523132">I shared an old story that's partly about
(system) documentation</a>,
and it sparked a thought, which is that we (I) should write up a
brief high level overview of <a href="https://support.cs.toronto.edu/">our</a>
overall environment. This should probably be one level higher than
<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/DoAnEndOfServiceWriteup">an end of service writeup</a>, which are
focused on a specific service (if we write them at all). The reason
to do this is because <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/WorklogsAssumeContext">our regular documentation assumes a lot of
context</a> and part of that context is what
our overall environment is. <a href="https://support.cs.toronto.edu/">We</a>
know what the environment is because it's the water we work in, but
a new person arriving here could very easily be lost.</p>

<p>What I'm thinking of is something as simple as saying (in a bit
more words) that we store our data on <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/ZFSFileserverSetupIII">a bunch of NFS fileservers</a> and people get access to their home
directories and so on by logging in to <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OurDifferentSysadminEnvironment">various multi-user Unix
servers</a> that all run Ubuntu Linux,
or using various standard services like email (IMAP and webmail),
Samba/CIFS file access, and printing. Our logins and passwords are
distributed around as files from <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/OurPasswordPropagation">a central password server and a
central NFS-mounted filesystem</a>. There's
some more that I would write here (including information about <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/CSLabNetworkLayout">our
networks</a>) and I'd probably put in a bit more
details about some names of the various servers and filesystems,
but not too much more.</p>

<p>(At least not in the front matter. Obviously such an overview could
get increasingly detailed in later sections.)</p>

<p>A bunch of this information is already on <a href="https://support.cs.toronto.edu/">our support website</a> in some form, but I feel the
support website is both too detailed and not complete enough. It's
too detailed because it's there to show people how to do things,
and it's not complete because we deliberately omit some things that
we consider implementation details (such as <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/ZFSFileserverSetupIII">our NFS fileservers</a>). A new person here should certainly
read all the way through the support site sooner or later, but
that's a lot of information to absorb. A high level overview is a
quick start guide that's there to orient people and leave them with
fewer moments of 'wait, you have a what?' or 'what is this even
talking about?' as they're exposed to <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/WhyWorklogsWorkForUs">our usual documentation</a>.</p>

<p>One reason to keep the high level overview at a high level is that
the less specific it is, the less it's going to fall out of date
as things change. Updating such a high level overview is always
going to be low on the priority list, since it's almost never used,
so the less updating it needs the better. Also, I can also write
somewhat more detailed high level overviews of specific aspects or
sub-parts of our environment, if I find myself feeling that the
genuine high level version doesn't say enough. Another reason to
keep it high level is to keep it short, because asking a new person
to read a couple of pages (at most) as high level orientation is a
lot better than throwing them into the deep end with dozens of pages
and thousands of words.</p>

<p>(I'm writing this down partly to motivate myself to do this when
we go back to work in the new year, even though it feels both trivial
and obvious. I have to remind myself that the obvious things about
our environment to me are that way partly because I'm soaking in
it.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/WriteHighLevelSystemOverview?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/WriteHighLevelSystemOverview

---

*ID: 16703158ba6334bf*
*抓取时间: 2026-03-12T13:49:26.048868*
