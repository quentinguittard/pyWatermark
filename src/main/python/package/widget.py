import os

from PySide2 import QtWidgets, QtCore, QtGui


class FileBrowser(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.le_file = QtWidgets.QLineEdit()
        self.btn_file_browser = QtWidgets.QPushButton("Browse")

    def create_layouts(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def add_widgets_to_layouts(self):
        self.layout.addWidget(self.le_file)
        self.layout.addWidget(self.btn_file_browser)

    def setup_connections(self):
        self.btn_file_browser.clicked.connect(self.get_file)

    def get_file(self):
        image_path = eval("QtCore.QStandardPaths().standardLocations(QtCore.QStandardPaths.PicturesLocation)")
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', image_path[0], "Image files (*.jpg *.png)")
        self.le_file.setText(path[0])
        self.file = path[0]

    def get_file_path(self):
        file_path = self.le_file.text()
        if os.path.exists(file_path):
            self.file = file_path
            return self.file
        else:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                            "Warning file not found",
                                            f"Warning : file path invalid : {file_path}")
            msg_box.exec_()
            return None


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = FileBrowser()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()