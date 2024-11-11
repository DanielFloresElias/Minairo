#ifndef DIRECTKINEMATIC_H
#define DIRECTKINEMATIC_H

#include <Arduino.h>

// Estructura para representar las velocidades del robot
struct robot_speed {
    float linear[2]; // Velocidades en X (linear[0]) y Y (linear[1])
    float angular;   // Velocidad angular (omega)
};

// Estructura para representar las velocidades de los motores
struct motor_speed {
    float angular[3]; // Velocidades angulares de los tres motores
};

class directKinematic {
public:
    // Constructor
    directKinematic(float RobotRadius, float WheelRadius);
    
    // Método para calcular la cinemática directa
    robot_speed calc(motor_speed MotorSpeed);

private:
    float _RobRad;   // Radio del robot
    float _WheelRad; // Radio de las ruedas
    const float _cos30 = 0.866; // cos(30 grados)
};

#endif
