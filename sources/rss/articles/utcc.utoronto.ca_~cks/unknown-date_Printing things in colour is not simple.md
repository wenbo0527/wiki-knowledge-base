# Printing things in colour is not simple

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-25T03:47:22Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Recently, <a href="http://verisimilitudes.net/">Verisimilitude</a> left a
comment on <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/X11DirectColorVisualNotes">my entry on X11's DirectColor visual type</a>, where they mentioned that L
Peter Deutsch, the author of Ghostscript, lamented using twenty-four
bit colour for Ghostscript rather than a more flexible approach,
which you may need in printing things with colour. As it happens,
I know a bit about this area for two or three reasons, which come
at it from different angles. A long time ago I was peripherally
involved in desktop publishing software, which obviously cares about
printing colour, and then later I became a hobby photographer and
at one point had some exposure to people who care about printing
photographs (both colour and black and white).</p>

<p>(The actual PDF format supports much more complex colour models
than basic 24-bit <a href="https://en.wikipedia.org/wiki/SRGB">sRGB</a> or
sGray colour, but apparently Ghostscript turns all of that into
24-bit colour internally. See <a href="https://doi.org/10.2352/issn.2169-2629.2019.27.12">eg</a>, which suggests
that modern Ghostscript has evolved into a more complex internal
colour model.)</p>

<p>On the surface, printing colour things out in physical media may
seem simple. You convert RGB colour to <a href="https://en.wikipedia.org/wiki/CMYK_color_model">CMYK colour</a> and then send the
result off to the printer, where your inkjet or laser printer uses
its CMYK ink or toner to put the result on the paper. Photographic
printers provide the first and lesser complication in this model,
because serious photographic printers have many more colours of ink
than CMYK and they put these inks on various different types of
fine art paper that have different effects on how the resulting
colours come out.</p>

<p>Photographic printers have so many ink colours because this results
in more accurate and faithful colours or, for black and white
photographs (where a set of grey inks may be used), in more accurate
and faithful greys. Photographers who care about this will carefully
profile their printer using its inks on the particular fine art
paper they're going to use in order to determine how RGB colours
can be most faithfully reproduced.  Then as part of the printing
process, the photographic print software and the printer driver
will cooperate to take the RGB photograph and map its colours to
what combination of inks and ink intensity can best do the job.</p>

<p>(Photographers use different fine art papers because the papers
have different characteristics; one of the high level ones is matte
versus glossy papers. But the rabbit hole of detailed paper differences
goes quite deep. So does the issue of how many inks a photo printer
should have and what they should be. Naturally photographers who make
prints have lots of opinions on this whole area.)</p>

<p>Where this stops being just a print driver issue is that people
editing photographs often want to see roughly how they'll look when
printed out without actually making a print (which is generally
moderately expensive).  This requires the print subsystem to be
capable of feeding colour mapping results back to the editing layer,
so you can see that certain things need to be different at the RGB
colour level so that they come out well in the printed photograph.
This is of course all an approximation, but at the very least photo
editing software like <a href="https://www.darktable.org/">darktable</a> wants
to be able to warn you when you're creating an 'out of gamut' colour
that can't be accurately printed.</p>

<p>(I don't have any current numbers for the cost of making prints on
photographic printers, but it's not trivial, especially if you're
making large prints; you'll use a decent amount of ink and the fine
art paper isn't cheap either. You don't want to make more test
prints than you really have to.)</p>

<p>All of this is still in the realm of RGB colour, though (although
<a href="https://en.wikipedia.org/wiki/Color_space">colour space</a> and
<a href="https://en.wikipedia.org/wiki/Linux_color_management">display profiling and management</a> complicate
the picture). To go beyond this we need to venture into the twin
worlds of printing advertising, including product boxes, and fine
art printing. Printed product ads and especially boxes for products
not infrequently use <a href="https://en.wikipedia.org/wiki/Spot_color">spot colours</a>, where part of the box
will be printed with a pure ink colour rather than approximated
with <a href="https://en.wikipedia.org/wiki/Process_color">process colours</a>
(CMYK or other). You don't really want to manage spot colours by
saying that they're a specific RGB value and then everything with
that RGB value will be printed with that spot colour; ideally you
want to manage them as a specific spot colour layer for each spot
colour you're using.  An additional complication is that product
boxes for mass products aren't necessarily printed with CMYK inks
at all; like photographic prints, they may use a custom ink set
that's designed to do a good job with the limited colour gamut that
appears on the product box.</p>

<p>(<a href="https://mastodon.social/@cks/115952068442223249">This leads to a fun little game you can play at home</a>.)</p>

<p>Desktop publishing software that wants to do a good job with this
needs a bunch of features. I believe that generally you want to
handle spot colours as separate editing layers even if they're
represented in RGB. You probably also want features to limit the
colour space and colours that the product designer can do, because
the company that will print your boxes may have told you it has
certain standard ink sets and please keep your box colours to things
they handle well as much as possible. Or you may want to use only
pure spot colours from your set of them and not have a product
designer accidentally set something to another colour.</p>

<p>Printing art books of fine art has similar issues. The artwork that
you're trying to reproduce in the art book may use paint colours
that don't reproduce well in standard CMYK colours, or in any colour
set without special inks (one case is metallic colours, which are
readily available for fine art paints and which some artists love).
The artist whose work you're trying to print may have strong opinions
about you doing a good job of it, while the more inks you use (and
the more special inks) the more expensive the book will be. Some
compromise is inevitable but you have to figure out where and what
things will be the most mangled by various ink set options. This
means your software should be able to map from something roughly
like RGB scans or photographs into ink sets and let you know about
where things are going to go badly.</p>

<p>For fine art books, my memory is that there are a variety of tricks
that you can play to increase the number of inks you can use. For
example, sometimes you can print different sections of the book
with different inks. This requires careful grouping of the pages
(and artwork) that will be printed on a single large sheet of paper
with a single set of inks at the printing plant. It also means that
your publishing software needs to track ink sets separately for
groups of pages and understand how the printing process will group
pages together, so it can warn you if you're putting an artwork
onto a page that clashes with the ink set it needs.</p>

<p>(Not all art books run into these issues. I believe that a lot of
art books for Japanese anime have relatively few problems here
because the art they're reproducing was already made for an environment
with a restricted colour gamut. No one animates with true metallic
colours for all sorts of reasons.)</p>

<p>To come back to PDFs and colour representation, we can see why you
might regret picking a single 24-bit RGB colour representation for
everything in a program that handles things that will eventually
be printed. I'm not sure there's any reasonable general format that
will cover everything you need when doing colour printing, but you
certainly might want to include explicit provisions for spot colours
(which are very common in product boxes, ads, and so on), and
apparently Ghostscript eventually gained support for them (as well
as various other colour related things).</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/PrintingColourNotSimple?showcomments#comments">2 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/tech/PrintingColourNotSimple

---

*ID: ef708fd54190e1d4*
*抓取时间: 2026-03-12T13:49:26.048555*
