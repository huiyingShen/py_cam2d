
import pyttsx3
from time import sleep
  
def onStart():
   print('starting')
  
def onWord(name, location, length):
   print('word', name, location, length)
  
def onEnd(name, completed):
   print('finishing', name, completed)
  
engine = pyttsx3.init()
  
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
  
sen = 'Geeks for geeks is a computer portal for Geeks'
  
  
engine.say(sen)
engine.isBusy()
print("engine.isBusy(), ",engine.isBusy())
engine.runAndWait()
sleep(.1)
print("engine.isBusy(), ",engine.isBusy())
sleep(.1)
print("engine.isBusy(), ",engine.isBusy())
sleep(5)
print("engine.isBusy(), ",engine.isBusy())
sleep(.1)
print("engine.isBusy(), ",engine.isBusy())