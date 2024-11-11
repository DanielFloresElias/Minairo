from serial import Serial
import time

baudrate = 115200
port = "COM5"
timeout = "0.1"
OutBuffer = bytearray(32)
InBuffer = bytearray(32)
Robot = Serial(port,baudrate)
OutBuffer = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

for i in range(0,50):
    Robot.write(OutBuffer)	##Enviar comanda
    InBuffer = Robot.read(44)	## Llegir resposta
    print(InBuffer)
    time.sleep(0.02)
Robot.close()
