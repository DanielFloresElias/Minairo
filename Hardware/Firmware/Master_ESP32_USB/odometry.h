#include <Arduino.h>
#include <math.h>

#include "COMParameters.h"
#ifndef odometry_h_
#define odometry_h_

class Odometry {
  public:
    Odometry(float ticks_per_rev, float r, float D);
    _ODOM calculate_odometry(int encoder_vals[], int prev_encoder_vals[], unsigned long InstantTime, unsigned long prev_InstantTime);
  private:
    float ticks_per_rev;
    float r;
    float D;
    float x;
    float y;
    float theta;
};

#endif