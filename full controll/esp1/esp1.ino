#include <HardwareSerial.h>

#define RS485_TX 17   // غيّر حسب الوصلة بين ESP32 و RS485
#define RS485_RX 16

HardwareSerial rs485Serial(1);

void setup() {
  Serial.begin(9600); // للتوصيل مع الكمبيوتر (USB)
  rs485Serial.begin(9600, SERIAL_8N1, RS485_RX, RS485_TX); // RS485 Serial
  Serial.println("ESP32 Control Ready");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    rs485Serial.println(command);  // إرسال الأمر إلى RS485
    Serial.println("Sent: " + command);  // تأكيد على الإرسال
  }

  if (rs485Serial.available()) {
    String response = rs485Serial.readStringUntil('\n');
    response.trim();
    Serial.println("Response from ESP32(2): " + response); // عرض الاستجابة إن وجدت
  }
}
