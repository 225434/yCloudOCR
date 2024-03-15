import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QAction, QGraphicsPixmapItem, QProgressDialog

from python.util.progress_dialog import ProgressDialog


class UiUtil:
    progress_dialog = None

    @staticmethod
    def add_action(window, menu, action_text, callback):
        action = QAction(action_text, window)
        if callback:
            action.triggered.connect(callback)
        menu.addAction(action)

    def load_image(self, qimage, scene, view):
        if not qimage.isNull():
            scene.clear()  # 清除现有的图形项
            pixmap = QPixmap.fromImage(qimage)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            scene.addItem(pixmap_item)
            # 重设场景
            view.setScene(scene)
            # 在调用fitInView之前，确保视图已经调整到新场景的尺寸
            view.setSceneRect(pixmap_item.boundingRect())
            # 使图像自适应视图
            view.fitInView(pixmap_item, Qt.KeepAspectRatio)
            # 清除可能存在的旧视图状态
            view.centerOn(pixmap_item)
            # 强制视图更新
            view.update()
            if scene.flag:
                scene.addPixmap(QPixmap(qimage))
        self.reset_mouse_event(view)

    @staticmethod
    def get_qimage_from_image_view(window):
        view = window.image_view
        items = view.scene().items()

        if items:
            pixmap_item = items[0]
            if isinstance(pixmap_item, QGraphicsPixmapItem):
                pixmap = pixmap_item.pixmap()
                qimage = pixmap.toImage()
                return qimage
        return None

    @staticmethod
    def get_qimage_from_result_image_view(window):
        view = window.result_image_view
        items = view.scene().items()

        if items:
            pixmap_item = items[0]
            if isinstance(pixmap_item, QGraphicsPixmapItem):
                pixmap = pixmap_item.pixmap()
                qimage = pixmap.toImage()
                return qimage
        return None

    @staticmethod
    def create_folder(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"文件夹 '{folder_path}' 已成功创建！")
        else:
            print(f"文件夹 '{folder_path}' 已存在。")

    @staticmethod
    def open_folder_dialog(folder_path):
        # 使用QFileDialog.getExistingDirectory方法打开现有文件夹
        os.startfile(folder_path)

    def show_progress_indicator(self, window):
        # 创建一个进度对话框
        self.progress_dialog = ProgressDialog(window)
        self.progress_dialog.show()

    def hide_progress_indicator(self):
        # 关闭进度对话框
        if self.progress_dialog is not None:
            self.progress_dialog.close()
            self.progress_dialog = None

    def cancel_progress_indicator(self):
        # 用户取消操作时的处理
        if self.progress_dialog is not None:
            self.progress_dialog.cancel()

    @staticmethod
    def reset_mouse_event(view):
        view.mousePressEvent = view.mousePressEvent
        view.mouseMoveEvent = view.mouseMoveEvent
        view.mouseReleaseEvent = view.mouseReleaseEvent

    @staticmethod
    def set_menu_enabled(menu, condition):
        for action in menu.actions():
            action.setEnabled(condition)
