from gtts import gTTS
import vlc
from time import sleep
import threading
import sys

instance = vlc.Instance()

class TtsSpeaker:
    def __init__(self) -> None:
        self.media_player = instance.media_player_new()
        self.stopped = False

    def set_media(self,txt):
        filename = txt + ".mp3"
        tts=gTTS(text=txt,lang="en")
        tts.save(filename)
        self.media = instance.media_new(filename) 


    def playUntilDone(self):
        self.stopped = False
        self.media_player.set_media(self.media)
        self.media_player.play()
        for n in range(1_000_000):
            if self.stopped: 
                self.media_player.stop()
                break
            sleep(0.01)
            pos = self.media_player.get_position()
            if pos > 0.1 and not self.media_player.is_playing(): 
                print(n,pos)
                break

    def play_text(self,txt):
        self.set_media(txt)
        threading.Thread(target=self.playUntilDone()).start()

    def stop(self,dt = 1):
        print("stop()")
        sleep(dt)
        self.stopped = True

    def test1(self):
        self.play_text("testing, 1, 2, 3, ...")
        threading.Thread(target=self.stop()).start()


def text_to_media(txt = "hello, world!"):
    filename = txt + ".mp3"
    tts=gTTS(text=txt,lang="en")
    tts.save(filename)
    return instance.media_new(filename) 

def play_text(txt,media_player):
    if media_player is None:
        media_player = instance.media_player_new()
    else:
        for n in range(1000):
            sleep(0.01)
            pos = media_player.get_position()
            print(pos)
            if pos > 0.5 and not media_player.is_playing(): 
                break

    media_player.set_media(text_to_media(txt))
    media_player.play()
    for n in range(1000):
        sleep(0.01)
        pos = media_player.get_position()
        # print("n, pos = ",n, pos)
        # if pos>0.99: return
        if pos > 0.5 and not media_player.is_playing(): return media_player

def unblock_play(txt,media_player=None):
    threading.Thread(target=play_text,args=(txt,media_player,)).start()
    return media_player
if __name__ == '__main__':
    TtsSpeaker().test1()
    # media_player = unblock_play("how are you doing today?",None)
    # unblock_play("I am fine thank you",media_player)
    # unblock_play("Am I the last one?",None)
 
    
