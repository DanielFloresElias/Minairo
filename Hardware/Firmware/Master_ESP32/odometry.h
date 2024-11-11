#include <Arduino.h>
#include <math.h>

#include "COMParameters.h"
#ifndef odometry_h_
#define odometry_h_

class Odometry {
  public:
   // Constructor
    Odometry(float ticks_per_rev, float r, float D);
    // Método para resetear la odometría
    void reset_odometry();
    // Método para calcular la odometría
    _ODOM calculate_odometry(int encoder_vals[], int prev_encoder_vals[], unsigned long InstantTime, unsigned long prev_InstantTime);
  private:
    float ticks_per_rev;
    float r;
    float D;
    float x;
    float y;
    float theta;
    const float _cos30 = 0.8660254;
};

#endif