#include "DHT.h"

#define moisture_sensor A1
#define ldr_sensor  A2


#define DHTPIN A0
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:

Serial.begin(9600);
pinMode(moisture_sensor,INPUT);
pinMode(ldr_sensor,INPUT);
dht.begin(); // initialize the sensor


}

void loop() {
  // put your main code here, to run repeatedly:
int moisture_value=analogRead(moisture_sensor);
float temperature_value = dht.readTemperature();
  if (isnan(temperature_value)) {
    Serial.println("Failed to read from DHT sensor!");
  }
int ldr_value=analogRead(ldr_sensor);
Serial.print(moisture_value);
Serial.print(";");
Serial.print(temperature_value);
Serial.print(";");
Serial.print(ldr_value);
Serial.print(";");
Serial.println("");
delay(1000);

}
