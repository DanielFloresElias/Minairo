from Minairo.Minairo_TCP import *
import time

IP = '192.168.1.1'
Robot = MinairoSocket(IP,22)
Robot.connect() ## Iniciar Connexión mediante socket TCP

## Resetear marco de referencia del robot
Robot.CtrlWord2 = 1
Robot.transmit()
Robot.CtrlWord2 = 0
Robot.transmit()

## Velocidad de rotación 0.2rad/s
Robot.setW(0.2)
while Robot.Odom_theta<360.0:   ## Girar hasta completar una revolución
    print(Robot.Odom_theta)
    Robot.transmit()
    time.sleep(0.02)

Robot.setW(0.0) ## Detener el Robot
Robot.transmit()

Robot.close()   ## Finalizar Connexión mediante socket TCP

