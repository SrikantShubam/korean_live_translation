from flask import Flask, render_template
import requests
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    # Send request to endpoint and get response
    url = "http://localhost:8000/translate_text"
    files = {"file": ("k4 inverse.jpeg", open("k4 inverse.jpeg", "rb"), "image/jpeg")}
    response = requests.post(url, files=files)
    json_data = response.json()
    print(json_data['translated_text'])

    # Decode image data from response
    img_str = json_data['image']
    img_bytes = base64.b64decode(img_str)

    # Load image from bytes
    img = Image.open(BytesIO(img_bytes))

    # Save image to a temporary file
    img_path = 'static/uploaded/temp.jpg'
    img.save(img_path)

    # Render HTML template with the image
    return render_template('index.html', img_path=img_path,translation=json_data['translated_text'])

if __name__ == '__main__':
    app.run(debug=True)
