#include <WiFi.h>
#include <WebSocketsServer.h>

// Constants
const char* ssid = "VIVOFIBRA-BC90";
const char* password = "21E5968853";

int count = 0;
String isClicked ="No";

String Site;
int transmit = 0;
// Globals
WebSocketsServer webSocket = WebSocketsServer(80);

// Called when receiving any WebSocket message
void onWebSocketEvent(uint8_t num,
                      WStype_t type,
                      uint8_t * payload,
                      size_t length) {

  // Figure out the type of WebSocket event
  switch(type) {

    // Client has disconnected
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;

    // New client has connected
    case WStype_CONNECTED:
      {
        IPAddress ip = webSocket.remoteIP(num);
        Serial.printf("[%u] Connection from ", num);
        Serial.println(ip.toString());
      }
      break;

    // Recebeu texto
    case WStype_TEXT:
      Serial.printf("[%u] Text: %s\n", num, payload);
      Site = (char*)payload;
      webSocket.sendTXT(num, isClicked);
      
      break;

    // For everything else: do nothing
    case WStype_BIN:
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
    default:
      break;
  }
}

void setup() {

  // Start Serial port
  Serial.begin(9600);

  // Connect to access point
  Serial.println("Connecting");
  WiFi.begin(ssid, password);
  while ( WiFi.status() != WL_CONNECTED ) {
    delay(500);
    Serial.print(".");
  }

  // Print our IP address
  Serial.println("Connected!");
  Serial.print("My IP address: ");
  Serial.println(WiFi.localIP());

  // Start WebSocket server and assign callback
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
}

void loop() {
  count++;
  // Look for and handle WebSocket data
  webSocket.loop();
  
  if(count == 50000){
    
    if(isClicked == "No"){
      count = 0;
      isClicked = "SIM";
      }else{
        count = 0;
        isClicked = "No";
        }
       Serial.println("Botão ligado?" + isClicked);
  }
}
