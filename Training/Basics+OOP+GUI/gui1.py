from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt6.QtCore import QTimer, QTime
from PyQt6.QtGui import QPainter, QPen
import sys

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Ammar Timer")
        self.setGeometry(100, 200, 300, 400)
        self.setFixedSize(300, 200)  

        self.layout = QVBoxLayout()
        
        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Enter time in seconds")
        self.layout.addWidget(self.time_input)
        
        self.label = QLabel("00:00", self)
        self.layout.addWidget(self.label)
        
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)
        
        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause_timer)
        self.layout.addWidget(self.pause_button)
        
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_timer)
        self.layout.addWidget(self.reset_button)
        
        self.setLayout(self.layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_remaining = 0
        
    def start_timer(self):
        if not self.timer.isActive():
            try:
                self.time_remaining = int(self.time_input.text())
                self.timer.start(1000)
            except ValueError:
                self.label.setText("Invalid input")
        
    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        
    def reset_timer(self):
        self.timer.stop()
        self.time_remaining = 0
        self.label.setText("00:00")
        
    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            self.label.setText(f"{minutes:02}:{seconds:02}")
        else:
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec())
