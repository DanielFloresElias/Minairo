from Minairo.Minairo_TCP import MinairoSocket
import time

STATUS = ['CENTERED','SHIFTED_LEFT','SHIFTED_RIGHT']
VECTOR = [-8, -4, -2, -1, 1, 2, 4, 8]
SENSOR_COUNT = 0
EN = True
Robot = MinairoSocket('192.168.1.1',22)
Robot.run()

while EN :
    SENSOR = Robot.getSensorLine_Digital()
    
    SENSOR_VALUE = 0
    SENSOR_COUNT = 0
    for n in range(8) :
        if SENSOR[n]:
            SENSOR_COUNT += 1
            SENSOR_VALUE += VECTOR[n]

    Robot.setX(0.1/(1+(abs(SENSOR_VALUE)*0.5)))
    #Robot.setY(SENSOR_VALUE*0.001)
    Robot.setW(SENSOR_VALUE*0.08)
    print(abs(SENSOR_VALUE))


    if SENSOR_COUNT==8:
        EN = False
        Robot.setX(0.0)
        Robot.setY(0.0)
        Robot.setW(0.0)
    #print (SENSOR_VALUE)
    time.sleep(0.1)
    

#Robot.setX(0.1)
#time.sleep(1)
#Robot.setX(0.0)

Robot.close()