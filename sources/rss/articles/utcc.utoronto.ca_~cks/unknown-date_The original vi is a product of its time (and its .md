# The original vi is a product of its time (and its time has passed)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-08T03:50:02Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Recently I saw another discussion of how some people are very
attached to the original, classical vi and its behaviors (<a href="https://lobste.rs/s/kbr1er/bob_beck_openbsd_on_why_vi_should_stay_vi">cf</a>).
I'm quite sympathetic to this view, since I too am very attached
to the idiosyncratic behavior of various programs I've gotten used
to (such as xterm's very specific behavior in various areas), but
at the same time <a href="https://mastodon.social/@cks/116030650374231189">I had a hot take over on the Fediverse</a>:</p>

<blockquote><p>Hot take: basic vim (without plugins) is mostly what vi should have
been in the first place, and much of the differences between vi
and vim are improvements. Multi-level undo and redo in an obvious
way? Windows for easier multi-file, cross-file operations? Yes please,
sign me up.</p>

<p>Basic vi is a product of its time, namely the early 1980s, and the
rather limited Unix machines of the time (yes a VAX 11/780 was
limited).</p>

<p>(The touches of vim superintelligence, not so much, and I turn them
off.)</p>
</blockquote>

<p>For me, vim is a combination of genuine improvements in vi's core
editing behavior (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/VimFeaturesThatHookedMe">cf</a>), frustrating (to
me) bits of trying too hard to be smart (which I mostly disable
when I run across them), and an extension mechanism I ignore but
people use to make vim into a superintelligent editor with things
like <a href="https://en.wikipedia.org/wiki/Language_Server_Protocol">LSP</a>
integrations.</p>

<p>Some of the improvements and additions to vi's core editing may be
things that Bill Joy either didn't think of or didn't think were
important enough. However, I feel strongly that some or even many
of omitted features and differences are a product of the limited
environments vi had to operate in. The poster child for this is
vi's support of only a single level of undo, which drastically
constrains the potential memory requirements (and implementation
complexity) of undo, especially since a single editing operation
in vi can make sweeping changes across a large file (consider a
whole-file ':...s/../../' substitution, for example).</p>

<p>(The lack of split windows might be one part memory limitations and
one part that splitting an 80 by 24 serial terminal screen is much
less useful than splitting, say, an 80 by 50 terminal window.)</p>

<p>Vim isn't the only improved version of vi that has added features
like multi-level undo and split windows so you can see multiple
files at once (or several parts of the same file); there's also at
least nvi. I'm used to vim so I'm biased, but I happen to think
that a lot of vim's choices for things like multi-level undo are
good ones, ones that will be relatively obvious and natural to new
people and avoid various sorts of errors and accidents. But other
people like nvi and I'm not going to say they're wrong.</p>

<p>I do feel strongly that giving stock vi to anyone who doesn't
specifically ask for it is doing them a disservice, and this includes
installing stock vi as 'vi' on new Unix installs. At this point,
what new people are introduced to and what is the default on systems
should be something better and less limited than stock vi. Time has
moved on and Unix systems should move on with it.</p>

<p>(I have similar feelings about the default shell for new accounts
for people, as opposed to system accounts. Giving people bare Bourne
shell is not doing them any favours and is not likely to make a
good first impression. I don't care what you give them but it should
at least support cursor editing, file completion, and history, and
those should be on by default.)</p>

<p>PS: I have complicated feelings about Unixes that install stock vi
as 'vi' and something else under its full name, because on the one
hand that sounds okay but on the other hand there is so much stuff
out there that says to use 'vi' because that's the one name that's
universal. And if you then make 'vi' the name of the default (visual)
editor, well, it certainly feels like you're steering new people
into it and doing them a disservice.</p>

<p>(I don't expect to change the mind of any Unix that is still shipping
stock vi as 'vi'. They've made their cultural decisions a long time
ago and they're likely happy with the results.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ViIsAProductOfItsTime?showcomments#comments">13 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/ViIsAProductOfItsTime

---

*ID: d0688835cc39e9e8*
*抓取时间: 2026-03-12T13:49:26.048393*
