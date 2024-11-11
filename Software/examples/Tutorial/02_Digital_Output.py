from Minairo.Minairo_TCP import *
from time import sleep

if __name__=="__main__":
    IP = '192.168.1.1'
    port = 22
    Robot = MinairoSocket(IP,port)
    Robot.run()
    Robot.confGPIO(1,'OUTPUT')
    for i in range(0,4):
        Robot.setGPIO(1,1)
        sleep(0.5)
        Robot.setGPIO(1,0)
        sleep(0.5)   

    Robot.stop()

