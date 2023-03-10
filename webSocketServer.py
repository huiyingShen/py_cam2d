from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import websocket
import threading
from time import time, sleep

clients = []
# pozClient = PozClient().test0()
class SimpleChat(WebSocket):
    def handleMessage(self):
        for client in clients:
            if client != self:
                client.sendMessage(self.address[0] + u' - ' + self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        for client in clients:
            client.sendMessage(self.address[0] + u' - connected')
        clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')


class KillableWebSocketServer(SimpleWebSocketServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._run_flag = True

    def serve_until_death(self):
        while self._run_flag:
            self.serveonce()

    def stop(self):
        self._run_flag = False


def launchServer(port=5000):
    server = KillableWebSocketServer('', int(port), SimpleChat)
    threading.Thread(target=server.serve_until_death, name='WebSocket Server').start()
    #server = SimpleWebSocketServer('', int(port), SimpleChat)
    #threading.Thread(target=server.serveforever, name='Server').start()
    print("server started,...")
    return server

    

def b64toImg(imgstring, filename = 'some_image.jpg'):
    import base64
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)

def test0():
    port = 5000
    def getClient(port = port):
        ws = websocket.WebSocket()
        ws.connect("ws://localhost:"+str(port), origin="local")
        print("client started,...")
        return ws

    running = True
    def sending(ws):
        cnt = 0
        while running:
            ws.send(f"hello, time = {time()}")
            if cnt%10 == 0:
                ws.send(f"image, please")
            # print("sending...")
            sleep(5.0)
    def receiving(ws):
        while running:
            txt = ws.recv()
            if len(txt) < 100:
                print("txt = ", txt)
            else:
                print("len = ",len(txt))
                print("txt[:100] = ",txt[:100])
                pos = txt.find(" _ ")
                print(txt[pos+3:100])
                b64toImg(txt[pos+3:])

    launchServer(port=port)
    sender = getClient(port=port)
    threading.Thread(target=sending, name='Ping Sender', args=(sender,)).start()
    receiver = getClient(port=port)
    receiving(receiver)



if __name__=="__main__":
    test0()
