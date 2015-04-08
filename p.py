#!/usr/bin/python

import Image, ImageDraw

W = 255
H = 128

img = Image.new("RGB", (W, H), "black")
img = Image.open("img/heart_PNG685.png")
draw = ImageDraw.Draw(img)

for x in range(W):
    for y in range(H):
        color = (x % 255, y % 255, (x % (y+1)) % 255)
        draw.point((x,y), fill=color)

draw.line((0, H/2, W, H/2), "yellow")
draw.rectangle([(200, 60), (100, 120)], outline="#FF00FF")
draw.text((20, 40), "quickies.seriot.ch")

img.save("img.png", "PNG")