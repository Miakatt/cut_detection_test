//------------------------------------------------------
// Connections
// Ch1 = GPIO5  = Pin D1
// Ch2 = GPIO12 = Pin D6
// Ch3 = GPIO13 = Pin D7
// Ch4 = GPIO14 = Pin D5
// Ch5 = GPIO15 = Pin D8
// Ch6 = GPIO16 = Pin D0
//------------------------------------------------------ 
// Use 10k Pull Up Resistors 
// Connect distal end to GND. 
// Open Circuit of copper strip causes voltage to increase. 
//------------------------------------------------------
// NOTE: THE MICROPROCESSOR NEEDS TO BE DISCONNECTED FROM THE BOARD BEFORE FLASHING.
// 
const int pins[6]= {5, 16, 14, 12, 13, 15};
                   

void setup() {
  // put your setup code here, to run once:
  for (int i=0; i<6; i++){
    pinMode(pins[i], INPUT);
    digitalWrite(pins[i], HIGH);
  }
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  Serial.begin(9600);
  delay(100);
  Serial.println("Begin Monitoring.");
}

void loop() {
  // put your main code here, to run repeatedly:
  int val[6] = {0};
  for (int i=0; i<6; i++){
    val[i] = digitalRead(pins[i]);
  }
  for (int i=0; i<6; i++){
    Serial.print(val[i]);
    Serial.print(" ");
  }
    Serial.println();
    Serial.flush();
    delay(100);
 
}
