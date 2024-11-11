from Minairo.Minairo_TCP import *
from time import sleep

if __name__=="__main__":
    IP = '192.168.1.1'
    port = 22
    Robot = MinairoSocket(IP,port)
    Robot.run()
    Robot.setX(0.1)
    Detection =False
    while not Detection:
        sensor = Robot.getSensorSharp()
        print(sensor)
        for i in range(0,4):
            if sensor[i]<100:
                Detection = True

    Robot.stop()

