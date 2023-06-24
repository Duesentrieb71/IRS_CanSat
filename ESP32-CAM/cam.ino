#include "esp_camera.h"
#include "SD_MMC.h"
#include "stdio.h"

// Camera configuration
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

int folderNumber = 0;
String folderName;

//primitive signaling between the main microcontroller and the camera
bool fromMain = false;
bool toMain = false;

void setup() {
  Serial.begin(115200);

  // Initialize SD card
  if (!SD_MMC.begin()) {
    Serial.println("SD Card Mount Failed");
    return;
  }

  // Initialize camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.pin_flash = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_SVGA;
  /*
    FRAMESIZE_QQVGA (160x120)
    FRAMESIZE_QCIF (176x144)
    FRAMESIZE_HQVGA (240x176)
    FRAMESIZE_QVGA (320x240)
    FRAMESIZE_CIF (400x296)
    FRAMESIZE_HVGA (480x320)
    FRAMESIZE_VGA (640x480) -> 8.2 FPS
    FRAMESIZE_SVGA (800x600) -> 8.1 FPS -> our choice
    FRAMESIZE_XGA (1024x768)
    FRAMESIZE_SXGA (1280x1024)
    FRAMESIZE_UXGA (1600x1200) -> 2.2 FPS
    FRAMESIZE_QXGA (2048x1536)
*/
  config.jpeg_quality = 12;
  config.fb_count = 1;
  
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  Serial.println("Camera and SD card ready");

  //search for existing folders and iterate the number to create a new folder for the images
  while (SD_MMC.exists("/" + String(folderNumber))) {
    folderNumber++;
  }
  //assign folder name to the folderName array
  folderName = String(folderNumber);

  SD_MMC.mkdir("/" + String(folderNumber));

  //set GPIO 1 as output
  pinMode(1, OUTPUT);
  //set GPIO 3 as input
  pinMode(3, INPUT);

  //set GPIO 1 to low
  digitalWrite(1, LOW);

  //sleep 1 second to allow the main microcontroller to boot
  delay(1000);

  //wait for the main microcontroller to signal that recording can start
  while (!fromMain) {
    checkFromMain();
  }

  //signal the main microcontroller that recording has started
  switchToMain();
}

void loop() {

  //capture a frame every loop
  captureFrame();

  //check if the main microcontroller wants to stop recording and restart the ESP32-CAM
  checkFromMain();
  if (fromMain) {
    switchToMain(); //signal the main microcontroller that the ESP32-CAM has restarted
    delay(1000); 
    ESP.restart();
  }
}

void captureFrame() {
  // Capture video frame
  camera_fb_t *fb = esp_camera_fb_get();

  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  // Save video frame to SD card
  writeFile(SD_MMC, fb->buf, fb->len);

  // Return the frame buffer to the camera driver
  esp_camera_fb_return(fb);
}

void writeFile(fs::FS &fs, const uint8_t *data, size_t size) {
  String path = "/" + folderName + "/" + String(millis()) + ".jpg";

  File file = fs.open(path.c_str(), FILE_WRITE);
  if (!file) {
    Serial.println("Failed to open file for writing");
    return;
  }

  file.write(data, size);
  file.close();
  Serial.printf("Saved to: %s\n", path.c_str());
}

void checkFromMain() {
  //check if GPIO 3 is high
  fromMain = digitalRead(3);
}

void switchToMain() {
  //set GPIO 1 to the opposite value of before
  toMain = !toMain;
  digitalWrite(1, toMain);
}


//TODO: (maybe) implement UART communication with the main microcontroller