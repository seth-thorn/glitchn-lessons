import os, sys, json, numpy as np
from PIL import Image
from chips import *
from lib import to_uint8, OX, OY
info=json.load(open(os.path.join(os.path.dirname(__file__), 'info.json')))
def card_box(chip):
    b=info[chip]['bb']; cx=(b[0]+b[2])/2; cy=(b[1]+b[3])/2
    return (round(cx-1274), round(cy-1048), round(cx-1274)+2548, round(cy-1048)+2096)
def crop(can, box):
    x0,y0,x1,y1=box; return to_uint8(can)[y0-OY:y1-OY, x0-OX:x1-OX]
if __name__=='__main__':
    cls={'4040':C4040,'40106':C40106,'4051':C4051,'4021':C4021}[sys.argv[1]]; c=cls()
    ims=[Image.fromarray(crop(c.frame(float(t)),card_box(sys.argv[1]))).resize((637,524),Image.LANCZOS) for t in sys.argv[2:]]
    W=Image.new('RGB',(637*len(ims),524)); [W.paste(im,(i*637,0)) for i,im in enumerate(ims)]; W.save('/tmp/claude-0/test.png')
