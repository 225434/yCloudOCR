import os

import cv2
import numpy as np
from PyQt5.QtCore import QRect, Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QRubberBand, QFileDialog

from python.service.shot_service import ShotService
from python.util.image_util import ImageUtil
from python.util.ui_util import UiUtil

SAVE_DIR = 'D:/Code/Python/OCR_Pro/saved/captured'


class ShotController:

    mouse_pressed = pyqtSignal(object)
    mouse_moved = pyqtSignal(object)
    mouse_released = pyqtSignal(object)

    def __init__(self, main_window):
        self.main_window = main_window  # 保存对主窗口的引用
        self.screenshot_menu = main_window.menubar.addMenu("截图")
        self.ui_tool = UiUtil()
        self.image_util = ImageUtil()

        self.origin = None
        self.shot_service = ShotService()
        self.image = None
        self.is_capturing = False
        self.rubber_band = None
        self.result_image_loaded = False
        self.scene = self.main_window.image_scene
        self.mutex = True

        self.setup_screenshot_menu_actions()

    def setup_screenshot_menu_actions(self):
        # 这里添加所有截图菜单项
        actions = [
            ("快速截图", self.quick_capture),
            ("不规则截图", self.shape_capture),
            ("Separator", None),
            ("完成截图", self.capture_image),
            ("Separator", None),
            ("表格增强", self.table_enhance),
            ("Separator", None),
            ("保存截图", self.save_captured_image)
        ]
        for action_text, callback in actions:
            if action_text == "Separator":
                self.screenshot_menu.addSeparator()
            else:
                self.ui_tool.add_action(self.main_window, self.screenshot_menu, action_text, callback)

    def quick_capture(self):
        if self.mutex:
            self.mutex = False
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self.main_window.image_view)
            self.main_window.image_view.mousePressEvent = lambda event: self.quick_mouse_press_event(event)
            self.main_window.image_view.mouseMoveEvent = lambda event: self.quick_mouse_move_event(event)
            self.main_window.image_view.mouseReleaseEvent = lambda event: self.quick_mouse_release_event(event)

    def shape_capture(self):
        if self.mutex:
            self.mutex = False
            self.main_window.image_scene.toggle_polygon_display()

    def table_enhance(self):
        image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_result_image_view(self.main_window))
        self.ui_tool.load_image(self.image_util.array_to_qimage(self.shot_service.table_enhance(image_array)),
                                self.main_window.result_image_scene, self.main_window.result_image_view)

    def capture_image(self):
        if self.rubber_band:
            self.image = self.shot_service.capture_image(self.rubber_band,
                                                         self.main_window.image_scene,
                                                         self.main_window.image_view,
                                                         self.main_window.result_image_scene,
                                                         self.main_window.result_image_view)
            self.rubber_band.hide()
            self.rubber_band = None  # 清理引用
            self.result_image_loaded = True
        elif self.main_window.image_scene.flag:
            self.shot_service.process_image(self.main_window)
            self.main_window.image_scene.toggle_polygon_display()
        self.mutex = True

    def save_captured_image(self):
        self.ui_tool.create_folder(SAVE_DIR)
        default_filename = self.image_util.get_filename('captured')
        default_save_path = os.path.join(SAVE_DIR, default_filename)
        filename, _ = QFileDialog.getSaveFileName(self.main_window,
                                                  "保存图像",
                                                  default_save_path,
                                                  "PNG 图像 (*.png);;JPG 图像 (*.jpg);;所有文件 (*)")
        if filename:
            if self.image.save(filename):
                print(f"已捕获的图像已保存在: {filename}")
            else:
                print("保存文件失败，请检查磁盘空间或文件权限。")

    def quick_mouse_press_event(self, event):
        if event.button() == Qt.LeftButton and self.rubber_band:
            self.origin = self.shot_service.get_limited_pos(event, self.main_window.image_view)
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()

    def quick_mouse_move_event(self, event):
        if event.buttons() == Qt.LeftButton and self.rubber_band:
            limited_pos = self.shot_service.get_limited_pos(event, self.main_window.image_view)
            self.rubber_band.setGeometry(QRect(self.origin, limited_pos).normalized())

    def quick_mouse_release_event(self, event):
        if event.button() == Qt.LeftButton and self.rubber_band:
            self.rubber_band.show()  # 可能需要调整此处逻辑以确保rubber_band在适当时机被销毁

    def process_image(self, array):
        mask = np.zeros(array.shape[:2], dtype=np.uint8)
        points = np.array([[p.x(), p.y()] for p in self.scene.vertices], np.int32)
        # noinspection PyTypeChecker
        cv2.fillPoly(mask, [points], 255)
        result = cv2.bitwise_and(array, array, mask=mask)
        return result

    def is_result_image_loaded(self):
        return self.result_image_loaded
