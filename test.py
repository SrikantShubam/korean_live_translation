from googletrans import Translator
from io import BytesIO
import os 
import easyocr
from PIL import Image, ImageDraw
import psutil
import requests
# os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# import torch
# print(torch.cuda.is_available())
pid = os.getpid()

# Create a Process object for the current process
process = psutil.Process(pid)

# Get the memory info for the process
mem_info = process.memory_info()
img='k4 inverse.jpeg'
# Load an image and perform OCR on it
image = Image.open(img)

# image = Image.open(BytesIO(response.content))

reader = easyocr.Reader(['ko','en'], gpu=True)
result = reader.readtext(img)
# print(result)

draw = ImageDraw.Draw(image)
for bbox, _, _ in result:
    bbox = [(int(point[0]), int(point[1])) for point in bbox]
    # print(bbox)
    draw.polygon(tuple(bbox), outline='red', width=2)
    # print(type(bbox))


image.show()
text_values = [text for _, text, _ in result]
print(text_values)

translator = Translator()

for i in text_values:
    translation = translator.translate(i, dest='en')
    print(translation.text)

# Print total memory used in megabytes
print(f"Memory usage: {mem_info.rss/1000000} mb")
