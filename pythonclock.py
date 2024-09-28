# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtGui import QFont

class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('电子时钟')
        self.resize(200, 100)

        layout = QVBoxLayout()
        self.timeLabel = QLabel(self)
        self.timeLabel.setAlignment(Qt.AlignCenter)
        
        # 设置字体大小为原来的3倍
        font = QFont()
        font.setPointSize(50)  # 假设原来的字体大小为12
        self.timeLabel.setFont(font)
        
        layout.addWidget(self.timeLabel)
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)

        self.updateTime()

    def updateTime(self):
        currentTime = QTime.currentTime()
        timeText = currentTime.toString('hh:mm:ss')
        self.timeLabel.setText(timeText)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = ClockWidget()
    clock.show()
    sys.exit(app.exec_())
