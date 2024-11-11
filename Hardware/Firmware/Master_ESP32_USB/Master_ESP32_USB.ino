/*
    __  __ _             _        _    __   ___
   |  \/  (_)           (_)      //   /_ | / _ \
   | \  / |_ _ __   __ _ _ _ __ ___    | || | | |
   | |\/| | | '_ \ / _` | | '__/ _ \   | || | | |
   | |  | | | | | | (_| | | | | (_) |  | || |_| |
   |_|  |_|_|_| |_|\__,_|_|_|  \___/   |_(_)___/

  Versión para comunicación série mediante USB. 

*/

#include <Wire.h>
#include "COMParameters.h"
#include "odometry.h"

int kk = 0;
bool RawFlag = false;

_RAW_IN Raw_IN;
_RAW_OUT Raw_OUT;

_SLAVE0_IN Slave_0_IN;
_SLAVE0_OUT Slave_0_OUT;

_SLAVE1_IN Slave_1_IN;
_SLAVE1_OUT Slave_1_OUT;

_SLAVE2_IN Slave_2_IN;
_SLAVE2_OUT Slave_2_OUT;

_ODOM Odom;


#define I2C_SDA 21
#define I2C_SCL 22


int led = 2;
int SALVE_0_ADDR = 8;
int SALVE_1_ADDR = 9;
int SALVE_2_ADDR = 10;
int n = 0;

bool TimeOut = false;
int TempsTimeOut = 500;
int TransmitTime = 20;
unsigned long TempsOld_TimeOut = 0;
unsigned long TempsOld_TransmitTime = 0;
unsigned long TempsOld_LED_Pulse = 0;
unsigned long LED_Pulse_width = 25;
unsigned long TempsCicle = 0;

// Variables Odometry
unsigned long EncoderOldTime = 0;
bool EncoderFirstPoll = true;
Odometry robot(4480, 0.04, 0.15);
int encoder_vals[3] = { 0, 0, 0 };
int prev_encoder_vals[3] = { 0, 0, 0 };

void setup() {

  Serial.begin(115200);

  Slave_0_IN.INPUT_DATA.CtrlWord1 = 0B0000000000000000;
  Slave_0_IN.INPUT_DATA.CtrlWord2 = 0B0000000000000000;
  Slave_0_IN.INPUT_DATA.SetPoint = 0;

  Slave_1_IN.INPUT_DATA.x = 0.0;
  Slave_1_IN.INPUT_DATA.y = 0.0;
  Slave_1_IN.INPUT_DATA.w = 0.0;

  Slave_2_IN.INPUT_DATA.GPIO_Config = B00000000;
  Slave_2_IN.INPUT_DATA.GPIO_Value = B00000000;
  Slave_2_IN.INPUT_DATA.Servo_0 = 1500;
  Slave_2_IN.INPUT_DATA.Servo_1 = 1500;
  Slave_2_IN.INPUT_DATA.Servo_2 = 1500;
  Slave_2_IN.INPUT_DATA.Servo_3 = 1500;
  Slave_2_IN.INPUT_DATA.Servo_4 = 1500;

  pinMode(led, OUTPUT);
  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.setClock(400000L);
}

void loop() {
  uint8_t i;


  if (Serial.available() >= 32) {
    // START DEL COMUNICATION-LED PULSE INDICATOR
    digitalWrite(led, HIGH);
    TempsOld_LED_Pulse = millis();

    // TRAMA DE LECTURA
    Serial.readBytes(Raw_IN.B, 32);

    // TRAMA DE RESPUESTA
    Serial.write(Raw_OUT.B, 80);

    // TRATAMIENTO DE LA TRAMA RECIBIDA //
    Slave_1_IN.INPUT_DATA.x = -Raw_IN.INPUT_DATA.x;  // x(m/s);
    Slave_1_IN.INPUT_DATA.y = -Raw_IN.INPUT_DATA.y;  // y(m/s);
    Slave_1_IN.INPUT_DATA.w = -Raw_IN.INPUT_DATA.w;  // w(m/s);
    Slave_2_IN.INPUT_DATA.GPIO_Config = Raw_IN.INPUT_DATA.GPIO_Config;
    Slave_2_IN.INPUT_DATA.GPIO_Value = Raw_IN.INPUT_DATA.GPIO_Value;
    Slave_2_IN.INPUT_DATA.Servo_0 = Raw_IN.INPUT_DATA.Servo_0;
    Slave_2_IN.INPUT_DATA.Servo_1 = Raw_IN.INPUT_DATA.Servo_1;
    Slave_2_IN.INPUT_DATA.Servo_2 = Raw_IN.INPUT_DATA.Servo_2;
    Slave_2_IN.INPUT_DATA.Servo_3 = Raw_IN.INPUT_DATA.Servo_3;
    Slave_2_IN.INPUT_DATA.Servo_4 = Raw_IN.INPUT_DATA.Servo_4;

    // RESET DEL TIMEOUT000
    TempsOld_TimeOut = millis();
  }




  // CONTROL DEL TIMEOUT DE LES TRANSMISSIONS PER LA UART //
  //////////////////////////////////////////////////////////
  if (millis() - TempsOld_TimeOut > TempsTimeOut) {
    Slave_1_IN.INPUT_DATA.x = 0.0;
    Slave_1_IN.INPUT_DATA.y = 0.0;
    Slave_1_IN.INPUT_DATA.w = 0.0;
  }
  // COMUNICATION-LED PULSE CONTROL //
  //////////////////////////////////////////////////////////
  if (millis() - TempsOld_LED_Pulse > LED_Pulse_width) {
    digitalWrite(led, LOW);
  }

  // CONTROL DE LES TRANSMISSIONS PER LA I2C //
  //////////////////////////////////////////////////////////

  if (millis() - TempsOld_TransmitTime > TransmitTime) {
    TempsOld_TransmitTime = millis();

    ///////////////// Comunicacion con SLAVE 0 /////////////////
    Wire.beginTransmission(SALVE_0_ADDR);  // transmit to device SLAVE_0
    for (int i = 0; i < sizeof(Slave_0_IN); i++) {
      Wire.write(Slave_0_IN.B[i]);
    }
    Wire.endTransmission();  // stop transmitting

    Wire.requestFrom(SALVE_0_ADDR, sizeof(Slave_0_OUT));  // Solicitar x bytes del esclavo 0
    n = 0;
    while (Wire.available()) {         // slave may send less than requested
      Slave_0_OUT.B[n] = Wire.read();  // receive a byte as character
      n++;
    }
    for (int i = 0; i < sizeof(Slave_0_OUT); i++) {
      Raw_OUT.B[i] = Slave_0_OUT.B[i];
    }

    ///////////////// Comunicacion con SLAVE 1 ///////////////// - Control de Motores Motrízes
    Wire.beginTransmission(SALVE_1_ADDR);  // transmit to device SLAVE_1
    for (int i = 0; i < sizeof(Slave_1_IN); i++) {
      Wire.write(Slave_1_IN.B[i]);
    }
    Wire.endTransmission();  // stop transmitting

    Wire.requestFrom(SALVE_1_ADDR, sizeof(Slave_1_OUT));  // Solicitar x bytes del esclavo 1
    n = 0;
    while (Wire.available()) {         // slave may send less than requested
      Slave_1_OUT.B[n] = Wire.read();  // receive a byte as character
      n++;
    }

    for (int i = 0; i < sizeof(Slave_1_OUT); i++) {
      Raw_OUT.B[i + 44] = Slave_1_OUT.B[i];
    }

    ///////////////// Comunicacion con SLAVE 2 /////////////////
    Wire.beginTransmission(SALVE_2_ADDR);  // transmit to device SLAVE_2
    for (int i = 0; i < sizeof(Slave_2_IN); i++) {
      Wire.write(Slave_2_IN.B[i]);
    }
    Wire.endTransmission();  // stop transmitting

    Wire.requestFrom(SALVE_2_ADDR, sizeof(Slave_2_OUT));  // Solicitar x bytes del esclavo 2
    n = 0;
    while (Wire.available()) {         // slave may send less than requested
      Slave_2_OUT.B[n] = Wire.read();  // receive a byte as character
      n++;
    }
    for (int i = 0; i < sizeof(Slave_2_OUT); i++) {
      Raw_OUT.B[i + 32] = Slave_2_OUT.B[i];
    }

    if (EncoderFirstPoll) {
      EncoderFirstPoll = false;
      EncoderOldTime = Slave_1_OUT.OUTPUT_DATA.InstantTime;
    }
    encoder_vals[0] = Slave_1_OUT.OUTPUT_DATA.EncoderValue_0;
    encoder_vals[1] = Slave_1_OUT.OUTPUT_DATA.EncoderValue_1;
    encoder_vals[2] = Slave_1_OUT.OUTPUT_DATA.EncoderValue_2;
    //Odometría
    Raw_OUT.OUTPUT_DATA.Odometry = robot.calculate_odometry(encoder_vals, prev_encoder_vals, Slave_1_OUT.OUTPUT_DATA.InstantTime, EncoderOldTime);
    for (int i = 0; i < 3; i++) prev_encoder_vals[i] = encoder_vals[i];
    EncoderOldTime = Slave_1_OUT.OUTPUT_DATA.InstantTime;
  }
}