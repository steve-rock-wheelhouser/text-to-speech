#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   text_to_speech.py
#
#
# Copyright (C) 2025 steve.rock@wheelhouser.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# --- Setup Instructions ---
# Active the venv on linux/macOS:
# python -m venv .venv
# source .venv/bin/activate
# pip install --upgrade pip
# 
# .\.venv\Scripts\Activate.ps1
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# pip install -r requirements.txt
# pip install --force-reinstall -r requirements.txt
#
#===========================================================================================

import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                               QSpinBox, QFormLayout, QFrame, QMessageBox, QGridLayout, QSizePolicy)
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtCore import Qt, QEvent, QSettings

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller. """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # _MEIPASS not defined, so we are running in a normal Python environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#=====================================================================================================
# --- Dark Mode Stylesheet ---
#=====================================================================================================
DARK_STYLESHEET = """
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: "Segoe UI", "Arial", sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 5px;
            }
            QLabel#ImageLabel {
                border: 2px dashed #4A4B4C;
                background-color: #252627;
                min-height: 300px;
                min-width: 400px;
            }
            #header_widget {
                background-color: #1e1e1e;
                border-bottom: 1px solid #1e1e1e;
            }
            QPushButton {
                background-color: #323232;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
                icon-size: 0px;
            }
            QPushButton:hover {
                background-color: #424242;
                border: 1px solid #007AFF;
            }
            QPushButton:disabled {
                background-color: #1e1e1e;
                color: #555;
                border: 1px solid #333;
            }
            QSpinBox {
                min-width: 80px;
                padding: 5px;
                font-size: 14px;
            }

            /* Specific style for the 'About' button */
            QPushButton#aboutButton {
                background-color: transparent;
                border: none;
                padding: 4px 8px;
                color: #00BFFF;
            }
            /* Style for the 'About' button on mouse hover */
            QPushButton#aboutButton:hover {
                background-color: #444444;
                border: none;
                border-radius: 4px;
            }
            /* Style for the 'About' button when pressed */
            QPushButton#aboutButton:pressed {
                background-color: #333333;
                border: none;
            }
            /* GroupBox Styling */
            QGroupBox {
                border: 1px solid #1e1e1e;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: normal;
                color: #ddd;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px 0 3px;
            }

            /* CheckBox Styling */
            QCheckBox {
                spacing: 5px;
                color: #ccc;
            }
            /* Style for the checkbox indicator */
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }

            /* Style for the checkbox indicator when unchecked */
            QCheckBox::indicator:unchecked {
                background-color: #3E3E3E;
                border: 1px solid #555555;
                border-radius: 3px;
            }

            /* Style for the unchecked checkbox indicator on mouse hover */
            QCheckBox::indicator:unchecked:hover {
                border: 1px solid #007AFF;
            }

            /* Style for the checkbox indicator when checked */
            QCheckBox::indicator:checked {
                background-color: #007AFF;
                border: 1px solid #007AFF;
                border-radius: 3px;
                image: url("{css_icon_path}");
            }
"""

#=====================================================================================================
#--- Main Application Class ---
#=====================================================================================================
class TextToSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text to Speech Tool")
        self.setGeometry(100, 100, 1000, 750)
        
        # --- Prepare and set stylesheet with correct resource paths ---
        css_icon_path = resource_path(os.path.join("assets", "icons", "custom_checkmark.png")).replace(os.sep, '/')

        QApplication.instance().setStyleSheet(DARK_STYLESHEET.replace("{css_icon_path}", css_icon_path))
        
        # --- Set Window Icon using resource_path ---
        icon_path = resource_path(os.path.join("assets", "icons", "icon.ico"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.original_cv_image = None
        self.result_cv_image = None

        # --- Main Widget and Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- Top Control Bar ---
        top_bar_layout = QHBoxLayout()
        self.load_button = QPushButton("Load Image")
        #self.load_button.clicked.connect(self.load_image)

        self.save_button = QPushButton("Save Result")
        #self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        
        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.show_about_dialog)

        top_bar_layout.addWidget(self.load_button)
        top_bar_layout.addStretch()
        #top_bar_layout.addWidget(self.image_size_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.save_button)
        top_bar_layout.addWidget(self.about_button)
        main_layout.addLayout(top_bar_layout)

    def show_about_dialog(self):
        """Shows the about dialog."""
        about_dlg = QMessageBox(self)
        about_dlg.setWindowTitle("About Text To Speech")

        # Set the icon
        icon_path = resource_path(os.path.join("assets", "icons", "icon.png"))
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            about_dlg.setIconPixmap(pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        about_dlg.setTextFormat(Qt.RichText)
        about_dlg.setText("<h3>Text to Speech Tool</h3>")
        about_dlg.setInformativeText(
            "<div style='font-size: 14px; font-weight: normal;'>"
            "This application uses (TOOLS) to build out audio phrases.<br><br>"
            "Supported input/output formats: PNG, JPEG, BMP, TIFF, GIF<br><br>"
            "<span style='color: #00BFFF;'>"
            "Version 0.1.0<br>"
            "</span><br>"
            "© 2025 Wheelhouser LLC<br>"
            "Visit our website: <a href='https://wheelhouser.com' style='color: #00BFFF;'>wheelhouser.com</a>"
            "</div>"
        )
        about_dlg.setStandardButtons(QMessageBox.Ok)
        about_dlg.exec()


#=====================================================================================================
#--- Application Entry Point ---
#=====================================================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec())

