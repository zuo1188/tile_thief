#!/usr/bin/env python
from math import pi,cos,sin,log,exp,atan
import sys, os


DEG_TO_RAD = pi/180
RAD_TO_DEG = 180/pi


def minmax (a,b,c):
    a = max(a,b)
    a = min(a,c)
    return a

class GoogleProjection:
    def __init__(self,levels=18):
        self.Bc = []
        self.Cc = []
        self.zc = []
        self.Ac = []
        c = 256
        for d in range(0,levels):
            e = c/2;
            self.Bc.append(c/360.0)
            self.Cc.append(c/(2 * pi))
            self.zc.append((e,e))
            self.Ac.append(c)
            c *= 2

    def fromLLtoPixel(self,ll,zoom):
        d = self.zc[zoom]
        e = round(d[0] + ll[0] * self.Bc[zoom])
        f = minmax(sin(DEG_TO_RAD * ll[1]),-0.9999,0.9999)
        g = round(d[1] + 0.5*log((1+f)/(1-f))*-self.Cc[zoom])
        return (e,g)

    def fromPixelToLL(self,px,zoom):
        e = self.zc[zoom]
        f = (px[0] - e[0])/self.Bc[zoom]
        g = (px[1] - e[1])/-self.Cc[zoom]
        h = RAD_TO_DEG * ( 2 * atan(exp(g)) - 0.5 * pi)
        return (f,h)



def split_bbox(bbox, minZoom=1,maxZoom=18):
    bboxs = []
    gprj = GoogleProjection(maxZoom+1)

    ll0 = (bbox[0],bbox[3])
    ll1 = (bbox[2],bbox[1])

    for z in range(minZoom,maxZoom + 1):
        px0 = gprj.fromLLtoPixel(ll0,z)
        px1 = gprj.fromLLtoPixel(ll1,z)

        # check if we have directories in place
        zoom = "%s" % z

        for x in range(int(px0[0]/256.0),int(px1[0]/256.0)+1):
            # Validate x co-ordinate
            if (x < 0) or (x >= 2**z):
                continue
            for y in range(int(px0[1]/256.0),int(px1[1]/256.0)+1):
                # Validate x co-ordinate
                if (y < 0) or (y >= 2**z):
                    continue

                p0 = (x * 256, (y + 1) * 256)
                p1 = ((x + 1) * 256, y * 256)

                # Convert to LatLong (EPSG:4326)
                l0 = gprj.fromPixelToLL(p0, z);
                l1 = gprj.fromPixelToLL(p1, z);

                #print(l0, l1)
                bboxs.append((l0[0], l0[1], l1[0], l1[1]))

    return bboxs


if __name__ == "__main__":
    bbox = (116.203411,39.801672,116.611279,40.0397)
    minZoom = 15
    maxZoom = 15
    bboxs = split_bbox(bbox, minZoom, maxZoom)
    print(bboxs)
