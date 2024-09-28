import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QDateTime, Qt, QDate
from PyQt5.QtGui import QPalette, QColor, QFont
from datetime import datetime

class ClockWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle('电子时钟')
        self.setGeometry(500, 500, 800, 800)

        # 设置窗口背景颜色为白色
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(Qt.white))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # 创建布局用于放置标签
        layout = QVBoxLayout()

        # 创建标签用于显示日期和时间
        self.beijing_label = QLabel(self)
        self.est_label = QLabel(self)
        self.date_label = QLabel(self)
        self.countdown_label = QLabel(self)

        # 设置字体为黑色，大小为66px
        font = QFont("Arial", 36)
        self.beijing_label.setFont(font)
        self.beijing_label.setStyleSheet("color: black;")
        self.beijing_label.setAlignment(Qt.AlignCenter)

        self.est_label.setFont(font)
        self.est_label.setStyleSheet("color: black;")
        self.est_label.setAlignment(Qt.AlignCenter)

        self.date_label.setFont(font)
        self.date_label.setStyleSheet("color: black;")
        self.date_label.setAlignment(Qt.AlignCenter)

        self.countdown_label.setFont(font)
        self.countdown_label.setStyleSheet("color: black;")
        self.countdown_label.setAlignment(Qt.AlignCenter)

        # 将标签添加到布局中
        layout.addWidget(self.date_label)
        layout.addWidget(self.beijing_label)
        layout.addWidget(self.est_label)
        layout.addWidget(self.countdown_label)

        # 创建容器并设置布局
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 设置定时器每秒更新一次
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次

        self.update_time()  # 初始化时调用一次

    def update_time(self):
        # 获取当前北京时间
        beijing_time = QDateTime.currentDateTime()

        # 计算美国东部时间（与北京时间时差为-12小时）
        est_time = beijing_time.addSecs(-12 * 3600)

        # 获取当前日期
        current_date = beijing_time.date()

        # 计算距离春节的天数
        next_spring_festival = self.get_next_spring_festival()
        days_until_spring_festival = current_date.daysTo(next_spring_festival)

        # 更新标签文本
        self.date_label.setText(f"当前日期: {beijing_time.toString('yyyy-MM-dd')}")
        self.beijing_label.setText(f"北京时间: {beijing_time.toString('hh:mm:ss')}")
        self.est_label.setText(f"美国东部时间: {est_time.toString('hh:mm:ss')}")
        self.countdown_label.setText(f"距离春节: {days_until_spring_festival} 天")

    def get_next_spring_festival(self):
        """获取下一个春节日期"""
        current_year = QDateTime.currentDateTime().date().year()
        # 假设春节在每年的2月10日
        spring_festival_date = QDate(current_year + 1, 2, 10)  # 假设下一个春节为 2025 年 2 月 10 日
        return spring_festival_date

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClockWindow()
    window.show()
    sys.exit(app.exec_())
