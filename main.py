# -*- coding: utf-8 -*-
"""
Minimal PyQt5 Application Template that uses ui_initializer
- Safe for PyInstaller builds (no early splash)
- Dynamic version banner (from config.defaults)
"""

import os, sys, time, logging
from logging.handlers import RotatingFileHandler
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QSplashScreen, QMainWindow, QMessageBox, QAction
from utilities.path_utils import base_path, resource_path

# --------------------------------------------------------------------------
# Version info (import from config)
# --------------------------------------------------------------------------
try:
    from config.defaults import FRIENDLYVERSIONNAME, BUILDNUMBER
except ImportError:
    FRIENDLYVERSIONNAME = "MyApp Template"
    BUILDNUMBER = "25.11-alpha.01"

# --------------------------------------------------------------------------
# Startup banner
# --------------------------------------------------------------------------
print(f"{FRIENDLYVERSIONNAME} {BUILDNUMBER} Portable version.")
print("Installing font cache — please wait...")
print("-" * 60)
sys.stdout.flush()

# --------------------------------------------------------------------------
# Logging (frozen-safe)
# --------------------------------------------------------------------------
if getattr(sys, "frozen", False):   
    LOG_DIR = os.path.join(os.environ.get("APPDATA", os.getcwd()), FRIENDLYVERSIONNAME.replace(" ", ""), "logs")
else:
    LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOGFILE = os.path.join(LOG_DIR, "app.log")

handler = RotatingFileHandler(LOGFILE, maxBytes=1_000_000, backupCount=3)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[handler, logging.StreamHandler(sys.stdout)]
)
logging.info("Logger initialized at %s", LOGFILE)

# --------------------------------------------------------------------------
# ui_initializer import
# --------------------------------------------------------------------------
import ui_initializer as gui


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(FRIENDLYVERSIONNAME)
        self.setWindowIcon(QIcon(base_path("resources/icons", "icon.png")))
        self.resize(900, 600)

        logging.info("Loading UI via ui_initializer.setup()")
        self.ui_initializer = gui.setup(self)

        if self.menuBar():
            self.menuBar().setNativeMenuBar(False)

        self._bind_menu_actions()
        logging.info("Main window ready")

    def _bind_menu_actions(self):
        def _get(name, cls):
            obj = self.findChild(cls, name)
            if obj is None:
                logging.debug("UI action '%s' not found (skipped)", name)
            return obj

        act_open  = _get("actionOpen",  QAction)
        act_exit  = _get("actionExit",  QAction)
        act_about = _get("actionAbout", QAction)

        if act_open:  act_open.triggered.connect(self._on_open)
        if act_exit:  act_exit.triggered.connect(self.close)
        if act_about: act_about.triggered.connect(self._on_about)

    def _on_open(self):
        QMessageBox.information(self, "Open", "Open action triggered (stub).")

    def _on_about(self):
        QMessageBox.information(
            self,
            "About",
            f"{FRIENDLYVERSIONNAME}\nVersion {BUILDNUMBER}\n\nA minimal PyQt5 template using ui_initializer."
        )

    def closeEvent(self, event):
        logging.info("Application closing...")
        super().closeEvent(event)


# --------------------------------------------------------------------------
# Main entrypoint
# --------------------------------------------------------------------------
def main():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    app = QtWidgets.QApplication(sys.argv)

    # ---------------- NORMAL SPLASH (safe for builds) ----------------
    splash_img = base_path("resources/icons", "splash.png")
    pix = QPixmap(splash_img)
    if pix.isNull():
        pix = QPixmap(400, 240)
        pix.fill(Qt.white)

    splash = QSplashScreen(pix)
    splash.setFont(QFont("Segoe UI", 10))
    splash.show()
    splash.showMessage(f"Starting {FRIENDLYVERSIONNAME}...", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
    app.processEvents()

    for msg, pct in [
        ("Loading resources", 20),
        ("Initializing UI", 50),
        ("Starting interface", 80),
    ]:
        splash.showMessage(f"{msg}... {pct}%", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
        app.processEvents()
        time.sleep(0.03)

    # ---------------- MAIN WINDOW ----------------
    win = ApplicationWindow()
    win.show()

    splash.showMessage("Ready", Qt.AlignBottom | Qt.AlignCenter, Qt.black)
    splash.finish(win)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
