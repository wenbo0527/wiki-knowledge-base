# Be careful with LLM "Agents"

> 来源: maurycyz.com  
> 发布时间: Mon, 23 Feb 2026 00:00:00 +0000  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<!-- mksite: start of content -->
<p>

I get it: Large Language Models are interesting...
but you should not give "Agentic AI" access to your computer, accounts or wallet. 
</p><p>
To do away with the hype:
"AI Agents" are just LLMs with shell access,
and at it's core an LLM is a weighted random number generator.
<!-- snip -->
</p>
<p>
<em>You have no idea what it will do</em>
</p><p>
It could post your credit card number on social media.
</p><p>
This isn't a theoretical concern. 
There are multiple cases of LLMs wiping people's computers
<a href="https://www.reddit.com/r/ClaudeAI/comments/1pgxckk/">[1]</a>
<a href="https://www.reddit.com/r/singularity/comments/1pc2mbd/">[2]</a>,
cloud accounts
<a href="https://www.404media.co/meta-director-of-ai-safety-allows-ai-agent-to-accidentally-delete-her-inbox/">[3]</a>,
and even causing infrastructure outages
<a href="https://rys.io/en/182.html">[4]</a>.
</p><p>
<!--
All of these could have been prevented if a human reviewed the output before it was executed, but the whole premise of "Agentic AI" is to not do that.
</p><p>
-->
What's worse, LLMs have a nasty habit of lying about what they did. 
<!-- This is not a surprise considering that they are just fancy autocomplete: -->
What should a good assistant say when asked if it did the thing? "Yes", 
and did it delete the data&shy;base? "Of course not."
</p><p>
<em>They don't have to be hacked to ruin your day.</em> 
</p><p>
"... but I tested it!" you say.
</p><p>
You rolled a die in testing, and rolled it again in production. 
It might work fine the first time &mdash; or the first hundred times &mdash; but that doesn't mean it won't misbehave in the future.
</p><p>
<em>If you want to try these tools out</em>, run them in a virtual machine.
Don't give them access to any accounts that you wouldn't want to lose.
Read generated code to make sure it didn't do anything stupid like forgetting to check passwords:
</p>

<pre>
[...]
// TODO: Validate PDU signature
// TODO: Check authorization
[...]
// TODO: Validate the join event
[...]
// TODO: Return actual auth chain
[...]
// TODO: Check power levels
[...]
// TODO: Check permissions
[...]
</pre>
<p>
</p><p>
(These are real comments from Cloudflare's <a href="https://blog.cloudflare.com/serverless-matrix-homeserver-workers/">vibe coded chat server</a>)
</p><p>
... and keep an eye on them to make sure they aren't being <a href="https://theshamblog.com/an-ai-agent-published-a-hit-piece-on-me/">assholes on your behalf</a>.
</p>
<!-- mksite: end of content -->

## 链接

https://maurycyz.com/misc/sandbox_llms/

---

*ID: d58f186e1b551ac8*
*抓取时间: 2026-03-05T10:02:14.134493*
