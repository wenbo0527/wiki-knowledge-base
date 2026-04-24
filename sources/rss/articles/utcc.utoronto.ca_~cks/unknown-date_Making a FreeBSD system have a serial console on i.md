# Making a FreeBSD system have a serial console on its second serial port

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-31T04:57:10Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Over on the Fediverse <a href="https://mastodon.social/@cks/115986180864803781">I said</a>:</p>

<blockquote><p>Today's other work achievement: getting a UEFI booted FreeBSD 15
machine to use a serial console on its second serial port, not its
first one. Why? Because the BMC's Serial over Lan stuff appears to be
hardwired to the second serial port, and life is too short to wire up
physical serial cables to test servers.</p>
</blockquote>

<p>The basics of serial console support for your FreeBSD machine are
covered in the <a href="https://man.freebsd.org/cgi/man.cgi?query=loader.conf">loader.conf</a> manual page,
under the '<code>console</code>' setting (in the 'Default Settings' section).
But between UEFI and FreeBSD's various consoles, things get
complicated, and for me the manual pages didn't do a great job of
putting the pieces together clearly. So I'll start with my descriptions
of all of the <a href="https://man.freebsd.org/cgi/man.cgi?query=loader.conf">loader.conf</a> variables that are relevant:</p>

<dl><dt><code>console="efi,comconsole"</code> </dt>
<dd>Sets both the bootloader console and
the kernel console to both the EFI console and the serial port,
by default COM1 (ttyu0, Linux ttyS0). This is somewhat harmful if
your UEFI BIOS is already echoing console output to the serial
port (or at least to the serial port you want); you'll get doubled
serial output from the FreeBSD bootloader, but not doubled output
from the kernel.<p>
</dd>
<dt><code>boot_multicons="YES"</code> </dt>
<dd>As covered in <a href="https://man.freebsd.org/cgi/man.cgi?query=loader_simp&amp;sektion=8">loader_simp(8)</a>,
this establishes multiple low level consoles for kernel messages.
It's not necessary if your UEFI BIOS is already echoing console
output to the serial port (and the bootloader and kernel can
recognize this), but it's harmless to set it just in case.<p>
</dd>
<dt><code>comconsole_speed="115200"</code> </dt>
<dd>Sets the serial console speed
(and in theory 115200 is the default). It's not necessary if the
UEFI BIOS has set things up but it's harmless. See <a href="https://man.freebsd.org/cgi/man.cgi?query=loader_simp&amp;sektion=8">loader_simp(8)</a>
again.<p>
</dd>
<dt><code>comconsole_port="0x2f8"</code> </dt>
<dd>Sets the serial port used to COM2.
It's not necessary if the UEFI BIOS has set things up, but again
it's harmless. You can use 0x3f8 to specify COM1, although it's
the default. See <a href="https://man.freebsd.org/cgi/man.cgi?query=loader_simp&amp;sektion=8">loader_simp(8)</a>.<p>
</dd>
<dt><code>hw.uart.console="io:0x2f8,br:115200"</code> </dt>
<dd>This tells the kernel
where the serial console is and what baud rate it's at, here COM2
and 115200 baud. The loader will automatically set it for you if
you set the comconsole_* variables, either because you also
need a '<code>console=</code>' setting or because you're being redundant.
See <a href="https://man.freebsd.org/cgi/man.cgi?query=loader.efi&amp;sektion=8">loader.efi(8)</a> (and
then <a href="https://man.freebsd.org/cgi/man.cgi?query=loader_simp&amp;sektion=8">loader_simp(8)</a> and <a href="https://man.freebsd.org/cgi/man.cgi?query=uart&amp;sektion=4">uart(4)</a>).<p>
(That the loader does this even without a 'comconsole' in your
nonexistent 'console=' line may some day be considered a bug and
fixed.)</dd>
</dl>

<p>If they agree with each other, you can safely set both hw.uart.console
and the comconsole_* variables.</p>

<p>On a system where the UEFI BIOS isn't echoing the UEFI console
output to a serial port, the basic version of FreeBSD using both
the video console (settings for which are in <a href="https://man.freebsd.org/cgi/man.cgi?query=vt&amp;sektion=4">vt(4)</a>) and the
serial console (on the default of COM1), with the primary being the
video console, is a loader.conf setting of:</p>

<blockquote><pre style="white-space: pre-wrap;">
console="efi,comconsole"
boot_multicons="YES"
</pre>
</blockquote>

<p>This will change both the bootloader console and the kernel console
after boot. If your UEFI BIOS is already echoing 'console' output
to the serial port, bootloader output will be doubled and you'll
get to see fun bootloader output like:</p>

<blockquote><pre style="white-space: pre-wrap;">
LLooaaddiinngg  ccoonnffiigguurreedd  mmoodduulleess......
</pre>
</blockquote>

<p>If you see this (or already know that your UEFI BIOS is doing this),
the minimal alternate loader.conf settings (for COM1) are:</p>

<blockquote><pre style="white-space: pre-wrap;">
# for COM1 / ttyu0
hw.uart.console="io:0x3f8,br:115200"
</pre>
</blockquote>

<p>(The details are covered in <a href="https://man.freebsd.org/cgi/man.cgi?query=loader.efi&amp;sektion=8">loader.efi(8)</a>'s
discussion of console considerations.)</p>

<p>If you don't need a 'console=' setting because of your UEFI BIOS,
you must set either <code>hw.uart.console</code> or the comconsole_*
settings. Technically, setting <code>hw.uart.console</code> is the correct
approach; that setting only comconsole_* still works may be a
bug.</p>

<p>If you don't explicitly set a serial port to use, FreeBSD will use
COM1 (ttyu0, Linux ttyS0) for the bootloader and kernel. This is
only possible if you're using 'console=', because otherwise you
have to directly or indirectly set 'hw.uart.console', which directly
tells the kernel which serial port to use (and the bootloader will
use whatever UEFI tells it to). To change the serial port to COM2,
you need to set the appropriate one of '<code>comconsole_port</code>' and
'<code>hw.uart.console</code>' from 0x3f8 (COM1) to the right PC port value
of 0x2f8.</p>

<p>So our more or less final COM2 /boot/loader.conf for a case where
you can turn off or ignore the BIOS echoing to the serial console
is:</p>

<blockquote><pre style="white-space: pre-wrap;">
console="efi,comconsole"
boot_multicons="YES"
comconsole_speed="115200"
# For the COM2 case
comconsole_port="0x2f8"
</pre>
</blockquote>

<p>If your UEFI BIOS is already echoing 'console' output to the serial
port, the minimal version of the above (again for COM2) is:</p>

<blockquote><pre style="white-space: pre-wrap;">
# For the COM2 case
hw.uart.console="io:0x2f8,br:115200"
</pre>
</blockquote>

<p>(As with Linux, the FreeBSD kernel will only use one serial port
as the serial console; you can't send kernel messages to two serial
ports. FreeBSD at least makes this explicit in its settings.)</p>

<p>As covered in <a href="https://man.freebsd.org/cgi/man.cgi?query=conscontrol">conscontrol</a> and elsewhere,
FreeBSD has a high level console, represented by <code>/dev/console</code>,
and a low level console, used directly by the kernel for things
like kernel messages. The high level console can only go to one
device, normally the first one; this is either the first one in
your '<code>console=</code>' line or whatever UEFI considers the primary
console. The low level console can go to multiple devices. Unlike
Linux, this can be changed on the fly once the system is up through
<a href="https://man.freebsd.org/cgi/man.cgi?query=conscontrol">conscontrol</a> (and also have its state checked).</p>

<p>Conveniently, you don't need to do anything to start a serial login
on your chosen console serial port. All four possible (PC) serial
ports, /dev/ttyu0 through /dev/ttyu3, come pre-set in <code>/etc/ttys</code>
with 'onifconsole' (and 'secure'), so that if the kernel is using
one of them, there's a getty started on it. I haven't tested what
happens if you use <a href="https://man.freebsd.org/cgi/man.cgi?query=conscontrol">conscontrol</a> to change the console on the
fly.</p>

<p>Booting FreeBSD on a UEFI based system is covered through the manual
page series of <a href="https://man.freebsd.org/cgi/man.cgi?query=uefi&amp;sektion=8">uefi(8)</a>, <a href="https://man.freebsd.org/cgi/man.cgi?query=boot&amp;sektion=8">boot(8)</a>,
<a href="https://man.freebsd.org/cgi/man.cgi?query=loader.efi&amp;sektion=8">loader.efi(8)</a>, and <a href="https://man.freebsd.org/cgi/man.cgi?query=loader&amp;sektion=8">loader(8)</a>. It's
not clear to me if loader.efi is the EFI specific version of
loader(8), or if the one loads and starts the other in a multi-stage
boot process. I suspect it's the former.</p>

<h3>Sidebar: What we may wind up with in loader.conf</h3>

<p>Here's what I think is a generic commented block for serial console
support:</p>

<blockquote><pre style="white-space: pre-wrap;">
# Uncomment if the UEFI BIOS does not echo to serial port
#console="efi,comconsole"
boot_multicons="YES"
comconsole_speed="115200"
# Uncomment for COM2
#comconsole_port="0x2f8"
# change 0x3f8 (COM1) to 0x2f8 for COM2
hw.uart.console="io:0x3f8,br:115200"
</pre>
</blockquote>

<p>All of this works for me on FreeBSD 15, but your distance may vary.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/FreeBSDSerialConsoleSecondPort?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/FreeBSDSerialConsoleSecondPort

---

*ID: 02860320b2e7e34e*
*抓取时间: 2026-03-12T13:49:26.048480*
