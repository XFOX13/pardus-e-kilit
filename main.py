from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QTimer, QTime
import sys

class PardusEKilit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PARDUS E-Kilit")
        self.setGeometry(100, 100, 420, 740)
        self.initUI()
        self.restart_interval = 40 * 60  # 40 dakika, saniye cinsinden

    def paintEvent(self, event):
        # Arka plan gradient'i çiz
        painter = QPainter(self)
        gradient = painter.linearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#114151"))
        gradient.setColorAt(1, QColor("#4e270f"))
        painter.fillRect(self.rect(), gradient)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)
        layout.setContentsMargins(30,40,30,40)
        layout.setSpacing(32)

        # Pardus logo (örnek: pardus_logo.png)
        logo_label = QLabel()
        logo_pixmap = QPixmap("pardus_logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Başlıklar
        pardus_label = QLabel("PARDUS")
        pardus_label.setFont(QFont("Arial", 32, QFont.Bold))
        pardus_label.setStyleSheet("color: #fff; margin-top:10px;")
        pardus_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(pardus_label)

        ekilit_label = QLabel("E-Kilit")
        ekilit_label.setFont(QFont("Arial", 22, QFont.Normal))
        ekilit_label.setStyleSheet("color: #fff")
        ekilit_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(ekilit_label)

        # 6 Haneli Kod Kutuları
        code_row = QHBoxLayout()
        self.code_boxes = []
        for _ in range(6):
            box = QLineEdit()
            box.setFixedSize(40,48)
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
            qr_pixmap = qr_pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            qr_label.setPixmap(qr_pixmap)
        qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(qr_label)

        # Butonlar
        btn_row = QHBoxLayout()
        self.close_btn = QPushButton("KAPAT")
        self.close_btn.setStyleSheet("background:#222; color:#fff; font-size:22px; border-radius:7px; padding:8px 26px; font-weight:bold")
        self.close_btn.clicked.connect(self.close)
        self.enter_btn = QPushButton("GİR")
        self.enter_btn.setStyleSheet("background:#222; color:#fff; font-size:22px; border-radius:7px; padding:8px 26px; font-weight:bold")
        self.enter_btn.clicked.connect(self.enter_code)
        btn_row.addWidget(self.close_btn)
        btn_row.addWidget(self.enter_btn)
        btn_widget = QWidget()
        btn_widget.setLayout(btn_row)
        layout.addWidget(btn_widget, alignment=Qt.AlignCenter)

        # Zamanlayıcı - her 40 dkda bir sıfırlanır/kapatır
        self.clock_label = QLabel("40:00")
        self.clock_label.setFont(QFont("Arial", 38, QFont.Bold))
        self.clock_label.setStyleSheet("color: #fff; background:transparent; margin-top:26px;")
        self.clock_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.clock_label)

        self.seconds_label = QLabel("m 00 s")
        self.seconds_label.setFont(QFont("Arial", 19))
        self.seconds_label.setStyleSheet("color: #fff; background:transparent;")
        self.seconds_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.seconds_label)

        # Timer
        self.time_left = QTime(0, 40, 0)  # 40 dakika
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.setLayout(layout)

    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        self.clock_label.setText(self.time_left.toString("mm:ss"))
        self.seconds_label.setText(f"m {self.time_left.second()} s")
        # Her 40 dakikada bir otomatik kendini kapatsın
        if self.time_left.minute() == 0 and self.time_left.second() == 0:
            self.timer.stop()
            self.close()  # Uygulama otomatik kapanır

    def enter_code(self):
        code = "".join(box.text() for box in self.code_boxes)
        # Doğrulama işlevi buraya (örnek kod: 102828)
        if code == "102828":
            self.timer.stop()
            self.clock_label.setText("Kilit Açıldı!")
            self.seconds_label.setText("")
        else:
            self.clock_label.setText("Yanlış Kod!")
            self.seconds_label.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = PardusEKilit()
    ui.show()
    sys.exit(app.exec_())