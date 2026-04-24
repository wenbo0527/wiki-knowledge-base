# Gnome, GSettings, gconf, and which one you want

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-02-24T03:22:41Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>On the Fediverse a while back, <a href="https://mastodon.social/@cks/116004100471770117">I said</a>:</p>

<blockquote><p>Ah yes, GNOME, it is of course my mistake that I used gconf-editor
instead of dconf-editor. But at least now Gnome-Terminal no longer
intercepts F11, so I can possibly use g-t to enter F11 into serial
consoles to get the attention of a BIOS. If everything works in UEFI
land.</p>
</blockquote>

<p>Gnome has had at least two settings systems, <a href="https://wiki.gnome.org/HowDoI/GSettings">GSettings</a>/<a href="https://en.wikipedia.org/wiki/Dconf">dconf</a> (<a href="https://wiki.gnome.org/Projects/dconf">also</a>) and the older <a href="https://en.wikipedia.org/wiki/GConf">GConf</a>. If you're using a modern
Gnome program, especially a standard Gnome program like gnome-terminal,
it will use <a href="https://wiki.gnome.org/HowDoI/GSettings">GSettings</a> and you will want to use <code>dconf-editor</code>
to modify its settings outside of whatever Preferences dialogs it
gives you (or doesn't give you). You can also use the <a href="https://man.archlinux.org/man/gsettings.1">gsettings</a> or <a href="https://man.archlinux.org/man/dconf.1">dconf</a> programs from the command
line.</p>

<p>(This can include Gnome-derived desktop environments like <a href="https://en.wikipedia.org/wiki/Cinnamon_(desktop_environment)">Cinnamon</a>,
which <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/CinnamonSeeingKeybindings">has updated to using GSettings</a>.)</p>

<p>If the program you're using hasn't been updated to the latest things
that Gnome is doing, for example <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/ThunderbirdBrowserWhereFrom">Thunderbird</a> (at least as of 2024), then it will
still be using <a href="https://en.wikipedia.org/wiki/GConf">GConf</a>. You need to edit its settings using
<code>gconf-editor</code> or <code>gconftool-2</code>, or possibly you'll need to look
at the GConf version of general Gnome settings. I don't know if
there's anything in Gnome that synchronizes general Gnome GSettings
settings into GConf settings for programs that haven't yet been
updated.</p>

<p>(This is relevant for programs, like <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/ThunderbirdBrowserWhereFrom">Thunderbird</a>, that use
general Gnome settings for things like 'how to open a particular
sort of thing'. Although I think modern Gnome may not have very
many settings for this because it always goes to the <a href="https://docs.gtk.org/gio/">GTK GIO
system</a>, based on <a href="https://wiki.archlinux.org/title/default_applications">the Arch Wiki's page
on Default Applications</a>.)</p>

<p>Because I've made this mistake between gconf-editor and dconf-editor
more than once, I've now created a personal gconf-editor cover script
that prints an explanation of the situation when I run it without a
special --really argument. Hopefully this will keep me sorted out the
next time I run gconf-editor instead of dconf-editor.</p>

<p>PS: Probably I want to use gsettings instead of dconf-editor and
<a href="https://man.archlinux.org/man/dconf.1">dconf</a> as much as possible, since gsettings works through the
GSettings layer and so apparently has more safety checks than
dconf-editor and dconf do.</p>

<p>PPS: Don't ask me what the equivalents are for KDE. <a href="https://utcc.utoronto.ca/~cks/space/blog/linux/KDEFontSizeMystery">KDE settings
are currently opaque to me</a>.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/linux/DconfVsGconfInGnome?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/DconfVsGconfInGnome

---

*ID: 4e16a37dcdb37218*
*抓取时间: 2026-03-12T13:49:26.048213*
