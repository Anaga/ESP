#define BLYNK_PRINT Serial

#include <BH1750FVI.h>
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include "credentials.h"
#include <TimeLib.h>
#include <WidgetRTC.h>

// sKot
// BLYNK_AUTH_TOKEN_SK 

//Black Mini
//BLYNK_AUTH_TOKEN_BM

//White Medium
// BLYNK_AUTH_TOKEN_WM
char auth[] = BLYNK_AUTH_TOKEN_BM;
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
    1 sec timet on V1 - get LightSensor Data from BH1750: 
    SCL <-> D1, SDA <-> D2
 *************************************************************/
 
//Median filter class
class MedianFilter{
  #define N 5
  uint16_t sorted_arr[N] = {0};
  uint16_t original_arr[N] = {0};
  uint16_t min;
  uint16_t max;
  void sort(){
      for(int j=0; j<N-1; j++){
          for(int i=0; i<N-1; i++){
              if(sorted_arr[i]>sorted_arr[i+1]) {
                  uint16_t temp = sorted_arr[i+1];
                  sorted_arr[i+1] = sorted_arr[i];
                  sorted_arr[i] = temp;
              }
          }
      }
  }
  void moveOrig(uint16_t val){
      for (int i=0; i<N-1; i++) original_arr[N] = original_arr[N+1];
      original_arr[N] = val;  }

  void copy(){ for (int i=0; i<N; i++) sorted_arr[i]=original_arr[i]; }

public:
  void init(uint16_t firstValue){
      for (int i=0; i<N; i++){
          sorted_arr[i]=firstValue;
          original_arr[N] =firstValue;
      }
      min=firstValue;
      max=firstValue;
  }
  uint16_t getVal() {return sorted_arr[N/2];}
  uint16_t putVal(uint16_t val){
      moveOrig(val);
      copy();
      //sort();

   return getVal();
  }

};

//MedianFilter luxFilter;
WidgetRTC rtc; 
BlynkTimer timer;

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
  /*  uint16_t lux_m;
  lux_m = luxFilter.putVal(lux);
  Serial.print("Light: ");
  Serial.print(lux_m);
  Serial.println(" lx");
  */  
}

BLYNK_CONNECTED() {
  // Synchronize time on connection
  Serial.println(F("BLYNK_CONNECTED")); 
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
  digitalWrite(LED_BUILTIN, HIGH);
  uint16_t lux = LightSensor.GetLightIntensity();
  //luxFilter.init(lux);  
}

void loop() {
  Blynk.run();
  timer.run();
}
