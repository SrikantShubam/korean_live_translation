from fastapi import FastAPI, File, UploadFile
from googletrans import Translator
import easyocr
from PIL import Image,ImageDraw
from io import BytesIO
import base64
app = FastAPI()

@app.post("/translate_text")
async def translate_text(file: UploadFile = File(...)):
    # Load image from file
    contents = await file.read()
    img = Image.open(BytesIO(contents))
 

    # img.show()    
    # Perform OCR on image
    reader = easyocr.Reader(['ko','en'], gpu=True)
    result = reader.readtext(img)
    draw = ImageDraw.Draw(img)
    for bbox, _, _ in result:
        bbox = [(int(point[0]), int(point[1])) for point in bbox]
        # print(bbox)
        draw.polygon(tuple(bbox), outline='red', width=2)
    # Extract text from result
    text_values = [text for _, text, _ in result]

    # Translate text to English
    translator = Translator()
    translations = []
    for i in text_values:
        translation = translator.translate(i, dest='en')
        translations.append(translation.text)
       # Encode image with polygon
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())     
    return {"original_text": text_values, "translated_text": translations, "image": img_str.decode('utf-8')}
