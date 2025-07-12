import sys
import os
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception:
        pass
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"

import pyautogui
import keyboard
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QMessageBox, QGraphicsDropShadowEffect,
    QFrame, QHBoxLayout, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QRect, QEventLoop
from PyQt6.QtGui import QFont, QColor, QIcon, QPainter, QLinearGradient, QPixmap, QMovie
import random
from PyQt6.QtWidgets import QProgressBar, QHBoxLayout
from PyQt6.QtCore import QPoint

# PyAutoGUI settings - for safety
pyautogui.PAUSE = 0.01  # Small pause for safety
pyautogui.FAILSAFE = True  # Keep failsafe enabled

agent_coordinates = {
    "Brimstone": (282, 344),
    "Phoenix": (81, 740),
    "Sage": (388, 744),
    "Sova": (189, 838),
    "Viper": (383, 834),
    "Cypher": (172, 422),
    "Reyna": (285, 741),
    "Killjoy": (185, 644),
    "Breach": (190, 354),
    "Omen": (382, 643),
    "Jett": (381, 543),
    "Raze": (186, 740),
    "Skye": (87, 834),
    "Yoru": (295, 894),
    "KAY/O": (87, 643),
    "Chamber": (380, 352),
    "Neon": (282, 638),
    "Fade": (387, 433),
    "Harbor": (196, 544),
    "Gekko": (74, 543),
    "Deadlock": (290, 450),
    "Astra": (75, 318),
    "Iso": (282, 543),
    "Clove": (73, 448),
    "Vyse": (93, 894),
    "Tejo": (282, 842),
    "Waylay": (175, 896),
}

lock_coordinate = (954, 761)
selected_agent = None

class LockThread(QThread):
    update_status = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.spamming = False
        self.last_f8_state = False

    def run(self):
        global selected_agent
        while self.running:
            try:
                # F8 toggle logic
                f8_pressed = keyboard.is_pressed("F8")
                if f8_pressed and not self.last_f8_state:
                    self.spamming = not self.spamming
                self.last_f8_state = f8_pressed

                if self.spamming and selected_agent:
                    x, y = agent_coordinates[selected_agent]
                    pyautogui.moveTo(x, y)
                    pyautogui.click()
                    pyautogui.moveTo(lock_coordinate[0], lock_coordinate[1])
                    pyautogui.click()
                time.sleep(0.01)  # 10ms wait
            except Exception as e:
                print(f"Thread error: {e}")
                time.sleep(0.1)

    def stop(self):
        self.running = False

MIDNIGHT_COLORS = [
    "#232946",  # deep blue
    "#393e6e",  # navy
    "#312e81",  # purple
    "#283046",  # blue-grey
    "#3a3f5a",  # dark slate
    "#4f518c",  # muted indigo
    "#22223b",  # midnight
    "#5f6caf",  # blue
    "#6d28d9",  # purple highlight
    "#1a2238",  # dark blue
    "#2d3250",  # blue-grey
    "#3e206d",  # deep purple
]

class AnimatedButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMinimumHeight(48)
        self.setMinimumWidth(120)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.selected = False
        self.base_color = "#232946"
        self.base_style = f"""
            QPushButton {{
                background: {self.base_color};
                color: #e0eaff;
                border: 2px solid #111;
                border-radius: 16px;
                padding: 8px 0px;
                font-weight: bold;
                box-shadow: 0 0 8px #111;
            }}
            QPushButton:hover {{
                background: #6d28d9;
                color: #fff;
                border: 2px solid #232946;
            }}
            QPushButton:pressed {{
                background: #393e6e;
            }}
        """
        self.selected_style = f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6d28d9, stop:1 {self.base_color});
                color: #fffbe7;
                border: 3px solid #232946;
                border-radius: 18px;
                font-weight: bold;
                box-shadow: 0 0 16px #6d28d9;
            }}
        """
        self.setStyleSheet(self.base_style)
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(18)
        glow.setColor(QColor("#111"))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(180)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.scale_anim = QPropertyAnimation(self, b"maximumWidth")
        self.scale_anim.setDuration(180)
        self.scale_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    def enterEvent(self, event):
        self.animation.setStartValue(self.geometry())
        new_geometry = QRect(self.x()-3, self.y()-3, self.width()+6, self.height()+6)
        self.animation.setEndValue(new_geometry)
        self.animation.start()
        self.scale_anim.setStartValue(self.width())
        self.scale_anim.setEndValue(self.width()+10)
        self.scale_anim.start()
        super().enterEvent(event)
    def leaveEvent(self, event):
        self.animation.setStartValue(self.geometry())
        new_geometry = QRect(self.x()+3, self.y()+3, self.width()-6, self.height()-6)
        self.animation.setEndValue(new_geometry)
        self.animation.start()
        self.scale_anim.setStartValue(self.width())
        self.scale_anim.setEndValue(120)
        self.scale_anim.start()
        super().leaveEvent(event)
    def set_selected(self, selected):
        self.selected = selected
        if selected:
            self.setStyleSheet(self.selected_style)
        else:
            self.setStyleSheet(self.base_style)

class GradientFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: #181c2f;
                border-radius: 20px;
                border: 2px solid #232946;
            }
        """)

class AnimatedLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                color: #e0eaff;
                background: transparent;
                padding: 10px;
                text-shadow: 2px 2px 8px #232946;
            }
        """)
        # Fade-in animation
        self.setGraphicsEffect(QGraphicsDropShadowEffect())
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

class StatusIndicator(QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(60)
        self.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #232946, stop:1 #393e6e);
                border: 2px solid #393e6e;
                border-radius: 15px;
                color: #e0eaff;
                padding: 15px;
                font-weight: bold;
                text-shadow: 2px 2px 8px #232946;
            }
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Segoe UI", 11))
        # Pulse animation
        self.pulse_animation = QPropertyAnimation(self, b"windowOpacity")
        self.pulse_animation.setDuration(2000)
        self.pulse_animation.setStartValue(0.7)
        self.pulse_animation.setEndValue(1.0)
        self.pulse_animation.setLoopCount(-1)
        self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.pulse_animation.start()

class InstalockUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VALORANT INSTALOCK – by Luarea")
        self.setWindowIcon(QIcon("bbl.ico"))
        self.setFixedSize(900, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #232946, stop:0.5 #393e6e, stop:1 #181c2f);
                color: #e0eaff;
            }
        """)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        # Title with animation
        self.title = AnimatedLabel("VALORANT INSTALOCK")
        self.title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.title.setStyleSheet("""
            QLabel {
                color: #e0eaff;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #232946, stop:1 #6d28d9);
                border-radius: 15px;
                padding: 20px;
                text-shadow: 2px 2px 8px #232946;
            }
        """)
        main_layout.addWidget(self.title)
        # Status indicator
        self.status = StatusIndicator()
        self.status.setText("Agent not selected")
        main_layout.addWidget(self.status)
        # Agents grid with enhanced styling
        grid_container = GradientFrame()
        grid_layout = QVBoxLayout(grid_container)
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid = QGridLayout()
        grid.setSpacing(18)
        grid.setContentsMargins(18, 18, 18, 18)
        agents = list(agent_coordinates.keys())
        cols = 6
        self.agent_buttons = {}
        for i, agent in enumerate(agents):
            btn = AnimatedButton(agent)
            btn.clicked.connect(lambda _, a=agent: self.select_agent(a))
            row = i // cols
            col = i % cols
            grid.addWidget(btn, row, col)
            self.agent_buttons[agent] = btn
        grid_layout.addLayout(grid)
        main_layout.addWidget(grid_container)
        # Control instructions with animation
        self.control = AnimatedLabel("▶ F8: Spam Lock (press F8)")
        self.control.setFont(QFont("Segoe UI", 12))
        self.control.setStyleSheet("""
            QLabel {
                color: #e0eaff;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #232946, stop:1 #6d28d9);
                border-radius: 10px;
                padding: 10px;
                text-shadow: 2px 2px 8px #232946;
            }
        """)
        main_layout.addWidget(self.control)
        # Signature with subtle animation
        self.signature = AnimatedLabel("Made by Luarea")
        self.signature.setFont(QFont("Segoe UI", 10))
        self.signature.setStyleSheet("""
            QLabel {
                color: #6d28d9;
                background: transparent;
                text-shadow: 2px 2px 8px #232946;
            }
        """)
        main_layout.addWidget(self.signature)
        self.setLayout(main_layout)
        # Thread setup
        self.thread = LockThread()
        self.thread.update_status.connect(self.update_status)
        self.thread.start()
        # Start fade-in animation for the entire window
        self.setWindowOpacity(0.0)
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(800)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_in_animation.start()

    def select_agent(self, agent):
        global selected_agent
        selected_agent = agent
        # Animate status change
        self.status.setText(f"Selected: {agent}")
        self.status.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #10B981);
                border: 2px solid #34D399;
                border-radius: 15px;
                color: white;
                padding: 15px;
                font-weight: bold;
            }
        """)
        # Animate selected button and reset others
        for a, btn in self.agent_buttons.items():
            btn.set_selected(a == agent)
        QTimer.singleShot(2000, lambda: self.status.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1F2937, stop:1 #374151);
                border: 2px solid #4B5563;
                border-radius: 15px;
                color: #F3F4F6;
                padding: 15px;
                font-weight: bold;
            }
        """))

    def update_status(self, message):
        self.status.setText(message)

    def closeEvent(self, event):
        # Fade-out animation before closing
        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(300)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out_animation.finished.connect(lambda: self.finish_close(event))
        self.fade_out_animation.start()

    def finish_close(self, event):
        # Safely stop the thread when closing the app
        if hasattr(self, 'thread'):
            self.thread.stop()
            self.thread.wait()
        event.accept()

class BloodDropLabel(QLabel):
    def __init__(self, x, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap('assets/blood_drop.png').scaled(28, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.x = x
        self.y = 0
        self.setFixedSize(28, 40)
        self.setStyleSheet('background: transparent;')
        self.falling = True
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setBlurRadius(18)
        self.glow.setColor(QColor('#ff1a1a'))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)
    def move_drop(self):
        self.y += 4
        self.move(self.x, self.y)
        if self.y > 30:
            self.hide()
            self.falling = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    instalock_ui = InstalockUI()
    instalock_ui.show()
    sys.exit(app.exec())