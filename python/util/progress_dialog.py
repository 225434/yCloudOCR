from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QLabel, QWidget, QHBoxLayout


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setWindowTitle('识别进度')
        self.setFixedSize(400, 200)

        # 设置窗口样式去除问号
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # 使用垂直布局
        layout = QVBoxLayout(self)

        # 添加标签并设置居中对齐
        self.label = QLabel("正在识别中...", self)
        self.label.setAlignment(Qt.AlignCenter)  # 设置标签文本在水平和竖直方向上都居中
        layout.addWidget(self.label)

        # 在进度条之前添加弹性空间
        layout.addStretch()

        # 添加进度条
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0)  # 设置为不确定模式
        self.progressBar.setAlignment(Qt.AlignCenter)  # 确保进度条内容居中对齐
        layout.addWidget(self.progressBar)

        # 在进度条之后添加弹性空间
        layout.addStretch()
