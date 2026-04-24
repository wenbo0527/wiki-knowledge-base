# Power glitches can leave computer hardware in weird states

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-03-10T03:58:36Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Late Friday night, the university's downtown campus experienced
some sort of power glitch or power event. A few machines rebooted,
a number of machines dropped out of contact for a bit (which probably
indicates some switches restarting), and most significantly, some
of our switches wound up in a weird, non-working state despite being
powered on. This morning we cured the situation by fully power
cycling all of them.</p>

<p>This isn't the first time we've seen brief power glitches leave
things in unusual states. In the past we've seen it with servers,
<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/BMCsCanNeedRebootingII">with BMCs (IPMIs)</a>, and with
switches. It's usually not every machine, either; some machines
won't notice and some will. When we were having semi-regular power
glitches, there were definitely some models of server that were
more prone to problems than others, but even among those models it
usually wasn't universal.</p>

<p>It's fun to speculate about reasons why some particular servers of
a susceptible model would survive and others not, but that's somewhat
beside today's point, which is that <strong>power glitches can get your
hardware into weird states</strong> (and your hardware isn't broken when
and because this happens; it can happen to hardware that's in
perfectly good order). We'd like to think that the computers around
us are binary, either shut off entirely or working properly, but
that clearly isn't the case. A power glitch like this peels back
the comforting illusion to show us the unhappy analog truth underneath.
Modern computers do a lot of work to protect themselves from such
analog problems, but obviously it doesn't always work completely.</p>

<p>(My wild speculation is that the power glitch has shifted at least
part of the overall system into a state that's normally impossible,
and either this can't be recovered from or the rest of the system
doesn't realize that it has to take steps to recover, for example
forcing a full restart. See also <a href="https://en.everybodywiki.com/Flea_Power">flea power</a>, where a powered off
system still retains some power, and sometimes this matters.)</p>

<p>PS: We've also had a few cases where <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/ServerWhenPowerCycleNotEnough">power cycling the hardware
wasn't enough</a>, which is almost
certainly <a href="https://en.everybodywiki.com/Flea_Power">flea power</a> at work.</p>

<p>PPS: My steadily increasing awareness of the fundamentally analog
nature of a lot of what I take as comfortably digital has come in
part from exposure on the Fediverse to people who deal with fun
things like <a href="https://en.wikipedia.org/wiki/Differential_signalling">differential signaling</a> for copper
Ethernet, USB, and PCIe, and the spooky world of DDR training, where
very early on your system goes to some effort to work out the signal
characteristics of your particular motherboard, RAM, and so on so
that it can run the RAM as fast as possible (<a href="https://www.systemverilog.io/design/ddr4-initialization-and-calibration/">cf</a>).</p>

<p>(Never mind all of the CPU errata about unusual situations that
aren't quite handled properly.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/PowerGlitchesWeirdHardwareStates?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/PowerGlitchesWeirdHardwareStates

---

*ID: 822d1a715b819028*
*抓取时间: 2026-03-12T13:49:26.048058*
