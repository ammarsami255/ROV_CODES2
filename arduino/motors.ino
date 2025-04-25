#include <SPI.h>

#define LED_PIN 13
#define CS_PIN 10

#define M1 3
#define M2 5
#define M3 6
#define M4 9
#define M5 10
#define M6 11

#define delay_test 1000

const int motors[] = { M1, M2, M3, M4, M5, M6 };

void setup() {
  Serial.begin(9600);

  pinMode(LED_PIN, OUTPUT);
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);

  for (int i = 0; i < 6; i++) {
    pinMode(motors[i], OUTPUT);
  }

  SPI.begin();

  // تغيير إعدادات التايمر لخفض التردد إلى 1kHz
  TCCR1B = (TCCR1B & 0b11111000) | 0x03;  // تايمر للمنافذ 9 و 10
  TCCR2B = (TCCR2B & 0b11111000) | 0x04;  // تايمر للمنافذ 3 و 11
}

void loop() {
  main_sys();
}

long readMS5540C() {
  digitalWrite(CS_PIN, LOW);
  delay(10);

  SPI.transfer(0xFF);
  delay(10);

  byte highByte = SPI.transfer(0x00);
  byte lowByte = SPI.transfer(0x00);

  digitalWrite(CS_PIN, HIGH);

  return (highByte << 8) | lowByte;
}

void test_function(int m) {
  if (m >= 1 && m <= 6) {
    int motorPin = motors[m - 1];
    analogWrite(motorPin, 128);
    delay(delay_test);
    analogWrite(motorPin, 0);
    delay(delay_test);
    Serial.println("test for Motor: " + String(m) + " with pin : " + String(motorPin));
  }
}

void main_sys() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "LED_ON") {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("Led on");
    } else if (command == "LED_OFF") {
      digitalWrite(LED_PIN, LOW);
      Serial.println("Led Off");

    } else if (command.startsWith("M")) {
      int motorNum = command.charAt(1) - '0';
      int speed = command.substring(3).toInt();
      Serial.println("main func to motor-->> " + String(motorNum));

      if (motorNum >= 1 && motorNum <= 6) {
        int motorPin = motors[motorNum - 1];
        int s = constrain(speed, 0, 255);
        analogWrite(motorPin, s);
      }
    } else if (command == "READ_MS5540C") {
      long pressure = readMS5540C();
      Serial.print("Pressure: ");
      Serial.println(pressure);
    } else if (command == "FORWARD") {
      forward();
    } else if (command == "BACKWARD") {
      backward();
    }
    else if (command == "RIGHT") {
      right();
    } else if (command == "LEFT") {
      left();
    }
    else if (command == "UP") {
      up();
    } else if (command == "DOWN") {
      down();
    }
  }
}
void forward() {
  analogWrite(M1, 128);
  analogWrite(M2, 128);
  Serial.println("Forward --> M1 , M2");
}
void backward() {
  analogWrite(M3, 128);
  analogWrite(M4, 128);
  Serial.println("Backward --> M3 , M4");
}

void right() {
  analogWrite(M1, 128);
  analogWrite(M3, 80);
  Serial.println("right --> M1 , M3");
}
void left() {
  analogWrite(M2, 128);
  analogWrite(M4, 80);
  Serial.println("left --> M2 , M4");
}

void up() {
  analogWrite(M5, 128);
  Serial.println("UP --> M5");
}
void down() {
  analogWrite(M6, 128);
    Serial.println("DOWN --> M6");
}