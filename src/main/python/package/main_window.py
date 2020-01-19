import os
from PySide2 import QtWidgets, QtCore, QtGui

from package.api.image import CustomImage
from package.widget import FileBrowser


class Worker(QtCore.QObject):
    """This is a class to create the worker of the threading system."""

    image_processed = QtCore.Signal(object, bool)
    finished = QtCore.Signal()

    def __init__(self, images_to_process, folder, pos, size=None,
                 wt_type=None, text=None, font=None, color=None, logo=None):
        """The constructor of the worker.

        :param images_to_process: The images items to process.
        :param folder: The name of the output folder.
        :param pos: The position of the watermark.
        :param size: The reduction size coefficient.
        :param wt_type: The type of the watermark.
        :param text: The text of the watermark.
        :param font: The font of the watermark.
        :param color: The color of the watermark.
        :param logo: The path of the image watermark.

        :type images_to_process: QWidgets.QListWidgetItem
        :type folder: str
        :type pos: str
        :type size: float
        :type wt_type: str
        :type text: str
        :type font: str
        :type color: str
        :type logo: str
        """
        super().__init__()
        self.images_to_process = images_to_process
        self.type = wt_type
        self.text = text
        self.font = font
        self.color = color
        self.logo = logo
        self.size = size
        self.folder = folder
        self.pos = pos
        self.runs = True

    def process_images(self):
        """Convert the all the images of the list."""
        for image_lw_item in self.images_to_process:
            if self.runs and not image_lw_item.processed:
                image = CustomImage(path=image_lw_item.text(), folder=self.folder)
                success = None
                if self.type == "text":
                    success = image.watermark_text(self.text, self.color, self.font, self.size, self.pos)
                elif self.type == "image":
                    success = image.watermark_image(self.logo, self.pos)
                self.image_processed.emit(image_lw_item, success)

        self.finished.emit()


class MainWindow(QtWidgets.QWidget):
    """This is a class to create the window of the application."""

    WATERMARK_POSITION = (
        "top left",
        "top right",
        "center",
        "bottom left",
        "bottom right",
    )

    DEFAULT_COLOR = "#000000"

    def __init__(self, ctx):
        """The constructor of the window.

        :param ctx: The context of the application.
        :type ctx: ApplicationContext
        """
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("pyWatermark")
        self.setup_ui()
        self.color = self.DEFAULT_COLOR

    def setup_ui(self):
        """Setup the user interface of the application."""
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        """Create the widgets of the application."""
        self.lbl_type = QtWidgets.QLabel("Type:")
        self.cb_type = QtWidgets.QComboBox()

        self.lbl_text = QtWidgets.QLabel("Text:")
        self.le_text = QtWidgets.QLineEdit()
        self.lbl_font = QtWidgets.QLabel("Font:")
        self.cb_font = QtWidgets.QFontComboBox()
        self.lbl_size = QtWidgets.QLabel("Size:")
        self.spn_size = QtWidgets.QSpinBox()
        self.lbl_color = QtWidgets.QLabel("Color:")
        self.btn_color = QtWidgets.QPushButton()

        self.lbl_logo = QtWidgets.QLabel("Logo:")
        self.fbw_logo = FileBrowser()

        self.lbl_position = QtWidgets.QLabel("Position:")
        self.cb_position = QtWidgets.QComboBox()
        self.lbl_margin = QtWidgets.QLabel("Margin:")
        self.spn_margin = QtWidgets.QSpinBox()
        self.lbl_outputDir = QtWidgets.QLabel("Output Directory:")
        self.le_outputDir = QtWidgets.QLineEdit()
        self.lw_files = QtWidgets.QListWidget()
        self.btn_process = QtWidgets.QPushButton("Process")
        self.lbl_dropInfo = QtWidgets.QLabel("^ Drop your images on the UI")

    def modify_widgets(self):
        """Apply a CSS style sheet to the user interface of the application and modify the widgets."""
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        # Alignment
        # self.le_text.setAlignment(QtCore.Qt.AlignRight)
        # self.spn_size.setAlignment(QtCore.Qt.AlignRight)
        # self.spn_margin.setAlignment(QtCore.Qt.AlignRight)
        # self.le_outputDir.setAlignment(QtCore.Qt.AlignRight)

        # Range
        self.spn_size.setRange(1, 4000)
        self.spn_size.setValue(75)
        self.spn_margin.setRange(1, 4000)
        self.spn_margin.setValue(25)

        # Color button
        self.btn_color.setMaximumWidth(50)
        self.btn_color.setMaximumHeight(30)
        self.btn_color.setStyleSheet("background-color:%s;" % self.DEFAULT_COLOR)

        self.fbw_logo.btn_file_browser.setIcon(QtGui.QIcon(self.ctx.get_resource("images/folder.svg")))

        # Divers
        self.cb_type.addItems(["text", "image"])
        self.cb_type.setCurrentIndex(0)
        self.hide_logo_widgets()
        self.le_text.setPlaceholderText("Your watermark")
        self.le_text.setText("watermark")
        self.cb_font.setCurrentFont(QtGui.QFont("Arial"))
        self.cb_position.addItems(self.WATERMARK_POSITION)
        self.le_outputDir.setPlaceholderText("Output directory")
        self.le_outputDir.setText("output")
        self.lbl_dropInfo.setVisible(False)

        # Drag & Drop
        self.setAcceptDrops(True)

        # List widget
        self.lw_files.setAlternatingRowColors(True)
        self.lw_files.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)

    def create_layouts(self):
        """Create the grid layout of the user interface."""
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        """Add created widgets to the user interface layout."""
        self.main_layout.addWidget(self.lbl_type, 0, 0, 1, 1)
        self.main_layout.addWidget(self.cb_type, 0, 1, 1, 1)

        self.main_layout.addWidget(self.lbl_text, 1, 0, 1, 1)
        self.main_layout.addWidget(self.le_text, 1, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_font, 2, 0, 1, 1)
        self.main_layout.addWidget(self.cb_font, 2, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_size, 3, 0, 1, 1)
        self.main_layout.addWidget(self.spn_size, 3, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_color, 4, 0, 1, 1)
        self.main_layout.addWidget(self.btn_color, 4, 1, 1, 1)

        self.main_layout.addWidget(self.lbl_logo, 5, 0, 1, 1)
        self.main_layout.addWidget(self.fbw_logo, 5, 1, 1, 1)

        self.main_layout.addWidget(self.lbl_position, 6, 0, 1, 1)
        self.main_layout.addWidget(self.cb_position, 6, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_margin, 7, 0, 1, 1)
        self.main_layout.addWidget(self.spn_margin, 7, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_outputDir, 8, 0, 1, 1)
        self.main_layout.addWidget(self.le_outputDir, 8, 1, 1, 1)
        self.main_layout.addWidget(self.lw_files, 9, 0, 1, 2)
        self.main_layout.addWidget(self.lbl_dropInfo, 10, 0, 1, 2)
        self.main_layout.addWidget(self.btn_process, 11, 0, 1, 2)

    def setup_connections(self):
        """Setup the connections."""
        QtWidgets.QShortcut(QtGui.QKeySequence('Backspace'), self.lw_files, self.delete_selected_items)
        self.cb_type.currentIndexChanged.connect(self.show_type_widgets)
        self.btn_color.clicked.connect(self.set_color)
        self.btn_process.clicked.connect(self.process_images)

    def process_images(self):
        """Convert the images in the list using threading."""
        watermark_type = self.cb_type.currentText()
        text = self.le_text.text()
        font = self.get_font_path()
        size = int(self.spn_size.value())
        color = self.color
        folder = self.le_outputDir.text()
        logo = self.fbw_logo.get_file_path()
        position = self.cb_position.currentText()

        if logo is None:
            return False

        lw_items = [self.lw_files.item(index) for index in range(self.lw_files.count())]
        images_to_process = [1 for lw_item in lw_items if not lw_item.processed]
        if not images_to_process:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                            "No image to process",
                                            "All the images are processed.")
            msg_box.exec_()
            return False

        self.thread = QtCore.QThread(self)

        if watermark_type == "text":
            self.worker = Worker(images_to_process=lw_items, pos=position, wt_type="text", text=text, font=font,
                                 size=size, color=color, folder=folder)
        elif watermark_type == "image":
            self.worker = Worker(images_to_process=lw_items, pos=position,  wt_type="image", logo=logo, folder=folder)

        self.worker.moveToThread(self.thread)
        self.worker.image_processed.connect(self.image_processed)
        self.thread.started.connect(self.worker.process_images)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()

        self.prg_dialog = QtWidgets.QProgressDialog("Process images", "Cancel", 1, len(images_to_process))
        self.prg_dialog.canceled.connect(self.abort)
        self.prg_dialog.show()

    def abort(self):
        """Stop the thread."""
        self.thread.quit()
        self.worker.runs = False

    def image_processed(self, lw_item, success):
        """Update the image item icon and the progress bar.

        :param lw_item: The image item
        :param success: True if the image is converted else False
        :type lw_item: QWidgets.QListWidgetItem
        :type success: bool
        """
        if success:
            lw_item.setIcon(self.ctx.img_checked)
            lw_item.processed = True
            self.prg_dialog.setValue(self.prg_dialog.value() + 1)

    def delete_selected_items(self):
        """Remove selected image item from the list."""
        for lw_item in self.lw_files.selectedItems():
            row = self.lw_files.row(lw_item)
            self.lw_files.takeItem(row)

    def dragEnterEvent(self, event):
        """Overload the dragEnterEvent method.

        :param event: The event when the cursor enters in the UI.
        :type event: QtGui.QDragEnterEvent
        """
        self.lbl_dropInfo.setVisible(True)
        event.accept()

    def dragLeaveEvent(self, event):
        """Overload the dragLeaveEvent method.

        :param event: The event when the cursor leaves the UI.
        :type event: QtGui.QDragLeaveEvent
        """
        self.lbl_dropInfo.setVisible(False)

    def dropEvent(self, event):
        """Overload the dropEvent method.

        :param event: The event when the user drops files in the UI.
        :type event: QtGui.QDropEvent
        """
        event.accept()
        for url in event.mimeData().urls():
            self.add_file(path=url.toLocalFile())

        self.lbl_dropInfo.setVisible(False)

    def add_file(self, path):
        """Add an image file in the image list to process.

        :param path: The path of the image file.
        :type path: str
        """
        items = [self.lw_files.item(index).text() for index in range(self.lw_files.count())]
        if path not in items:
            lw_item = QtWidgets.QListWidgetItem(path)
            lw_item.setIcon(self.ctx.img_unchecked)
            lw_item.processed = False
            self.lw_files.addItem(lw_item)

    def set_color(self):
        """Set the background color of the color button.
        And the watermark text color.
        """
        self.color = QtWidgets.QColorDialog.getColor()
        if self.color.isValid():
            self.btn_color.setStyleSheet("background-color:%s;" % self.color.name())

    def get_font_path(self):
        """Get the path of the selected font.

        :return: The path of the selected font.
        :rtype: str
        """
        base_path = eval("QtCore.QStandardPaths().standardLocations(QtCore.QStandardPaths.FontsLocation)")
        font = self.cb_font.currentFont()

        font_path = os.path.join(base_path[0], font.family() + ".ttf")

        if os.path.exists(font_path):
            return font_path
        else:
            raise OSError(f"{font.family()} does not found : {font_path}")

    def hide_logo_widgets(self):
        """Hide image watermark widgets.
        """
        self.lbl_logo.hide()
        self.fbw_logo.hide()

    def show_logo_widgets(self):
        """Show image watermark widgets.
        """
        self.lbl_logo.show()
        self.fbw_logo.show()

    def hide_text_widgets(self):
        """Hide text watermark widgets.
        """
        self.lbl_text.hide()
        self.le_text.hide()
        self.lbl_font.hide()
        self.cb_font.hide()
        self.lbl_size.hide()
        self.spn_size.hide()
        self.lbl_color.hide()
        self.btn_color.hide()

    def show_text_widgets(self):
        """Show text watermark widgets.
        """
        self.lbl_text.show()
        self.le_text.show()
        self.lbl_font.show()
        self.cb_font.show()
        self.lbl_size.show()
        self.spn_size.show()
        self.lbl_color.show()
        self.btn_color.show()

    def show_type_widgets(self):
        """Show widgets corresponding to the selected watermark type.
        """
        if self.cb_type.currentText() == "text":
            self.hide_logo_widgets()
            self.show_text_widgets()
        elif self.cb_type.currentText() == "image":
            self.show_logo_widgets()
            self.hide_text_widgets()
