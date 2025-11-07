from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QTime
import sys

class PardusEKilit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PARDUS E-Kilit")
        self.setGeometry(100, 100, 400, 700)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #114151, stop:1 #4e270f);
            }
        """)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        layout.setContentsMargins(30,40,30,40)
        layout.setSpacing(30)

        # Pardus logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("pardus_logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Başlık
        pardus_label = QLabel("PARDUS")
        pardus_label.setFont(QFont("Arial", 30, QFont.Bold))
        pardus_label.setStyleSheet("color: #fff; margin-top:10px;")
        pardus_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(pardus_label)

        ekilit_label = QLabel("E-Kilit")
        ekilit_label.setFont(QFont("Arial", 20, QFont.Normal))
        ekilit_label.setStyleSheet("color: #fff; margin-bottom:10px;")
        ekilit_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(ekilit_label)

        # 6 Haneli Kod Kutuları
        code_row = QHBoxLayout()
        self.code_boxes = []
        for _ in range(6):
            box = QLineEdit()
            box.setFixedSize(38,48)
            box.setMaxLength(1)
            box.setAlignment(Qt.AlignCenter)
            box.setFont(QFont("Consolas", 24, QFont.Bold))
            box.setStyleSheet("background: #181818; color: #fff; border-radius:8px;")
            self.code_boxes.append(box)
            code_row.addWidget(box)
        code_widget = QWidget()
        code_widget.setLayout(code_row)
        layout.addWidget(code_widget, alignment=Qt.AlignCenter)

        # QR Kod Görseli
        qr_label = QLabel()
        qr_pixmap = QPixmap("qrcode.png")
        if not qr_pixmap.isNull():
            qr_pixmap = qr_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            qr_label.setPixmap(qr_pixmap)
        qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(qr_label)

        # Butonlar
        btn_row = QHBoxLayout()
        self.close_btn = QPushButton("KAPAT")
        self.close_btn.setStyleSheet("background:#222; color:#fff; font-size:19px; border-radius:7px; padding:8px 22px;")
        self.close_btn.clicked.connect(self.close)
        self.enter_btn = QPushButton("GİR")
        self.enter_btn.setStyleSheet("background:#222; color:#fff; font-size:19px; border-radius:7px; padding:8px 22px;")
        self.enter_btn.clicked.connect(self.enter_code)
        btn_row.addWidget(self.close_btn)
        btn_row.addWidget(self.enter_btn)
        btn_widget = QWidget()
        btn_widget.setLayout(btn_row)
        layout.addWidget(btn_widget, alignment=Qt.AlignCenter)

        # Zamanlayıcı
        self.clock_label = QLabel("40:00")
        self.clock_label.setFont(QFont("Arial", 38, QFont.Bold))
        self.clock_label.setStyleSheet("color: #fff; margin-top:26px;")
        self.clock_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.clock_label)

        self.seconds_label = QLabel("m 00 s")
        self.seconds_label.setFont(QFont("Arial", 19))
        self.seconds_label.setStyleSheet("color: #fff;")
        self.seconds_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.seconds_label)

        # Timer
        self.time_left = QTime(0, 40, 0) # 40 dakika örnektir!
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.setLayout(layout)

    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        self.clock_label.setText(self.time_left.toString("mm:ss"))
        self.seconds_label.setText(f"m {self.time_left.second()} s")
        if self.time_left.minute() == 0 and self.time_left.second() == 0:
            self.timer.stop()
            # Burada otomatik kilit veya bir işlem ekleyebilirsin

    def enter_code(self):
        code = "".join(box.text() for box in self.code_boxes)
        if code == "102828":  # örnek! Bunu dosya veya algoritmadan çekebilirsin
            self.timer.stop()
            self.clock_label.setText("Kilit Açıldı!")
            self.seconds_label.setText("")
        else:
            self.clock_label.setText("Yanlış Kod!")
            self.seconds_label.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = PardusEKilit()
    ui.show()
    sys.exit(app.exec_())
