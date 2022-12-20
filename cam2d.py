import numpy as np
import cv2
# from numba import jit

from market_data import getMarketData
import pyttsx3
engine = pyttsx3.init()

# @jit
def dist2(p1,p2):
    return (p2[0] - p1[0])*(p2[0] - p1[0]) + (p2[1] - p1[1])*(p2[1] - p1[1])


def project_point_to_line(p, p1, p2):
    # Get vector from p1 to p2
    v = p2[0] - p1[0], p2[1]-p1[1]
    # Get vector from p1 to point
    u = p[0] - p1[0], p[1]-p1[1]
    # Get length of vector
    d2 = v[0]*v[0] + v[1]*v[1]
    # Get dot product
    dot = u[0]*v[0] + u[1]*v[1]
    # Get scalar multiple
    proj = dot/d2
    return proj

def getDist2(p,vPnt):
    vProj = []
    if len(vPnt) == 0: return -1
    if len(vPnt) == 1: 
        dx = p[0]-vPnt[0][0]
        dy = p[1]-vPnt[0][1]
        return cv2.sqrt(dx*dx +dy*dy)
    for i in range(len(vPnt))[1:]:
        p1,p2 = vPnt[i-1],vPnt[i]
        proj = project_point_to_line(p,p1,p2)
        if proj <0 or proj > 1: continue
        # print("closer point found: proj {:.3f}".format(proj))
        dx = (p2[0] - p1[0])*proj
        dy = (p2[1] - p1[1])*proj
        vProj.append((p1[0]+dx,p1[1]+dy))

    d2Min = 9999999999.0
    # print("1: len(vProj) = {}".format(len(vProj)))
    vProj.extend(vPnt)
    # print("2: len(vProj) = {}".format(len(vProj)))
    for pt in vProj:
        d2 = dist2(p,pt)
        # print("d = ", pt, np.sqrt(d2))
        if d2Min > d2:
            d2Min = d2
    return d2Min

class Cam2D:
    def __init__(self):
        self.true_img = cv2.imread("market_tmap.png")
        self.arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
        self.arucoParams = cv2.aruco.DetectorParameters_create()
        self.corners, self.ids, _ = cv2.aruco.detectMarkers(self.true_img , self.arucoDict, parameters=self.arucoParams)
        self.get_labels_legends()

    def findId(self,id):
        for i in range(len(self.ids)):
            if id[0] == self.ids[i][0]:
                return i
        return -1

    
    def procFrame(self,frame):
        corners, ids, _ = cv2.aruco.detectMarkers(frame , self.arucoDict, parameters=self.arucoParams)
        if ids is None: return
        vCn1,vCn2 = [],[]
        for i,id in enumerate(ids):
            indx = self.findId(id)
            if indx != -1:
                # print(self.ids[indx][0])
                vCn1.extend(corners[i][0])
                vCn2.extend(self.corners[indx][0])
        # print(np.array(vCn2))
        self.h, status = cv2.findHomography(np.array(vCn1),np.array(vCn2))
        self.frm = frame
        # print(h)

    def project(self,xy):
        out = np.matmul(self.h,np.array([xy[0],xy[1],1.0]))
        out *= 1.0/out[2]
        return out

    def get_labels_legends(self):
        self.streets,self.nm_des = getMarketData()
        # print(self.streets)
    def getDescription(self,name):
        try:
            return self.nm_des[name]
        except:
            return "???"
        
    def sayStreet(self,name):
        des = self.getDescription(name)
        engine.say(des)

    def findClosestStreet(self,p):
        # print("p = ",p)
        d2Min = 9999999999.0
        stMin = ""
        for st in self.streets:
            d2 = getDist2(p,st[1])
            # print("{}, {}".format(np.sqrt(d2),st))
            if d2Min > d2:
                d2Min = d2
                stMin = st
                # print("    {}, {}".format(np.sqrt(d2Min),st))
        return stMin,np.sqrt(d2Min)

    def getDistance(self,p,name):
        st = self.findStreet(name)
        return np.sqrt(getDist2(p,st[1]))
    
    def findStreet(self,name):
        for st in self.streets:
            if st[0] == name:
                return st
    
    def drawStreet(self,name):
        st = self.findStreet(name)
        pts = np.array(st[1],np.int32)
        pts = pts.reshape((-1, 1, 2))
        # print(pts.shape)
        isClosed = False
        color = (255, 0, 0)
        thickness = 2
        return cv2.polylines(self.true_img, [pts],isClosed, color, thickness)
 

    def test0(self):
        from time import time
        t = time()
        st,dist = self.findClosestStreet((400.0,400.0))
        print('dt = {}'.format(time()-t))
        print(st[0],dist)

    
    def test1(self):
        frm = cv2.imread('marker_test.jpg')
        self.procFrame(frm)
        for xy in (400,400),(500,500),(500,700):
            out = self.project(xy)
            cv2.circle(self.frm,(xy[0],xy[1]),3,(0,255,0),3)
            cv2.circle(self.true_img,(int(out[0]),int(out[1])),3,(0,255,0),3)
            st,d = self.findClosestStreet((out[0],out[1]))
            print("closest: {}, {}".format(st[0],d))
            print(self.getDescription(st[0]))

        cv2.imshow("frm",self.frm)
        cv2.imshow("proj",self.true_img)

        cv2.waitKey(0)


    def test2(self):
        p =  (102.443601126121, 373.35692389820997)
        cv2.circle(self.true_img,(int(p[0]),int(p[1])),3,(0,255,0),3)
        img = self.drawStreet('HYS')
        d = self.getDistance(p,'HYS')
        print("HYS, d = {}".format(d))
        d = self.getDistance(p,'GRV')
        print("GRV, d = {}".format(d))
        # img = self.drawStreet('GRV')
        cv2.imshow("frm",img)
        cv2.waitKey(0)


if __name__ == '__main__':
    # test3()
    # d = {}
    # d['1'] = "jnk 1"    
    # d['2'] = "jnk 2"
    # print(d['3'])
    Cam2D().test1()