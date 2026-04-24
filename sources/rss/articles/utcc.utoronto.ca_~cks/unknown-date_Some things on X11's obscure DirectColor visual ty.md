# Some things on X11's obscure DirectColor visual type

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-04T03:21:26Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>The <a href="https://en.wikipedia.org/wiki/X_Window_System">X Window System</a>
has a long standing concept called 'visuals'; to simplify, an X
visual determines how to determine the colors of your pixels. As I
wrote about a number of years ago, <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/X11TruecolorHistory">these days X11 mostly uses
'TrueColor' visuals</a>, which directly supply
8-bit values for red, green, and blue ('24-bit color'). However X11
has <a href="https://tronche.com/gui/x/xlib/window/visual-types.html">a number of visual types</a>, such as
the straightforward <em>PseudoColor</em> indirect colormap (where every
pixel value is an index into an RGB colormap; typically you'd get
8-bit pixels and 24-bit colormaps, so you could have 256 colors out
of a full 24-bit gamut). One of the (now) obscure visual types is
<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ColourModelsX10vsX11">DirectColor</a>. To quote:</p>

<blockquote><p>For <strong>DirectColor</strong>, a pixel value is decomposed into separate RGB
subfields, and each subfield separately indexes the colormap for the
corresponding value. The RGB values can be changed dynamically.</p>
</blockquote>

<p>(This is specific to X11; <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/ColourModelsX10vsX11">X10 had a different display color model</a>.)</p>

<p>In a PseudoColor visual, each pixel's value is taken as a whole and
used as an index into a colormap that gives the RGB values for that
entry. In DirectColor, the pixel value is split apart into three
values, one each for red, green, and blue, and each value indexes
a separate colormap for that color component. Compared to a PseudoColor
visual of the same pixel depth (size, eg each pixel is an 8-bit
byte), you get less possible variety within a single color component
and (I believe) no more colors in total.</p>

<p>When this came up in <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/X11TruecolorHistory">my old entry about TrueColor and PseudoColor
visuals</a>, in a comment <a href="http://plasmasturm.org/">Aristotle Pagaltzis</a> speculated:</p>

<blockquote><p>[...] maybe it can be implemented as three LUTs in front of a DAC’s
inputs or something where the performance impact is minimal? (I’m
not a hardware person.) [...]</p>
</blockquote>

<p>I was recently reminded of this old entry and when I reread that
comment, an obvious realization struck me about why DirectColor
might make hardware sense. Back in the days of analog video,
essentially every serious sort of video connection between your
computer and your display carried the red, green, and blue components
separately; you can see this in <a href="https://en.wikipedia.org/wiki/VGA_connector">the VGA connector</a> pinouts, and on old
Unix workstations these might literally be separate wires connected
to separate <a href="https://en.wikipedia.org/wiki/BNC_connector">BNC connectors</a>
on your CRT display.</p>

<p>If you're sending the red, green, and blue signals separately you
might also be generating them separately, with one DAC per color
channel. If you have separate DACs, it might be easier to feed them
from separate <a href="https://en.wikipedia.org/wiki/Lookup_table">LUTs</a>
and separate pixel data, especially back in the days when much of
a Unix workstation's graphics system was implemented in relatively
basic, non-custom chips and components. You can split off the bits
from the raw pixel value with basic hardware and then route each
color channel to its own LUT, DAC, and associated circuits (although
presumably you need to drive them with a common clock).</p>

<p>The other way to look at DirectColor is that it's a more flexible
version of TrueColor. A TrueColor visual is effectively a 24-bit
DirectColor visual where the color mappings for red, green, and
blue are fixed rather than variable (this is in fact <a href="https://tronche.com/gui/x/xlib/window/visual-types.html">how it's
described in the X documentation</a>). Making
these mappings variable costs you only a tiny bit of extra memory
(you need 256 bytes for each color) and might require only a bit
of extra hardware in the color generation process, and it enables
the program using the display to change colors on the fly with small
writes to the colormap rather than large writes to the framebuffer
(which, back in the days, were not necessarily very fast). For
instance, if you're looking at a full screen image and you want to
brighten it, you could simply shift the color values in the colormaps
to raise the low values, rather than recompute and redraw all the
pixels.</p>

<p>(Apparently DirectColor was often used with 24-bit pixels, split
into one byte for each color, which is the same pixel layout as a
24-bit TrueColor visual; see eg <a href="https://starlink.eao.hawaii.edu/docs/sc15.htx/sc15se11.html">this section of the Starlink
Project's Graphics Cookbook</a>.
Also, <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/DirectColorHardware">this seems to be how the A/UX X server worked</a>. If you were going to do 8-bit pixels I
suspected people preferred PseudoColor to DirectColor.)</p>

<p>These days this is mostly irrelevant and the basic simplicity of
the TrueColor visual has won out. Well, what won out is PC graphics
systems that followed the same basic approach of fixed 24-bit RGB
color, and then X went along with it on PC hardware, which became
more or less the only hardware.</p>

<p>(<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/DirectColorHardware">There probably was hardware with DirectColor support</a>. While X on PC Unixes will probably still
claim to support DirectColor visuals, as reported in things like
xdpyinfo, I suspect that it involves software emulation. Although
these days you could probably implement DirectColor with GPU
shaders at basically no cost.)</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/unix/X11DirectColorVisualNotes?showcomments#comments">One comment</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/unix/X11DirectColorVisualNotes

---

*ID: b024069d2d83d74c*
*抓取时间: 2026-03-12T13:49:26.049097*
