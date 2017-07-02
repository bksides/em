from __future__ import print_function
import os, sys
from PIL import Image, ImageDraw
from numpy import subtract

class Graph:
    def __init__(self, xmin, ymin, xmax, ymax, stepx=1, stepy=1):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.__functions__ = {}
        self.__points__ = []

    def addFunction(self, function, color = (255, 0, 0)):
        self.__functions__[function] = color

    def addPoint(self, point):
        self.__points__.append(point)

    def renderToFile(self, name, sizex, sizey):
        def pixelToCoord(pixel):
            return (self.xmin + pixel[0]*(self.xmax-self.xmin)/sizex,
                        self.ymin + (sizey - pixel[1])*(self.ymax-self.ymin)/sizey)
        def coordToPixel(coord):
            return (int((coord[0]-self.xmin)*sizex/(self.xmax-self.xmin)),
                        int(sizey-((coord[1]-self.ymin)*sizey/(self.ymax-self.ymin))))
        myImage = Image.new("RGB", (sizex, sizey), "#cccccc")
        for func in self.__functions__:
            for x in range(sizex):
                graphx = pixelToCoord((x, 0))[0]
                lastgraphx = pixelToCoord((x-1, 0))[0]
                cury = coordToPixel((graphx, func((graphx,))))[1]
                lasty = coordToPixel((lastgraphx, func((lastgraphx,))))[1]
                miny = min(lasty, cury)
                maxy = max(lasty, cury)
                for y in range(miny-1, maxy):
                    if y < sizey and y >= 0:
                        myImage.putpixel((x, y), self.__functions__[func])
                for y in range(maxy, sizey):
                    if y < sizey and y >= 0:
                        fromcol = myImage.getpixel((x, y))
                        myImage.putpixel((x, y), tuple(int((a+b)/2) for a,b in zip(fromcol, self.__functions__[func])))
        draw = ImageDraw.Draw(myImage)
        for point in self.__points__:
            draw.arc([coordToPixel(point)[0], coordToPixel(point)[1]-8, coordToPixel(point)[0]+1, coordToPixel(point)[1]], 0, 360, "#000000ff")
        myImage.save("vis/" + name, "PNG")

if __name__ == "__main__":
    main()
