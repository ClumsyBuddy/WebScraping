import keyboard
import threading
from time import sleep

class MyClass():
        ContinueLoop = True
   
def KeyCheck(stop, Delay=1):
        while stop.ContinueLoop == True:
                print("Looping")
                if keyboard.is_pressed("l"):
                    stop.ContinueLoop = False
                    print("Exiting app")
                sleep(Delay)

def CallStuff(stop, Delay=1):
    count = 0
    while stop.ContinueLoop == True:
        count += 1
        print("Calling Stuff")
        sleep(Delay)

def Temp():
    print("Hello World")


def main():
    stop = MyClass

    t1 = threading.Thread(target=KeyCheck, args=(stop,0.01,))

    t2 = threading.Thread(target=CallStuff, args=(stop,0.01,))

    t3 = threading.Thread(target=Temp)

    t1.start()
    
    t2.start()

    t3.start()

    if stop.ContinueLoop == False:
       print("Good bye")


if __name__ == '__main__':
   main()