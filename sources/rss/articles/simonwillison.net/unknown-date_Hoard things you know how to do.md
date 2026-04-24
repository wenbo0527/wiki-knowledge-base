# Hoard things you know how to do

> 来源: simonwillison.net  
> 发布时间: 2026-02-26T20:33:27+00:00  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><em><a href="https://simonwillison.net/guides/agentic-engineering-patterns/">Agentic Engineering Patterns</a> &gt;</em></p>
    <p>Many of my tips for working productively with coding agents are extensions of advice I've found useful in my career without them. Here's a great example of that: <strong>hoard things you know how to do</strong>.</p>
<p>A big part of the skill in building software is understanding what's possible and what isn't, and having at least a rough idea of how those things can be accomplished.</p>
<p>These questions can be broad or quite obscure. Can a web page run OCR operations in JavaScript alone? Can an iPhone app pair with a Bluetooth device even when the app isn't running? Can we process a 100GB JSON file in Python without loading the entire thing into memory first?</p>
<p>The more answers to questions like this you have under your belt, the more likely you'll be able to spot opportunities to deploy technology to solve problems in ways other people may not have thought of yet.</p>
<p>Knowing that something is theoretically possible is not the same as having seen it done for yourself. A key asset to develop as a software professional is a deep collection of answers to questions like this, ideally illustrated by running code.</p>
<p>I hoard solutions like this in a number of different ways. My <a href="https://simonwillison.net">blog</a> and <a href="https://til.simonwillison.net">TIL blog</a> are crammed with notes on things I've figured out how to do. I have <a href="https://github.com/simonw">over a thousand GitHub repos</a> collecting code I've written for different projects, many of them small proof-of-concepts that demonstrate a key idea.</p>
<p>More recently I've used LLMs to help expand my collection of code solutions to interesting problems.</p>
<p><a href="https://tools.simonwillison.net">tools.simonwillison.net</a> is my largest collection of LLM-assisted tools and prototypes. I use this to collect what I call <a href="https://simonwillison.net/2025/Dec/10/html-tools/">HTML tools</a> - single HTML pages that embed JavaScript and CSS and solve a specific problem.</p>
<p>My <a href="https://github.com/simonw/research">simonw/research</a> repository has larger, more complex examples where I’ve challenged a coding agent to research a problem and come back with working code and a written report detailing what it found out.</p>
<h2 id="recombining-things-from-your-hoard">Recombining things from your hoard</h2>
<p>Why collect all of this stuff? Aside from helping you build and extend your own abilities, the assets you generate along the way become incredibly powerful inputs for your coding agents.</p>
<p>One of my favorite prompting patterns is to tell an agent to build something new by combining two or more existing working examples.</p>
<p>A project that helped crystallize how effective this can be was the first thing I added to my tools collection - a browser-based <a href="https://tools.simonwillison.net/ocr">OCR tool</a>, described <a href="https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/">in more detail here</a>.</p>
<p>I wanted an easy, browser-based tool for OCRing pages from PDF files - in particular PDFs that consist entirely of scanned images with no text version provided at all.</p>
<p>I had previously experimented with running the <a href="https://tesseract.projectnaptha.com/">Tesseract.js OCR library</a> in my browser, and found it to be very capable. That library provides a WebAssembly build of the mature Tesseract OCR engine and lets you call it from JavaScript to extract text from an image.</p>
<p>I didn’t want to work with images though, I wanted to work with PDFs. Then I remembered that I had also worked with Mozilla’s <a href="https://mozilla.github.io/pdf.js/">PDF.js</a> library, which among other things can turn individual pages of a PDF into rendered images.</p>
<p>I had snippets of JavaScript for both of those libraries in my notes.</p>
<p>Here’s the full prompt I fed into a model (at the time it was Claude 3 Opus), combining my two examples and describing the solution I was looking for:</p>
<div><textarea>This code shows how to open a PDF and turn it into an image per page:
```html
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
  &lt;title&gt;PDF to Images&lt;/title&gt;
  &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.9.359/pdf.min.js&quot;&gt;&lt;/script&gt;
  &lt;style&gt;
    .image-container img {
      margin-bottom: 10px;
    }
    .image-container p {
      margin: 0;
      font-size: 14px;
      color: #888;
    }
  &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;input type=&quot;file&quot; id=&quot;fileInput&quot; accept=&quot;.pdf&quot; /&gt;
  &lt;div class=&quot;image-container&quot;&gt;&lt;/div&gt;

  &lt;script&gt;
  const desiredWidth = 800;
    const fileInput = document.getElementById(&#x27;fileInput&#x27;);
    const imageContainer = document.querySelector(&#x27;.image-container&#x27;);

    fileInput.addEventListener(&#x27;change&#x27;, handleFileUpload);

    pdfjsLib.GlobalWorkerOptions.workerSrc = &#x27;https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.9.359/pdf.worker.min.js&#x27;;

    async function handleFileUpload(event) {
      const file = event.target.files[0];
      const imageIterator = convertPDFToImages(file);

      for await (const { imageURL, size } of imageIterator) {
        const imgElement = document.createElement(&#x27;img&#x27;);
        imgElement.src = imageURL;
        imageContainer.appendChild(imgElement);

        const sizeElement = document.createElement(&#x27;p&#x27;);
        sizeElement.textContent = `Size: ${formatSize(size)}`;
        imageContainer.appendChild(sizeElement);
      }
    }

    async function* convertPDFToImages(file) {
      try {
        const pdf = await pdfjsLib.getDocument(URL.createObjectURL(file)).promise;
        const numPages = pdf.numPages;

        for (let i = 1; i &lt;= numPages; i++) {
          const page = await pdf.getPage(i);
          const viewport = page.getViewport({ scale: 1 });
          const canvas = document.createElement(&#x27;canvas&#x27;);
          const context = canvas.getContext(&#x27;2d&#x27;);
          canvas.width = desiredWidth;
          canvas.height = (desiredWidth / viewport.width) * viewport.height;
          const renderContext = {
            canvasContext: context,
            viewport: page.getViewport({ scale: desiredWidth / viewport.width }),
          };
          await page.render(renderContext).promise;
          const imageURL = canvas.toDataURL(&#x27;image/jpeg&#x27;, 0.8);
          const size = calculateSize(imageURL);
          yield { imageURL, size };
        }
      } catch (error) {
        console.error(&#x27;Error:&#x27;, error);
      }
    }

    function calculateSize(imageURL) {
      const base64Length = imageURL.length - &#x27;data:image/jpeg;base64,&#x27;.length;
      const sizeInBytes = Math.ceil(base64Length * 0.75);
      return sizeInBytes;
    }

    function formatSize(size) {
      const sizeInKB = (size / 1024).toFixed(2);
      return `${sizeInKB} KB`;
    }
  &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;
```
This code shows how to OCR an image:
```javascript
async function ocrMissingAltText() {
    // Load Tesseract
    var s = document.createElement(&quot;script&quot;);
    s.src = &quot;https://unpkg.com/tesseract.js@v2.1.0/dist/tesseract.min.js&quot;;
    document.head.appendChild(s);

    s.onload = async () =&gt; {
      const images = document.getElementsByTagName(&quot;img&quot;);
      const worker = Tesseract.createWorker();
      await worker.load();
      await worker.loadLanguage(&quot;eng&quot;);
      await worker.initialize(&quot;eng&quot;);
      ocrButton.innerText = &quot;Running OCR...&quot;;

      // Iterate through all the images in the output div
      for (const img of images) {
        const altTextarea = img.parentNode.querySelector(&quot;.textarea-alt&quot;);
        // Check if the alt textarea is empty
        if (altTextarea.value === &quot;&quot;) {
          const imageUrl = img.src;
          var {
            data: { text },
          } = await worker.recognize(imageUrl);
          altTextarea.value = text; // Set the OCR result to the alt textarea
          progressBar.value += 1;
        }
      }

      await worker.terminate();
      ocrButton.innerText = &quot;OCR complete&quot;;
    };
  }
```
Use these examples to put together a single HTML page with embedded HTML and CSS and JavaScript that provides a big square which users can drag and drop a PDF file onto and when they do that the PDF has every page converted to a JPEG and shown below on the page, then OCR is run with tesseract and the results are shown in textarea blocks below each image.</textarea></div>
<p>This worked flawlessly! The model kicked out a proof-of-concept page that did exactly what I needed.</p>
<p>I ended up <a href="https://gist.github.com/simonw/6a9f077bf8db616e44893a24ae1d36eb">iterating with it a few times</a> to get to my final result, but it took just a few minutes to build a genuinely useful tool that I’ve benefited from ever since.</p>
<h2 id="coding-agents-make-this-even-more-powerful">Coding agents make this even more powerful</h2>
<p>I built that OCR example back in March 2024, nearly a year before the first release of Claude Code. Coding agents have made hoarding working examples even more valuable.</p>
<p>If your coding agent has internet access you can tell it to do things like:</p>
<p><div><textarea>Use curl to fetch the source of `https://tools.simonwillison.net/ocr` and `https://tools.simonwillison.net/gemini-bbox` and build a new tool that lets you select a page from a PDF and pass it to Gemini to return bounding boxes for illustrations on that page.</textarea></div>
(I specified <code>curl</code> there because Claude Code defaults to using a WebFetch tool which summarizes the page content rather than returning the raw HTML.)</p>
<p>Coding agents are excellent at search, which means you can run them on your own machine and tell them where to find the examples of things you want them to do:
<div><textarea>Add mocked HTTP tests to the `~/dev/ecosystem/datasette-oauth` project inspired by how `~/dev/ecosystem/llm-mistral` is doing it.</textarea></div>
Often that's enough - the agent will fire up a search sub-agent to investigate and pull back just the details it needs to achieve the task.</p>
<p>Since so much of my research code is public I'll often tell coding agents to clone my repositories to <code>/tmp</code> and use them as input:
<div><textarea>Clone `simonw/research` from GitHub to `/tmp` and find examples of compiling Rust to WebAssembly, then use that to build a demo HTML page for this project.</textarea></div>
The key idea here is that coding agents mean we only ever need to figure out a useful trick <em>once</em>. If that trick is then documented somewhere with a working code example our agents can consult that example and use it to solve any similar shaped project in the future.</p>
    
        <p>Tags: <a href="https://simonwillison.net/tags/coding-agents">coding-agents</a>, <a href="https://simonwillison.net/tags/ai-assisted-programming">ai-assisted-programming</a>, <a href="https://simonwillison.net/tags/generative-ai">generative-ai</a>, <a href="https://simonwillison.net/tags/agentic-engineering">agentic-engineering</a>, <a href="https://simonwillison.net/tags/ai">ai</a>, <a href="https://simonwillison.net/tags/llms">llms</a></p>

## 链接

https://simonwillison.net/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/#atom-everything

---

*ID: d0933fdad4d8a689*
*抓取时间: 2026-03-05T10:01:51.143478*
