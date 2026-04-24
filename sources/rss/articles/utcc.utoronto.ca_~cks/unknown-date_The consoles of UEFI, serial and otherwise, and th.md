# The consoles of UEFI, serial and otherwise, and their discontents

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-03T03:07:13Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p><a href="https://en.wikipedia.org/wiki/UEFI">UEFI</a> is the modern firmware
standard for x86 PCs and other systems; sometimes the actual
implementation is called <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/UEFIAndBIOSAndOtherPCTerms">a UEFI BIOS</a>,
but the whole area is a bit confusing. I recently wrote about
<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/FreeBSDSerialConsoleSecondPort">getting FreeBSD to use a serial console on a UEFI system</a> and mentioned that some
UEFI BIOSes could echo console output to a serial port, which caused
<a href="https://www.robohack.ca/~woods/">Greg A. Woods</a> to ask a good
question in a comment:</p>

<blockquote><p>So, how does one get a typical UEFI-supporting system to use a serial
console right from the firmware?</p>
</blockquote>

<p>The mechanical answer is that you go into your UEFI BIOS settings
and see if it has any options for what is usually called 'console
redirection'. If you have it, you can turn it on and at that point
the <em>UEFI console</em> will include the serial device you picked,
theoretically allowing both output and input from the serial device.
This is very similar to the 'console redirection' option in 'legacy'
pre-UEFI BIOSes, although it's implemented rather differently. An
important note here is that <strong>UEFI BIOS console redirection only
applies to things using the UEFI console</strong>. Your UEFI BIOS definitely
uses the UEFI console, and your UEFI operating system boot loader
hopefully does. Your operating system almost certainly doesn't.</p>

<p>A UEFI BIOS doesn't need to have such an option and typical desktop
ones probably don't. The UEFI standard provides a standard set of
ways to implement console redirection (and alternate console devices
in general), but UEFI doesn't require it; it's perfectly standard
compliant for a UEFI BIOS to only support the video console. Even
if your UEFI BIOS provides console redirection, your actual experience
of trying to use it may vary. Watching boot output is likely to be
fine, but trying to interact with the BIOS from your serial port
may be annoying.</p>

<p>How all of this works is that UEFI has a notion of an <a href="https://uefi.org/specs/UEFI/2.11/12_Protocols_Console_Support.html">EFI console</a>,
which is (to quote the documentation) "used to handle input and
output of text-based information intended for the system user during
the operation of code in the boot services environment". The EFI
console is an abstract thing, and it's also some <a href="https://uefi.org/specs/UEFI/2.11/03_Boot_Manager.html#globally-defined-variables">globally defined
variables</a>
that include <code>ConIn</code> and <code>ConOut</code>, the <a href="https://uefi.org/specs/UEFI/2.11/10_Protocols_Device_Path_Protocol.html">device paths</a>
of the console input and output device or devices. Device paths can
include multiple sub-devices (in <a href="https://uefi.org/specs/UEFI/2.11/10_Protocols_Device_Path_Protocol.html#generic-device-path-structures">generic device path structures</a>),
and one of the examples specifically mentioned is:</p>

<blockquote><p>[...] An example of this would be the <code>ConsoleOut</code> environment
variable that consists of both a VGA console and serial output
console. This variable would describe a console output stream that is
sent to both VGA and serial concurrently and thus has a Device Path
that contains two complete Device Paths. [...]</p>
</blockquote>

<p>(Sometimes this is 'ConsoleIn' and 'ConsoleOut', <a href="https://uefi.org/specs/UEFI/2.11/Apx_R_Glossary.html">eg</a>, and sometimes
'ConIn' and 'ConOut'. Don't ask me why.)</p>

<p>In theory, a UEFI BIOS can hook a wide variety of things up to
ConIn, ConOut, or both, as it decides (and implements), possibly
including things like <a href="https://uefi.org/specs/UEFI/2.11/10_Protocols_Device_Path_Protocol.html#ipv4-device-path">IPv4 connections</a>.
In practice it's up to the UEFI BIOS to decide what it will bother
to support. Server UEFI BIOSes will typically support serial console
redirection, which is to say connecting some serial port to ConIn
and ConOut in addition to the VGA console. Desktop motherboard UEFI
BIOSes probably won't. I don't know if there are very many server
UEFI BIOSes that will use only the serial console and exclude the
VGA console from ConIn and ConOut.</p>

<p>(Also in theory I believe a UEFI BIOS could wire up ConOut to include
a serial port but not connect it to ConIn. In practice I don't know
of any that do.)</p>

<p>EFI also defines <a href="https://uefi.org/specs/UEFI/2.11/12_Protocols_Console_Support.html">a protocol (a set of function calls) for console
input and output</a>. For
input, what people (including the UEFI BIOS itself) get back is
either or both of an EFI scan code or a Unicode character. The 'EFI
scan code' is used to determine what special key you typed, for
example F11 to go into some UEFI BIOS setup mode. The UEFI standard
also has <a href="https://uefi.org/specs/UEFI/2.11/Apx_B_Console.html">an appendix with examples of mapping various sorts of
input to these EFI scan codes</a>, which is
very relevant for entering anything special over a serial console.</p>

<p>If you look at this <a href="https://uefi.org/specs/UEFI/2.11/Apx_B_Console.html">appendix B</a>, you'll note
that it has entries for both 'ANSI X3.64 / DEC VT200-500 (8-bit
mode)' and 'VT100+ (7-bit mode)'. Now you have two UEFI BIOS
questions. First, does your UEFI BIOS even implement this, or does
it either ignore the whole issue (leaving you with no way to enter
special characters) or come up with its own answers? And second,
does your BIOS restrict what it recognizes over the serial port to
just whatever type it's set the serial port to, or will it recognize
either sequence for something like F11? The latter question is very
relevant because your terminal emulator environment may or may not
generate what your UEFI BIOS wants for special keys like F11 (or
it may even intercept some keys, like F11; <a href="https://mastodon.social/@cks/116004100471770117">ideally you can turn
this off</a>).</p>

<p>(Another question is what your UEFI BIOS may call the option that
controls what serial port key mapping it's using. One machine I've
tested on calls the setting "Putty KeyPad" and the correct value
for the "ANSI X3.64" version is "XTERMR6", for example, which
corresponds to what xterm, Gnome-Terminal and probably other modern
terminal programs send.)</p>

<p>Another practical issue is that if you do anything fancy with a
UEFI serial console, such as go into the BIOS configuration screens,
your UEFI BIOS may generate output that assumes a very specific and
unusual terminal resolution. For instance, the Supermicro server
I've been using for <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/FreeBSDSerialConsoleSecondPort">my FreeBSD testing</a> appears to require a 100x30
terminal in its BIOS configuration screens; if you have any other
resolution you get various sorts of jumbled results. Many of our
Dell servers take a different approach, where the moment you turn
on serial console redirection they choke their BIOS configuration
screens down to an ASCII 80x24 environment. OS boot environments
may be more forgiving in various ways.</p>

<p>The good news is that your operating system's bootloader will
probably limit itself to regular characters, and in practice what
you care about a lot of the time is interacting with the bootloader
(for example, for alternate boot and disaster recovery), not your
UEFI BIOS.</p>

<p>As FreeBSD discusses in <a href="https://man.freebsd.org/cgi/man.cgi?query=loader.efi&amp;sektion=8">loader.efi(8)</a>,
it's not necessarily straightforward for an operating system boot
loader to decode what the UEFI ConIn and ConOut are connected to
in order to pass the information to the operating system (which
normally won't be using UEFI to talk to its console(s)). This means
that the UEFI BIOS console(s) may not wind up being what the OS
console(s) are, and you may have to configure them separately.</p>

<p>PS: As you may be able to tell from what I've written here, if
you care significantly about UEFI BIOS access from the serial
port, you should expect to do a bunch of experimentation with
your specific hardware. Remember to re-check your results with
new server generations and new UEFI BIOS firmware versions.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/UEFISerialConsoles?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/UEFISerialConsoles

---

*ID: caaf3e36aa101967*
*抓取时间: 2026-03-12T13:49:26.048446*
