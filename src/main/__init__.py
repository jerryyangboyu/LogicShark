import sys

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
import PySide6.QtCore
import Graph, Console, Component, Main

if __name__ == '__main__':
    app = QApplication(sys.argv)

    PySide6.QtCore.QDir.addSearchPath("icons", "resources")

    main_widget = Main.MainWindow()

    main_widget.setWindowTitle("Logic Shark")
    main_widget.show()

    sys.exit(app.exec())