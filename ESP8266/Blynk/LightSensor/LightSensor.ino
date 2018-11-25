#define BLYNK_PRINT Serial

#include <Wire.h>
#include <BH1750.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include "credentials.h"


char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = WIFI_SSID;
char pass[] = WIFI_PASSWD;

BH1750 lightMeter;

void setup() {
  // Debug console
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(5, OUTPUT);
  Serial.begin(9600);
  Blynk.begin(auth, ssid, pass);

    // Initialize the I2C bus (BH1750 library doesn't do this automatically)
  // On esp8266 devices you can select SCL and SDA pins using Wire.begin(D4, D3);
  Wire.begin();

  lightMeter.begin();
  Serial.println(F("BH1750 Test"));
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

void loop() {
  Blynk.run();
}
