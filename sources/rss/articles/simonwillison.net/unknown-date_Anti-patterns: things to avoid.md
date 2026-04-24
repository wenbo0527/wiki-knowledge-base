# Anti-patterns: things to avoid

> 来源: simonwillison.net  
> 发布时间: 2026-03-04T17:34:42+00:00  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><em><a href="https://simonwillison.net/guides/agentic-engineering-patterns/">Agentic Engineering Patterns</a> &gt;</em></p>
    <p>There are some behaviors that are anti-patterns in our weird new world of agentic engineering.</p>
<h2 id="inflicting-unreviewed-code-on-collaborators">Inflicting unreviewed code on collaborators</h2>
<p>This anti-pattern is common and deeply frustrating.</p>
<p><strong>Don't file pull requests with code you haven't reviewed yourself</strong>.</p>
<p>If you open a PR with hundreds (or thousands) of lines of code that an agent produced for you, and you haven't done the work to ensure that code is functional yourself, you are delegating the actual work to other people.</p>
<p>They could have prompted an agent themselves. What value are you even providing?</p>
<p>If you put code up for review you need to be confident that it's ready for other people to spend their time on it. The initial review pass is your responsibility, not something you should farm out to others.</p>
<p>A good agentic engineering pull request has the following characteristics:</p>
<ul>
<li>The code works, and you are confident that it works. <a href="https://simonwillison.net/2025/Dec/18/code-proven-to-work/">Your job is to deliver code that works</a>.</li>
<li>The change is small enough to be reviewed efficiently without inflicting too much additional cognitive load on the reviewer. Several small PRs beats one big one, and splitting code into separate commits is easy with a coding agent to do the Git finagling for you.</li>
<li>The PR includes additional context to help explain the change. What's the higher level goal that the change serves? Linking to relevant issues or specifications is useful here.</li>
<li>Agents write convincing looking pull request descriptions. You need to review these too! It's rude to expect someone else to read text that you haven't read and validated yourself.</li>
</ul>
<p>Given how easy it is to dump unreviewed code on other people, I recommend including some form of evidence that you've put that extra work in yourself. Notes on how you manually tested it, comments on specific implementation choices or even screenshots and video of the feature working go a <em>long</em> way to demonstrating that a reviewer's time will not be wasted digging into the details.</p>
    
        <p>Tags: <a href="https://simonwillison.net/tags/ai">ai</a>, <a href="https://simonwillison.net/tags/llms">llms</a>, <a href="https://simonwillison.net/tags/ai-ethics">ai-ethics</a>, <a href="https://simonwillison.net/tags/coding-agents">coding-agents</a>, <a href="https://simonwillison.net/tags/ai-assisted-programming">ai-assisted-programming</a>, <a href="https://simonwillison.net/tags/generative-ai">generative-ai</a>, <a href="https://simonwillison.net/tags/agentic-engineering">agentic-engineering</a>, <a href="https://simonwillison.net/tags/code-review">code-review</a></p>

## 链接

https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/#atom-everything

---

*ID: 1904a6343c20860b*
*抓取时间: 2026-03-05T10:01:51.143435*
