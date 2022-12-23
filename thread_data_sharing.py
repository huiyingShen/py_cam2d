# SuperFastPython.com
# example of using an event object
from time import sleep
from random import random
from threading import Thread, Event
 
 # create a shared event object
event = Event()

# target task function
def task(event, number):
    # wait for the event to be set
    event.wait()
    # begin processing
    value = random()
    sleep(value)
    print(f'Thread {number} got {value}')
 
def test1():
# create a suite of threads
    for i in range(5):
        thread = Thread(target=task, args=(event, i))
        thread.start()
    # block for a moment
    print('Main thread blocking...')
    sleep(2)
    # start processing in all threads
    event.set()
    # wait for all the threads to finish...

def loop(event, dt):
    for i in range(999):
        event.wait(timeout=dt)
        print('i = ', i)
        if event.is_set():
            break

    event.clear()

def stop(event,dt):
    sleep(dt)
    event.set()

def test2():
    Thread(target=loop, args=(event, 0.1)).start()
    Thread(target=stop, args=(event, 1.0)).start()

if __name__ == "__main__":
    test2()