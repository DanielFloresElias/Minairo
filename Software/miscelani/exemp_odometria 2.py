import math

class OmnidirectionalRobot:
    def __init__(self, ticks_per_rev, r, D):
        self.ticks_per_rev = ticks_per_rev
        self.r = r
        self.D = D
        self.x = 0.0  # Posición acumulada en x
        self.y = 0.0  # Posición acumulada en y
        self.theta = 0.0  # Orientación acumulada en grados

    def calculate_odometry(self, encoder_vals, prev_encoder_vals, InstantTime, prev_InstantTime):
        """
        Calcula la posición, orientación y velocidad del robot omnidireccional.

        :param encoder_vals: Lista de valores actuales de los encoders [encoder0, encoder1, encoder2]
        :param prev_encoder_vals: Lista de valores previos de los encoders [encoder0, encoder1, encoder2]
        :param InstantTime: Tiempo actual de la lectura del encoder (en milisegundos)
        :param prev_InstantTime: Tiempo previo de la lectura del encoder (en milisegundos)
        :return: dict con posición x, y, theta (en grados), velocidad lineal, y dirección de la velocidad
        """
        
        # Convertir el tiempo de milisegundos a segundos
        dT = (InstantTime - prev_InstantTime) / 1000.0
        
        # Convertir ticks a radianes
        delta_ticks = [encoder_vals[i] - prev_encoder_vals[i] for i in range(3)]
        delta_rad = [(2 * math.pi * delta_ticks[i]) / self.ticks_per_rev for i in range(3)]
        print (delta_rad)

        # Convertir radianes a desplazamiento lineal de las ruedas
        delta_s = [delta_rad[i] * self.r for i in range(3)]

        # Ángulos de las ruedas en radianes
        theta_0 = math.radians(-60)
        theta_1 = math.radians(60)
        theta_2 = math.radians(180)
        
        # Cinemática inversa para obtener las velocidades en el marco del robot
        inv_kin_matrix = [
            [-math.sin(theta_0), -math.sin(theta_1), -math.sin(theta_2)],
            [math.cos(theta_0), math.cos(theta_1), math.cos(theta_2)],
            [1 / self.D, 1 / self.D, 1 / self.D]
        ]
        
        # Velocidades de las ruedas
        wheel_velocities = [delta_s[i] / dT for i in range(3)]

        # Velocidades del robot (vx, vy, omega)
        robot_velocities = [
            sum(inv_kin_matrix[0][i] * wheel_velocities[i] for i in range(3)) / self.r,
            sum(inv_kin_matrix[1][i] * wheel_velocities[i] for i in range(3)) / self.r,
            sum(inv_kin_matrix[2][i] * wheel_velocities[i] for i in range(3)) / self.r
        ]

        # Calcular desplazamientos en el marco del robot
        vx, vy, omega = robot_velocities
        dx = vx * dT
        dy = vy * dT
        dtheta = omega * dT

        # Actualizar la posición y orientación del robot en el marco global
        self.x += dx * math.cos(math.radians(self.theta)) - dy * math.sin(math.radians(self.theta))
        self.y += dx * math.sin(math.radians(self.theta)) + dy * math.cos(math.radians(self.theta))
        self.theta += math.degrees(dtheta)

        # Calcular la velocidad lineal total y la dirección de la velocidad
        velocity_linear = math.sqrt(vx**2 + vy**2)
        direction_angle = math.degrees(math.atan2(vy, vx))

        return {
            'x': self.x,
            'y': self.y,
            'theta': self.theta,
            'velocity_linear': velocity_linear,
            'direction_angle': direction_angle
        }

# Ejemplo de uso
robot = OmnidirectionalRobot(ticks_per_rev=2048, r=0.05, D=0.15)

# Valores iniciales
encoder_vals = [100, -50,0]
prev_encoder_vals = [0, 0, 0]
InstantTime = 100  # Tiempo actual en milisegundos
prev_InstantTime = 0  # Tiempo anterior en milisegundos

# Primer cálculo de odometría
odometry = robot.calculate_odometry(encoder_vals, prev_encoder_vals, InstantTime, prev_InstantTime)
print(odometry)

# Valores nuevos
prev_encoder_vals = encoder_vals
encoder_vals = [200,-100, 0]
prev_InstantTime = InstantTime
InstantTime = 200  # Tiempo actual en milisegundos

# Segundo cálculo de odometría
odometry = robot.calculate_odometry(encoder_vals, prev_encoder_vals, InstantTime, prev_InstantTime)
print(odometry)
