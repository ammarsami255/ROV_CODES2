#include <HardwareSerial.h>

#define RS485_RX 16
#define RS485_TX 17

// تعريف دبابيس المحركات (تأكد من إنهم متصلين صح فعلاً بالهاردوير)
#define motor1Pin 3
#define motor2Pin 5
#define motor3Pin 6
#define motor4Pin 9
#define motor5Pin 10
#define motor6Pin 11
#define ledPin 2

HardwareSerial rs485Serial(1);  // RS-485 Serial

void setup() {
  // بدء الاتصال التسلسلي
  rs485Serial.begin(9600, SERIAL_8N1, RS485_RX, RS485_TX);
  Serial.begin(115200);

  // تهيئة دبابيس المحركات كمخرجات
  pinMode(motor1Pin, OUTPUT);
  pinMode(motor2Pin, OUTPUT);
  pinMode(motor3Pin, OUTPUT);
  pinMode(motor4Pin, OUTPUT);
  pinMode(motor5Pin, OUTPUT);
  pinMode(motor6Pin, OUTPUT);
  pinMode(ledPin, OUTPUT);

  Serial.println("ESP32(2) ready to receive and control 6 motors.");
}

void loop() {
  if (rs485Serial.available()) {
    String command = rs485Serial.readStringUntil('\n');
    command.trim();
    Serial.println("Received: " + command);

    if (command == "LED_ON") {
      digitalWrite(ledPin, HIGH);
      rs485Serial.println("LED is ON");
    } else if (command == "LED_OFF") {
      digitalWrite(ledPin, LOW);
      rs485Serial.println("LED is OFF");
    } else if (command.startsWith("M")) {
      int motor = command.charAt(1) - '0';
      int speed = command.substring(3).toInt();

      switch (motor) {
        case 1: analogWrite(motor1Pin, speed); break;
        case 2: analogWrite(motor2Pin, speed); break;
        case 3: analogWrite(motor3Pin, speed); break;
        case 4: analogWrite(motor4Pin, speed); break;
        case 5: analogWrite(motor5Pin, speed); break;
        case 6: analogWrite(motor6Pin, speed); break;
        default:
          rs485Serial.println("Invalid motor number");
          return;
      }

      rs485Serial.println("Motor " + String(motor) + " set to speed " + String(speed));
    } else if (command == "FORWARD") {
      analogWrite(motor1Pin, 255);
      analogWrite(motor2Pin, 255);
      analogWrite(motor3Pin, 255);
      analogWrite(motor4Pin, 255);
      analogWrite(motor5Pin, 255);
      analogWrite(motor6Pin, 255);
      rs485Serial.println("Moving FORWARD");
    } else if (command == "BACKWARD") {
      analogWrite(motor1Pin, 128);
      analogWrite(motor2Pin, 128);
      analogWrite(motor3Pin, 128);
      analogWrite(motor4Pin, 128);
      analogWrite(motor5Pin, 128);
      analogWrite(motor6Pin, 128);
      rs485Serial.println("Moving BACKWARD");
    } else if (command == "STOP") {
      analogWrite(motor1Pin, 0);
      analogWrite(motor2Pin, 0);
      analogWrite(motor3Pin, 0);
      analogWrite(motor4Pin, 0);
      analogWrite(motor5Pin, 0);
      analogWrite(motor6Pin, 0);
      rs485Serial.println("Motors STOPPED");
    } else {
      rs485Serial.println("Unknown command: " + command);
    }
  }
}
