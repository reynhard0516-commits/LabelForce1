# app/workers/tasks.py
from app.workers.queue import q
from PIL import Image
import time, os

def prelabel_image(path: str):
    """
    A simple CPU placeholder that returns a bbox based on image size.
    In production, replace with model inference.
    """
    try:
        im = Image.open(path)
        w,h = im.size
        bbox = [int(w*0.1), int(h*0.1), int(w*0.9), int(h*0.9)]
    except Exception:
        bbox = [50,50,200,150]
    return {"bboxes":[{"label":"object","bbox":bbox,"confidence":0.8}]}

def enqueue_prelabel(path: str):
    return q.enqueue(prelabel_image, path)
