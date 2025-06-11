from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout
)
from PySide6.QtGui import QMouseEvent, QPainter, QPixmap, QPainterPath
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QSize, QUrl
from PySide6.QtGui import QDesktopServices
import sys

class RoundedIconButton(QPushButton):
    def __init__(self, image_path):
        super().__init__()
        self.setFixedSize(40, 40)
        self.image = QPixmap(image_path)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("helpButton")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 8, 8)
        painter.setClipPath(path)
        painter.drawPixmap(self.rect(), self.image)

class CarouselWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Created by IrisDMA")
        self.setGeometry(200, 200, 700, 450)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.old_pos = QPoint()

        self.container = QWidget()
        self.container.setObjectName("container")
        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        help_container = QWidget()
        help_layout = QVBoxLayout(help_container)
        help_layout.setContentsMargins(0, 0, 0, 0)
        help_layout.setSpacing(4)
        help_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.help_button = RoundedIconButton("img/discord.png")
        self.help_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://guns.lol/irisdma")))

        self.help_label = QLabel("Need Help?")
        self.help_label.setObjectName("helpLabel")
        self.help_label.setAlignment(Qt.AlignHCenter)

        help_inner = QWidget()
        inner_layout = QVBoxLayout(help_inner)
        inner_layout.setAlignment(Qt.AlignHCenter)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(4)
        inner_layout.addWidget(self.help_button, alignment=Qt.AlignHCenter)
        inner_layout.addWidget(self.help_label, alignment=Qt.AlignHCenter)

        help_layout.addWidget(help_inner)
        main_layout.addWidget(help_container)

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.build_intro_page())
        self.stacked.addWidget(self.build_page("Spoofing HWID", [
            "1. Download the spoofer below",
            "2. Extract the folder (password: IrisDMA)",
            "3. Run \"IrisSpoofer.exe\" as administrator"
        ], "https://cdn.discordapp.com/attachments/1373270795299586171/1382358478353334332/1337.rar?ex=684add28&is=68498ba8&hm=49db3c02293847d4450f6c8351f8a9ec8c54f466f4918800f5cb097c2840adb9&"))

        self.stacked.addWidget(self.build_page("MAC Spoofing", [
            "1. Download the spoofer below",
            "2. Run \"IrisSpoofer.exe\" as administrator"
        ], "https://cdn.discordapp.com/attachments/1373270795299586171/1382359993830867076/main.bat?ex=684ade91&is=68498d11&hm=5a99fd09474d96486a629d1b81dfe17319ce97739c08c547e8ea7a46c75865cf&"))

        self.stacked.addWidget(self.build_page("VolumeID Spoofing", [
            "1. Download the spoofer below",
            "2. Run \"VolumeID.exe\" as administrator",
            "3. Change disk characters like: AB12-CD34 → 43DC-21BA"
        ], "https://cdn.discordapp.com/attachments/1373270795299586171/1382360655881048114/VolumeID.exe?ex=684adf2f&is=68498daf&hm=4214ac3149436dc92c76d22ab594d1c970749df2078a0d0c4660b0ee7e6e724f&"))

        self.stacked.addWidget(self.build_page("Disk Spoofing", [
            "1. Restart your system",
            "2. Download the spoofer below",
            "3. Run \"disk.ps1\"",
            "4. This hides your disk serials until restart"
        ], "https://cdn.discordapp.com/attachments/1373270795299586171/1382361550815498321/run.ps1?ex=684ae004&is=68498e84&hm=285cf670c480b154d9171a82820ca35f2d2a83625a37fb9cc0e7e1a34e99b800&"))

        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("←")
        self.prev_btn.clicked.connect(self.show_prev)
        self.prev_btn.setObjectName("navButton")

        self.next_btn = QPushButton("→")
        self.next_btn.clicked.connect(self.show_next)
        self.next_btn.setObjectName("navButton")

        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)

        main_layout.addWidget(self.stacked)
        main_layout.addLayout(nav_layout)
        self.setCentralWidget(self.container)
        self.apply_styles()

    def build_intro_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        title = QLabel("🛠️ Requirements")
        title.setStyleSheet("color: #b388eb; font-size: 26px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addLayout(self.icon_line("img/windows.png", "Windows 10"))
        layout.addLayout(self.icon_line("img/usb.png", "USB Stick (8GB+)"))

        tips = QLabel(
            "🖥 Simple Setup:\n"
            "1. Insert USB stick\n"
            "2. Download Windows 10 ISO\n"
            "3. Use Rufus to burn ISO to USB\n"
            "4. Boot into USB from BIOS\n"
            "5. Install Windows with no internet connection"
            
        )
        tips.setStyleSheet("color: white; font-size: 13px;")
        tips.setAlignment(Qt.AlignCenter)
        tips.setWordWrap(True)
        layout.addWidget(tips)

        return page

    def icon_line(self, img_path, text):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        layout.setSpacing(6)
        icon = QLabel()
        icon.setPixmap(QPixmap(img_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label = QLabel(text)
        label.setStyleSheet("color: white; font-size: 13px;")
        layout.addWidget(icon)
        layout.addWidget(label)
        return layout

    def build_page(self, title_text, instructions_list, url):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(18)

        title = QLabel(title_text)
        title.setStyleSheet("color: #b388eb; font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        instructions = QLabel("\n".join(instructions_list))
        instructions.setStyleSheet("color: white; font-size: 14px;")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True)

        download_btn = QPushButton("DOWNLOAD SPOOFER")
        download_btn.setFixedSize(240, 42)
        download_btn.setObjectName("downloadButton")
        download_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))

        layout.addWidget(title)
        layout.addWidget(instructions)
        layout.addWidget(download_btn)
        return page

    def show_next(self):
        index = self.stacked.currentIndex()
        if index < self.stacked.count() - 1:
            self.animate_transition(index, index + 1)
            self.stacked.setCurrentIndex(index + 1)

    def show_prev(self):
        index = self.stacked.currentIndex()
        if index > 0:
            self.animate_transition(index, index - 1)
            self.stacked.setCurrentIndex(index - 1)

    def animate_transition(self, from_index, to_index):
        direction = 1 if to_index > from_index else -1
        offset = self.stacked.width() * direction
        from_widget = self.stacked.widget(from_index)
        to_widget = self.stacked.widget(to_index)
        to_widget.setGeometry(offset, 0, self.stacked.width(), self.stacked.height())
        self.stacked.setCurrentWidget(to_widget)
        anim = QPropertyAnimation(to_widget, b"pos")
        anim.setDuration(300)
        anim.setStartValue(QPoint(offset, 0))
        anim.setEndValue(QPoint(0, 0))
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()
        self._anim = anim

    def apply_styles(self):
        self.container.setStyleSheet("""
        #container {
            background-color: #0a0a0a;
            border-radius: 16px;
        }

        #navButton {
            background-color: #4c2a85;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            font-size: 18px;
        }

        #navButton:hover {
            background-color: #6a42a1;
        }

        #downloadButton {
            background-color: #4c2a85;
            color: white;
            font-size: 15px;
            font-weight: bold;
            border: none;
            border-radius: 12px;
        }

        #downloadButton:hover {
            background-color: #6a42a1;
        }

        #helpLabel {
            color: white;
            font-size: 10px;
        }
        """)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarouselWindow()
    window.show()
    sys.exit(app.exec())
