> For the complete documentation index, see [llms.txt](https://help.telebotstudio.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation.md).
# TBS Media Libraries (PIL & CV) Documentation
TeleBot Studio includes two built-in image-processing libraries, both available with no imports or setup required: \*\*`Lib.PIL`\*\* for general-purpose image editing, and \*\*`Lib.CV`\*\* for more advanced computer vision tasks, including face detection.
Both libraries work entirely in-memory — load an image from bytes, transform it, and send it straight back to Telegram, with no file system access needed.
\*\*\*
## Lib.PIL — Image Editing
`Lib.PIL` is a general-purpose image editing library, built on Pillow. Use it for resizing, cropping, drawing text and shapes, watermarking, filters, and combining images.
### I/O
\*\*`openFromBytes(image\_bytes)`\*\* Loads an image from raw bytes (e.g. from `Request.get(url).content`) and returns an image object.
\*\*`toBytes(image, format="JPEG", \*\*params)`\*\* Exports an image object back to bytes, ready to send with `Bot.sendPhoto()`. Supports any format Pillow can write (`"JPEG"`, `"PNG"`, `"WEBP"`, etc).
\*\*`createImage(width, height, color=(255, 255, 255))`\*\* Creates a new blank canvas of the given size and background color.
\*\*`createGradient(width, height, start\_color, end\_color, direction="horizontal")`\*\* Creates a two-color gradient image. `direction` can be `"horizontal"` or `"vertical"`.
```python
resp = Request.get("https://example.com/photo.jpg")
img = Lib.PIL.openFromBytes(resp.content)
Bot.sendPhoto(photo=Lib.PIL.toBytes(img, format="PNG"))
banner = Lib.PIL.createGradient(600, 200, (255, 0, 128), (0, 128, 255))
Bot.sendPhoto(photo=Lib.PIL.toBytes(banner))
```
### Transform
\*\*`resize(image, width=None, height=None, resample=None)`\*\* Resizes an image. Provide either `width` or `height` alone to scale proportionally, or both to set an exact size.
\*\*`crop(image, box)`\*\* Crops an image to a `(left, top, right, bottom)` box.
\*\*`rotate(image, angle, expand=False)`\*\* Rotates an image by `angle` degrees. Set `expand=True` to resize the canvas so nothing gets cut off.
\*\*`flip(image, direction="horizontal")`\*\* Flips an image. `direction` can be `"horizontal"` or `"vertical"`.
```python
img = Lib.PIL.resize(img, width=400)
img = Lib.PIL.crop(img, (0, 0, 300, 300))
img = Lib.PIL.rotate(img, 90, expand=True)
img = Lib.PIL.flip(img, "vertical")
```
### Adjustments & Filters
\*\*`adjustBrightness(image, factor)`\*\* / \*\*`adjustContrast(image, factor)`\*\* / \*\*`adjustColor(image, factor)`\*\* / \*\*`adjustSharpness(image, factor)`\*\* Adjusts the given property. `factor=1.0` is unchanged, `<1.0` decreases, `>1.0` increases.
\*\*`applyFilter(image, filter\_type)`\*\* Applies a named filter. Supported values: `"blur"`, `"sharpen"`, `"grayscale"`, `"contour"`, `"emboss"`, `"edge\_enhance"`, `"smooth"`, `"detail"`, `"find\_edges"`.
\*\*`invert(image)`\*\* Inverts all colors in the image.
```python
img = Lib.PIL.adjustBrightness(img, 1.3)
img = Lib.PIL.adjustContrast(img, 1.2)
img = Lib.PIL.applyFilter(img, "blur")
img = Lib.PIL.invert(img)
```
### Composition
\*\*`composite(image1, image2, mask=None)`\*\* Combines two images using a mask. If no mask is given, blends them evenly.
\*\*`paste(base\_image, image\_to\_paste, position=(0, 0), mask=None)`\*\* Pastes one image onto another at the given position.
\*\*`blend(image1, image2, alpha=0.5)`\*\* Blends two images together. `alpha` controls the mix ratio (`0.0` = all `image1`, `1.0` = all `image2`).
\*\*`addBorder(image, border, color="black")`\*\* Adds a solid border of `border` pixels around the image.
\*\*`addWatermark(image, watermark, position=None, opacity=1.0)`\*\* Overlays a watermark image. If `position` is omitted, it's placed in the bottom-right corner.
\*\*`applyMask(image, mask)`\*\* Applies a grayscale mask as the image's transparency (alpha channel).
```python
canvas = Lib.PIL.createImage(300, 100, (255, 255, 255))
watermark = Lib.PIL.createImage(60, 30, (255, 0, 0))
result = Lib.PIL.addWatermark(canvas, watermark, opacity=0.6)
result = Lib.PIL.addBorder(result, 10, "gold")
```
### Drawing
\*\*`drawText(image, text, position, color=(255, 255, 255), font\_size=20, font\_path=None)`\*\* Draws text onto an image at the given `(x, y)` position.
\*\*`drawRectangle(image, xy, outline="black", fill=None, width=1)`\*\* / \*\*`drawCircle(image, xy, outline="black", fill=None, width=1)`\*\* / \*\*`drawLine(image, xy, fill="black", width=1)`\*\* Draws a rectangle, circle (ellipse), or line, given the appropriate coordinates.
```python
img = Lib.PIL.drawText(img, "Winner!", (20, 20), color=(255, 255, 0), font\_size=32)
img = Lib.PIL.drawRectangle(img, [10, 10, 200, 100], outline="red", width=3)
img = Lib.PIL.drawCircle(img, [50, 50, 150, 150], outline="blue", width=3)
```
### Channels & Modes
\*\*`convertMode(image, mode)`\*\* Converts the image's color mode (e.g. `"RGB"`, `"L"` for grayscale, `"RGBA"`).
\*\*`splitChannels(image)`\*\* / \*\*`mergeChannels(r, g, b)`\*\* Splits an image into its individual color channels, or merges three channels back into one image.
\*\*`getSize(image)`\*\* Returns `(width, height)`.
```python
gray = Lib.PIL.convertMode(img, "L")
r, g, b = Lib.PIL.splitChannels(img)
merged = Lib.PIL.mergeChannels(r, g, b)
width, height = Lib.PIL.getSize(img)
```
\*\*\*
## Lib.CV — Computer Vision
`Lib.CV` is built on OpenCV, for more advanced image processing — geometric transforms, thresholding, edge detection, and real face detection.
Images in `Lib.CV` are handled as NumPy arrays, in BGR color order internally — but every method's `color` parameter accepts standard RGB tuples, so you never need to think about the conversion yourself.
### I/O
\*\*`readImage(image\_bytes)`\*\* Decodes an image from raw bytes into a NumPy array.
\*\*`toBytes(image, format=".jpg", params=None)`\*\* Encodes an image array back to bytes. `format` is a file extension string, e.g. `".jpg"` or `".png"`.
\*\*`createBlank(width, height, color=(255, 255, 255))`\*\* Creates a new blank image of the given size and color.
```python
resp = Request.get("https://example.com/photo.jpg")
img = Lib.CV.readImage(resp.content)
Bot.sendPhoto(photo=Lib.CV.toBytes(img, format=".png"))
```
### Geometry & Color
\*\*`resize(image, width=None, height=None)`\*\* Resizes an image, scaling proportionally if only one dimension is given.
\*\*`rotate(image, angle)`\*\* Rotates an image by `angle` degrees around its center.
\*\*`perspectiveTransform(image, src\_points, dst\_points)`\*\* Warps an image by mapping four source points to four destination points.
\*\*`convertColor(image, conversion\_type)`\*\* Converts color space. Supported values: `"gray"`, `"rgb"`, `"hsv"`, `"hls"`, `"lab"`.
\*\*`threshold(image, thresh\_value=127, max\_value=255, type="binary")`\*\* Applies a fixed threshold. `type` can be `"binary"`, `"binary\_inv"`, `"trunc"`, `"tozero"`, `"tozero\_inv"`.
\*\*`adaptiveThreshold(image, max\_value=255, block\_size=11, c=2)`\*\* Applies a locally-adaptive threshold, useful for images with uneven lighting.
```python
img = Lib.CV.resize(img, width=320)
gray = Lib.CV.convertColor(img, "gray")
thresh = Lib.CV.threshold(gray, 127, 255, "binary")
```
### Filters & Effects
\*\*`applyFilter(image, filter\_type)`\*\* Applies a named filter. Supported values: `"blur"`, `"sharpen"`, `"grayscale"`, `"sepia"`, `"invert"`, `"emboss"`.
\*\*`detectEdges(image, threshold1=100, threshold2=200)`\*\* Runs Canny edge detection.
\*\*`morphOperations(image, operation, kernel\_size=5)`\*\* Applies a morphological operation. `operation` can be `"erode"`, `"dilate"`, `"open"`, `"close"`, `"gradient"`.
\*\*`blendImages(image1, image2, alpha=0.5)`\*\* Blends two images together, resizing `image2` to match `image1` if needed.
```python
blurred = Lib.CV.applyFilter(img, "blur")
edges = Lib.CV.detectEdges(img)
dilated = Lib.CV.morphOperations(thresh, "dilate", kernel\_size=3)
```
### Drawing & Contours
\*\*`drawText(image, text, position, color=(255, 255, 255), font\_scale=1.0, thickness=2)`\*\* Draws text onto an image.
\*\*`drawRectangle(image, pt1, pt2, color=(0, 0, 0), thickness=2)`\*\* Draws a rectangle between two corner points.
\*\*`findContours(image, mode="external", method="simple")`\*\* Finds contours (outlines of shapes) in an image. Returns a list of contours.
\*\*`drawContours(image, contours, color=(0, 255, 0), thickness=2)`\*\* Draws a list of contours (as returned by `findContours`) onto an image.
```python
img = Lib.CV.drawText(img, "Detected", (10, 30), color=(255, 0, 0))
img = Lib.CV.drawRectangle(img, (20, 40), (150, 120), color=(0, 255, 0))
contours = Lib.CV.findContours(thresh)
img = Lib.CV.drawContours(img, contours, color=(255, 0, 255))
```
### Face Detection
\*\*`detectFaces(image)`\*\* Detects faces in an image using Haar cascade detection. Returns a list of `(x, y, width, height)` bounding boxes.
\*\*`drawFaces(image, faces, color=(0, 255, 0), thickness=2)`\*\* Draws bounding boxes around a list of detected faces (as returned by `detectFaces`).
```python
faces = Lib.CV.detectFaces(img)
Bot.sendMessage(text=f"Found {len(faces)} face(s)")
img = Lib.CV.drawFaces(img, faces, color=(0, 255, 255), thickness=3)
Bot.sendPhoto(photo=Lib.CV.toBytes(img))
```
\*\*\*
## Choosing Between PIL and CV
Both libraries can resize, crop, blend, and draw on images — for most everyday editing tasks (watermarks, text overlays, filters, memes), \*\*`Lib.PIL`\*\* is the simpler choice and has a more complete set of composition tools (masks, watermarking, channel splitting).
Reach for \*\*`Lib.CV`\*\* specifically when you need:
\* Face detection
\* Contour/shape detection
\* Perspective transforms
\* Adaptive thresholding for uneven lighting
\* More advanced morphological operations
Both libraries can be used together in the same command — decode an image once, and pass it between `Lib.PIL` and `Lib.CV` methods as needed for your use case.
---
# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.
## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.
Perform an HTTP GET request on the current page URL with the `ask` query parameter, and the optional `goal` query parameter:
```
GET https://help.telebotstudio.com/tbs-media-libraries-pil-and-cv-documentation.md?ask=&goal=
```
`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is optional and describes the broader end goal you are ultimately trying to accomplish on behalf of the user. GitBook uses it to tailor the answer towards what is most useful for that goal.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.
Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
