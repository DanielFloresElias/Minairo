#include <Arduino.h>
#include <math.h>
#include "odometry.h"

class OmnidirectionalRobot {
  public:
    OmnidirectionalRobot(float ticks_per_rev, float r, float D)
      : ticks_per_rev(ticks_per_rev), r(r), D(D), x(0.0), y(0.0), theta(0.0) {}

    struct Odometry {
      float x;
      float y;
      float theta;
      float velocity_linear;
      float direction_angle;
    };

    Odometry calculate_odometry(int encoder_vals[], int prev_encoder_vals[], unsigned long InstantTime, unsigned long prev_InstantTime) {
      // Convertir el tiempo de milisegundos a segundos
      float dT = (InstantTime - prev_InstantTime) / 1000.0;

      // Convertir ticks a radianes
      float delta_ticks[3];
      float delta_rad[3];
      float delta_s[3];
      for (int i = 0; i < 3; i++) {
        delta_ticks[i] = encoder_vals[i] - prev_encoder_vals[i];
        delta_rad[i] = (2 * M_PI * delta_ticks[i]) / ticks_per_rev;
        delta_s[i] = delta_rad[i] * r;
      }

      // Ángulos de las ruedas en radianes
      float theta_0 = radians(60);
      float theta_1 = radians(180);
      float theta_2 = radians(300);

      // Cinemática inversa para obtener las velocidades en el marco del robot
      float inv_kin_matrix[3][3] = {
        {-sin(theta_0), -sin(theta_1), -sin(theta_2)},
        {cos(theta_0), cos(theta_1), cos(theta_2)},
        {1 / D, 1 / D, 1 / D}
      };

      // Velocidades de las ruedas
      float wheel_velocities[3];
      for (int i = 0; i < 3; i++) {
        wheel_velocities[i] = delta_s[i] / dT;
      }

      // Velocidades del robot (vx, vy, omega)
      float robot_velocities[3] = {0, 0, 0};
      for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
          robot_velocities[i] += inv_kin_matrix[i][j] * wheel_velocities[j];
        }
        robot_velocities[i] /= r;
      }

      float vx = robot_velocities[0];
      float vy = robot_velocities[1];
      float omega = robot_velocities[2];

      // Calcular desplazamientos en el marco del robot
      float dx = vx * dT;
      float dy = vy * dT;
      float dtheta = omega * dT;

      // Actualizar la posición y orientación del robot en el marco global
      x += dx * cos(radians(theta)) - dy * sin(radians(theta));
      y += dx * sin(radians(theta)) + dy * cos(radians(theta));
      theta += degrees(dtheta);

      // Calcular la velocidad lineal total y la dirección de la velocidad
      float velocity_linear = sqrt(vx * vx + vy * vy);
      float direction_angle = degrees(atan2(vy, vx));

      Odometry odometry = {x, y, theta, velocity_linear, direction_angle};
      return odometry;
    }

  private:
    float ticks_per_rev;
    float r;
    float D;
    float x;
    float y;
    float theta;
};

// Ejemplo de uso
OmnidirectionalRobot robot(2048, 0.05, 0.15);

void setup() {
  Serial.begin(115200);

  // Valores iniciales
  int encoder_vals[3] = {1000, 1050, 1100};
  int prev_encoder_vals[3] = {950, 1000, 1050};
  unsigned long InstantTime = 2000;  // Tiempo actual en milisegundos
  unsigned long prev_InstantTime = 1900;  // Tiempo anterior en milisegundos

  // Primer cálculo de odometría
  OmnidirectionalRobot::Odometry odometry = robot.calculate_odometry(encoder_vals, prev_encoder_vals, InstantTime, prev_InstantTime);
  Serial.print("x: "); Serial.print(odometry.x); Serial.print(" y: "); Serial.print(odometry.y);
  Serial.print(" theta: "); Serial.print(odometry.theta); Serial.print(" velocity_linear: "); Serial.print(odometry.velocity_linear);
  Serial.print(" direction_angle: "); Serial.println(odometry.direction_angle);

  // Valores nuevos
  prev_encoder_vals[0] = encoder_vals[0];
  prev_encoder_vals[1] = encoder_vals[1];
  prev_encoder_vals[2] = encoder_vals[2];
  encoder_vals[0] = 1050;
  encoder_vals[1] = 1100;
  encoder_vals[2] = 1150;
  prev_InstantTime = InstantTime;
  InstantTime = 2100;  // Tiempo actual en milisegundos

  // Segundo cálculo de odometría
  odometry = robot.calculate_odometry(encoder_vals, prev_encoder_vals, InstantTime, prev_InstantTime);
  Serial.print("x: "); Serial.print(odometry.x); Serial.print(" y: "); Serial.print(odometry.y);
  Serial.print(" theta: "); Serial.print(odometry.theta); Serial.print(" velocity_linear: "); Serial.print(odometry.velocity_linear);
  Serial.print(" direction_angle: "); Serial.println(odometry.direction_angle);
}

void loop() {
  // No hay necesidad de hacer nada aquí
}
