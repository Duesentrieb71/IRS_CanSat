#include <SoftwareSerial.h>

#define IBUS_BAUD_RATE 115200
#define IBUS_RX_PIN 2 // Change this to the GPIO pin you connected the iBUS signal to

SoftwareSerial iBusSerial(IBUS_RX_PIN, -1); // RX, TX (TX not used)

void setup() {
  Serial.begin(115200); // Debug serial communication
  iBusSerial.begin(IBUS_BAUD_RATE);
}

void loop() {
  if (iBusSerial.available()) {
    int channelData = iBusSerial.read();
    Serial.print("Channel data: ");
    Serial.println(channelData);
  }
  else {
    delay(1)
    Serial.println("No Data")
  }
}
