import tkinter as tk
import cv2
import serial
import threading
import time

SERIAL_PORT = "COM10"  
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
except Exception as e:
    print("Error connecting to Arduino:", e)
    arduino = None

led_state = False  
key_pressed = None  # لتتبع الزر المضغوط حاليًا

def send_command(command):
    if arduino:
        arduino.write((command + "\n").encode())
        time.sleep(0.1)
        response = arduino.readline().decode().strip()
        if response:
            status_label.config(text="Arduino: " + response)

def toggle_led():
    global led_state
    led_state = not led_state
    send_command("LED_ON" if led_state else "LED_OFF")

def control_motor(motor):
    send_command(f"M{motor} 128")

def read_pressure():
    send_command("READ_MS5540C")

def test_all_motors():
    for i in range(1, 7):
        send_command(f"M{i} 128")
        time.sleep(1)
        send_command(f"M{i} 0")

def key_press(event):
    global key_pressed
    if key_pressed is not None:
        return  # تجاهل الضغط إذا كان فيه زر مضغوط بالفعل
    
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
        control_motor(int(event.char))
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
            send_command(f"M{chr(key)} 128")
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

root = tk.Tk()
root.title("Control Unit")
root.geometry("400x510")

tk.Button(root, text="Turn LED ON/OFF", command=toggle_led, bg="yellow").pack(pady=5)

for i in range(1, 7):
    tk.Button(root, text=f"Motor {i}", command=lambda i=i: control_motor(i)).pack(pady=2)

tk.Button(root, text="Test All Motors", command=test_all_motors, bg="blue").pack(pady=10)
tk.Button(root, text="Read Pressure Sensor", command=read_pressure, bg="gray").pack(pady=5)
tk.Button(root, text="Open Camera", command=lambda: threading.Thread(target=open_camera, daemon=True).start(), bg="green").pack(pady=5)

status_label = tk.Label(root, text="Status: Waiting", fg="blue")
status_label.pack(pady=10)

controls_text = """[Controls]
↑ ↓ ← → → Move (Forward, Backward, Left, Right)
I / K     → Move (Up, Down)
L         → Toggle LED
P         → Read Pressure Sensor
1 - 6     → Control Motors
Q         → Quit Camera Mode"""

controls_label = tk.Label(root, text=controls_text, justify="left", font=("Arial", 10), fg="black")
controls_label.pack(pady=10)

root.bind("<KeyPress>", key_press)  
root.bind("<KeyRelease>", key_release)  

root.mainloop()
