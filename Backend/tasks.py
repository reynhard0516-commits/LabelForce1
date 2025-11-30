from redis import Redis
from rq import Queue
from PIL import Image
import time, os, json

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
r = Redis.from_url(redis_url)
q = Queue('default', connection=r)

def prelabel_image(path):
    time.sleep(1)
    try:
        im = Image.open(path)
        w,h = im.size
        bbox = [int(w*0.1), int(h*0.1), int(w*0.8), int(h*0.8)]
    except Exception:
        bbox = [50,50,200,150]
    return {'bboxes': [{'label':'demo','bbox':bbox,'confidence':0.85}]}
