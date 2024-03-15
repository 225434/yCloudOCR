import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class QuestionDialog(QDialog):
    def __init__(self, parent=None, title="", message="", textA="", textB=""):
        super().__init__(parent)
        self.setWindowTitle(title)

        # 设置窗口样式以去除问号
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.yesButton = QPushButton(textA)
        self.noButton = QPushButton(textB)
        self.initUI(message)

    def initUI(self, message):
        layout = QVBoxLayout(self)

        # 添加消息文本并设置文本居中
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)  # 设置文本在水平和竖直方向都居中
        layout.addWidget(label)

        # 添加按钮并连接信号
        layout.addWidget(self.yesButton)
        layout.addWidget(self.noButton)

        # 连接到自定义方法
        self.yesButton.clicked.connect(self.on_yes_clicked)
        self.noButton.clicked.connect(self.on_no_clicked)

        self.setLayout(layout)
        self.setFixedSize(400, 200)

    def on_yes_clicked(self):
        # 自定义的按钮点击动作
        os.startfile('D:/Code/Python/OCR_Pro/saved/recognized')
        self.accept()

    def on_no_clicked(self):
        self.reject()

    def showDialog(self):
        # 显示对话框并等待用户响应
        result = self.exec_()
        return result == QDialog.Accepted
