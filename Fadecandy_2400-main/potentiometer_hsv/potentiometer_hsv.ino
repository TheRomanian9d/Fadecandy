int sensorPin = A0;
int sensorValue;
int hsg;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  sensorValue = analogRead(sensorPin);
  hsg = map(sensorValue, 0, 1023, 0, 359);
  Serial.println(hsg);
  
}
