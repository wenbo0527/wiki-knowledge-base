# Sometimes the simplest version of a text table is printed from a command

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-01T03:17:38Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Back when we had just started with <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusGrafanaSetup-2019">our current metrics and
dashboards adventure</a>, I wrote about
how <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SimpleTextVsGraphs">sometimes the simplest version of a graph is a text table</a>. Today I will extend that further: sometimes
the simplest version of a text table is to have a command that
prints it out, rather than making people look at a web page.</p>

<p>We recently had <a href="https://mastodon.social/@cks/116084506995715846">a major power outage at work</a>, and in the
aftermath <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PDUsCanFailEventually">not all of our machines came back</a>.
One of my co-workers is an extreme early bird and he came in to the
university about as early as it's possible to on the TTC, and started
work on troubleshooting what was going on. One of the things he
needed to know was what machines were still down, so he could figure
out any common elements to them (and see what machines were stubbornly
not coming back on even though they ought to be).</p>

<p>We have <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusGrafanaSetup-2019">Grafana dashboards</a> for this,
and the information about what machines are down is present in some
of them in tabular form. But it's a table embedded in a widget in
a web page, and you need a browser to look at it, which you may not
have from the server console of some server you just powered up.
Since I like command line tools, at one point I wrote some little
scripts that <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusQueryWithCurl">make queries to our Prometheus server with curl</a> and run the result through 'jq' to extract
things. One of them is called 'promdownhosts' and it prints out
what you'd expect. Initially this was just something I used, but
several years ago <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/MentionLittleScripts">I mentioned my collection of these scripts to
my co-workers</a> and we wound up making them
group scripts in a central location.</p>

<p>(I initially wrote this script and a few others for use during our
planned power outages and other downtimes, because it was a convenient
way of seeing what we hadn't yet turned on or might have missed.)</p>

<p>Early in the morning of that Tuesday, bringing machines back up
after the power outage and finding <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PDUsCanFailEventually">dead PDUs</a>,
my co-worker used the 'promdownhosts' script extensively to
troubleshoot things. One of the nice aspects of it being a script
was that he could put the names of uninteresting machines in a file
and then exclude them easily with things like 'promdownhosts | fgrep
-v -f /tmp/ignore-these' (something that's much harder to do in a
web page dashboard interface, especially if the designer hasn't
thought of that). And in general, the script made (and makes) this
information quite readily accessible in a compact format that was
quick to skim and definitely free of distractions.</p>

<p>Not everything can be presented this way, in a list or a table
printed out in plain text from a command line tool. Sometimes tables
on a web page are the better option, and it's good to have options
in general; sometimes we want to look at this information along
with other information too. As I've found out the hard way sometimes,
there's only so much information you can cram into a plain text
table before the result is increasingly hard to read.</p>

<p>(I have <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/PrometheusMyQuietAlertMonitoring">a command that summarizes our current Prometheus alerts</a> and its output is significantly
harder to read because I need it to be compact and there's more
information to present. It's probably only really suitable for my
use because I understand all of its shorthand notations, including
the internal Prometheus names for our alerts.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SimpleTextViaCommands?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SimpleTextViaCommands

---

*ID: 6ac0ece9f9a2a8a7*
*抓取时间: 2026-03-12T13:49:26.048158*
