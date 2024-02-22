#include <SoftwareSerial.h>

SoftwareSerial LoRa(9, 10);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  LoRa.begin(9600);
}

String Input = "Hello World";

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    String Instream = Serial.readString();

    Serial.print(Instream);
    
    LoRa.print(Instream); 
  }
}
