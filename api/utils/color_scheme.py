#!/usr/bin/python
from PIL import Image, ImageDraw
import random
import sys


def is_sim(k, p):
    if abs(k[0] - p[0])<25 and abs(k[1] - p[1])<25 and abs(k[2] - p[2])<25:
        return True
    return False


def main():
    name_of_start_img = sys.argv[1]
    num_of_finish_colors = int(sys.argv[2])
    num_of_start_color = int(sys.argv[3])

    png = Image.open(name_of_start_img)
    png.load()

    img = Image.new("RGB", png.size, (255, 255, 255))
    img.paste(png, mask=png.split()[3])

    w, h = img.size

    start_colors = {}
    obj = img.load()

    for i in range(w):
        for j in range(h):
            if start_colors.get(obj[i, j], None):
                start_colors[obj[i, j]] += 1
            else:
                start_colors[obj[i, j]] = 1

    colors_key_all = sorted(start_colors.keys(), key=lambda key: start_colors[key], reverse=True)[:num_of_start_color] 

    most_often_colors = []
    finish_colors = {}

    for k in colors_key_all:
        if not len(most_often_colors):
            finish_colors[k] = start_colors[k]
            most_often_colors.append(k)
        else:
            flag = True
            for p in most_often_colors:
                if is_sim(k, p):
                    finish_colors[p] += start_colors[k]
                    flag = False
                    break;
            if flag:
                finish_colors[k] = start_colors[k]
                most_often_colors.append(k)

    '''for k in sorted(finish_colors.keys(), key=lambda key: finish_colorsfinish_colors[key], reverse=True):
        print k, finish_colors[k]'''


    for i, k in enumerate(sorted(finish_colors.keys(), key=lambda key: finish_colors[key], reverse=True)):
        if i >= num_of_finish_colors:
            finish_colors.pop(k)

    num_of_finish_colors = len(finish_colors)

    size = num_of_finish_colors*100, 512
    new_img = Image.new('RGBA', size)
    d = ImageDraw.Draw(new_img)

    for i,k in enumerate(sorted(finish_colors.keys(), key=lambda key: finish_colors[key], reverse=True)):
        d.rectangle([(i*100,0),((i+1)*100,512)], fill=k)

    new_img.save(name_of_start_img.split('.')[0]+'_sch.jpg')

if __name__ == '__main__':
    main()