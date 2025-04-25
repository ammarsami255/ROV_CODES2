// تعريف الدبابيس للمحركات
int motor1Pin = 3;
int motor2Pin = 5;
int motor3Pin = 6;
int motor4Pin = 9;
int ledPin = 13;

void setup() {
  // تهيئة الدبابيس كمخرجات
  pinMode(motor1Pin, OUTPUT);
  pinMode(motor2Pin, OUTPUT);
  pinMode(motor3Pin, OUTPUT);
  pinMode(motor4Pin, OUTPUT);
  pinMode(ledPin, OUTPUT);

  // بدء الاتصال التسلسلي
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // إزالة المسافات الزائدة

    // التعامل مع الأوامر المختلفة
    if (command == "LED_ON") {
      digitalWrite(ledPin, HIGH); // تشغيل الـ LED
    }
    else if (command == "LED_OFF") {
      digitalWrite(ledPin, LOW); // إيقاف الـ LED
    }
    else if (command.startsWith("M")) {
      // التحكم بالمحركات عبر PWM
      int motor = command.charAt(1) - '0';  // الرقم المخصص للمحرك
      int speed = command.substring(3).toInt(); // السرعة

      switch (motor) {
        case 1:
          analogWrite(motor1Pin, speed);
          break;
        case 2:
          analogWrite(motor2Pin, speed);
          break;
        case 3:
          analogWrite(motor3Pin, speed);
          break;
        case 4:
          analogWrite(motor4Pin, speed);
          break;
      }
    }
    else if (command == "FORWARD") {
      analogWrite(motor1Pin, 255); // التحكم في السرعة
      analogWrite(motor2Pin, 255);
      analogWrite(motor3Pin, 255);
      analogWrite(motor4Pin, 255);
    }
    else if (command == "BACKWARD") {
      analogWrite(motor1Pin, 128);
      analogWrite(motor2Pin, 128);
      analogWrite(motor3Pin, 128);
      analogWrite(motor4Pin, 128);
    }
    else if (command == "STOP") {
      analogWrite(motor1Pin, 0);
      analogWrite(motor2Pin, 0);
      analogWrite(motor3Pin, 0);
      analogWrite(motor4Pin, 0);
    }
  }
}
