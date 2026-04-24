# Writing code is cheap now

> 来源: simonwillison.net  
> 发布时间: 2026-02-23T16:20:42+00:00  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><em><a href="https://simonwillison.net/guides/agentic-engineering-patterns/">Agentic Engineering Patterns</a> &gt;</em></p>
    <p>The biggest challenge in adopting agentic engineering practices is getting comfortable with the consequences of the fact that <em>writing code is cheap now</em>.</p>
<p>Code has always been expensive. Producing a few hundred lines of clean, tested code takes most software developers a full day or more. Many of our engineering habits, at both the macro and micro level, are built around this core constraint.</p>
<p>At the macro level we spend a great deal of time designing, estimating and planning out projects, to ensure that our expensive coding time is spent as efficiently as possible. Product feature ideas are evaluated in terms of how much value they can provide <em>in exchange for that time</em> - a feature needs to earn its development costs many times over to be worthwhile!</p>
<p>At the micro level we make hundreds of decisions a day predicated on available time and anticipated tradeoffs. Should I refactor that function to be slightly more elegant if it adds an extra hour of coding time? How about writing documentation? Is it worth adding a test for this edge case? Can I justify building a debug interface for this?</p>
<p>Coding agents dramatically drop the cost of typing code into the computer, which disrupts <em>so many</em> of our existing personal and organizational intuitions about which trade-offs make sense.</p>
<p>The ability to run parallel agents makes this even harder to evaluate, since one human engineer can now be implementing, refactoring, testing and documenting code in multiple places at the same time.</p>
<h2 id="good-code">Good code still has a cost</h2>

<p>Delivering new code has dropped in price to almost free... but delivering <em>good</em> code remains significantly more expensive than that.</p>
<p>Here's what I mean by "good code":</p>
<ul>
<li>The code works. It does what it's meant to do, without bugs.</li>
<li>We <em>know the code works</em>. We've taken steps to confirm to ourselves and to others that the code is fit for purpose.</li>
<li>It solves the right problem.</li>
<li>It handles error cases gracefully and predictably: it doesn't just consider the happy path. Errors should provide enough information to help future maintainers understand what went wrong.</li>
<li>It’s simple and minimal - it does only what’s needed, in a way that both humans and machines can understand now and maintain in the future.</li>
<li>It's protected by tests. The tests show that it works now and act as a regression suite to avoid it quietly breaking in the future.</li>
<li>It's documented at an appropriate level, and that documentation reflects the current state of the system - if the code changes an existing behavior the existing documentation needs to be updated to match.</li>
<li>The design affords future changes. It's important to maintain <a href="https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it">YAGNI</a> - code with added complexity to anticipate future changes that may never come is often bad code - but it's also important not to write code that makes future changes much harder than they should be.</li>
<li>All of the other relevant "ilities" - accessibility, testability, reliability, security, maintainability, observability, scalability, usability - the non-functional quality measures that are appropriate for the particular class of software being developed.</li>
</ul>
<p>Coding agent tools can help with most of this, but there is still a substantial burden on the developer driving those tools to ensure that the produced code is good code for the subset of good that's needed for the current project.</p>
<h2 id="we-need-to-build-new-habits">We need to build new habits</h2>
<p>The challenge is to develop new personal and organizational habits that respond to the affordances and opportunities of agentic engineering. </p>
<p>These best practices are still being figured out across our industry. I'm still figuring them out myself.</p>
<p>For now I think the best we can do is to second guess ourselves: any time our instinct says "don't build that, it's not worth the time" fire off a prompt anyway, in an asynchronous agent session where the worst that can happen is you check ten minutes later and find that it wasn't worth the tokens.</p>
    
        <p>Tags: <a href="https://simonwillison.net/tags/coding-agents">coding-agents</a>, <a href="https://simonwillison.net/tags/ai-assisted-programming">ai-assisted-programming</a>, <a href="https://simonwillison.net/tags/generative-ai">generative-ai</a>, <a href="https://simonwillison.net/tags/ai">ai</a>, <a href="https://simonwillison.net/tags/llms">llms</a>, <a href="https://simonwillison.net/tags/agentic-engineering">agentic-engineering</a></p>

## 链接

https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/#atom-everything

---

*ID: 96cdeb32cb892e67*
*抓取时间: 2026-03-05T10:01:51.143522*
