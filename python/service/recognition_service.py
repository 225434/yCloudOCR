import os

from PyQt5.QtGui import QFont
from paddleocr import PaddleOCR
from paddleocr.ppstructure.predict_system import save_structure_res

from python.util.image_util import ImageUtil
from python.util.question_dialog import QuestionDialog
from python.util.recognition_thread import TableRecognitionThread
from python.util.ui_util import UiUtil


class RecognitionService:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui_tool = UiUtil()
        self.image_tool = ImageUtil()

    @staticmethod
    def recognize_text(array):
        ocr = PaddleOCR(use_angle_cls=True,
                        use_gpu=True,
                        rec_model_path='resources/model/paddleOCR/ch_PP-OCRv3_rec_infer')
        text = ocr.ocr(array, cls=True)
        if text is None or text == '':
            text = '无结果'
        else:
            recognized_texts = []
            for line in text:
                line_text = '\n'.join([word_info[1][0] for word_info in line])
                recognized_texts.append(line_text)

            text = '\n'.join(recognized_texts)
        print("识别结果:\n" + text)
        return text

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
