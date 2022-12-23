import sys
from time import sleep
import threading

from PyQt5 import QtCore, QtWidgets, QtMultimedia
def jnk(plr):
   for _ in range(10):
        sleep(0.5)
        state = plr.state()
        print(state)
        if state == 0:
            return
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    filename = 'welcome.mp3'
    fullpath = QtCore.QDir.current().absoluteFilePath(filename) 
    media = QtCore.QUrl.fromLocalFile(fullpath)
    content = QtMultimedia.QMediaContent(media)
    player = QtMultimedia.QMediaPlayer()
    player.setMedia(content)
    player.play()
    threading.Thread(target=jnk,args=(player,)).start()
    sleep(2)

    sys.exit(app.exec_())