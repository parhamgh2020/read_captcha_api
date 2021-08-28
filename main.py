import easyocr
from fastapi import FastAPI
import base64
from pydantic import BaseModel
import io
from PIL import Image
from yaml import reader


app = FastAPI()

reader = easyocr.Reader(['en'])


class Captcha(BaseModel):
    image_byte: str


@app.get('/')
def hello():
    return {"instruction": "type 'docs' at the end of the url"}


@app.post("/")
async def create_item(captcha: Captcha):
    image_byte = captcha.image_byte
    b = base64.b64decode(image_byte)
    img = Image.open(io.BytesIO(b))
    text = reader.readtext(img, detail=0)
    return {'number': text[0]}
