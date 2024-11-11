'''
    __  __ _             _        _  
   |  \/  (_)           (_)      //   
   | \  / |_ _ __   __ _ _ _ __ ___  
   | |\/| | | '_ \ / _` | | '__/ _ \ 
   | |  | | | | | | (_| | | | | (_) | 
   |_|  |_|_|_| |_|\__,_|_|_|  \___/ 

   Descripción: Esta libreria permite controlar un Robot MINAIRÓ 1.0 mediante distintos métodos
    implementados en la Clase "MinairoSocket" para Python3 .
    En la versión * se transmiten todos los paràmetros en una sala instrucción en RAW.

   Versión: 
   Autor: Daniel Flores Elias
   mail: daniel.flores@gmail.com

   Metodos:
        MinairoSocket(IP,port)
        run():
        transmit():
        stop():
        close():
        setPullingTime(x):
        getPullingTime():
        setVel(x,y,w):
        setX(x):
        setY(y):
        setW(w):
        setSensorLine_Threshold(x):
        getSensorLine_Threshold():
        getSensorLine_Analog():
        getSensorLine_Digital():
        getSensorSharp():
        getAnalogs():
        confGPIO(pin,mode):
        setGPIO(pin,value):
        getGPIO():
        setSERVO(pin,value):
        getSONAR():
_______________________________________________________________________________________


   Copyright (c) 2023 Institut Jaume Huguet-Valls, Daniel Flores
   <daniel.flores@gmail.com>  All rights reserved.
   See the bottom of this file for the license terms.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are
   met:

   1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

   3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
   HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from socket import *
from threading import Thread, Timer
from struct import pack,unpack
from ctypes import *
import time
from tkinter import *
from math import tan,pi,cos,sin,pow

class MinairoSocket():
    """MinairoSocket() - Requiere IP del MINAIRÓ i numero de puerto"""
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.obj = socket()
        self.command = ""
        self.InByte = ''
        self.InString = ""
        self.OutBuffer = bytearray(32)
        self.InBuffer = bytearray(80)
        self.pullingTime = 0.025  #Tiempo de ciclo para adquisición de datos con el Robot
        self.thread_runs = True
        self.X = 0.0    # Velocidad en m/s
        self.Y = 0.0    # Velocidad en m/s
        self.W = 0.0    # Velocidad en rad/s
        self.SensorLine_Analog = [0,0,0,0,0,0,0,0]
        self.SensorLine_Digital = [False,False,False,False,False,False,False,False]
        self.SensorLine_Threshold = 2400
        self.SensorSharp = [0,0,0,0]
        self.CtrlWord1 = 0
        self.CtrlWord2 = 0
        self.StatusWord1 = 0
        self.StatusWord2 = 0
        self.EncoderValue = 0
        self.EncoderValue_0 = 0
        self.EncoderValue_1 = 0
        self.EncoderValue_2 = 0
        self.InstantTime = 0        # milliseconds from robot startup
        self.Odom_x = 0.0
        self.Odom_y = 0.0
        self.Odom_theta = 0.0
        self.Odom_velocity_linear = 0.0
        self.Odom_omega = 0.0
        self.SetPoint = 0
        self.AuxMotor = {"SP": 0, "PV": 0, "Home": 0, "H_SW": 0, "L_SW": 0}
        self.Motor_set_Transmit = False
        self.GPIO_conf = [0,0,0,0,0,0,0]
        self.GPIO_value = [0,0,0,0,0,0,0]
        self.GPIO_status = [0,0,0,0,0,0,0]
        self.GPIO_conf_Transmit = False
        self.GPIO_set_Transmit = False
        self.Analogicas = [0,0,0,0]
        self.Sonar = 0
        self.Servos = [1500,1500,1500,1500,1500]
        self.Servo_set_Transmit = False
        self.setOutBuffer()
        self.TransmitCounter = 0
        self.T1 = round(time.time()*1000)
        self.T2 = round(time.time()*1000)
        print (f"Minairo 1.0 en host:{self.host} creat")

    def setOutBuffer(self):
        Vx = pack('f', self.X)
        Vy = pack('f', self.Y)
        Vw = pack('f', self.W)
        CtrlW1 = pack('H', self.CtrlWord1)
        CtrlW2 = pack('H', self.CtrlWord2)
        SP = pack('I', self.SetPoint)
        GPIO_C = 0
        for k in range(0,7):
            if self.GPIO_conf[k]==1:
                GPIO_C = GPIO_C | 1<<k
            else:
                GPIO_C = GPIO_C & ~(1<<k)
        GPIO_C = pack('b',GPIO_C)
        GPIO_V = 0
        for k in range(0,7):
            if self.GPIO_value[k]==1:
                GPIO_V = GPIO_V | 1<<k
            else:
                GPIO_V = GPIO_V & ~(1<<k)
        GPIO_V = pack('b',GPIO_V)
        Srv0 = pack('H', self.Servos[0])
        Srv1 = pack('H', self.Servos[1])
        Srv2 = pack('H', self.Servos[2])
        Srv3 = pack('H', self.Servos[3])
        Srv4 = pack('H', self.Servos[4])
        self.OutBuffer = Vx + Vy + Vw + CtrlW1 + CtrlW2 + SP + GPIO_C + GPIO_V + Srv0 + Srv1 + Srv2 + Srv3 + Srv4

    def getInBuffer(self):
        [self.StatusWord1] = unpack('H', self.InBuffer[0:2])
        [self.StatusWord2] = unpack('H', self.InBuffer[2:4])
        [self.EncoderValue] = unpack('i', self.InBuffer[4:8])
        [LS_0] = unpack('H', self.InBuffer[8:10])
        [LS_1] = unpack('H', self.InBuffer[10:12])
        [LS_2] = unpack('H', self.InBuffer[12:14])
        [LS_3] = unpack('H', self.InBuffer[14:16])
        [LS_4] = unpack('H', self.InBuffer[16:18])
        [LS_5] = unpack('H', self.InBuffer[18:20])
        [LS_6] = unpack('H', self.InBuffer[20:22])
        [LS_7] = unpack('H', self.InBuffer[22:24])
        [SS_0] = unpack('H', self.InBuffer[24:26])
        [SS_1] = unpack('H', self.InBuffer[26:28])
        [SS_2] = unpack('H', self.InBuffer[28:30])
        [SS_3] = unpack('H', self.InBuffer[30:32])
        [GPIO_Status] = unpack('B', self.InBuffer[32:33])
        [AN_0] = unpack('H', self.InBuffer[34:36])
        [AN_1] = unpack('H', self.InBuffer[36:38])
        [AN_2] = unpack('H', self.InBuffer[38:40])
        [AN_3] = unpack('H', self.InBuffer[40:42])
        [self.Sonar] = unpack('H', self.InBuffer[42:44])
        [self.EncoderValue_0] = unpack('i', self.InBuffer[44:48])
        [self.EncoderValue_1] = unpack('i', self.InBuffer[48:52])
        [self.EncoderValue_2] = unpack('i', self.InBuffer[52:56])
        [self.InstantTime] = unpack('I', self.InBuffer[56:60])
        [self.Odom_x] = unpack('f', self.InBuffer[60:64])
        [self.Odom_y] = unpack('f', self.InBuffer[64:68])
        [self.Odom_theta] = unpack('f', self.InBuffer[68:72])
        [self.Odom_velocity_linear] = unpack('f', self.InBuffer[72:76])
        [self.Odom_omega] = unpack('f', self.InBuffer[76:80])
        self.SensorLine_Analog  = [LS_0,LS_1,LS_2,LS_3,LS_4,LS_5,LS_6,LS_7]
        self.SensorSharp = [SS_0,SS_1,SS_2,SS_3]
        self.Analogicas = [AN_0,AN_1,AN_2,AN_3]
        for k in range(0,7):
            if GPIO_Status & 1<<k:
                self.GPIO_status[k]= 1
            else:
                self.GPIO_status[k]= 0

    def connect(self):
        self.obj.connect((self.host,self.port))

 
    def buidarSocket(self):
        while 1:
            s = self.obj.recv(1).decode()
            if s == '\n':
                break;

    def sendCommand(self, data):
        self.command = data + '\n'
        self.obj.send( self.command.encode())

    def read(self):
        self.InByte = ''
        self.InString = ""
        while self.InByte != '\n':
            self.InString += self.InByte
            self.InByte = self.obj.recv(1).decode()
        return self.InString

    def close(self):
        self.obj.close()
        print (f"Minairo 1.0 en host:{self.host} desconectado")

    def stop(self):
        self.thread_runs = False
        self.X = 0.0
        self.Y = 0.0
        self.W = 0.0

    def run(self):
        self.thread_runs = True
        self.connect()
        self.transmitCyclic()
    
    def transmitCyclic(self):
        if self.thread_runs:
            self.transmit()
            Timer(self.pullingTime, self.transmitCyclic).start()
        else:
            self.transmit()
            self.obj.close()

    def transmit(self):
        ################# c m d _ R A W #################
        self.setOutBuffer()
        self.obj.send(self.OutBuffer)
        self.InBuffer = self.obj.recv(80)
        self.getInBuffer()

    def setVel(self,x,y,w):
        self.X = x
        self.Y = y
        self.W = w

    def setX(self,x):
        self.X = x
    
    def getX(self):
        return self.X
    
 
    def setY(self,y):
        self.Y = y

    def getY(self):
        return self.Y

    def setW(self,w):
        self.W = w

    def getW(self):
        return self.W

    def setSensorLine_Threshold(self,x):
        self.SensorLine_Threshold = x

    def getSensorLine_Threshold(self):
        return self.SensorLine_Threshold

    def getSensorLine_Analog(self):
        return self.SensorLine_Analog

    def getSensorLine_Digital(self):
        for x in range(0,8):
            if self.SensorLine_Analog[x]>=self.SensorLine_Threshold:
                self.SensorLine_Digital[x] = True
            else:
                self.SensorLine_Digital[x] = False
        return self.SensorLine_Digital

    def getSensorSharp(self):
        Sensor = [0,0,0,0]
        for x in range(0,4):
            Sensor[x] = int(32120*((1+self.SensorSharp[x])**(-1.238)))
            if Sensor[x] > 400:
                Sensor[x] = 400
        return Sensor
    
    def getAnalogs(self):
        return self.Analogicas

    def setPullingTime(self,x):
        self.pullingTime = x

    def getPullingTime(self):
        return self.pullingTime
    
    def confGPIO(self,pin,mode):
        '''
        FORMATO: confGPIO( pin , mode )

        PARAMETROS:
            pin -> Numero de pin [0..6]
            mode -> [INPUT,OUTPUT]
        '''
        if mode == "INPUT":
            self.GPIO_conf[pin] = 0
        if mode == "OUTPUT":
            self.GPIO_conf[pin] = 1

    def setGPIO(self,pin,value):
        '''
        FORMATO: confGPIO( pin , value )

        PARAMETROS:
            pin -> Numero de pin [0..6]
            value -> [0,1]
        '''
        if value :
            self.GPIO_value[pin] = 1
        else:
            self.GPIO_value[pin] = 0

    def getGPIO(self,pin):
        '''
        FORMATO: getGPIO( pin )

        PARAMETROS:
            pin -> Numero de pin [0..6]

        RETORNA:
            Estado de la GPIO [0..1]
        '''
        return self.GPIO_status[pin]

    def setSERVO(self,pin,value):
        '''
        FORMATO: setSERVO( pin , value )

        PARAMETROS:
            pin -> Numero de Servo [0..4]
            value -> [1000..2000] Ancho de Pulsos en microsegundos
        '''
        self.Servos[pin] = value

    def getSONAR(self):
        '''
        FORMATO: getSONAR()

        RETORNA:
            [X]  Vector con distáncia hasta obstaculo  [0 .. 4000] mm
        '''
        return ((self.Sonar * 0.1759)+5.0039)
    
    def setMotorPosition(self,consigna):
        '''
        FORMATO: setMotorPosition(consigna)

        PARAMETROS:
            
        '''
        self.AuxMotor['SP'] = consigna

    def setMotorHome(self):
        '''
        FORMATO: setMotorHome()

        PARAMETROS:
            
        '''
        self.AuxMotor['Home'] = 1
