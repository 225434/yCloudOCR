from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class DropDialog(QDialog):
    def __init__(self, file_dropped_callback, parent=None, tip=''):
        super().__init__(parent)
        self.file_dropped_callback = file_dropped_callback
        self.tip = tip

        # 设置窗口标题
        self.setWindowTitle('拖拽打开文件')

        # 设置窗口大小
        self.setFixedSize(400, 200)

        # 设置布局和标签
        self.layout = QVBoxLayout()
        self.label = QLabel('将文件拖拽至此窗口\n\n' + self.tip, self)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(10)  # 设置字体大小为18
        self.label.setFont(font)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # 启用拖放
        self.setAcceptDrops(True)

        # 去除问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        # 使用传入的回调函数处理文件路径
        image = self.file_dropped_callback(file_path)
        self.close()
        return image
