from PyQt5.QtCore import QPoint, Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QPolygonF, QColor
from PyQt5.QtWidgets import QGraphicsScene, \
    QGraphicsPixmapItem

from python.util.image_util import ImageUtil
from python.util.ui_util import UiUtil


class ImageScene(QGraphicsScene):
    def __init__(self, parent, flag):
        super().__init__(parent)
        self.vertices = [QPoint(100, 100), QPoint(200, 100), QPoint(200, 200), QPoint(100, 200)]
        self.selected_vertex = None
        self.vertex_radius = 10
        self.line_width = 3
        self.ui_tool = UiUtil()
        self.image_util = ImageUtil()
        self.show_polygon = False
        self.setBackgroundBrush(Qt.white)
        self.item = None
        self.flag = flag

    def addPixmap(self, pixmap):
        self.item = QGraphicsPixmapItem(pixmap)
        self.addItem(self.item)
        self.center_polygon()

    def center_polygon(self):
        if self.item and not self.vertices:
            return
        # 计算多边形的边界矩形
        poly_bounds = QRectF(QPointF(min(v.x() for v in self.vertices), min(v.y() for v in self.vertices)),
                             QPointF(max(v.x() for v in self.vertices), max(v.y() for v in self.vertices)))
        # 计算图像的中心点
        img_center = self.item.boundingRect().center()
        # 计算多边形中心和图像中心之间的偏移
        offset = img_center - poly_bounds.center()
        # 更新多边形顶点位置
        self.vertices = [vertex + offset for vertex in self.vertices]

    def mousePressEvent(self, event):
        if self.flag:
            point = self.item.mapFromScene(event.scenePos())
            for idx, vertex in enumerate(self.vertices):
                if (vertex - point).manhattanLength() < self.vertex_radius * 2:
                    self.selected_vertex = idx
                    break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.flag and self.selected_vertex is not None:
            point = event.scenePos()
            new_vertices = self.vertices[:]
            new_vertices[self.selected_vertex] = point
            if self.is_valid_polygon(new_vertices):
                self.vertices[self.selected_vertex] = point
                self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.flag:
            self.selected_vertex = None
        super().mouseReleaseEvent(event)

    def drawForeground(self, painter, rect):
        if self.show_polygon:
            super().drawForeground(painter, rect)

            pen_width = 5
            pen = QPen(Qt.green, pen_width)  # 设置多边形边缘为默认的荧光绿色
            painter.setPen(pen)
            poly = QPolygonF(self.vertices)
            painter.drawPolygon(poly)

            # 假设你有方法self.getImage()来获取当前的QImage对象
            image = self.ui_tool.get_qimage_from_image_view(self.parent())  # 确保这个方法返回当前场景中的QImage对象

            # 绘制顶点
            for vertex in self.vertices:
                # 获取顶点位置的颜色
                color = image.pixelColor(int(vertex.x()), int(vertex.y()))

                # 计算对比色
                contrast_color = QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())

                # 设置笔和画刷为对比色来绘制顶点
                painter.setPen(contrast_color)
                painter.setBrush(contrast_color)
                painter.drawEllipse(vertex, self.vertex_radius, self.vertex_radius)
    @staticmethod
    def is_convex_polygon(vertices):
        if len(vertices) < 4:
            return True

        def cross_product(o, a, b):
            return (a.x() - o.x()) * (b.y() - o.y()) - (a.y() - o.y()) * (b.x() - o.x())
        sign = 0
        for i in range(len(vertices)):
            o, a, b = vertices[i], vertices[(i + 1) % len(vertices)], vertices[(i + 2) % len(vertices)]
            cross = cross_product(o, a, b)
            if cross != 0:
                if sign == 0:
                    sign = 1 if cross > 0 else -1
                elif sign * cross < 0:
                    return False
        return True

    def is_valid_polygon(self, vertices):
        n = len(vertices)
        if n < 3:
            return False

        for i in range(n):
            if self.distance_between_points(vertices[i], vertices[(i + 1) % n]) < 80:
                return False

        return self.is_convex_polygon(vertices)

    @staticmethod
    def distance_between_points(p1, p2):
        return (p1 - p2).manhattanLength()

    def toggle_polygon_display(self):
        self.show_polygon = not self.show_polygon
        self.update()
