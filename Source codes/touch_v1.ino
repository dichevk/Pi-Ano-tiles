/*
   >=16 capactive touch tiles
   UART communication of Arduino to Pi (USB)

   Date: 12/10/2020
   Author: M.Lievense

   Source: https://learn.sparkfun.com/tutorials/mpr121-hookup-guide/all
*/

#include "mpr121.h"
#include <Wire.h>

// Global Constants
#define TOU_THRESH  0x06
#define REL_THRESH  0x0A

// Pin settings
int irqpin_1 = 2;  // Digital 2

// Variable
boolean show = true;
boolean touchStates[12];

void setup() {
  pinMode(irqpin_1, INPUT);
  digitalWrite(irqpin_1, HIGH); //enable pullup resistor

  Serial.begin(115200); // usb
  Serial.println("Serial active");
  Wire.begin();

  mpr121_setup(0x5A);
  delay(100);

  Serial.println("Touch sensor started");
}

void loop() {
  if (!digitalRead(irqpin_1)) {
    readTouchInputs(0x5A);
//    for (int i = 0; i < 12; i++) Serial.print(touchStates[i]);
//    Serial.println('/n');
  }
}

// ********** MPR121 Touch sensors **********

void readTouchInputs(int ADDR) {
  //read the touch state from the MPR121
  Wire.requestFrom(ADDR, 2);

  byte LSB = Wire.read();
  byte MSB = Wire.read();
  int ID = 0;

  uint16_t touched = ((MSB << 8) | LSB); //16bits that make up the touch states
  for (int i = 0; i < 12; i++) { // Check what electrodes were pressed
    ID = i;

    if (touched & (1 << i)) {
      if (touchStates[i] == 0) {
        //pin i was just touched
        if(ID<10) Serial.println(ID);
      } else if (touchStates[i] == 1) {
        //pin i is still being touched
      }
      touchStates[i] = 1;
    } else {
      if (touchStates[i] == 1) {
        //Serial.print("O");
        //Serial.println(ID);
      }
      touchStates[i] = 0;
    }
  }
}

void mpr121_setup(int ADDR) {
  set_register(ADDR, ELE_CFG, 0x00);
  // Section A - Controls filtering when data is > baseline.
  set_register(ADDR, MHD_R, 0x01);
  set_register(ADDR, NHD_R, 0x01);
  set_register(ADDR, NCL_R, 0x00);
  set_register(ADDR, FDL_R, 0x00);
  // Section B - Controls filtering when data is < baseline.
  set_register(ADDR, MHD_F, 0x01);
  set_register(ADDR, NHD_F, 0x01);
  set_register(ADDR, NCL_F, 0xFF);
  set_register(ADDR, FDL_F, 0x02);
  // Section C - Sets touch and release thresholds for each electrode
  set_register(ADDR, ELE0_T, TOU_THRESH);
  set_register(ADDR, ELE0_R, REL_THRESH);

  set_register(ADDR, ELE1_T, TOU_THRESH);
  set_register(ADDR, ELE1_R, REL_THRESH);

  set_register(ADDR, ELE2_T, TOU_THRESH);
  set_register(ADDR, ELE2_R, REL_THRESH);

  set_register(ADDR, ELE3_T, TOU_THRESH);
  set_register(ADDR, ELE3_R, REL_THRESH);

  set_register(ADDR, ELE4_T, TOU_THRESH);
  set_register(ADDR, ELE4_R, REL_THRESH);

  set_register(ADDR, ELE5_T, TOU_THRESH);
  set_register(ADDR, ELE5_R, REL_THRESH);

  set_register(ADDR, ELE6_T, TOU_THRESH);
  set_register(ADDR, ELE6_R, REL_THRESH);

  set_register(ADDR, ELE7_T, TOU_THRESH);
  set_register(ADDR, ELE7_R, REL_THRESH);

  set_register(ADDR, ELE8_T, TOU_THRESH);
  set_register(ADDR, ELE8_R, REL_THRESH);

  set_register(ADDR, ELE9_T, TOU_THRESH);
  set_register(ADDR, ELE9_R, REL_THRESH);

  set_register(ADDR, ELE10_T, TOU_THRESH);
  set_register(ADDR, ELE10_R, REL_THRESH);

  set_register(ADDR, ELE11_T, TOU_THRESH);
  set_register(ADDR, ELE11_R, REL_THRESH);

  // Section D
  // Set the Filter Configuration
  // Set ESI2
  set_register(ADDR, FIL_CFG, 0x04);

  // Section E
  // Electrode Configuration
  // Set ELE_CFG to 0x00 to return to standby mode
  set_register(ADDR, ELE_CFG, 0x0C);  // Enables all 12 Electrodes


  // Section F
  // Enable Auto Config and auto Reconfig
  /*set_register(0x5A, ATO_CFG0, 0x0B);
    set_register(0x5A, ATO_CFGU, 0xC9);  // USL = (Vdd-0.7)/vdd*256 = 0xC9 @3.3V   set_register(0x5A, ATO_CFGL, 0x82);  // LSL = 0.65*USL = 0x82 @3.3V
    set_register(0x5A, ATO_CFGT, 0xB5);*/  // Target = 0.9*USL = 0xB5 @3.3V

  set_register(ADDR, ELE_CFG, 0x0C);
}

void set_register(int address, unsigned char r, unsigned char v) {
  Wire.beginTransmission(address);
  Wire.write(r);
  Wire.write(v);
  Wire.endTransmission();
}
