// Miakatt - 17/04/2023

//------------------------------------------------------
// Connections
// Ch1 = GPIO5  = Pin D1 
// Ch2 = GPIO4 = Pin D2
// Ch3 = GPIO14 = Pin D5  //
// Ch4 = GPIO12 = Pin D6  // 
// Ch5 = GPIO13 = Pin D7  // 
//------------------------------------------------------ 
//------------------------------------------------------ 
// Use 10k Pull Up Resistors 
// Connect distal end to GND. 
// Open Circuit of copper strip causes voltage to increase. 
//------------------------------------------------------

const int pins[5]= {5, 4, 14, 12, 13};
const int LED = 2;
unsigned long startMillis;  // Variables required to control accurate timing of the loop
unsigned long currentMillis;                  
const unsigned long period = 100;  // Send readings every 100ms

void setup() {
  // Set up the input pins. External pull-up resistors are used. 
  for (int i=0; i<5; i++){
    pinMode(pins[i], INPUT);
    delay(100);
  }
  pinMode(LED, OUTPUT);   // On Board LED
  digitalWrite(LED, LOW); // Turn LED On

  Serial.begin(115200);    // Set up Serial Port Communication
  delay(1000);             // Wait 1s
  digitalWrite(LED, HIGH); // Turn off LED
  startMillis = millis();  // Get first reading for timing the loop. 
}


void loop() {
  // put your main code here, to run repeatedly:
  currentMillis = millis(); 
  if (currentMillis - startMillis >= period){
  
    int val[5] = {0};
    for (int i=0; i<5; i++){
      val[i] = digitalRead(pins[i]);    // read the input pins
    }
    for (int i=0; i<5; i++){            // send the readings out (1 or 0) to the Serial port. 
      Serial.print(val[i]);
      Serial.print(" ");
    }
      Serial.println();
                    
  
    startMillis = currentMillis;
  }
}
