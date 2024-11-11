#include <Arduino.h>
#include "directKinematic.h"

// Constructor de la clase
directKinematic::directKinematic(float RobotRadius, float WheelRadius)
{
    _RobRad = RobotRadius;
    _WheelRad = WheelRadius;
}

// Método para calcular la cinemática directa
robot_speed directKinematic::calc(motor_speed MotorSpeed)
{
    robot_speed RobotVel;

    // Cálculo de las velocidades lineales en X y Y, y la velocidad angular
    float v1 = MotorSpeed.angular[0] * _WheelRad;
    float v2 = MotorSpeed.angular[1] * _WheelRad;
    float v3 = MotorSpeed.angular[2] * _WheelRad;

    // Cinemática directa: calcular la velocidad en los ejes X, Y y angular (omega)
    RobotVel.linear[0] = (-v1 * _cos30 + v2 * _cos30) / 2.0;    // Velocidad en X
    RobotVel.linear[1] = (v1 * 0.5 + v2 * 0.5 - v3) / 2.0;      // Velocidad en Y
    RobotVel.angular = (v1 + v2 + v3) / (3 * _RobRad);          // Velocidad angular

    return RobotVel;  // Retorna la estructura con las velocidades del robot
}
