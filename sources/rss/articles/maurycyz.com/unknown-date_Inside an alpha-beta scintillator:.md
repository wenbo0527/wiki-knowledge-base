# Inside an alpha-beta scintillator:

> 来源: maurycyz.com  
> 发布时间: Thu, 12 Feb 2026 00:00:00 +0000  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<!-- mksite: start of content -->

<p></p>

Just a heads up: this post is incomplete. 
However, it may be a while before I am able to finish it.
I am publishing it early in hopes that you will still find it somewhat interesting. 

<p>
I've recently acquired this tiny contamination monitor:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/ah.jpg" />
<center>Just 4 cm wide!</center>
<!-- snip -->
<p>
It's more sensitive then a <a href="https://ludlums.com/products/all-products/product/model-44-9">Ludlum 44-9</a>
despite being smaller then it's pancake style G-M tube. 
</p><p>
<em>After removing four hex screws</em>, the <a href="https://www.radviewdetection.com/abplus">AlphaHound</a> easily comes apart:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/open.jpg" />
<center>Oooo</center>
<p>
This is very nice: Many similarly sized devices are difficult or impossible to open without damaging them.
If it ever breaks, it won't be hard to get inside. 
</p><p>
<em>The top half</em> has the buzzer, display and buttons.
It does have some SMD components, but it's just voltage regulators and decoupling capacitors:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/screen1.jpg" />
<p>
The display is a <a href="https://www.crystalfontz.com/product/cfal128128a0015w-128x128-square-oled-display">Crystalfontz CFAL128128A0-015W</a> monochrome OLED:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/screen3.jpg" />
<p>
Neither the display or the PCB are mounted to anything:
They are held in place by pressure. 
Because of this, the back side of the PCB must be blank to avoid breaking the OLED display:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/screen2.jpg" />
<center>Wow, such component density.</center>
<p>
<em>The buttons</em> live on a tiny daughter board:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/buttons.jpg" />
<p>
These were a relatively late addition to the design, and are connected to the main PCB with a long ribbon cable.
Unlike everything else, this board is actually screwed in to the case:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/front_case.jpg" />
<p>
<em>The case itself</em> is 3D printed stainless steel, which is a reasonable choice for small volume products.
However, the resulting metal is porous and hard to clean.
(it's still an improvement over plastic in my book) 
</p><p>
The black tape is my doing: 
This detector was one of the first (of this version) made and it had a loose screen:
The tape takes up just enough space to keep things tight.
</p><p>
<em>The bottom half</em> connects to the top with a short ribbon-cable:
<p>
<img src="https://maurycyz.com/misc/ah_teardown/riser.jpg" />
</p>
Most of the board space is taken up by the battery, which is held in place by an FDM printed bracket glued to the board:
<p>
<img src="https://maurycyz.com/misc/ah_teardown/pcb.jpg" />
</p>
<em>The battery is the</em> <a href="https://www.adafruit.com/product/4237">LP552530</a>, a tiny 350 mA hour lithium polymer cell. 
This only provides a few hours of runtime, but there's only so much space in this thing.
</p><p>
There are no components under the battery: 
all the detector's electronics are contained within the tiny 3x2 cm section above it.
</p><p>
<em>The detector</em> is hidden underneath the board:
<p>
<img src="https://maurycyz.com/misc/ah_teardown/stack.jpg" />
</p>
Particles enter through the back, travel through both mylar sheets and hit the white square of scintillator material.
The square converts the radiation's energy into a flash of light, which is detected by two photodiodes on the back side of the board. 
</p><p>
To keep out stray light, the scintillator is mounted in a ring of black rubber, which makes contact with black foam glued to the PCB and mylar. 
When assembled, the foam is compressed and creates a light-proof seal against the rubber.
</p><p>
<em>The scintillator</em> is a sandwich of two different materials:
Silver dopped zinc sulfide painted onto polyvinyltoluene mixed with an organic phosphor (EJ-212).
</p><p>
The zinc sulfide detects alpha particles, and the plastic scintillator detects beta. 
Alphas will produce a <a href="https://maurycyz.com/projects/spinthariscope/">bright flash with a slow decay</a>, and betas produce a much faster and dimer flash.
The detector takes both of these factors into account to tell the difference between the two types of radiation.
</p><p>
<em>The MICROFC-60035-SMT-TR photodiodes</em> are very special:
Instead of being a single photodiode, these SiPM's have an array of tiny reverse biased diodes:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/sipm.png" />
<center>In practice, the capacitors are connected to a low-Z output.</center>
<p>
Each diode is run above its usual breakdown voltage, but they don't start conducting immediately.
However, once a free electron-hole pair is created, the electron is accelerated by the electric field and slams into silicon atoms.
These collisions are energetic enough to liberate more electrons: causing exponential "avalanche" breakdown.
</p><p>
<b>A single photon</b> is enough to make the diode start conducting. 
</p><p>
It's a similar principle to a G-M tube, just for visible light. 
Just like a G-M counter, the diode includes a quenching resistor which causes the voltage to drop once the discharge starts. 
This resets the photodiode so it can continue detecting light.
</p><p>
These detectors have quantum-limited performance &gt; 1 gigahertz bandwidth: 
something that's ordinarily <a href="https://lcamtuf.substack.com/p/shining-light-on-photodiodes">super difficult to do</a>.
</p><p>
A single avalanche diode isn't able to measure the intensity of a light flash, but the SiPM contains thousands of them:
The amplitude of the output pulse depends on how many diodes are triggered, which is proportional to the brightness of the light.
</p><p>
<em>There's also a tiny LED</em> which is used for a self test:
If the SiPMs are able to pick up a dim LED flash, they should be able to pick up particle events.
</p><p>
<em>Ok, back to the board:</em>
</p>
<img src="https://maurycyz.com/misc/ah_teardown/map.jpg" />
<center>A map of the hound</center>
<p>
<em>The microcontroller is the ATSAMD21G18</em>, a 32-bit ARM processor capable of running at up to 48 MHz.
That might sound slow, but it's actually quite powerful for an embedded system:
It doesn't have to run chrome. 
</p><p>
<em>The second largest chip is an ADXL335 accelerometer</em>. 
In earlier versions, this was used to control the device, but is being phased out due to it's high cost.
</p><p>
Most of the other chips are too small to have a full part number printed on, but they are mostly voltage regulators, comparators and opamps. 
</p><p>
<em>The top left</em> has a very standard boost converter: 
</p>
<img src="https://maurycyz.com/misc/ah_teardown/boost.png" />
<p>
This converts 3.3 volts into ~30 volts which is used to run the photodiodes. 
</p><p>
<em>I don't currently have a way to strip off the conformal coating</em> covering it, so I can't trace out the pulse processing circuit. 
However, I'm quite confident it uses a peak detector circuit to measure the height of the pulse:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/theory1.png" />
<center>Theoretical pulse detection scheme: Don't look too closely.</center>
<p>
This is a safe assumption because the microcontroller simply isn't fast enough to measure the 100 nanosecond scale pulses:
The ADC is only able to measure a voltage every ~3000 nanoseconds. 
</p><p>
The pulse shape discrimination is likely done by using an opamp integrator to time how long the pulse stays over a given threshold:
</p>
<img src="https://maurycyz.com/misc/ah_teardown/theory2.png" />
<center>Theoretical PSD scheme: Don't look too closely.</center>
<p>
This method produces similar pulse scatter plots to the real detector &mdash;
including the distinctive curve of the alpha cluster &mdash;
and is relatively simple...
</p><p>
... but I don't know if this is actually how it works. 
</p><p>
This section will be updated soon™.
</p>
<!--
<b>TODO: Get scope traces of pulse detector/discriminator circuit. </b>
Betting it's using time-over-threshold. 
</p><p>
# Electronics
</p><p>
Plastic decay time 2.4 ns, ZnS(Ag) 200 ns.
</p><p>
G2L: AP2202 voltage reulgator
</p><p>
ATSAMD21G18
-->
<!-- mksite: end of content -->

## 链接

https://maurycyz.com/misc/ah_teardown/

---

*ID: 8383c02fbd2bf0ee*
*抓取时间: 2026-03-05T10:02:14.134501*
