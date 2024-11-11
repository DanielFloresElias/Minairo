from tkinter import *
from Minairo.Minairo_TCP import MinairoSocket
from Minairo.Minairo_Utilities import Clock, TON

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
            #############################################################
            ############# C O D I G O   D E   U S U A R I O #############
            #############################################################
            print(Robot.getSONAR())
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
    window.config(width=220, height=50)

    ## Boto Exit
    btnSortir = Button(window, text="Exit", bg="grey",width=10,command=Sortir)
    btnSortir.place(x=70, y=10)
    Robot.connect()
    window.after(1,Loop)        # Llamada programada en 1ms a la función Loop
    window.mainloop()           # Arrancar la instancia de Ventana de Tkinter tipo Tk.
