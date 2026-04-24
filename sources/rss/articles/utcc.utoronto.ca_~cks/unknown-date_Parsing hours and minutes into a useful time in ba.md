# Parsing hours and minutes into a useful time in basic Python

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-20T03:48:34Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Suppose, not hypothetically, that you have a program that optionally
takes a time in the past to, for example, report on things as of
that time instead of as of right now. You would like to allow people
to specify this time as just 'HH:MM', with the meaning being that
time today (letting people do 'program --at 08:30'). This is
convenient for people using your program but irritatingly hard
today with the Python standard library.</p>

<p>(In the following code examples, I need a Unix timestamp and we're
working in local time, so I wind up calling <a href="https://docs.python.org/3/library/time.html">time.mktime()</a>. We're working in
local time because <a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/ServerUTCTimeViews">that's what is useful for us</a>.)</p>

<p>As I discovered or noticed a long time ago, <a href="https://docs.python.org/3/library/time.html">the time module</a> is <a href="https://utcc.utoronto.ca/~cks/space/blog/python/GMTTimestringToSeconds">a thin shim over
the C library time functions</a> and inherits
their behavior. One of these behaviors is that if you ask
<a href="https://docs.python.org/3/library/time.html#time.strptime">time.strptime()</a> to parse
a time format of '%H:%M', you get back a <a href="https://docs.python.org/3/library/time.html#time.struct_time"><code>struct_time</code></a>
object that is in 1900:</p>

<pre style="white-space: pre-wrap;">
>>> import time
>>> time.strptime("08:10", "%H:%M")
time.struct_time(tm_year=1900, tm_mon=1, tm_mday=1, tm_hour=8, tm_min=10, tm_sec=0, tm_wday=0, tm_yday=1, tm_isdst=-1)
</pre>

<p>There are two solutions I can think of, the straightforward brute
force approach that uses only the <a href="https://docs.python.org/3/library/time.html">time</a> module and a more
theoretically correct version using <a href="https://docs.python.org/3/library/datetime.html">datetime</a>, which comes
in two variations depending on whether you have Python 3.14 or
not.</p>

<p>The brute force solution is to re-parse a version of the time
string with the date added. Suppose that you have a series of
time formats that people can give you, including '%H:%M', and
you try them all until one works, with code like this:</p>

<blockquote><pre style="white-space: pre-wrap;">
 for fmt in tfmts:
     try:
         r = time.strptime(tstr, fmt)
         # Fix up %H:%M and %H%M
         if r.tm_year == 1900:
             dt = time.strftime("%Y-%m-%d ", time.localtime(time.time()))
             # replace original r with the revised one.
             r = time.strptime(dt + tstr, "%Y-%m-%d "+fmt)
         return time.mktime(r)
     except ValueError:
         continue
</pre>
</blockquote>

<p>I think the correct, elegant way using only the standard library
is to use <a href="https://docs.python.org/3/library/datetime.html">datetime</a>
to combine today's date and the parsed time into a correct datetime
object, which can then be turned into a struct_time and passed
to <a href="https://docs.python.org/3/library/time.html#time.mktime">time.mktime</a>.
Before Python 3.14, I believe this is:</p>

<blockquote><pre style="white-space: pre-wrap;">
         r = time.strptime(tstr, fmt)
         if r.tm_year == 1900:
             tm = datetime.time(hour=r.tm_hour, minute=r.tm_min)
             today = datetime.date.today()
             dt = datetime.datetime.combine(today, tm)
             r = dt.timetuple()
         return time.mktime(r)
</pre>
</blockquote>

<p>There are variant approaches to the basic transformation I'm doing
here but I think this is the most correct one.</p>

<p>If you have Python 3.14 or later, you have <a href="https://docs.python.org/3/library/datetime.html#datetime.time.strptime">datetime.time.strptime()</a>
and I think you can do the slightly clearer:</p>

<blockquote><pre style="white-space: pre-wrap;">
[...]
             tm = datetime.time.strptime(tstr, fmt)
             today = datetime.date.today()
             dt = datetime.datetime.combine(today, tm)
             r = dt.timetuple()
[...]
</pre>
</blockquote>

<p>If you can work with <a href="https://docs.python.org/3/library/datetime.html#datetime-objects">datetime.datetime</a> objects,
you can skip converting back to a <a href="https://docs.python.org/3/library/time.html#time.struct_time">time.struct_time</a>
object. In my case, the eventual result I need is a Unix timestamp
so I have no choice.</p>

<p>You can wrap this up into a general function:</p>

<blockquote><pre style="white-space: pre-wrap;">
def strptime_today(tstr, fmt):
   r = time.strptime(tstr, fmt)
   if r.tm_year != 1900:
      return r
   tm = datetime.time(hour=r.tm_hour, minute=r.tm_min, second=r.tm_sec)
   today = datetime.date.today()
   dt = datetime.datetime.combine(today, tm)
   return dt.timetuple()
</pre>
</blockquote>

<p>This version of time.strptime() will return the time today if given
a time format with only hours, minutes, and possibly seconds. Well,
technically it will do this if given any format without the year,
but dealing with all of the possible missing fields is left as an
exercise for the energetic, partly because there's no (relatively)
reliable signal for missing months and days the way there is for
years. For many programs, a year of 1900 is not even close to being
valid and is some sort of mistake at best, but January 1st is a
perfectly ordinary day of the year to care about.</p>

<p>(Now that I've written this function I may update my code to use
it, instead of the brute force <a href="https://docs.python.org/3/library/time.html">time</a> package only version.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/python/HoursMinutesToTime?showcomments#comments">5 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/python/HoursMinutesToTime

---

*ID: 07d6651fb374b12c*
*抓取时间: 2026-03-12T13:49:26.048262*
