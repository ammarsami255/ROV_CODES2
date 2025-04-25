import tkinter as tk
import cv2
import serial
import threading
import time
from inputs import get_gamepad
import machine  # لتفعيل PWM في ESP

SERIAL_PORT = "COM10"
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
except Exception as e:
    print("Error connecting to Arduino:", e)
    arduino = None

led_state = False
key_pressed = None

# دبابيس PWM للتحكم في المحركات
motor_pins = [5, 4, 0, 2, 14, 12]  # دبابيس ESP للتحكم في المحركات (GPIO)
motors = [machine.PWM(machine.Pin(pin), freq=1000, duty=0) for pin in motor_pins]  # تفعيل PWM للمحركات

# وظيفة لإرسال الأوامر إلى Arduino (أو ESP عبر السيريال)
def send_command(command):
    if arduino:
        arduino.write((command + "\n").encode())
        time.sleep(0.05)
        response = arduino.readline().decode().strip()
        if response:
            status_label.config(text="Arduino: " + response)

def toggle_led():
    global led_state
    led_state = not led_state
    send_command("LED_ON" if led_state else "LED_OFF")

def control_motor(motor, speed):
    motors[motor - 1].duty(speed)  # تغيير سرعة المحرك باستخدام PWM

def read_pressure():
    send_command("READ_MS5540C")

def test_all_motors():
    for i in range(1, 7):
        control_motor(i, 128)  # تغيير سرعة جميع المحركات
        time.sleep(1)
        control_motor(i, 0)  # إيقاف المحرك

def key_press(event):
    global key_pressed
    if key_pressed is not None:
        return
    key_pressed = event.keysym

    if event.keysym == "Up":
        send_command("FORWARD")
    elif event.keysym == "Down":
        send_command("BACKWARD")
    elif event.keysym == "Left":
        send_command("LEFT")
    elif event.keysym == "Right":
        send_command("RIGHT")
    elif event.keysym == "i":
        send_command("UP")
    elif event.keysym == "k":
        send_command("DOWN")
    elif event.char in "123456":
        control_motor(int(event.char), 128)  # تعديل السرعة للمحرك المحدد
    elif event.char == "p":
        read_pressure()
    elif event.char == "l":
        toggle_led()

def key_release(event):
    global key_pressed
    if key_pressed == event.keysym:
        key_pressed = None

def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key in [ord(str(i)) for i in range(1, 7)]:
            control_motor(i, 128)  # تعديل السرعة عند الضغط على الأزرار
        elif key == ord('p'):
            send_command("READ_MS5540C")
        elif key == ord('l'):
            toggle_led()
        elif key == 82:
            send_command("FORWARD")
        elif key == 84:
            send_command("BACKWARD")
        elif key == 81:
            send_command("LEFT")
        elif key == 83:
            send_command("RIGHT")
        elif key == ord('i'):
            send_command("UP")
        elif key == ord('k'):
            send_command("DOWN")

    cap.release()
    cv2.destroyAllWindows()

def gamepad_listener():
    def map_axis(val):
        return int(((val + 32768) / 65535) * 255)

    while True:
        events = get_gamepad()
        lx = 0
        ly = 0
        for event in events:
            if event.ev_type == "Key" and event.code == "BTN_TL" and event.state == 1:
                send_command("M6 1228")

            if event.ev_type == "Absolute":
                if event.code == "ABS_Y":
                    ly = map_axis(event.state)
                elif event.code == "ABS_X":
                    lx = map_axis(event.state)

        forward_back = ly - 128
        left_right = lx - 128

        if abs(forward_back) > abs(left_right):
            if forward_back < -30:
                speed = min(128, int(abs(forward_back)))
                send_command("FORWARD")
                control_motor(1, speed)
                control_motor(2, speed)
                control_motor(3, speed)
                control_motor(4, speed)
            elif forward_back > 30:
                speed = min(128, int(abs(forward_back)))
                send_command("BACKWARD")
                control_motor(1, speed)
                control_motor(2, speed)
                control_motor(3, speed)
                control_motor(4, speed)
        elif abs(left_right) > 30:
            speed = min(100, int(abs(left_right)))
            if left_right < 0:
                send_command("LEFT")
                control_motor(1, 0)
                control_motor(3, 0)
                control_motor(2, speed)
                control_motor(4, speed)
            else:
                send_command("RIGHT")
                control_motor(2, 0)
                control_motor(4, 0)
                control_motor(1, speed)
                control_motor(3, speed)
        else:
            send_command("STOP")

root = tk.Tk()
root.title("Control Unit")
root.geometry("400x510")

tk.Button(root, text="Turn LED ON/OFF", command=toggle_led, bg="yellow").pack(pady=5)

for i in range(1, 7):
    tk.Button(root, text=f"Motor {i}", command=lambda i=i: control_motor(i, 128)).pack(pady=2)

tk.Button(root, text="Test All Motors", command=test_all_motors, bg="blue").pack(pady=10)
tk.Button(root, text="Read Pressure Sensor", command=read_pressure, bg="gray").pack(pady=5)
tk.Button(root, text="Open Camera", command=lambda: threading.Thread(target=open_camera, daemon=True).start(), bg="green").pack(pady=5)

status_label = tk.Label(root, text="Status: Waiting", fg="blue")
status_label.pack(pady=10)

controls_text = """[Controls]
↑ ↓ ← →  → Move (Forward, Backward, Left, Right)
I / K     → Move (Up, Down)
L         → Toggle LED
P         → Read Pressure Sensor
1 - 6     → Control Motors
Q         → Quit Camera Mode

[Xbox Controller]
Analog    → Move & Control Speed
LT        → M6 Speed 1228"""

controls_label = tk.Label(root, text=controls_text, justify="left", font=("Arial", 10), fg="black")
controls_label.pack(pady=10)

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

threading.Thread(target=gamepad_listener, daemon=True).start()

root.mainloop()
