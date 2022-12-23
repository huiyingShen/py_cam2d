# https://pypi.org/project/pyttsx3/
import pyttsx3
from time import sleep

locationMax  = 20
def onStart():
   print('starting')
  
def onWord(name, location, length):
   print('word', name, location, length)
   if location > locationMax:
      engine.stop()
  
def onEnd(name, completed):
   print('finishing', name, completed)

  
engine = pyttsx3.init()
  
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
  
sen = 'Geeks for geeks is a computer portal for Geeks'
  
engine.setProperty('rate', 150)
engine.say(sen,'speech 1: ')
engine.runAndWait()
locationMax  = 10
def onEnd2(name, completed):
   print('finishing 2, ...', name, completed)

engine.connect('finished-utterance', onEnd2)
engine.say("hello, how are doing today?",'speech 2: ')
engine.runAndWait()
