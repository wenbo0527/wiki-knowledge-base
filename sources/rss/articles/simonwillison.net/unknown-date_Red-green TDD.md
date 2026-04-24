# Red/green TDD

> 来源: simonwillison.net  
> 发布时间: 2026-02-23T07:12:28+00:00  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><em><a href="https://simonwillison.net/guides/agentic-engineering-patterns/">Agentic Engineering Patterns</a> &gt;</em></p>
    <p>"<strong>Use red/green TDD</strong>" is a pleasingly succinct way to get better results out of a coding agent.</p>
<p>TDD stands for Test Driven Development. It's a programming style where you ensure every piece of code you write is accompanied by automated tests that demonstrate the code works.</p>
<p>The most disciplined form of TDD is test-first development. You write the automated tests first, confirm that they fail, then iterate on the implementation until the tests pass.</p>
<p>This turns out to be a <em>fantastic</em> fit for coding agents. A significant risk with coding agents is that they might write code that doesn't work, or build code that is unnecessary and never gets used, or both.</p>
<p>Test-first development helps protect against both of these common mistakes, and also ensures a robust automated test suite that protects against future regressions. As projects grow the chance that a new change might break an existing feature grows with them. A comprehensive test suite is by far the most effective way to keep those features working.</p>
<p>It's important to confirm that the tests fail before implementing the code to make them pass. If you skip that step you risk building a test that passes already, hence failing to exercise and confirm your new implementation.</p>
<p>That's what "red/green" means: the red phase watches the tests fail, then the green phase confirms that they now pass.</p>
<p>Every good model understands "red/green TDD" as a shorthand for the much longer "use test driven development, write the tests first, confirm that the tests fail before you implement the change that gets them to pass".</p>
<p>Example prompt:
<div><textarea>Build a Python function to extract headers from a markdown string. Use red/green TDD.</textarea></div></p>
    
        <p>Tags: <a href="https://simonwillison.net/tags/testing">testing</a>, <a href="https://simonwillison.net/tags/tdd">tdd</a>, <a href="https://simonwillison.net/tags/coding-agents">coding-agents</a>, <a href="https://simonwillison.net/tags/ai-assisted-programming">ai-assisted-programming</a>, <a href="https://simonwillison.net/tags/agentic-engineering">agentic-engineering</a></p>

## 链接

https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/#atom-everything

---

*ID: ce24184bf4d5ec40*
*抓取时间: 2026-03-05T10:01:51.143535*
