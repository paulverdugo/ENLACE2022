#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
  
// Set WiFi credentials and establish local port for communication via UDP
#define WIFI_SSID "UCSD-DEVICE"
#define WIFI_PASS "Fj7UPsFHb84e"
#define UDP_PORT 20044
 
// Declare the pins where data will be entered
WiFiUDP UDP;
double value = 0; // 
double analogin = 5; // 
double analogin1 = 4;
double val2 = 0;
double value2 = 0;
double value1 = 0;

//Declare the variable in this case the message and the data as char
char packet[255];
char reply1[] = "Sensor1: ";
char reply2[] = "Sensor2: ";
char sig[] = "01";

void setup() {
  // Setup serial port
  Serial.begin(115200);
  Serial.println();
  
  // Begin WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  
  // Connecting to WiFi... WiFi configuration
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  // Loop continuously while WiFi is not connected
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }
  
  // Connected to WiFi
  Serial.println();
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
 

}
void loop() {
  //capture data by analog reading and printing
  value = analogRead(analogin);
  value1 = value/1023;
  Serial.print("sensor1: ");
  Serial.println(value1);
  delay(1000);
  val2 = analogRead(analogin1);
  value2 = val2/1023;
  Serial.print("sensor2: ");
  Serial.println(value2);
  delay(100);
  
  //choose IP address to send data
  UDP.beginPacket("100.81.32.131", 20044);
  UDP.write(reply1);
    //convert double variable to char
  UDP.write(sig[int(value1)]);
  UDP.write(reply2);
  UDP.write(sig[int(value2)]);
  UDP.endPacket();

 
}
 
