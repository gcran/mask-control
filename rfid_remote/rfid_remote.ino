#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

const char *ssid =  "Echelon-IV";   // name of your WiFi network
const char *password =  "goteamventure"; // password of the WiFi network

const char *ID = "bot_rfid";  // Name of our device, must be unique
const char *TOPIC = "remote/command";  // Topic to subcribe to

const char* broker = "192.168.1.101";
WiFiClient wclient;

PubSubClient client(wclient); // Setup MQTT client
char command_str[50];


const int RST_PIN = 0;  
const int SS_PIN = 5; 
MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

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
      // digitalWrite(LIGHT, 1);

    } else {
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

unsigned long getID() {
  if ( ! mfrc522.PICC_ReadCardSerial()) { //Since a PICC placed get Serial and continue
    return 0;
  }
  unsigned long hex_num;
  hex_num =  mfrc522.uid.uidByte[0] << 24;
  hex_num += mfrc522.uid.uidByte[1] << 16;
  hex_num += mfrc522.uid.uidByte[2] << 8;
  hex_num += mfrc522.uid.uidByte[3];
  mfrc522.PICC_HaltA(); // Stop reading
  return hex_num;
}

void setup() {
  Serial.begin(115200); // Start serial communication at 115200 baud
  SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();		// Init MFRC522
  delay(100);
  mfrc522.PCD_DumpVersionToSerial();
  setup_wifi(); // Connect to network
  client.setServer(broker, 1883);
}

void loop() {
  if (!client.connected())  // Reconnect if connection is lost
  {
    // digitalWrite(LIGHT, 0);
    reconnect();
  }
  client.loop();
  

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
	if ( ! mfrc522.PICC_IsNewCardPresent()) {
		return;
	}

	// Select one of the cards
	unsigned long uid = getID();
  if (uid != 0) {
    Serial.println(uid);
    sprintf(command_str, "%lu", uid);
    client.publish(TOPIC, command_str);
  }

	// Dump debug info about the card; PICC_HaltA() is automatically called
  // for (int i = 0; i < mfrc522.uid.size; i++) {
  //   Serial.print(mfrc522.uid.uidByte[i]);
  //   uid += mfrc522.uid.uidByte[i];
  // }
	// Serial.println();  
	// Serial.println(uid);
  // int uid[mfrc522.uid.size];
  // for (int i = mfrc522.uid.size - 1; i >= 0; i--) {
  //   uid[i] = mfrc522.uid.uidByte[i];
  //   Serial.println(mfrc522.uid.uidByte[i], HEX);
  // }
  // mfrc522.PICC_DumpDetailsToSerial(&(mfrc522.uid));
  // Serial.println(mfrc522.uid.size);
  // Serial.println(uid);
  // mfrc522.PICC_HaltA();

}
