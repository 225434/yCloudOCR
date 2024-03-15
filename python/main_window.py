from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QGraphicsScene,
    QGraphicsView, QGraphicsPixmapItem, QTextBrowser, QFileDialog,
    QRubberBand, QAction, QWidget, QMenu
)

from python.controller.image_view_controller import ImageScene
from python.controller.main_controller import MainController
from python.controller.quick_controller import QuickController

WINDOW_SIZE = (1440, 840)
MINIUM_SIZE = (1080, 720)


class MainWindow(QMainWindow):

    IMAGE_INIT_PATH = 'resources/static/init/image_init.png'
    TEXT_INIT_PATH = 'resources/static/init/text_init.png'
    LOGO_ICON_PATH = 'resources/static/init/logo.icon'
    STYLE_FILE_PATH = 'python/qss/styles.qss'

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR")
        self.resize(*WINDOW_SIZE)
        self.setMinimumSize(*MINIUM_SIZE)
        self.setWindowIcon(QIcon(self.LOGO_ICON_PATH))

        # 部件初始化
        # self.image_scene = QGraphicsScene(self)
        self.image_scene = ImageScene(self, True)
        # self.image_scene.addPixmap(QPixmap(QImage(self.IMAGE_INIT_PATH)))
        self.image_view, _ = self.create_graphics_view(QImage(self.IMAGE_INIT_PATH))
        # self.image_scene.addPixmap(QPixmap(QImage(self.IMAGE_INIT_PATH)))
        # self.image_view = QGraphicsView(self.image_scene)
        self.result_image_scene = ImageScene(self, False)

        self.result_image_view, self.result_image_pixmap_item = self.create_graphics_view(QImage(self.TEXT_INIT_PATH))
        self.result_text = QTextBrowser(self)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self.image_view)  # 添加 QRubberBand
        self.menubar = self.menuBar()
        self.file_dialog = QFileDialog()
        self.fresh_tool = QMenu("Fresh Tool", self)
        self.default_action = QAction("默认操作", self)  # 创建默认的 QAction
        self.origin = QPoint()
        self.opened_list = []

        # Controller
        self.controller = MainController(self)
        self.quick = QuickController(self)
        
        self.init_ui()

    def init_ui(self):
        self.load_style_sheet(self.STYLE_FILE_PATH)
        self.setup_menus()
        self.result_text.setFixedHeight(200)  # 设置文本显示组件
        self.setup_layout()

    def load_style_sheet(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def setup_layout(self):
        main_widget = QWidget(self)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 组织布局
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_view)
        image_layout.addWidget(self.result_image_view)

        main_layout.addLayout(image_layout)
        main_layout.addWidget(self.result_text)

        self.setCentralWidget(main_widget)

    def setup_menus(self):
        # 创建菜单栏
        self.menubar = self.menuBar()

    def create_graphics_view(self, qimage):
        pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(qimage))
        scene = QGraphicsScene()
        scene.addItem(pixmap_item)
        view = QGraphicsView(scene, self)
        return view, pixmap_item

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 检查场景是否有内容
        if not self.image_scene.itemsBoundingRect().isEmpty():
            # 重新调整图像以适应窗口的新大小
            self.image_view.fitInView(self.image_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            self.result_image_view.fitInView(self.result_image_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            # 强制视图更新
            self.update()