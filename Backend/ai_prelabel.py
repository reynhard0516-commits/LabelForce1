import random
from PIL import Image

def run_prelabel(image_path):
    try:
        im = Image.open(image_path)
        w,h = im.size
        bbox = [int(w*0.1), int(h*0.1), int(w*0.8), int(h*0.8)]
    except Exception:
        bbox = [50,50,200,150]
    return {'boxes':[{'label':'demo','bbox':bbox,'confidence': round(random.uniform(0.6,0.95),2)}]}
