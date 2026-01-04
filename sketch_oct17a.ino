#include <ESP32Servo.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClient.h>
#define RELAY 21
#define BUZZER 23
#define SERVO_PIN 14
#define SSID "ADMIN12345"
#define PASS "ADMIN12345"
Servo servo;
HTTPClient http;
WiFiClient wifiClient;

void setup() {
  Serial.begin(9600);
  pinMode(RELAY, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(2, OUTPUT);
  servo.attach(SERVO_PIN);

  digitalWrite(BUZZER, LOW);
  digitalWrite(RELAY, LOW);
  digitalWrite(2, LOW);
  servo.write(90);
  beep(2);
  initWiFi();
  Serial.println("Setup complete");
}

void loop() {
  getFromServer();
  delay(1000);
}
void throw_fabric() {
  servo.write(0);
  delay(1000);
  servo.write(90);
  delay(1000);
}
void beep(int times) {

  while (times--) {
    digitalWrite(BUZZER, HIGH);
    delay(100);
    digitalWrite(BUZZER, LOW);
    delay(100);
  }
}

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);
  unsigned long s_time = millis();
  Serial.println("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    if (millis() - s_time > 5000)
      break;
    delay(500);
  }
  Serial.print("WiFi Connected ");
  Serial.println(WiFi.localIP());
}
void getFromServer() {
  if (WiFi.status() == WL_CONNECTED) {
    String url = "http://codingprojects.cloud/get_values.php?id=16&field=1";
    http.begin(wifiClient, url);
    int code = http.GET();
    Serial.println(code);
    if ( code == 200) {
      String payload = http.getString();
      Serial.println(payload);
      if (payload == "1") {
        sendDataToServer();
        Serial.println("Bad fabric");
        beep(2);
        delay(1500);
        digitalWrite(2, HIGH);
        digitalWrite(RELAY, HIGH);
        throw_fabric();
      }
      digitalWrite(RELAY, LOW);
      digitalWrite(2, LOW);
    }
  }
}
void sendDataToServer() {
  if (WiFi.status() == WL_CONNECTED) {
    String url = "http://codingprojects.cloud/set_values.php?id=16&field1=0";
    http.begin(wifiClient, url);
    int code = http.GET();
    Serial.println(code);
  }
}
