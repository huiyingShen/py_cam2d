import cv2
import numpy as np
import base64
from webSocketServer import launchServer
import websocket
from hand import detect_hand
from time import time,sleep
import threading
from PyQt5.QtCore import QThread

plea4data = "image, please!"

class TheClient(QThread):
    def __init__(self,host,port, trace = True, on_message = None):
        super().__init__()
        websocket.enableTrace(trace)
        if on_message is None:
            self.ws = websocket.WebSocketApp("ws://" + host + ":" + str(port),
                                on_open=self.on_open,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)
        else:
             self.ws = websocket.WebSocketApp("ws://" + host + ":" + str(port),
                                on_open=self.on_open,
                                on_message=on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)  
    def on_error(self, ws,error):
        print(error)

    def on_close(self, ws,close_status_code, close_msg):
        print("### closed ###")

    def on_open(self,ws):
        print("Opened connection")

class WebcamClient(TheClient):   
    cap = cv2.VideoCapture(0)
                                
    def on_message(self, ws, txt):
        print("on_message:")
        if len(txt) < 100:
            print(txt)
        pos = txt.find(plea4data)
        if pos != -1:
            success, image = self.cap.read()
            if success:
                _, buffer = cv2.imencode('.jpg', image)
                jpg_as_text = base64.b64encode(buffer)
                ws.send(jpg_as_text)
    def run(self):
        threading.Thread(target=self.ws.run_forever).start()

class HandClient(TheClient): 
    xy = (-1,-1)
    running = True      
    t0 = time()
    def on_message(self, ws, txt):
        print("on_message:")
        self.ready = False
        if len(txt) < 100:
            print("txt = ", txt)
        else:
            print("len = ",len(txt))
            # print("txt[:100] = ",txt[:100])
            s = txt[:100]+"_test"
            pos = s.find(' - ')
            print("pos = ", pos)
            print(txt[pos+3:100])
            try:
                jpg_as_np = np.fromstring(base64.b64decode(txt[pos+3:]), dtype=np.uint8)
                image = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
                image,self.xy = detect_hand(image)
                self.postProcImage(image)
            except:
                pass

    def postProcImage(self,image):
        cv2.imwrite("hand_detection.jpg",image)
        cv2.imshow('MediaPipe Hands', image)
        cv2.waitKey(300)
        self.ready = True

    def receiving(self):
        from time import time,sleep
        self.t0 = time()
        self.ready = True
        while self.running:
            sleep(0.333)
            x,y = self.xy
            if x > 0: self.ws.send("index finger: {},{}".format(x,y))
            # print("self.ready, time()-self.t0 = ", self.ready,time()-self.t0)
            if self.ready or time()-self.t0  > 1.0:
                self.ws.send(plea4data)
                self.t0 = time()

    def run(self):
        threading.Thread(target=self.ws.run_forever).start()
        threading.Thread(target=self.receiving).start()

def test0():
    host, port = "localhost",5001
    launchServer(port = port)
    try: launchServer(port = port)
    except: pass

    WebcamClient(host, port, trace=False ).run()
    HandClient(host, port, trace=False).run()

def test1():
    host, port = "localhost",5001
    # launchServer(port = port)
    try: launchServer(port = port)
    except: pass
 
    WebcamClient(host, port, trace=False ).run()
    HandClient(host, port, trace=False).run()

if __name__ == "__main__":
    test1()
    # HandClient("localhost",5001, trace=False).run()


    
