from tkinter import *
from Minairo.Minairo_TCP import *
from Minairo.Minairo_Utilities import *
from Minairo.Minairo_Widgets import *
from PID import *

def Loop():
    # FUNCIÓN CICLICA
    # Esta función sé ejecuta ciclicamente con un periodo de 1 milisegundo.
    # mediante los objetos de tipo Clock de la libreria 'Minairo_TCP_V3_1', se podran ejecutar procesos en
    # intervalos de tiempo predeterminados. 

    # Definición de variables globales
    global CycleClock
    global Grafcet
    global T1
    global counter
    global ShutDown
    global FirstCycle
    global Enc0_Offset
    global Enc1_Offset
    global Enc2_Offset
    global ResetOdometry
    global pid
    T1.update()
    #Definición de variables locales 

    if CycleClock.timeout():
            if ResetOdometry:
                ResetOdometry = False
                Robot.CtrlWord2 = 1
            else:
                Robot.CtrlWord2 = 0
            Robot.transmit()
            if FirstCycle:
                FirstCycle=False
                Enc0_Offset = Robot.EncoderValue_0
                Enc1_Offset = Robot.EncoderValue_1
                Enc2_Offset = Robot.EncoderValue_2

            Enc0.set(f"{Robot.EncoderValue_0-Enc0_Offset} ticks")
            Enc1.set(f"{Robot.EncoderValue_1-Enc1_Offset} ticks")
            Enc2.set(f"{Robot.EncoderValue_2-Enc2_Offset} ticks")
            InstantTime.set(f"{Robot.InstantTime} ms")
            Odom_x.set(f"{Robot.Odom_x} m")
            Odom_y.set(f"{Robot.Odom_y} m")
            Odom_theta.set(f"{Robot.Odom_theta} rad")
            Odom_velocity_linear.set(f"{Robot.Odom_velocity_linear} m/s")
            Odom_omega.set(f"{Robot.Odom_omega} rad/s")
            #############################################################
            ############# C O D I G O   D E   U S U A R I O #############
            #############################################################
            
            match Grafcet:

                case 0:
                    Robot.setVel(0.0,0.0,0.0)
                    Grafcet = 10
                case 10:
                    pid.setpoint = 1
                    control_signal = pid.compute(Robot.Odom_x,time.time())
                    Robot.setX(control_signal)
                    print(f"Control Signal: {control_signal}m/s, Actual Value: {Robot.Odom_x}m, Done: {pid.Done()}")
                    if pid.Done():
                        Robot.setX(0.0)
                        Grafcet = 10
                case 20:
                    '''
                    Robot.setW(0.314159265)
                    T1.PT(5000)
                    T1.IN(True)
                    if T1.Q():
                        T1.IN(False)
                        Grafcet = 0
                    '''
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
    T1 = TON()
    counter = 0
    CycleClock = Clock(50)      # Reloj para ciclo de trabajo, periodo T=50ms F=20Hz.
    ShutDown = False
    FirstCycle = True
    ResetOdometry = True
    Enc0_Offset = 0
    Enc1_Offset = 0
    Enc2_Offset = 0
    # Crear un controlador PID con kp=2, ki=0.1, kd=0.01 y setpoint en 10
    pid = PID(kp=0.5, ki=0.001, kd=0.0000, setpoint=0, min_output=-0.1, max_output=0.1)

    ## Creación i configuración de la ventana con Tkinter
    window = Tk()
    window.title("Minairo 1.0 -> IP{}".format(IP))
    window.config(width=220, height=400)



    ## Etiquetes
    Enc0 = StringVar(value='t')
    Enc1 = StringVar(value="")
    Enc2 = StringVar(value="")
    InstantTime = StringVar(value="")
    Odom_x = StringVar(value="")
    Odom_y = StringVar(value="")
    Odom_theta = StringVar(value="")
    Odom_velocity_linear = StringVar(value="")
    Odom_omega = StringVar(value="")

    Enc0.set(f"{Robot.EncoderValue_0} ticks")
    Enc1.set(f"{Robot.EncoderValue_1} ticks")
    Enc2.set(f"{Robot.EncoderValue_2} ticks")
    InstantTime.set(f"{Robot.InstantTime} ms")
    Odom_x.set(f"{Robot.Odom_x} m")
    Odom_y.set(f"{Robot.Odom_y} m")
    Odom_theta.set(f"{Robot.Odom_theta} rad")
    Odom_velocity_linear.set(f"{Robot.Odom_velocity_linear} m/s")
    Odom_omega.set(f"{Robot.Odom_omega} rad/s")


    lbl_Enc0 = Label(window,textvariable=Enc0)
    lbl_Enc1 = Label(window,textvariable=Enc1)
    lbl_Enc2 = Label(window,textvariable=Enc2)
    lbl_InstantTime = Label(window,textvariable=InstantTime)
    lbl_Odom_x = Label(window,textvariable=Odom_x)
    lbl_Odom_y = Label(window,textvariable=Odom_y)
    lbl_Odom_theta = Label(window,textvariable=Odom_theta)
    lbl_Odom_velocity_linear = Label(window,textvariable=Odom_velocity_linear)
    lbl_Odom_omega = Label(window,textvariable=Odom_omega)

    lbl_Enc0.place(x=5, y=5)
    lbl_Enc1.place(x=5, y=25)
    lbl_Enc2.place(x=5, y=45)
    lbl_InstantTime.place(x=5, y=65)
    lbl_Odom_x.place(x=5, y=85)
    lbl_Odom_y.place(x=5, y=105)
    lbl_Odom_theta.place(x=5, y=125)
    lbl_Odom_velocity_linear.place(x=5, y=145)
    lbl_Odom_omega.place(x=5, y=165)

    ## Boto Exit
    btnSortir = Button(window, text="Exit", bg="grey",width=10,command=Sortir)
    btnSortir.place(x=70, y=250)
    Robot.connect()
    window.after(1,Loop)        # Llamada programada en 1ms a la función Loop
    window.mainloop()           # Arrancar la instancia de Ventana de Tkinter tipo Tk.
