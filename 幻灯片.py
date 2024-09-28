import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和固定大小
        self.setWindowTitle('Image Slideshow')
        self.setFixedSize(1200, 1400)

        # 创建一个标签用于显示图片
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # 创建布局并将标签添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        # 创建一个小部件并设置布局
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 定义图片路径
        self.image_paths = [
            r"C:\Users\17489\Pictures\Screenshots\sdf.png",
            r"C:\Users\17489\Pictures\Screenshots\yifei2.png",
            r"C:\Users\17489\Pictures\Screenshots\cewcdasc.png",
            r"C:\Users\17489\Pictures\Screenshots\3334.png",
            r"C:\Users\17489\Pictures\Screenshots\屏幕截图 2024-09-27 185520.png",
            r"C:\Users\17489\Pictures\Screenshots\1q.png",
            r"C:\Users\17489\Pictures\Screenshots\20241.png",
            r"C:\Users\17489\Pictures\Screenshots\yifei1.png",
            r"C:\Users\17489\Pictures\Screenshots\th.jpg",
            r"C:\Users\17489\Pictures\Screenshots\qwea.png",
            r"C:\Users\17489\Pictures\Screenshots\mdccds.png",
            r"C:\Users\17489\Pictures\Screenshots\屏幕截图 2024-09-27 185839.png",
            r"C:\Users\17489\Pictures\Screenshots\屏幕截图 2024-09-27 190602.png"
        ]

        self.current_index = 0

        # 设置 QTimer，每3秒切换一张图片
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(3000)  # 每3000毫秒(3秒)触发一次

        # 显示初始图片
        self.update_image()

    def update_image(self):
        """更新图片"""
        if os.path.exists(self.image_paths[self.current_index]):
            pixmap = QPixmap(self.image_paths[self.current_index])
            self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.current_index = (self.current_index + 1) % len(self.image_paths)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())
