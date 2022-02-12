int sensorPin = A0;
int sensorValue;
int hvg;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  sensorValue = analogRead(sensorPin);
  hvg = map(sensorValue, 0, 1023, 0, 359);
  Serial.println(hvg);
  
}
