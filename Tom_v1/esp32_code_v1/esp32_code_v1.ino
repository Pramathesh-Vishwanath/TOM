#include <ArduinoJson.h>
//#include <ArduinoJson.hpp>
#include <WiFi.h>
#include <ESPmDNS.h>
#include <WebSocketsServer.h>
#include <ESPAsyncWebServer.h>

char webpage[] PROGMEM = R"=====(
<!DOCTYPE html>
<html>
<script>
var connection = new WebSocket('ws://'+location.hostname+':81/');
var R=0;
var L=0;

function button_1() {
  L=1;
  R=0;
  console.log("L");
  send_data();
}

function button_2() {
  L=0;
  R=1;
  console.log("R");
  send_data();
}

function button_3() {
  L=1;
  R=1;
  console.log("F");
  send_data();
}

function button_4() {
  L=0;
  R=0;
  console.log("S");
  send_data();
}

function send_data() {
  var full_data = '{"1":'+L+',"2":'+R+'}';
  connection.send(full_data);
}
</script>
<body>
<center>
<h1>My Home Automation</h1>
<h3> CAR </h3>
<button onclick="button_1()">L</button><button onclick="button_2()">R</button><button onclick="button_3()">F</button><button onclick="button_4()">S</button>
</center>
</body>
</html>
)=====";


// Replace with your WiFi credentials
const char* ssid = "The_Black_Box";
const char* password = "sudo_open_box";

AsyncWebServer server(80); // server port 80
WebSocketsServer websockets(81);

void notFound(AsyncWebServerRequest *request)
{
  request->send(404, "text/plain", "Page Not found");
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {
  switch (type) 
  {
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;
    case WStype_CONNECTED: {
        IPAddress ip = websockets.remoteIP(num);
        Serial.printf("[%u] Connected from %d.%d.%d.%d url: %s\n", num, ip[0], ip[1], ip[2], ip[3], payload);
        websockets.sendTXT(num, "Connected from server");
      }
      break;
    case WStype_TEXT:
      Serial.printf("[%u] Received: %s\n", num, payload);
      String message = String((char*)( payload));
      
      DynamicJsonDocument doc(200);
      DeserializationError error = deserializeJson(doc, message);
      if (error) {
        Serial.print("deserializeJson() failed: ");
        Serial.println(error.c_str());
        return;
      }

      int M1 = doc["1"];
      int M2 = doc["2"];
      if (M1 == 1 && M2 == 1) {  // Move forward
        digitalWrite(6, HIGH);
        digitalWrite(8, LOW);
        digitalWrite(21, HIGH);
        digitalWrite(47, LOW);
      } 
      else if (M1 == 1 && M2 == 0) {  // Left turn
        digitalWrite(6, HIGH);
        digitalWrite(8, LOW);
        digitalWrite(21, LOW);
        digitalWrite(47, LOW);
      } 
      else if (M1 == 0 && M2 == 1) {  // Right turn
        digitalWrite(6, LOW);
        digitalWrite(8, LOW);
        digitalWrite(21, HIGH);
        digitalWrite(47, LOW);
      } 
      else {  // Stop both motors
        digitalWrite(6, LOW);
        digitalWrite(8, LOW);
        digitalWrite(21, LOW);
        digitalWrite(47, LOW);
      }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(6, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(21, OUTPUT);
  pinMode(47, OUTPUT);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nConnected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp32")) { // Access via http://esp32.local
    Serial.println("MDNS responder started");
  }

  server.on("/", [](AsyncWebServerRequest * request) { 
    request->send_P(200, "text/html", webpage);
  });

  server.onNotFound(notFound);

  server.begin();
  websockets.begin();
  websockets.onEvent(webSocketEvent);
}

void loop() {
  websockets.loop();
}