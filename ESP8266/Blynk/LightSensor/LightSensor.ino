#define BLYNK_PRINT Serial

#include <BH1750FVI.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include "credentials.h"
#include <TimeLib.h>
#include <WidgetRTC.h>

char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = WIFI_SSID;
char pass[] = WIFI_PASSWD;

BH1750FVI LightSensor(BH1750FVI::k_DevModeContLowRes);
/*
  Connecting the sensor to a NodeMCU ESP8266:
  VCC  <-> 3V3
  GND  <-> GND
  SDA  <-> D2
  SCL  <-> D1
*/  


 /*************************************************************
  App project setup:
    1 sec timet on V1 - get LightSensor Data from BH1750: SCL  <-> D1, SDA  <-> D2
    Time Input widget on V2.

  slider input on V5 - PWM on D5 in WeMos
    
 *************************************************************/


WidgetRTC rtc;
 
BlynkTimer timer;
BlynkTimer timer10sec;

// This function sends Arduino's up time every second to Virtual Pin (1).
// In the app, Widget's reading frequency should be set to PUSH. This means
// that you define how often to send data to Blynk App.
void myTimerEvent()
{
  // You can send any value at any time.
  // Please don't send more that 10 values per second.
  uint16_t lux = LightSensor.GetLightIntensity();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");
  Blynk.virtualWrite(V1,lux );
}

void clockDisplay()
{
  // You can call hour(), minute(), ... at any time
  // Please see Time library examples for details

  String currentTime = String(hour()) + ":" + minute() + ":" + second();
  String currentDate = String(day()) + " " + month() + " " + year();
  Serial.print("Current time: ");
  Serial.print(currentTime);
  Serial.print(" ");
  Serial.print(currentDate);
  Serial.println();

  // Send time to the App
  Blynk.virtualWrite(V4, currentTime);

}

BLYNK_CONNECTED() {
  // Synchronize time on connection
  rtc.begin();

}

void setup() {
  // Debug console
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(5, OUTPUT);
  Serial.begin(9600);
  Blynk.begin(auth, ssid, pass);

  LightSensor.begin();  
  Serial.println(F("BH1750 Test")); 
  timer.setInterval(1000L, myTimerEvent);

  setSyncInterval(1 * 60); // Sync interval in seconds (10 minutes)
  // Display digital clock every 10 seconds
  timer10sec.setInterval(1000L, clockDisplay);
}

BLYNK_WRITE(V5) {
  int slideValue = param.asInt(); // assigning incoming value from pin V5 to a variable
  int pinValue = 0;
  pinValue = map(slideValue, -10000, 10000, 0, 500);
  Serial.print("V5 Slider value is: ");
  Serial.print(slideValue);
  Serial.print(", D5 pin value is: ");
  Serial.println(pinValue);
  analogWrite(D5, pinValue);
  Blynk.virtualWrite(V0, pinValue); 
}

BLYNK_WRITE(V2) {
  TimeInputParam t(param);
  Serial.println(String("Start: ") +
                   t.getStartHour() + ":" +
                   t.getStartMinute() + ":" +
                   t.getStartSecond());
  Serial.print("V2 timer value is: ");
  long startTimeInSecs = param[0].asLong();
  Serial.println(startTimeInSecs);
  Serial.println(String("Time zone: ") + t.getTZ());
  Serial.println();
}

void loop() {
  Blynk.run();
  timer.run();
}
