# Notes on blog future-proofing

> 来源: maurycyz.com  
> 发布时间: Fri, 23 Jan 2026 00:00:00 +0000  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<!-- mksite: start of content -->
<p>

<em>One of the great things about <a href="https://maurycyz.com/misc/starting_a_blog/">web pages</a> is that they are long-lived and mutable</em>.
There's no need to aim for perfection on the first draft:
A page can continue to be improved for years after its original publication.
</p><p>
However, this mutability comes at a cost:
</p><p>
<a href="https://commons.wikimedia.org/wiki/File:First_Web_Server.jpg"><img src="https://maurycyz.com/misc/futureproofing/first_server.jpg" /></a>
<center>DO NOT POWER [IT] DOWN!! &mdash; The first web server.</center>
</p><p>
Servers are just computers:
If they ever break or are turned off, the web site vanishes off the internet. 
</p><p>
<!-- snip -->
</p>
<p>
</p>

<p>
<!--  External links: 3rd party archiving services -->
<em>If you've ever been reading something more than a few years old</em>, you've probably noticed that <a href="https://en.wikipedia.org/wiki/Link_rot">none of the links work</a>.
Even if the destination site still exists, It's common for them to have <a href="https://www.w3.org/Provider/Style/URI">changed the URL format</a> so that old links don't work. 
</p><p>
To be clear, links are a good thing: 
They allow readers to look deeper into a topic, and <a href="https://maurycyz.com/real_pages/">external links</a> are how we find new places on the internet. 
</p><p>
<h1>Preserving external links:</h1>
</p><p>
<em>3rd party are services like <a href="https://archive.org/">archive.org</a> are hit-and-miss</em>:
By most accounts, only <a href="https://arxiv.org/abs/1212.6177">around 50%</a> of pages ever make it to the archive, and even if they have a copy, it's still just a web site:
Many other archiving services <!--like peeep.us--> have vanished or lost data.
These services are good for archiving one's own site, but aren't great at defending against link rot.
</p><p>
<em>If I want to be sure links will always work, they have to be archived locally.</em>
</p><p>
I don't want to run a <a href="https://en.wikipedia.org/wiki/Web_crawler">crawler:</a>
</p><p>
Unless carefully watched,
these can place a lot of <a href="https://lwn.net/Articles/1008897/">load on the target</a> server or/and fill up my disk with infinite dynamic pages:
These could be intentional <a href="https://maurycyz.com/babble/entry-point">honeypots</a> or something as harmless as a web based calendar.
</p><p>
I'd spend more time putting out fires than actually writing. 
</p><p>
With that in mind, I decided to use Chromium's "save" feature to archive single pages.
This has one huge benefit over something like recursive wget:
</p><p>
It saves the final DOM, not what was served over HTTP.
</p><p>
<em>A lot of sites use Javascript to render content</em>:
For example, Substack uses it render math, and despite popular belief, there's more then just Nazis on there:
It's also home to <a href="https://lcamtuf.substack.com/">Lcamtuf's</a> excellent blog.
Other sites go further by delivering all content as JSON and rendering it client side.
You might think that only large corporate sites do this...
<a href="https://kristoff.it/blog/static-site-paradox/">but that's just not the case</a>. 
</p><p>
These types of pages could be preserved with a caching proxy,
but the odds that fifty megabytes of Javascript work in ten years are not good:
</p><p>
It's better to run the Javascript now and save the results for later. 
</p><p>
</p>
<details>
Format choice
<p>
Chrome supports saving in two formats: MHTML and standard HTML with a directory to store the resources. 
</p><p>
On paper, <a href="https://datatracker.ietf.org/doc/html/rfc2557">MHTML</a> very nice &mdash;
it's a standardized, single-file web archive with browser support
&mdash; unfortunately it's only really supported by Chrome: 
depending on a single application is not great for long-term preservation.
</p><p>
Right now, I have enough space to store both formats:
When a link breaks, I'll either serve MHTML (faster, more faithful) or the multi-file archives (more compatible) depending on the current state of support.
</p>
</details>
<p>
<h1>This site itself:</h1>
</p><p>
This blog uses an <a href="https://maurycyz.com/misc/new_ssg/">(almost) zero-dependency site generator</a>: 
The only thing it needs is a C compiler.
</p><p>
<em>When it does break, all the previously generated HTML can be served as-is</em>:
It's only used to update the site.
</p><p>
All the blog posts have URLs beginning with /projects, /misc, /tutorials or /astro:
If I reorganize things, it won't take up a lot of namespace to keep the old URLs working. 
<!--
</p><p>
<h1>The hit-by-a-bus scenario:</h1>
</p><p>
I do have redundant backups of the server, but they do require manual intervention to restore.
The server might continue to run for a while, but it's only a matter of time until something goes wrong. 
</p><p>
In that case, a locally hosted copy won't do much good. 
This is where 3rd party services like <a href=https://archive.org>archive.org</a> shine: 
My site is popular enough for them to have a fairly complete crawl, and I manually submit new posts.
</p><p>
If archive.org vanishes, this <h-n>wget</h-n> command will download everything:
</p><p>
<pre>
<h-c># Recursive wget command to download everything from maurycyz.com, including</h-c>
<h-c># images hosted on a subdomain. Excludes crawler trap and gzip bomb.</h-c>
<h-c># Please don't spam unless you want to be firewalled.</h-c>
<h-n>wget</h-n> --recursive -l inf -N                     \
     --span-hosts                              \
     --domains=<h-v>maurycyz.com</h-v>,<h-v>large.maurycyz.com</h-v> \
     -X <h-v>/babble/</h-v> -X <h-v>/bomb/</h-v>                     \
     --force-directories                       \
     <h-v>https://maurycyz.com/</h-v>
</pre>
</p><p>
... but please don't host a copy while this server is up:
I don't need outdated versions floating around on the internet. 
</p><p>
As of 2026-01-20, this website is around 1.6 GB.
-->
</p>
<!-- mksite: end of content -->

## 链接

https://maurycyz.com/misc/futureproofing/

---

*ID: c343a7a99bd2510b*
*抓取时间: 2026-03-05T10:02:14.134509*
