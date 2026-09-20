import sys
from PySide6.QtWidgets import QApplication

from config import SOFTWARE_NAME, VERSION
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(SOFTWARE_NAME)
    app.setApplicationVersion(VERSION)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
