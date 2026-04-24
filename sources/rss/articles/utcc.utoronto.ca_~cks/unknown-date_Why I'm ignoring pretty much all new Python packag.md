# Why I'm ignoring pretty much all new Python packaging tools

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-30T03:59:45Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>One of the things going on right now is that Python is doing a
Python developer survey. On the Fediverse, I follow a number of
people who do Python stuff, and they've been posting about various
aspects of the survey, including a section on what tools people use
for what. This gave me an interesting although very brief look into
a world that I'm deliberately ignoring, and I'm doing that because
I feel my needs are very simple and are well met by basic, essentially
universal tools that I already know and have.</p>

<p>Although I do some small amount of Python programming, I'm not a
Python developer; you could call me a consumer of Python things,
both programs and packages. The thing I do most is use programs
written in Python that aren't single-file, dependency free things,
almost always for my own personal use (for example, <a href="https://utcc.utoronto.ca/~cks/space/blog/web/ToolsToSeeVolumeSources"><code>asncounter</code></a> and <a href="https://github.com/python-lsp/python-lsp-server">the Python language server</a>). The tool I use
for almost all of these is <a href="https://utcc.utoronto.ca/~cks/space/blog/python/PipxEarlyNotes">pipx</a>, which I feel
handles pretty much everything I could ask for and comes pre-packaged
in most Linuxes. Admittedly <a href="https://utcc.utoronto.ca/~cks/space/blog/python/MyVenvActivationScript">I've written some tools to make my
life nicer</a>.</p>

<p>(One important think pipx does is install each program separately.
This allows me to remove one clearly and also <a href="https://utcc.utoronto.ca/~cks/space/blog/python/PyPyAndPipx">to use PyPy or
CPython as I prefer</a> on a program by program basis.)</p>

<p>For programs that <a href="https://support.cs.toronto.edu/">we</a> want to
use as part of our operations (<a href="https://rseichter.github.io/fangfrisch/">for example</a>), the modern, convenient
approach is to make <a href="https://docs.python.org/3/library/venv.html">a venv</a>
and then install the program into it with pip. Pip is functionally
universal and the resulting venvs effectively function as <a href="https://utcc.utoronto.ca/~cks/space/blog/python/VenvsCanUsuallyBeMoved">self
contained artifacts that can be moved or put anywhere</a> (provided that we stick to the same Ubuntu
LTS version). So far we haven't tried to upgrade these in place;
<a href="https://utcc.utoronto.ca/~cks/space/blog/python/VenvsReplaceNotUpdate">if a new version of the program comes out, we build a new venv
and swap which one is used</a>.</p>

<p>(It's possible that package dependencies of the program could be
updated even if it hasn't released a new version, but we treat these
built venvs as if they were compiled binaries; once produced, they're
not modified.)</p>

<p>Finally, <a href="https://utcc.utoronto.ca/~cks/space/blog/python/DjangoORMDesignPuzzleII">our Django based web application</a>
now uses a Django setup where Django is installed into a venv and
then the production tree of our application <a href="https://utcc.utoronto.ca/~cks/space/blog/python/VenvsVsSourceTrees">lives outside that
venv</a> (previously we didn't use venvs at all
but <a href="https://utcc.utoronto.ca/~cks/space/blog/python/Pythonpath310Vs312Change">that stopped working</a>). Our application
isn't versioned or built into a Python artifact; it's a VCS tree
and is managed through VCS operations. The Django venv is created
separately, and I use pip for that because again pip is universal
and familiar. This is a crude and brute force approach but it's
also ensured that I haven't had to care about the Python packaging
ecosystem (and how to make Python packages) for <a href="https://utcc.utoronto.ca/~cks/space/blog/python/DjangoORMDesignPuzzleII">the past fifteen
years</a>. At the moment we use only standard
Django without any third party packages that we'd also have to add
to the venv and manage, and I expect that we're going to stay that
way. A third party package would have to be very attractive (or
become extremely necessary) in order for us to take it on and
complicate life.</p>

<p>I'm broadly aware that there are a bunch of new Python package
management and handling tools that go well beyond pip and pipx in
both performance and features. My feeling so far is that I don't
need anything more than I have and I don't do the sort of regular
Python development where the extra features the newer tools have
would make a meaningful difference.
And to be honest, I'm wary of some or all of these turning out to
be a flavour of the month. My mostly outside impression is that
Python packaging and package management has had a great deal of
churn over the years, and from seeing the Go ecosystem go through
similar things from closer up I know that being stuck with a now
abandoned tool is not particularly fun. Pip and pipx aren't the
modern hot thing but they're also very unlikely to go away.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/python/PythonPackageToolsMyIgnoring?showcomments#comments">4 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/python/PythonPackageToolsMyIgnoring

---

*ID: 105423228bce2eb8*
*抓取时间: 2026-03-12T13:49:26.048494*
