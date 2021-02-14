from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from stackapi import StackAPI
import json
from math import floor


THREE_FOUR_SIX = 346
FOUR_HUNDRED = 400

def get_data(question_id):
    data = {}
    SITE = StackAPI('codegolf')

    answers = SITE.fetch('questions/{ids}/answers', 
                        ids=[question_id], 
                        filter='!*SU8CGYZitCB.D*(BDVIficKj7nFMLLDij64nVID)N9aK3GmR9kT4IzT*5iO_1y3iZ)6W.G*')

    for answer in answers["items"]:

        soup = BeautifulSoup(answer["body"], features="lxml")
        try:
            title = soup.body.h1.text
            raw_parts = title.split(",")
            components = []
            count = 0
            for i in raw_parts:
                if count:
                    components.extend(i.split())
                else:
                    count = 1
            bytecount = str(min([int(i) for i in components if i.isnumeric()]))
            data[parts[0]] = bytecount
        except:pass
        
    return data


def get_offset(n):
    current_max = 1
    current_count = 0
    current_n = 0

    while True:
        current_n += 1
        current_count += 1

        if current_count == n + 1:
            y, x = current_max, current_n
            break
        if current_n == current_max:
            current_max += 1
            current_n = 0
        
    return x-1, y-1, current_max


def add_lang(draw,n,max_n,name,lang_data):
    try:
        data = lang_data["languages"][name]
    except:
        data = {
            "primary color":"#ffffff",
            "secondary color":"#000000",
            "font":"ArialUnicodeMS"
        }
    
     
    column, row, _ = get_offset(n)

    x = THREE_FOUR_SIX*2 * column + THREE_FOUR_SIX * (max_n - row)
    y = 600 * row
    size = 1
       
    font = ImageFont.truetype("fonts/" + data.get("font", "ArialUnicodeMS") + ".ttf", size=size)

    draw.polygon([(692+x,200+y),(THREE_FOUR_SIX+x,y),(x,200+y),(x,600+y),(THREE_FOUR_SIX+x,800+y),(692+x,600+y)],fill=data["primary color"])
    while ((font.getsize(name)[0] < 650) and (font.getsize(name)[1] < 370)):
        size += 1
        font = ImageFont.truetype(f"fonts/{font_name}.ttf",size=size)

    size = floor(size*0.9)
    font = ImageFont.truetype(f"fonts/{font_name}.ttf",size=size)

    
    w, h = font.getsize(name)
    offset_x, offset_y = font.getoffset(name)
    if name.upper() != name:
        _, h = font.getsize('a')
        _, offset_y = font.getoffset('a')
    
    w += offset_x
    h += offset_y

    coords = (x+(THREE_FOUR_SIX-w//2),y+FOUR_HUNDRED-h//2)#-floor(h*0.15))
    #draw.rectangle([coords,(coords[0]+w,coords[1]+h)],fill="#00000000",outline="yellow",width=2)
    draw.text(coords,name,fill=data["secondary color"],font=font)
    #draw.line([(coords[0],coords[1]+h//2),(coords[0]+w,coords[1]+h//2)],fill=(255,0,255),width=2)
    


if __name__ == "__main__":
    
    

    data = get_data(58615)
    '''
    data = {
        "05AB1E":"6",
        "Vyxal":"5",
        "J":"7",
        "Python 3":"67",
        "MAWP":"85",
        "Limn":"178",
        "Lua":"35",
        "Scheme":"183",
        "Malbolge":"72",
        "PHP":"91",
        "APL":"6",
        "Python 2":"65",
        "JavaScript (ES6)":"64",
        "R":"85",
        "Haskell":"90",
        "x86-16 machine code":"130",
        "PowerShell":"129",
        "asm2bf":"136",
        "naz":"158"
    }
    '''
    sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: int(item[1]))}

    ima_size_x, ima_size_y, max_ = get_offset(len(data.keys()))
    ima = Image.new('RGB',((max_-1) * 792,(ima_size_y + 2) * 600),"#36393E")
    draw = ImageDraw.Draw(ima)


    q, max_n, _ = get_offset(len(data.keys()))
    with open("data.json","r") as f:
        lang_data = json.load(f)
    #print(sorted_data)
    for i in range(len(data.keys())):
        add_lang(draw,i,max_n,list(sorted_data.keys())[i],lang_data)

    ima.show()
