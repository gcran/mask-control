#include <WiFi.h>
#include <PubSubClient.h>

const char *ssid =  "Echelon-IV";   // name of your WiFi network
const char *password =  "goteamventure"; // password of the WiFi network

const byte SW1 = 0;           // Pin to control the light with
const byte SW2 = 4;           // Pin to control the light with
const byte LIGHT = 2;
int prev_sw1 = 1;
int prev_sw2 = 1;
const char *ID = "bot_remote";  // Name of our device, must be unique
const char *TOPIC = "remote/command";  // Topic to subcribe to

// IPAddress broker(192,168,1,101); // IP address of your MQTT broker eg. 192.168.1.50
const char* broker = "192.168.1.101";
WiFiClient wclient;

PubSubClient client(wclient); // Setup MQTT client
int command=0;
const char *command_str = "0";

// Connect to WiFi network
void setup_wifi() {
  Serial.print("\nConnecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password); // Connect to network

  while (WiFi.status() != WL_CONNECTED) { // Wait for connection
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

// Reconnect to client
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(ID)) {
      Serial.println("connected");
      Serial.print("Publishing to: ");
      Serial.println(TOPIC);
      Serial.println('\n');
      digitalWrite(LIGHT, 1);

    } else {
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200); // Start serial communication at 115200 baud
  pinMode(SW1,INPUT_PULLUP);  // Configure SWITCH_Pin as an input pull-up resistor (active low)
  pinMode(SW2,INPUT_PULLUP);  // Configure SWITCH_Pin as an input pull-up resistor (active low)
  pinMode(LIGHT,OUTPUT);  // Configure connection light
  digitalWrite(LIGHT, 0);
  delay(100);
  setup_wifi(); // Connect to network
  client.setServer(broker, 1883);
}

void loop() {
  if (!client.connected())  // Reconnect if connection is lost
  {
    digitalWrite(LIGHT, 0);
    reconnect();
  }
  client.loop();
  

  // if the switch is being pressed

  if((digitalRead(SW1) == 0) & (prev_sw1 == 1))
  {
    command_str = "Button 1";
    client.publish(TOPIC, command_str);
    Serial.println(command_str);
  } else if((digitalRead(SW2) == 0) & (prev_sw2 == 1))
  {
    command_str = "Button 2";
    client.publish(TOPIC, command_str);
    Serial.println(command_str);
  }

  prev_sw1 = digitalRead(SW1);
  prev_sw2 = digitalRead(SW2);

}
