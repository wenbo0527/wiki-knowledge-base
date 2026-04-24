# A little bit of complex design in phone "Level" applications

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-01T02:24:14Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Modern smartphones have a lot of sensors; for example, they often
have sensors that will report the phone's orientation and when it
changes (which is used for things like 'wake up the screen when you
pick up the phone'). One of the uses for these sensors is for little
convenience applications, such as a "Level" app that uses the
available sensors to report when the phone is level so you can use
it as a level, <a href="https://mastodon.social/@cks/115764574676916514">sometimes for trivial purposes</a>.</p>

<p>For years, this application seemed pretty trivial and obvious to
me, with the only somewhat complex bit being figuring out how the
person is holding the phone to determine which sort of level they
wanted and then adjusting the display to clearly reflect that (while
keeping it readable, something that Apple's current efforts partially
fail). Then <a href="https://mastodon.social/@cks/115799856430417404">I had a realization</a>:</p>

<blockquote><p>Today's random thought: Your phone, like mine, probably has a "Level"
app, which is most naturally used with the phone on its side for
better accuracy, including resting on top of (or below) things. Your
phone (also like mine) probably has buttons on the sides that make
its sides not 100% straight and level end to end (because the buttons
make bumps). So, how does the Level app deal with that? Does it have
a range of 'close enough to level', or some specific compensation, or
button detection?</p>
</blockquote>

<p>(By 'on its side' I meant with the long side of the phone, as opposed
to the top or the bottom, which are often flat and button-less. You
can also use the phone as a level horizontally, on top of a flat
surface, where you have the bump of the camera lenses to worry
about.)</p>

<p><a href="https://utcc.utoronto.ca/~cks/space/blog/tech/SmartphoneInfiltratedMyLife">My current phone</a> has a noticeable
camera bump, and <a href="https://phyphox.org/">the app I use to get relatively raw sensor data</a> suggests that there's a detectable, roughly
1.5 degree difference in tilt between resting all of the phone on
a surface and just having the phone case edge around the camera
bump on the surface (which should make the phone as 'level' as
possible). However, once it's reached a horizontal '0 degrees'
level, the "Level" app will treat both of them as equivalent (I can
tilt the phone back and forth without disturbing the green level
marking). This isn't just the Level app being deliberately imprecise;
before I achieve a horizontal 0 degrees level, the "Level" app does
respond to tilting the phone back and forth, typically changing its
tilt reading by a degree.</p>

<p>(Experimentation suggests that the side buttons create less tilt,
probably under a degree, and also that the Level app probably ignores
that tilt when it's reached 0 degrees of tilt. It may ignore such
small changes in tilt in general, and there's certainly some noise
in the sensor readings.)</p>

<p>As a system administrator and someone who peers into technology for
fun, I'm theoretically well aware that often there's more behind
the scenes than is obvious. But still, it can surprise me when I
notice an aspect of something I've been using for years without
thinking about it. There's a lot of magic that goes into making
things work the way we expect them to (for example, <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/MicrowaveGoodUIBehavior">digital
microwaves doing what you want with time</a>;
this Level app behavior also sort of falls under the category of
'good UI').</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/LevelPhoneAppDesignComplexity

---

*ID: 3c756f0be8243426*
*抓取时间: 2026-03-12T13:49:26.048807*
