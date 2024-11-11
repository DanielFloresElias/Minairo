from tkinter import *
from Minairo.Minairo_TCP import MinairoSocket
from Minairo.Minairo_Utilities import Clock, TON
from Minairo.Minairo_Widgets import MinairoSensorLine, MinairoSensorPerimetre, MinairoSonar

def Loop():
    # FUNCIÓN CICLICA
    # Esta función sé ejecuta ciclicamente con un periodo de 1 milisegundo.
    # mediante los objetos de tipo Clock de la libreria 'Minairo_TCP_V3_1', se podran ejecutar procesos en
    # intervalos de tiempo predeterminados. 

    # Definición de variables globales
    global CycleClock
    global ShutDown
    global Grafcet

    #Definición de variables locales 

    if CycleClock.timeout():
            Robot.transmit()
            SensorLine.update(Robot.getSensorLine_Analog())
            SensorPerimetre.update(Robot.getSensorSharp())
            SensorSonar.plot(Robot.getSONAR(),10)
            SensorSonar.update()
            #############################################################
            ############# C O D I G O   D E   U S U A R I O #############
            #############################################################
            match Grafcet:

                case 0:
                    Robot.setVel(0.1,0.0,0.0)
                    Grafcet = 10
                case 10:
                    Grafcet = 0
                case _:
                    Grafcet=0

            #############################################################
            ################# F I N   D E   C O D I G O #################
            #############################################################

    if not ShutDown:
        window.after(1,Loop) # Llamada programada en 1ms a la función Loop
    else:
        Robot.transmit()
        Robot.close()
        window.destroy()
        
def Sortir():
    global ShutDown
    Robot.stop()
    ShutDown = True
    
if __name__=="__main__":
    IP = '192.168.1.1'
    Robot = MinairoSocket(IP,22)
    Grafcet = 0
    CycleClock = Clock(50)      # Reloj para ciclo de trabajo, periodo T=50ms F=20Hz.
    ShutDown = False

    ## Creación i configuración de la ventana con Tkinter
    window = Tk()
    window.title("Minairo 4.0 -> IP{}".format(IP))
    window.config(width=220, height=500)

    ## Widget para visualizar el estado del sensor de línea.
    SensorLine = MinairoSensorLine(window)
    SensorLine.dimensions(200,100)
    SensorLine.place(x=9,y=10)    

    ## Widget para visualizar el estado de los sensores perimetrales.
    SensorPerimetre = MinairoSensorPerimetre(window)
    SensorPerimetre.dimensions(200,100)
    SensorPerimetre.place(x=9,y=120)

    ## Widget para visualizar el estado del sonar.
    SensorSonar = MinairoSonar(window)
    SensorSonar.dimensions(200)
    SensorSonar.place(x=9,y=240)  

    ## Boto Exit
    btnSortir = Button(window, text="Exit", bg="grey",width=10,command=Sortir)
    btnSortir.place(x=70, y=460)
    Robot.connect()
    window.after(1,Loop)        # Llamada programada en 1ms a la función Loop
    window.mainloop()           # Arrancar la instancia de Ventana de Tkinter tipo Tk.
