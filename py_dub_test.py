
# import required module
from pydub import AudioSegment
from pydub.playback import play
 
# for playing mp3 file
song = AudioSegment.from_mp3("welcome.mp3")
print('playing sound using  pydub')
play(song)