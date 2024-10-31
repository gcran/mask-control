#include "Adafruit_seesaw.h"
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <math.h>

// define input button mapping
#define BUTTON_X         6
#define BUTTON_Y         2
#define BUTTON_A         5
#define BUTTON_B         1
#define BUTTON_SELECT    0
#define BUTTON_START    16

// define motor constants:
// maximum, minimum and center angles
const int L_PAN_ULIM = 135;
const int L_TILT_ULIM = 135;
const int L_PAN_LLIM = 45;
const int L_TILT_LLIM = 45;
const int L_PAN_CENTER = 90;
const int L_TILT_CENTER = 90;

const int R_PAN_ULIM = 120;
const int R_TILT_ULIM = 120;
const int R_PAN_LLIM = 70;
const int R_TILT_LLIM = 70;
const int R_PAN_CENTER = 90;
const int R_TILT_CENTER = 90;

// servo speed, maximum counts per second
const int SRV_RATE = 300;

// LED cross fade rate, counts per second
const int LED_RATE = 4095;

// device update rate in milliseconds
const int UPDATE_RATE = 20;

// define max and min pulse rates, and full range of servo motors
const float MIN_PULSE = 5e-4;
const float MAX_PULSE = 2.4e-3;
const int SRV_RANGE = 180;


// define PWM period and full scale input range
const float PWM_PERIOD = 20e-3;
const int SRV_PWM_FREQ = 50;
const int LED_PWM_FREQ = 240;
const int FSR = 0x0FFF;
int min_count, max_count;

// define PCA9685 addresses
const int SRV_ADDR = 0x40;
const int LED_ADDR = 0x41;
const int PAD_ADDR = 0x50;
const int L_PAN_CHANNEL = 1;
const int L_TILT_CHANNEL = 0;
const int R_PAN_CHANNEL = 2;
const int R_TILT_CHANNEL = 3;
const int l_r = 3;
const int l_g = 1;
const int l_b = 2;
const int r_r = 10;
const int r_g = 15;
const int r_b = 12;

uint32_t button_mask = (1UL << BUTTON_X) | (1UL << BUTTON_Y) | (1UL << BUTTON_START) |
                       (1UL << BUTTON_A) | (1UL << BUTTON_B) | (1UL << BUTTON_SELECT);
uint32_t prev_buttons = 0;

Adafruit_seesaw ss;
Adafruit_PWMServoDriver srv_pca = Adafruit_PWMServoDriver(SRV_ADDR);
Adafruit_PWMServoDriver led_pca = Adafruit_PWMServoDriver(LED_ADDR);

// initialize commands and setpoints
int l_tilt_cmd = 0;
int l_pan_cmd = 0;
int r_tilt_cmd = 0;
int r_pan_cmd = 0;
int r_cmd = 0;
int g_cmd = 0;
int b_cmd = 0;

int l_tilt_stpt = 0;
int r_tilt_stpt = 0;
int l_pan_stpt = 0;
int r_pan_stpt = 0;
int r_stpt = 0;
int g_stpt = 0;
int b_stpt = 0;

float intensity = 1;

unsigned long prev_time;
bool serial_override = false;

void setup() {
  // Serial monitor setup
  Serial.begin(115200);
 
  // Print to monitor
  Serial.println("PCA9685 Servo Test");
  
  // calculate count ranges
  min_count = round((MIN_PULSE / PWM_PERIOD) * FSR);
  max_count = round((MAX_PULSE / PWM_PERIOD) * FSR);

  // start peripherals
  srv_pca.begin();
  led_pca.begin();
  led_pca.setPWMFreq(LED_PWM_FREQ);
  srv_pca.setPWMFreq(SRV_PWM_FREQ);
  ss.begin(PAD_ADDR);
  ss.pinModeBulk(button_mask, INPUT_PULLUP);
  ss.setGPIOInterrupts(button_mask, 1);
  Serial.println(ss.getVersion());

  srv_pca.setPWM(L_TILT_CHANNEL, 0, angle2count(L_TILT_CENTER));
  srv_pca.setPWM(R_TILT_CHANNEL, 0, angle2count(R_TILT_CENTER));
  srv_pca.setPWM(L_PAN_CHANNEL, 0, angle2count(L_PAN_CENTER));
  srv_pca.setPWM(R_PAN_CHANNEL, 0, angle2count(R_PAN_CENTER));
  led_pca.setPWM(l_r, 0, 0);
  led_pca.setPWM(l_g, 0, 0);
  led_pca.setPWM(l_b, 0, 0);
  led_pca.setPWM(r_r, 0, 0);
  led_pca.setPWM(r_g, 0, 0);
  led_pca.setPWM(r_b, 0, 0);  

  prev_time = millis();
}

void loop() {

  // check for serial data and commands
  int numbytes = Serial.available();
  if (numbytes > 0) {
    char serial_input[36];
    for (int i=0; i<numbytes;i++) {
      serial_input[i] = Serial.read();
    }
    char * token = strtok(serial_input, " ");
    int arg_cnt = 0;
    while (token != NULL) {
      int arg = strtol(token, NULL, 10);
      switch (arg_cnt) {
        case 0:
          if (arg == 1) {
            serial_override = true;
          } else {
            serial_override = false;
          }
        case 1:
          l_tilt_stpt = angle2count(min(L_TILT_ULIM, max(L_TILT_LLIM, arg)));
        case 2:
          r_tilt_stpt = angle2count(min(R_TILT_ULIM, max(R_TILT_LLIM, arg)));
        case 3:
          l_pan_stpt = angle2count(min(L_PAN_ULIM, max(L_PAN_LLIM, arg)));
        case 4:
          r_pan_stpt = angle2count(min(R_PAN_ULIM, max(R_PAN_LLIM, arg)));
        case 5:
          r_stpt = min(4095, max(0, arg));
        case 6:
          g_stpt = min(4095, max(0, arg));
        case 7:
          b_stpt = min(4095, max(0, arg));
      }
      arg_cnt++;
      token = strtok(NULL, " ");
    }
  } else {
      
      // acquire thumbstick position and convert to servo position
      if (serial_override == false) {
        int pan_pot = 1023 - ss.analogRead(14);
        int tilt_pot = 1023 - ss.analogRead(15);

        l_tilt_stpt = angle2count(pot2angle(tilt_pot, L_TILT_LLIM, L_TILT_ULIM, L_TILT_CENTER));
        r_tilt_stpt = angle2count(pot2angle(tilt_pot, R_TILT_LLIM, R_TILT_ULIM, R_TILT_CENTER));
        l_pan_stpt = angle2count(pot2angle(pan_pot, L_PAN_LLIM, L_PAN_ULIM, L_PAN_CENTER));
        r_pan_stpt = angle2count(pot2angle(pan_pot, R_PAN_LLIM, R_PAN_ULIM, R_PAN_CENTER));

        // check button state and set lights
        uint32_t buttons = ss.digitalReadBulk(button_mask);
        if (! (buttons & (1UL << BUTTON_A))) {
          Serial.print("A ");
          r_stpt = 3000;
          b_stpt = 2000;
          g_stpt = 3000;
        }
        if (! (buttons & (1UL << BUTTON_B))) {
          Serial.print("B ");
          if ((prev_buttons & (1UL << BUTTON_B))) {
            if (intensity >= 1) {
              intensity = 0;
              } else {
                intensity = intensity + 0.1;
            }
          }
        }
        if (! (buttons & (1UL << BUTTON_Y))) {
          Serial.print("Y ");
          r_stpt = 4095;
          b_stpt = 0;
          g_stpt = 0;
        }
        if (! (buttons & (1UL << BUTTON_X))) {
          Serial.print("X ");
          r_stpt = 0;
          b_stpt = 0;
          g_stpt = 0;
        }
        if (! (buttons & (1UL << BUTTON_SELECT))) {
          Serial.print("SEL ");
        }
        if (! (buttons & (1UL << BUTTON_START))) {
          Serial.print("START ");
        }
        prev_buttons = buttons;
      }
  }

  // determine motor and led command
  unsigned long curr_time = millis();
  unsigned long delta_time = curr_time - prev_time;
  if (delta_time >= UPDATE_RATE) {
    l_tilt_cmd = rateLimit(l_tilt_cmd, l_tilt_stpt, SRV_RATE, delta_time);
    r_tilt_cmd = rateLimit(r_tilt_cmd, r_tilt_stpt, SRV_RATE, delta_time);
    l_pan_cmd = rateLimit(l_pan_cmd, l_pan_stpt, SRV_RATE, delta_time);
    r_pan_cmd = rateLimit(r_pan_cmd, r_pan_stpt, SRV_RATE, delta_time);
    r_cmd = round(intensity * rateLimit(r_cmd, r_stpt, LED_RATE, delta_time));
    g_cmd = round(intensity * rateLimit(g_cmd, g_stpt, LED_RATE, delta_time));
    b_cmd = round(intensity * rateLimit(b_cmd, b_stpt, LED_RATE, delta_time));

    // Serial.print(buttons);
    Serial.print(" ");
    Serial.print(l_tilt_cmd);
    Serial.print(" ");
    Serial.print(l_pan_cmd);
    Serial.print(" ");
    Serial.print(r_cmd);
    Serial.print(" ");
    Serial.print(g_cmd);
    Serial.print(" ");
    Serial.println(b_cmd);

    srv_pca.setPWM(L_TILT_CHANNEL, 0, l_tilt_cmd);
    srv_pca.setPWM(R_TILT_CHANNEL, 0, r_tilt_cmd);
    srv_pca.setPWM(L_PAN_CHANNEL, 0, l_pan_cmd);
    srv_pca.setPWM(R_PAN_CHANNEL, 0, r_pan_cmd);
    led_pca.setPWM(l_r, 0, r_cmd);
    led_pca.setPWM(l_g, 0, g_cmd);
    led_pca.setPWM(l_b, 0, b_cmd);
    led_pca.setPWM(r_r, 0, r_cmd);
    led_pca.setPWM(r_g, 0, g_cmd);
    led_pca.setPWM(r_b, 0, b_cmd);

    prev_time = curr_time;
  }

  
  
}

// convert angle into PWM count
int angle2count(float a) {
  return map(a, 0, SRV_RANGE, min_count, max_count);
}

// convert thumbstick position to angle
float pot2angle(int p, int l, int u, int c) {
  if (p >= 512) {
    return map(p, 512, 1023, c, u);
  } else {
    return map(p, 0, 511, l, c);
  }
}

int rateLimit(int c_pos, int stpt, int r, unsigned long t) {
  int err = stpt - c_pos;
  int max_count = r * (t / 1000.0);
  if (err > 0) {
    return c_pos + min(max_count, err);
  } else {
    return c_pos + max(-max_count, err);
  }

}