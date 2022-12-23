from gtts import gTTS
import vlc
from time import sleep
import threading
import sys

instance = vlc.Instance()


def text_to_media(txt = "hello, world!"):
    tts=gTTS(text=txt,lang="en")
    filename = txt + ".mp3"
    tts.save(filename)

    return vlc.Media(filename) 

def play_text(txt = "hello, world!"):
    media_player = instance.media_player_new()
    media_player.set_media(text_to_media(txt))
    media_player.play()
    for n in range(1000):
        sleep(0.01)
        pos = media_player.get_position()
        # print("n, pos = ",n, pos)
        # if pos>0.99: return
        if pos > 0.5 and not media_player.is_playing(): return

    
if __name__ == '__main__':
    play_text()
    play_text("how are you doing today?")
 
    
