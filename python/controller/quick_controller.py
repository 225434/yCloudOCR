import os

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from paddleocr.ppstructure.predict_system import save_structure_res

from python.service.edit_service import EditService
from python.service.recognition_service import RecognitionService
from python.util.drop_dialog import DropDialog
from python.util.image_util import ImageUtil
from python.util.question_dialog import QuestionDialog
from python.util.recognition_thread import TableRecognitionThread
from python.util.text_recognition_thread import RecognitionThread
from python.util.ui_util import UiUtil


class QuickController:
    def __init__(self, main_window):
        self.main_window = main_window  # 保存对主窗口的引用
        self.quick_menu = main_window.menubar.addMenu("快速开始")
        self.ui_tool = UiUtil()
        self.image_tool = ImageUtil()
        self.file_path = None
        self.font = QFont()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.count = 0
        self.edit_service = EditService()
        self.recognition_service = RecognitionService(self)

        self.ui_tool.add_action(self.main_window, self.quick_menu, "识别文字", self.quick_start_text)
        self.ui_tool.add_action(self.main_window, self.quick_menu, "识别表格", self.quick_start_table)

    def quick_start_text(self):
        self.main_window.result_text.setText('')
        self.recognize_text_init()
        self.drop_open_file()
        temp_array = self.image_tool.open_array(self.file_path)
        gray_image = cv2.cvtColor(temp_array, cv2.COLOR_BGR2GRAY)
        self.recognize_text(gray_image)

    def quick_start_table(self):
        self.drop_open_file()
        temp_array = self.image_tool.open_array(self.file_path)
        # gray_image = cv2.cvtColor(temp_array, cv2.COLOR_BGR2GRAY)
        array = self.edit_service.table_enhance(temp_array)
        self.recognize_table(array)

    def drop_open_file(self):
        dialog = DropDialog(self.open_image_from_path, self.main_window, '快速模式下，建议图片中只包含一份识别信息')
        dialog.exec_()

    def recognize_text_init(self):
        self.font.setFamily('Microsoft YaHei')
        self.font.setPointSize(13)
        self.main_window.result_text.setFont(self.font)

    def open_image_from_path(self, file_path):
        self.file_path = file_path
        self.image_tool.get_qimage_from_path(file_path)

    def update_text(self):
        self.timer.start(300)
        self.count += 1
        if self.count % 2 == 0:
            self.main_window.result_text.setText('识别中. . .')
        else:
            self.main_window.result_text.setText('识别中. . . . . .')

        if self.count >= 4:
            self.timer.stop()
            self.count = 0

    def recognize_text(self, array):
        self.recognize_text_init()
        self.update_text()
        # 创建新的线程来执行文本识别
        self.recognition_thread = RecognitionThread(array, self.recognition_service)
        self.recognition_thread.textRecognized.connect(self.on_text_recognized)
        self.recognition_thread.start()

    def on_text_recognized(self, text):
        self.main_window.result_text.setText(text)

    def recognize_table(self, array):
        self.recognition_thread = TableRecognitionThread(array)

        # 连接信号槽
        self.recognition_thread.recognition_complete.connect(self.on_recognition_complete)
        self.recognition_thread.recognition_failed.connect(self.on_recognition_failed)

        # 显示进度指示器
        self.ui_tool.show_progress_indicator(self.main_window)

        # 启动线程
        self.recognition_thread.start()

    def on_recognition_complete(self, result):
        self.ui_tool.hide_progress_indicator()
        save_path = 'D:/Code/Python/OCR_Pro/saved/recognized'
        filename = self.image_tool.get_filename('recognized')
        save_structure_res(result, save_path,
                           os.path.basename(filename).split('.')[0])
        dialog = QuestionDialog(self.main_window, '识别成功', '结果已保存', '打开', '继续')
        dialog.showDialog()

    def on_recognition_failed(self):
        self.ui_tool.hide_progress_indicator()
        dialog = QuestionDialog(self.main_window, '识别失败', '识别失败，请重试', '打开', '继续')
        dialog.showDialog()