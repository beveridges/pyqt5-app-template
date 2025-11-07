# -*- coding: utf-8 -*-
"""
ui_initializer.py — minimal UI loader for MyApp Template
Adds File, Help menus and opens local rendered docs (like mvc_calculator)
"""

import os
import sys
import subprocess
import urllib.request
from urllib.parse import urljoin
from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5 import uic
from utilities.path_utils import base_path


class UIInitializer:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        # --- Load main UI ---
        uic.loadUi(base_path("uis", "main.ui"), self.main_window)
        mw = self.main_window

        # --- Menus ---
        mw.file_menu = mw.menuBar().addMenu("&File")
        mw.help_menu = mw.menuBar().addMenu("&Help")
        mw.menuBar().setStyleSheet("font-size: 10pt; font-family: 'Segoe UI';")

        # --- File actions ---
        mw.exitAction = QAction(QIcon(), "E&xit", mw)
        mw.exitAction.setShortcut(QKeySequence("Ctrl+Q"))
        mw.exitAction.triggered.connect(mw.close)
        mw.file_menu.addAction(mw.exitAction)

        # --- Help actions ---
        mw.aboutAction = QAction("&About", mw)
        mw.docsAction = QAction("&Documentation", mw)

        mw.help_menu.addAction(mw.docsAction)
        mw.help_menu.addAction(mw.aboutAction)

        mw.docsAction.triggered.connect(self.launch_help)
        mw.aboutAction.triggered.connect(self.show_about)

    # ----------------------------------------------------------------------
    def launch_help(self):
        """Open the rendered MkDocs help site (docs_site/site/index.html) — Chrome-preferred."""
        import subprocess
        import sys
        import os
        from pathlib import Path
        from PyQt5.QtWidgets import QMessageBox
    
        site_index = base_path("docs_site/site", "index.html")
    
        if not os.path.exists(site_index):
            QMessageBox.warning(
                self.main_window,
                "Help not found",
                f"Cannot find MkDocs help site at:\n{site_index}\n\n"
                "Run:\n\n    mkdocs build\n\n"
                "to generate it."
            )
            return
    
        file_url = Path(site_index).as_uri()
    
        try:
            # --- Prefer Google Chrome (exact same logic as mvc_calculator) ---
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
    
            chrome_exe = next((p for p in chrome_paths if os.path.exists(p)), None)
    
            if chrome_exe:
                subprocess.Popen([chrome_exe, file_url])
                return  # ✅ success → done
    
            # --- Fallback: default browser ---
            if sys.platform.startswith("win"):
                os.startfile(file_url)
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", file_url])
            else:
                subprocess.Popen(["xdg-open", file_url])
    
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"Could not open documentation:\n{e}")


    # ----------------------------------------------------------------------
    def show_about(self):
        QMessageBox.information(
            self.main_window,
            "About MyApp Template",
            "MyApp Template\nVersion 25.11-alpha.01\n\nCreated with PyQt5."
        )


def setup(main_window):
    """Convenience wrapper for app main window."""
    ui = UIInitializer(main_window)
    return ui
