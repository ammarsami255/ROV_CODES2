from inputs import get_gamepad
import time

# دالة لتحويل القيم من النطاق الكبير إلى النطاق الذي نحتاجه
def scale_value(value, min_input, max_input, min_output, max_output):
    return int(min_output + (float(value - min_input) / (max_input - min_input)) * (max_output - min_output))

def gamepad_listener():
    while True:
        events = get_gamepad()

        for event in events:
            # طباعة كل الأحداث
            print(f"Event Code: {event.code}, Event State: {event.state}")

            if event.ev_type == "Absolute":
                if event.code == "ABS_X":
                    # تحويل القيم الخاصة بالمحور X
                    scaled_x = scale_value(event.state, -32768, 32767, -100, 100)
                    print(f"Left Stick X (scaled): {scaled_x}")

                elif event.code == "ABS_Y":
                    # تحويل القيم الخاصة بالمحور Y
                    scaled_y = scale_value(event.state, -32768, 32767, -100, 100)
                    print(f"Left Stick Y (scaled): {scaled_y}")

                elif event.code == "ABS_RX":
                    # تحويل القيم الخاصة بالمحور X للجويستيك الأيمن
                    scaled_rx = scale_value(event.state, -32768, 32767, -100, 100)
                    print(f"Right Stick X (scaled): {scaled_rx}")

                elif event.code == "ABS_RY":
                    # تحويل القيم الخاصة بالمحور Y للجويستيك الأيمن
                    scaled_ry = scale_value(event.state, -32768, 32767, -100, 100)
                    print(f"Right Stick Y (scaled): {scaled_ry}")

                elif event.code == "ABS_Z":  # Left Trigger
                    # تحويل القيم الخاصة بالـ Left Trigger
                    scaled_z = scale_value(event.state, 0, 255, 0, 100)
                    print(f"Left Trigger (scaled): {scaled_z}")

                elif event.code == "ABS_RZ":  # Right Trigger
                    # تحويل القيم الخاصة بالـ Right Trigger
                    scaled_rz = scale_value(event.state, 0, 255, 0, 100)
                    print(f"Right Trigger (scaled): {scaled_rz}")

        time.sleep(0.1)  # كل ثانية هنقرأ الإحداثيات الجديدة

if __name__ == "__main__":
    gamepad_listener()
