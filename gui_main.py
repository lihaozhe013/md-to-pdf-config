import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from i18n import detect_system_lang, load_language


def main():
    load_language(detect_system_lang())

    app = QApplication(sys.argv)
    app.setApplicationName("md-to-pdf GUI")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
