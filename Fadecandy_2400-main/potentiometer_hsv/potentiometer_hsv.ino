int sensorPin = A0;
int sensorValue;
int hsv;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // opens serial communication
}

void loop() {
  // put your main code here, to run repeatedly:
  sensorValue = analogRead(sensorPin); // get analog reading from potentiometer pin
  hsv = map(sensorValue, 0, 1023, 0, 359); //remap potentiometer reading to 0-359 range and assign to hsv variable
  Serial.println(hsv); // print hsv value to serial on a new line
  
}
