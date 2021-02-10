from PIL import Image, ImageDraw
from bs4 import BeautifulSoup
from stackapi import StackAPI


def get_data(question_id):
    data = {}
    SITE = StackAPI('codegolf')

    answers = SITE.fetch('questions/{ids}/answers', ids=[
                         question_id], filter='/2.2/filters/create?include=husk is:answer created:1m&unsafe=false')

    for answer in answers["items"]:

        soup = BeautifulSoup(answer["body"], features="lxml")
        try:
            title = soup.body.h1.text
        except:pass
        parts = ''.join(c for c in title if c.isalnum() or c.isspace()).split()
        bytecount = min([i for i in parts if i.isnumeric()])
        data[parts[0]] = bytecount

    return data


def get_offset(n):
    current_max = 1
    current_count = 0
    current_n = 0

    while True:
        current_n += 1
        current_count += 1

        if current_count == n + 1:
            y = current_max
            x = current_n
            break
        if current_n == current_max:
            current_max += 1
            current_n = 0
        
    return x-1, y-1


def add_lang(draw,n,max_n,name,color1,color2):
    column, row = get_offset(n)

    x = 346*2 * column + 346 * (max_n - row)
    y = 600 * row

    draw.polygon([(692+x,200+y),(346+x,y),(x,200+y),(x,600+y),(346+x,800+y),(692+x,600+y)],fill=color1)


if __name__ == "__main__":
    
    ima = Image.new('RGB',(15000,15000))
    draw = ImageDraw.Draw(ima)

    data = get_data(58615)

    sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: int(item[1]))}

    q, max_n = get_offset(len(data.keys()))
    #print(sorted_data)
    for i in range(len(data.keys())):
        add_lang(draw,i,max_n,list(sorted_data.keys())[i],255,128)

    ima.show()
