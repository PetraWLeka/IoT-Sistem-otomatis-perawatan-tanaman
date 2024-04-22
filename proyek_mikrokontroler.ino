int waterPumpPin = 2; 
int moistureThreshold = 1; 
 
int lightSensor = A0; 
int led = 13; 
float lightReading = 0; 
 
void setup() { 
  pinMode(waterPumpPin, OUTPUT); 
  pinMode(led, OUTPUT); 
  digitalWrite(waterPumpPin, HIGH); 
   
  Serial.begin(9600); // Initialize serial communication 
} 
 
void loop() { 
  float soilMoisture = -0.0016 * analogRead(soilMoisturePin) + 1.6336; 
  //Serial.print("Soil moisture: "); 
  Serial.print(soilMoisture); 
  Serial.print(",");
   
  lightReading = 0.0031 * analogRead(lightSensor) + 0.5868; 
  //lightReading = analogRead(lightSensor);
  Serial.print(lightReading, DEC); 
  Serial.print(",");
  if (lightReading <= 1) { 
    digitalWrite(led, HIGH); 
    Serial.print(1); 
  }
  else { 
    digitalWrite(led, LOW); 
    Serial.print(0); 
  }
  Serial.print(",");
  
    if (soilMoisture < moistureThreshold) { 
    digitalWrite(waterPumpPin, LOW); 
    Serial.println(1); 
    delay(5000); 
    digitalWrite(waterPumpPin, HIGH);
  } 
  else{
     digitalWrite(waterPumpPin, HIGH); 
    Serial.println(0); 
  }
  
  if (Serial.available() > 0) {
  char command = Serial.read();
  
    if (command == '1'){
    digitalWrite(led,HIGH);
  } else if (command == '0'){
    digitalWrite(led,LOW);
  } else if (command == '2'){
    digitalWrite(waterPumpPin,LOW);
    delay(4000);
  } else if (command == '3'){
    digitalWrite(waterPumpPin,HIGH);
    delay(4000);
  } 
}
   
  delay(1000); 
}