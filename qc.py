import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QWidget, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
)
from PyQt5.QtCore import QTimer, QRectF, Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPixmap, QPainter

class SpeedometerScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.speed = 0
        self.max_speed = 180
        self.radius = 150

        # 创建仪表盘
        self.create_speedometer()

        # 初始化指针
        self.pointer = QGraphicsLineItem()
        self.pointer.setPen(QPen(Qt.red, 3))
        self.addItem(self.pointer)
        self.update_pointer()

    def create_speedometer(self):
        """创建车速表刻度盘"""
        for i in range(10):  # 刻度从0到180，间隔20
            angle = 30 * i - 120  # 将0-180的刻度映射到-120°到120°
            x1 = self.radius * math.cos(math.radians(angle))
            y1 = self.radius * math.sin(math.radians(angle))
            x2 = (self.radius - 20) * math.cos(math.radians(angle))
            y2 = (self.radius - 20) * math.sin(math.radians(angle))

            line = QGraphicsLineItem(x1, y1, x2, y2)
            line.setPen(QPen(Qt.black, 3))
            self.addItem(line)

            # 在刻度旁边标注数字
            label = QLabel(str(i * 20))
            label_item = self.addWidget(label)
            label_item.setPos(x2 - 10, y2 - 10)

    def update_pointer(self):
        """更新指针位置，显示当前车速"""
        angle = (self.speed / self.max_speed) * 240 - 120  # 速度转换为角度
        x = self.radius * 0.9 * math.cos(math.radians(angle))
        y = self.radius * 0.9 * math.sin(math.radians(angle))
        self.pointer.setLine(0, 0, x, y)

    def set_speed(self, speed):
        """设置车速并更新指针"""
        self.speed = min(speed, self.max_speed)
        self.update_pointer()


class CarDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化界面
        self.setWindowTitle("汽车仪表盘")
        self.setGeometry(200, 200, 800, 600)

        # 初始化油量和车速
        self.speed = 0
        self.fuel_level = 50  # 初始油量为50%

        # 创建主布局
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        # 车速表
        self.speedometer_scene = SpeedometerScene()
        self.speedometer_view = QGraphicsView(self.speedometer_scene)
        self.speedometer_view.setRenderHint(QPainter.Antialiasing)  # 添加平滑渲染
        self.speedometer_view.setFixedSize(300, 300)

        self.top_layout.addWidget(self.speedometer_view)

        # 显示油量
        self.fuel_label = QLabel(f"油量：{self.fuel_level}%")
        self.fuel_label.setStyleSheet("font-size: 20px;")
        self.top_layout.addWidget(self.fuel_label)

        # 中间显示车辆图片
        self.car_image_label = QLabel()
        pixmap = QPixmap(r"C:\Users\17489\Pictures\Screenshots\gvyu.png")
        self.car_image_label.setPixmap(pixmap.scaled(400, 200, Qt.KeepAspectRatio))
        self.main_layout.addWidget(self.car_image_label, alignment=Qt.AlignCenter)

        # 加速和刹车按钮
        self.accelerate_btn = QPushButton("油门")
        self.accelerate_btn.clicked.connect(self.accelerate)

        self.brake_btn = QPushButton("刹车")
        self.brake_btn.clicked.connect(self.brake)

        self.bottom_layout.addWidget(self.accelerate_btn)
        self.bottom_layout.addWidget(self.brake_btn)

        # 档位按钮
        self.gear_buttons = []
        for i in range(1, 6):
            btn = QPushButton(f"{i}档")
            btn.setFixedSize(80, 40)
            btn.clicked.connect(self.change_gear)
            self.gear_buttons.append(btn)
            self.bottom_layout.addWidget(btn)

        # 设置布局
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # 创建定时器用于更新车速
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(100)

        # 刹车定时器
        self.brake_timer = QTimer()
        self.brake_timer.timeout.connect(self.slow_down)

    def accelerate(self):
        """点击油门增加车速"""
        if self.speed < 180:
            self.speed += 10
        self.update_speed()

    def brake(self):
        """点击刹车逐渐减速"""
        if not self.brake_timer.isActive():
            self.brake_timer.start(200)  # 每200毫秒降低速度

    def slow_down(self):
        """逐渐降低车速"""
        if self.speed > 0:
            self.speed -= 5
        else:
            self.speed = 0
            self.brake_timer.stop()
        self.update_speed()

    def update_speed(self):
        """更新车速显示"""
        self.speedometer_scene.set_speed(self.speed)

    def change_gear(self):
        """切换档位"""
        sender = self.sender()
        selected_gear = self.gear_buttons.index(sender) + 1
        self.set_speed_for_gear(selected_gear)

    def set_speed_for_gear(self, gear):
        """根据档位设置对应的速度"""
        speed_map = {
            1: 10,
            2: 20,
            3: 40,
            4: 60,
            5: 80,
        }
        self.speed = speed_map.get(gear, 0)
        self.update_speed()


def main():
    app = QApplication(sys.argv)
    dashboard = CarDashboard()
    dashboard.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

