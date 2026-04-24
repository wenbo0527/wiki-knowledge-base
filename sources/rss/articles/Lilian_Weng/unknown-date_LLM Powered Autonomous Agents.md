# LLM Powered Autonomous Agents

> 来源: Lilian Weng  
> 发布时间: Fri, 23 Jun 2023 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<p>Building agents with LLM (large language model) as its core controller is a cool concept. Several proof-of-concepts demos, such as <a href="https://github.com/Significant-Gravitas/Auto-GPT">AutoGPT</a>, <a href="https://github.com/AntonOsika/gpt-engineer">GPT-Engineer</a> and <a href="https://github.com/yoheinakajima/babyagi">BabyAGI</a>, serve as inspiring examples. The potentiality of LLM extends beyond generating well-written copies, stories, essays and programs; it can be framed as a powerful general problem solver.</p>
<h1 id="agent-system-overview">Agent System Overview</h1>
<p>In a LLM-powered autonomous agent system, LLM functions as the agent&rsquo;s brain, complemented by several key components:</p>
<ul>
<li><strong>Planning</strong>
<ul>
<li>Subgoal and decomposition: The agent breaks down large tasks into smaller, manageable subgoals, enabling efficient handling of complex tasks.</li>
<li>Reflection and refinement: The agent can do self-criticism and self-reflection over past actions, learn from mistakes and refine them for future steps, thereby improving the quality of final results.</li>
</ul>
</li>
<li><strong>Memory</strong>
<ul>
<li>Short-term memory: I would consider all the in-context learning (See <a href="https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/">Prompt Engineering</a>) as utilizing short-term memory of the model to learn.</li>
<li>Long-term memory: This provides the agent with the capability to retain and recall (infinite) information over extended periods, often by leveraging an external vector store and fast retrieval.</li>
</ul>
</li>
<li><strong>Tool use</strong>
<ul>
<li>The agent learns to call external APIs for extra information that is missing from the model weights (often hard to change after pre-training), including current information, code execution capability, access to proprietary information sources and more.</li>
</ul>
</li>
</ul>
<figure>
	<img src="https://lilianweng.github.io/agent-overview.png" style="width: 100%;" />
	<figcaption>Overview of a LLM-powered autonomous agent system.</figcaption>
</figure>
<h1 id="component-one-planning">Component One: Planning</h1>
<p>A complicated task usually involves many steps. An agent needs to know what they are and plan ahead.</p>

## 链接

https://lilianweng.github.io/posts/2023-06-23-agent/

---

*ID: 00cacf7c851b4f4d*
*抓取时间: 2026-03-05T10:01:44.823760*
