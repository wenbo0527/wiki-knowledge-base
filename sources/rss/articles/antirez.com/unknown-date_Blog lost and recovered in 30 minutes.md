# Blog lost and recovered in 30 minutes

> 来源: antirez.com  
> 发布时间: Mon, 02 Dec 2013 09:52:19 +0100  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

Yesterday I lost all my blog data in a rather funny way. When I installed this new blog engine, that is basically a Lamer News slightly modified to serve as a blog, I spinned a Redis instance manually with persistence *disabled* just to see if it was working and test it a bit.
<br />
<br />I just started a screen instance, and run something like ./redis-server --port 10000. Since this is equivalent to an empty config file with just "port 10000" inside I was running no disk backed at all.
<br />
<br />Since Redis very rarely crashes, guess what, after more than one year it was still running inside the screen session, and I totally forgot that it was running like that, happily writing controversial posts in my blog. Yesterday my server was under attack. This caused an higher then normal load, and Linode rebooted the instance. As a result my blog was gone.
<br />
<br />The good thing is that I recovered everything in about 30 minutes because simple systems are really better than complex systems when something bad happens. This blog is composed of posts that are just the verbatim dump of what I write in a text area. No formatting at all. Comments are handled by Disqus and the ID I submit is just the post ID.
<br />
<br />All I had to do is to setup a new Redis server (this time with AOF, demonized, and a proper configuration file) and search in google one after the other the posts by URL (which is the same for all the post, only the incremental ID changes). For every post I opened the Google cache of the post, select the text, copy, and submit the new post.
<br />
<br />The only thing I lost are the post dates... I could fix them modifying a bit the blog code to allow me to do this, but not sure I'll be able to find the time.
<br />
<br />Long story short, this is a trivial example, and an human error, but even in serious well maintained systems shit happens, and when the architecture of something is simple, it is simpler to deal with even during failures.
<br />
<br />Without to mention that now I know I don't have to enable backups as I can recovery everything. No, just kidding.
<a href="http://antirez.com/news/65">Comments</a>

## 链接

http://antirez.com/news/65

---

*ID: 7ca855343a81c0d7*
*抓取时间: 2026-03-05T10:02:11.704852*
