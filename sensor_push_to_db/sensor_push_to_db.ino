#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char *ssid = "vivo Y100";
const char *password = "12345678";
const char *apiEndpoint = "http://192.168.137.1:8000/sensor";

void setup() {
  pinMode(39, INPUT);
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Read sensor data here
  int sensorValue = analogRead(39);
  Serial.print("sensor value is : ");
  Serial.println(sensorValue);

  // Create JSON object and add sensor data
  StaticJsonDocument<200> jsonDocument;
  jsonDocument["value"] = sensorValue;

  // Serialize JSON to string
  String payload;
  serializeJson(jsonDocument, payload);
  // Serialize JSON to string

  Serial.println(payload);

  // Send POST request to the API endpoint
  HTTPClient http;
  http.begin(apiEndpoint);
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(payload);

Serial.print("HTTP Response code: ");
Serial.println(httpResponseCode);

if (httpResponseCode > 0) {
  // Print response payload
  String response = http.getString();
  Serial.println(response);
} else {
  // Print error message
  Serial.print("Error code: ");
  Serial.println(httpResponseCode);
  Serial.print("Error message: ");
  Serial.println(http.errorToString(httpResponseCode).c_str());
}

  http.end();

  delay(5000); // Send data every 5 seconds (adjust as needed)
}
