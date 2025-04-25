import cv2
import numpy as np

# تحميل الصورة
img = cv2.imread('shapes.png')

# تحويل الصورة لـ HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# لون #484E5A بالـ RGB هو (72, 78, 90) - هنحوله لـ HSV
bgr_color = np.uint8([[[72, 78, 90]]])  # اللون في BGR
hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)[0][0]  # تحويله إلى HSV

# تحديد نطاق اللون المطلوب
lower = np.array([hsv_color[0] - 1, 30, 30])  # أقل درجة
upper = np.array([hsv_color[0] + 1, 255, 255])  # أعلى درجة

# إنشاء القناع (mask) لاستخراج اللون فقط
mask = cv2.inRange(hsv, lower, upper)

# تطبيق القناع على الصورة الأصلية
result = cv2.bitwise_and(img, img, mask=mask)

# تحويل للصورة الرمادية والثريشولد
gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

# البحث عن الكونتورز
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# رسم الكونتورز والتعرف على الأشكال
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    x, y = approx.ravel()[0], approx.ravel()[1] - 5
    cv2.drawContours(img, [approx], 0, (0, 255, 0), 3)

    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    elif len(approx) == 4:
        x1, y1, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
        cv2.putText(img, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    else:
        cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

cv2.imshow("Filtered Shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
