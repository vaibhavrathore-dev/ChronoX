import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit,
    QFileDialog, QProgressBar
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QSound


# ===== RESOURCE PATH (IMPORTANT FOR EXE) =====
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class ChronoX(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChronoX – Control Your Time")
        self.setWindowIcon(QIcon(resource_path("chronox_logo.png")))
        self.setMinimumSize(1000, 650)

        self.time_left = 0
        self.total_time = 0
        self.alarm_sound = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        # ===== LOGO =====
        self.logo_label = QLabel()
        pixmap = QPixmap(resource_path("chronox_logo.png"))
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        # ===== TITLE =====
        self.title = QLabel("ChronoX")
        self.title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white;")

        # ===== SUBTITLE =====
        self.subtitle = QLabel("Control Your Time")
        self.subtitle.setFont(QFont("Segoe UI", 16))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("color: #3A8DFF;")

        # ===== INPUT =====
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter time in seconds...")
        self.input_field.setFixedHeight(45)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: white;
                border: 2px solid #3A8DFF;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)

        # ===== TIME DISPLAY =====
        self.time_display = QLabel("00:00:00")
        self.time_display.setFont(QFont("Consolas", 60, QFont.Bold))
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet("color: white;")

        # ===== PROGRESS BAR =====
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(15)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #1a1a1a;
                border-radius: 7px;
            }
            QProgressBar::chunk {
                background-color: #3A8DFF;
                border-radius: 7px;
            }
        """)

        # ===== BUTTONS =====
        self.start_btn = self.create_button("Start", self.start_timer)
        self.pause_btn = self.create_button("Pause", self.pause_timer)
        self.reset_btn = self.create_button("Reset", self.reset_timer)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.reset_btn)

        # ===== SOUND BUTTON =====
        self.sound_btn = self.create_button("Choose Alarm Sound", self.choose_sound)
        self.sound_label = QLabel("Default System Beep")
        self.sound_label.setStyleSheet("color: white;")

        sound_layout = QHBoxLayout()
        sound_layout.addWidget(self.sound_btn)
        sound_layout.addWidget(self.sound_label)

        # ===== ADD TO MAIN LAYOUT =====
        main_layout.addWidget(self.logo_label)
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.subtitle)
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.time_display)
        main_layout.addWidget(self.progress)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(sound_layout)

        self.setLayout(main_layout)

        # ===== MAIN WINDOW STYLE =====
        self.setStyleSheet("background-color: #0d0d0d;")

    def create_button(self, text, function):
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3A8DFF;
                color: white;
                border-radius: 10px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #2c6edb;
            }
        """)
        btn.clicked.connect(function)
        return btn

    def start_timer(self):
        if self.time_left == 0:
            try:
                self.time_left = int(self.input_field.text())
                self.total_time = self.time_left
                self.progress.setMaximum(self.total_time)
            except:
                return

        if self.time_left > 0:
            self.timer.start(1000)

    def pause_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.time_left = 0
        self.time_display.setText("00:00:00")
        self.progress.setValue(0)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1

            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60

            self.time_display.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
            self.progress.setValue(self.total_time - self.time_left)
        else:
            self.timer.stop()
            self.trigger_alarm()

    def choose_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Alarm Sound", "", "Sound Files (*.wav)"
        )
        if file_path:
            self.alarm_sound = file_path
            self.sound_label.setText(os.path.basename(file_path))

    def trigger_alarm(self):
        if self.alarm_sound:
            QSound.play(self.alarm_sound)
        else:
            QApplication.beep()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChronoX()
    window.show()
    sys.exit(app.exec_())
