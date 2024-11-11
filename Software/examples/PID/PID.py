class PID():
    def __init__(self, kp, ki, kd, setpoint=0, min_output=float('-inf'), max_output=float('inf')):
        """
        Inicializa el controlador PID con los valores de las ganancias
        kp, ki, kd y el setpoint deseado.
        
        Args:
        kp (float): Ganancia proporcional.
        ki (float): Ganancia integral.
        kd (float): Ganancia derivativa.
        setpoint (float): Valor de referencia o objetivo.
        min_output (float): Salida mínima del controlador.
        max_output (float): Salida máxima del controlador.
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.min_output = min_output
        self.max_output = max_output
        
        # Variables internas
        self.previous_error = 0
        self.integral = 0
        self.last_time = None

    def reset(self):
        """
        Reinicia el controlador PID (por ejemplo, cuando se empieza de nuevo).
        """
        self.previous_error = 0
        self.integral = 0
        self.last_time = None

    def Done(self):
        if self.previous_error < 0.001:
            return True
        else:
            return False

    def compute(self, actual_value, current_time):
        """
        Calcula la salida del PID basada en el valor actual del sistema.
        
        Args:
        actual_value (float): Valor actual del sistema que se está controlando.
        current_time (float): Tiempo actual (usado para calcular el delta de tiempo).

        Returns:
        float: La salida del PID después de aplicar las correcciones.
        """
        # Error entre el setpoint y el valor actual
        error = self.setpoint - actual_value

        # Si es la primera vez que se llama, inicializamos last_time
        if self.last_time is None:
            self.last_time = current_time
            return 0
        
        # Calculamos el tiempo transcurrido
        delta_time = current_time - self.last_time
        self.last_time = current_time

        if delta_time <= 0.0:
            return 0

        # Proporcional
        proportional = self.kp * error

        # Integral (acumulación de errores)
        self.integral += error * delta_time
        integral = self.ki * self.integral

        # Derivativo (cambio en el error)
        derivative = self.kd * (error - self.previous_error) / delta_time
        self.previous_error = error

        # PID Output
        output = proportional + integral + derivative

        # Clamping output to min/max values
        output = max(self.min_output, min(self.max_output, output))

        return output

'''  EXEMPLE D'ÚS

import time

# Crear un controlador PID con kp=1, ki=0.1, kd=0.01 y setpoint en 10
pid = PID(kp=1, ki=0.1, kd=0.01, setpoint=10, min_output=-100, max_output=100)

# Simulamos un sistema con una lectura actual de 0
actual_value = 0

# Iteramos para ver cómo el PID ajusta el valor a lo largo del tiempo
for i in range(100):
    current_time = time.time()
    control_signal = pid.compute(actual_value, current_time)
    print(f"Time: {i}, Control Signal: {control_signal}, Actual Value: {actual_value}")
    
    # Supongamos que el sistema responde de forma lineal a la señal de control
    actual_value += control_signal * 0.1
    
    time.sleep(0.1)  # Simulación de tiempo real
'''