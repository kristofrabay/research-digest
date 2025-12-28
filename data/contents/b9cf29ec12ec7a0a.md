# How to add PDF understanding to your AI Agent

**URL:** https://www.asterlabs.ai/blog/pdf-understanding
**Published:** 2024-12-15T07:46:56.000Z

---

## Summary

The webpage explains how to add PDF understanding to an AI Agent by leveraging **multimodal** capabilities of modern LLMs like GPT-4V, Claude vision, and Gemini.

The core solution involves:
1.  **Text Extraction:** Converting the readable text from the PDF into a string using tools like `PyMuPDF` (Python) or `pdf-parse` (JavaScript).
2.  **Image Conversion:** Converting each page of the PDF into an image format (PNG) so that vision models can process the visual layout.

The article highlights that relying solely on traditional OCR loses crucial context like table structure and image information. By sending **both the extracted text and the page images** to a multimodal LLM, the agent achieves a much better understanding of the document's content. The ordering of text and images in the prompt matters, with Anthropic preferring images before text, and OpenAI preferring text before images.

For **Retrieval Augmented Generation (RAG)** applications, the process extends to:
*   Chunking both the text and LLM-generated descriptions of the content.
*   Generating embeddings for retrieval.
*   Storing the corresponding image file path with the text chunk so that relevant images can be retrieved and passed to the LLM alongside the text during a query.

---

## Full Content

How to add PDF understanding to your AI Agent | Aster Labs
# How to add PDF understanding to your AI Agent
December 15, 2024
Anthropic recently announced[PDF support](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support)for their API.
Based on my research and Anthropic&#x27;s docs, the approach they used matches what I&#x27;ve done personally to add PDF understanding to my Agent workflows. It works well, like kind of insanely well... especially when combined with tool calling (future post coming on that).
Let&#x27;s walk through how it&#x27;s built, and how you can implement it in your own agents.
## [](#the-challenge)The Challenge
LLMs can&#x27;t directly process PDFs so we need to convert them into a format that can be sent to an LLM API in a chat completion. The simplest approach, where a lot of people start, is to use an OCR library (i.e.[Tesseract](https://github.com/tesseract-ocr/tesseract)) to extract the readable text from the PDF and send that to the LLM.
The issue with &quot;traditional&quot; OCR is that it loses a lot of context from the PDF. For example:
* Tables are converted to text, losing the structure of the table... especially when it comes to headers and labels.
* Images are mostly ignored, which can be a problem if the PDF contains important visual information.
* The relationship between text elements is lost... for example, if there&#x27;s a checkbox with a label, the OCR may grab the label but will likely miss the checkbox.
Complicating things further, when you OCR a PDF and then send it to an LLM with a prompt, you don&#x27;t actually know if issues in understanding the content are due to bad OCR or the LLM (or both).
## [](#the-solution)The Solution
What a number of LLM researchers have figured out over the last year is that vision models are actually really good at understanding images of documents. And it makes sense that some significant portion of multi-modal LLM training data is images of pages of documents... the internet is full of them.
So in addition to extracting the text, if we can also convert the document&#x27;s pages to images then we can send BOTH to the LLM and get a much better understanding of the document&#x27;s content.
In the case of a 2-page PDF document, the prompt ends up looking like this:
```
`readable\_pdf\_text=&quot;...&quot;response=client.chat.completions.create(model=&quot;gpt-4o&quot;,messages=[{&quot;role&quot;:&quot;user&quot;,&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:f&quot;Summarize the following document: {readable\_pdf\_text}&quot;,},{&quot;type&quot;:&quot;image\_url&quot;,&quot;image\_url&quot;:{&quot;url&quot;:f&quot;data:image/png;base64,{base64\_image}&quot;},},{&quot;type&quot;:&quot;image\_url&quot;,&quot;image\_url&quot;:{&quot;url&quot;:f&quot;data:image/png;base64,{base64\_image}&quot;},},],}],)print(response.choices[0])`
```
NOTE: Ordering the message types properly does matter! And it differs depending on which LLM provider you&#x27;re using.
OpenAI prefers text before images, while Anthropic prefers images before text. Anthropic provides specific context for this in their docs:
```
`Justaswithdocument-queryplacement,Claudeworksbestwhenimagescomebeforetext.Imagesplacedaftertextorinterpolatedwithtextwillstillperformwell,butifyourusecaseallowsit,werecommendanimage-then-textstructure.`
```
## [](#the-implementation)The Implementation
There are two basic parts to the implementation:
1. Text extraction - converting readable text from the PDF to a string.
2. Image conversion - converting each page of the PDF to an image.
From a code and infrastructure standpoint, you can implement the functionality in javascript or python. However, I could not find a good way to do the image extraction in a serverless javascript environment like Vercel. Any javascript libraries with dependencies on`&lt;canvas&gt;`seemed to work locally, but would either overflow container image size limits or just fail to run in Vercel serverless functions.
So I ended up using a Python Flask endpoint on Vercel to handle the image conversion.
### [](#text-extraction)Text Extraction
In python, I use`PyMuPDF`([https://pymupdf.readthedocs.io/en/latest/index.html](https://pymupdf.readthedocs.io/en/latest/index.html)) for text extraction. It&#x27;s built on top of Tesseract, and provides a clean API for extracting text content.
In javascript, I use`pdf-parse`to extract the text content... it&#x27;s built on top of`PDF.js`([https://github.com/mozilla/pdf.js](https://github.com/mozilla/pdf.js)) from Mozilla.
Implementation is super simple... here&#x27;s a function that extracts the text from a base64 encoded PDF:
```
`asyncfunctionprocessPDFContent(pdfDataUrl){try{// Extract base64 data from data URLconstbase64Data=pdfDataUrl.split(&#039;,&#039;)[1];// Convert base64 to bufferconstpdfBuffer=Buffer.from(base64Data,&#039;base64&#039;);// Parse PDFconstdata=awaitpdfParse(pdfBuffer);// Return the extracted textreturndata.text;}catch(error){console.error(&#039;Error processing PDF:&#039;,error);return&#039;[Error extracting PDF content]&#039;;}}`
```
### [](#image-extraction)Image Extraction
Images are where it gets a bit more complicated.
In python, you can still use`PyMuPDF`to convert the pages to images. The only decision to make is the resolution of the image.
Anthropic and OpenAI both do automatic resizing down to the maximum size accepted by their APIs, so I just try to match the aspect ratio of a standard document.
I did try a few different javascript libraries, but ultimately settled on using a python Flask endpoint in Vercel. Here&#x27;s a reference example project for their python support:[GitHub](https://github.com/vercel/examples/tree/main/python/flask3).
The specific dependencies that I got working in`requirements.txt`are:
```
`Flask==3.0.3gunicorn==22.0.0PyMuPDF==1.24.7Werkzeug==3.0.3`
```
NOTE: Vercel&#x27;s deployment of python functions is really, really dumb. All code from your entire project is deployed alongside the actual python function, which immediately caused`Error:TheServerlessFunction...exceedsthemaximumsizelimit`problems.
The fix is to manually exclude file paths from the deployment of your python functions in your`vercel.json`file, like this:
```
`&quot;functions&quot;:{&quot;api/\*\*/\*.py&quot;:{&quot;memory&quot;:1024,&quot;excludeFiles&quot;:&quot;{public/\*\*,\*\*/node\_modules/\*\*,src/\*\*,python/\*\*,docs/\*\*}&quot;}}`
```
Ok. Now that you can get a python Flask endpoint running on Vercel, let&#x27;s look at the code for the image conversion.
It&#x27;s pretty straightforward:
```
`fromflaskimportFlask,request,jsonifyimportpymupdfimportbase64app=Flask(\_\_name\_\_)@app.route(&quot;/api/transformers/pdfToPNG&quot;,methods=[&#039;POST&#039;])defpdf\_to\_png():try:#Getthepagelimitparameter(optional)page\_limit=request.args.get(&#039;limit&#039;,type=int)#GetPDFdatafromrequestpdf\_bytes=base64.b64decode(request.json[&#039;base64&#039;])#ReadthePDFfilepdf\_file=pymupdf.open(&quot;pdf&quot;,pdf\_bytes)#Determinehowmanypagestoprocesstotal\_pages=pdf\_file.page\_countpages\_to\_process=min(total\_pages,page\_limit)ifpage\_limitelsetotal\_pages#ConvertpagestoPNGimages=[]forpage\_numinrange(pages\_to\_process):page=pdf\_file[page\_num]#Renderpagetoanimagewithproperaspectratiotomatchastandarddocumentpix=page.get\_pixmap(matrix=pymupdf.Matrix(1.7,2.0))#GetPNGbytesandconverttobase64img\_bytes=pix.tobytes(&quot;png&quot;)base64\_image=base64.b64encode(img\_bytes).decode()images.append({&#039;page&#039;:page\_num+1,&#039;data&#039;:base64\_image})pdf\_file.close()returnjsonify({&#039;total\_pages&#039;:total\_pages,&#039;pages\_converted&#039;:pages\_to\_process,&#039;images&#039;:images})exceptExceptionase:returnjsonify({&#039;error&#039;:str(e)}),500`
```
## [](#next-steps)Next Steps
So far, we&#x27;ve only focused on one-time processing of a PDF. This works well if your agent only needs to process the PDF once, or if your user is uploading the file in a specific chat conversation.
However, we should also consider the scenario where PDFs are needed for RAG (Retrieval Augmented Generation). For example, if your agent needs to understand the full contents of a PDF across many different conversations, you&#x27;ll want to pre-process the PDF once and then retrieve it when relevant.
The core tenets of text and image extraction are the same, but for RAG, we need to store them in chunks so the agent can retrieve the most relevant parts of the file as needed.
There are a ton of options for how to approach this, but I&#x27;ll focus on the simplest approach that&#x27;s worked for me across different use cases:
1. Extract the text and images from the PDF.
2. Use an LLM to generate an inventory of contents and descriptions for each page.
3. Chunk both the text and the generated descriptions.
4. Generate embeddings for the text and descriptions.
5. Store the image file path in the same row as the chunk and embeddings.
6. When running semantic search, retrieve both the text chunk and the image file and pass them both to the LLM in a message.
This implies page-size chunks, but you may also find the need to introduce semantic chunking where you identify logical breakpoints in the document that span 1 or multiple pages.
With semantic chunking you may end up needing multiple image files per chunk, but that&#x27;s okay - I&#x27;ve seen good performance even if the images include contents of other chunks. A rough rule of thumb is not to include more than 5 images (so 5 different pages) in a single chunk, because the LLM starts to lose ability to accurately gather info from every page. This is just my experience, and your mileage may vary.
## [](#conclusion)Conclusion
Adding PDF understanding to your AI agent doesn&#x27;t have to be intimidating. The combination of text extraction and image conversion gives you a robust foundation that works surprisingly well with multi-modal LLMs.
The key takeaways:
* Don&#x27;t rely on OCR alone - you&#x27;ll miss important context and structure
* Use both text extraction and image conversion to get the full picture
* Consider your deployment environment early (serverless has limitations)
* For RAG applications, think about how you&#x27;ll store and retrieve both text and images
I&#x27;ve found this approach to be incredibly reliable across different types of PDFs - from simple text documents to complex forms and technical diagrams. The extra effort to implement image conversion alongside text extraction pays off in much more accurate and context-aware responses from your agent.
Feel free to use the code examples above as a starting point for your own implementation. And if you run into any issues or have questions, reach out to me on[Twitter/X](https://x.com/cpdough).
