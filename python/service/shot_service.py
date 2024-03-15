import cv2
import numpy as np
from PyQt5.QtCore import QPoint

from python.util.image_util import ImageUtil
from python.util.ui_util import UiUtil


class ShotService:
    def __init__(self):
        self.ui_tool = UiUtil()
        self.image_tool = ImageUtil()
        self.is_quick_capture_active = False

    @staticmethod
    def get_limited_pos(event, view):
        # 获取 QGraphicsPixmapItem 的区域
        pixmap_rect = view.scene().itemsBoundingRect()

        # 将 QGraphicsPixmapItem 的区域转换为 QGraphicsView 的坐标系统
        image_rect = view.mapFromScene(pixmap_rect).boundingRect()

        # 获取鼠标的位置，但是限制在图片的区域内
        x = min(max(event.pos().x(), image_rect.left()), image_rect.right())
        y = min(max(event.pos().y(), image_rect.top()), image_rect.bottom())
        return QPoint(x, y)

    def capture_image(self, rubber_band, image_scene, image_view, result_image_scene, result_image_view):
        if rubber_band.isVisible():
            # 获取选择区域相对于图像的坐标和大小
            view_rect = rubber_band.geometry()
            scene_rect = image_view.mapToScene(view_rect).boundingRect()
            x, y, w, h = scene_rect.x(), scene_rect.y(), scene_rect.width(), scene_rect.height()

            # 从 QGraphicsPixmapItem 获取 QPixmap 对象
            pixmap = image_scene.items()[0].pixmap()  # 注意这里从当前image_scene的第一个item获取pixmap
            cropped_pixmap = pixmap.copy(x, y, w, h)

            # 将 QPixmap 转换为 QImage
            captured_qimage = cropped_pixmap.toImage()
            self.ui_tool.load_image(captured_qimage, result_image_scene, result_image_view)
            return captured_qimage

    def process_image(self, window):
        array = self.image_tool.qimage_to_array(self.ui_tool.get_qimage_from_image_view(window))
        mask = np.zeros(array.shape[:2], dtype=np.uint8)
        points = np.array([[p.x(), p.y()] for p in window.image_scene.vertices], np.int32)
        cv2.fillPoly(mask, [points], 255)
        masked = cv2.bitwise_and(array, array, mask=mask)
        trans_mask = mask == 0
        masked[trans_mask] = [255, 255, 255]
        captured_qimage = self.image_tool.array_to_qimage(masked)
        self.ui_tool.load_image(captured_qimage, window.result_image_scene, window.result_image_view)
        return masked

    @staticmethod
    def table_enhance(array):
        gray = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
        # 使用Canny边缘检测
        edges = cv2.Canny(gray, 50, 150, apertureSize=7)
        # 使用HoughLinesP进行线检测
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=200, maxLineGap=5)
        # 将检测到的线绘制在原图上
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(array, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return array
