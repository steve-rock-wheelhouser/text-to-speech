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
import json
import re
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QTextEdit,
                               QSpinBox, QMessageBox, QGridLayout, QGroupBox, QTabWidget, QInputDialog,
                               QScrollArea, QRadioButton, QButtonGroup, QListWidget, QAbstractItemView, QListView, QLineEdit,
                               QSizePolicy)
from PySide6.QtGui import QPixmap, QIcon, QPalette, QColor
from PySide6.QtCore import Qt, QThread, Signal, QSettings, QPoint, QTimer

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
            /* Main Window and general widgets */
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: "Segoe UI", "Arial", sans-serif;
                font-size: 14px;
            }
            /* General Labels */
            QLabel {
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 5px;
            }
            /* Label for Image Display */
            QLabel#ImageLabel {
                border: 2px dashed #4A4B4C;
                background-color: #252627;
                min-height: 300px;
                min-width: 400px;
            }
            /* Path Labels */
            QLabel#PathLabel {
                color: #00BFFF;
                font-weight: normal;
            }
            #header_widget {
                background-color: #1e1e1e;
                border-bottom: 1px solid #1e1e1e;
            }
            /* Buttons and Inputs */
            QPushButton {
                background-color: #323232;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 6px;
                icon-size: 0px;
            }
            /* Button Hover State */
            QPushButton:hover {
                background-color: #424242;
                border: 1px solid #007AFF;
            }
            /* Button Disabled State */
            QPushButton:disabled {
                background-color: #1e1e1e;
                color: #555555;
                border: 1px solid #333333;
            }
            /* Audio Control SpinBoxes */
            QSpinBox {
                min-width: 80px;
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
                color: #dddddd;
            }

            /* Title Styling */
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px 0 3px;
            }

            /* CheckBox Styling */
            QCheckBox {
                spacing: 5px;
                color: #cccccc;
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

            /* Radio Button Styling */
            QRadioButton {
                spacing: 8px;
                color: #ffffff;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
                border-radius: 2px;
                border: 1px solid #555555;
                background-color: #252627;
            }
            QRadioButton::indicator:checked {
                background-color: #007AFF;
                border: 1px solid #007AFF;
                image: url("{css_icon_path}");
            }
            QRadioButton::indicator:hover {
                border: 1px solid #007AFF;
            }
            /* Text Input Area */
            QTextEdit {
                background-color: #252627;
                border: 1px solid #555555;
            }

            /*default frame of the QScrollArea widget that holds the content of the "General" tab*/
            QScrollArea {
                border: none;
            }

            /* Tab Widget Styling */
            QTabWidget::pane {
                border-top: 1px solid #555555;
                margin-top: -1px;
            }
            QTabBar::tab {
                background-color: #252627;
                border: 1px solid #555555;
                padding: 8px 20px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:!selected {
                margin-top: 2px; /* Make non-selected tabs look smaller */
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e; /* Same as window background */
                border-bottom-color: #1e1e1e; /* Seamless with pane */
            }
            QTabBar::tab:hover {
                background-color: #424242;
            }

            /* Voice Selection ComboBox and Local Styles */
            QComboBox {
                background-color: #323232;
                border: 1px solid #555555;
                border-radius: 2px;
                padding: 4px;
            }
            QComboBox:hover {
                border: 1px solid #007AFF;
            }
            
            QComboBox QAbstractItemView {
                background-color: #191919;
                color: white;
                selection-background-color: #2A82DA;
                outline: 0px;
                border: 1px solid #555555;
            }
            
            /* Vertical ScrollBar Style */
            QScrollBar:vertical {
                border: none;
                background: #191919;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #505050;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
"""

#=====================================================================================================
#--- Helper Functions & Constants (Ported from save_character.py) ---
#=====================================================================================================
# Offsets relative to the "Calm" (Baseline) settings
# Format: (Rate Offset %, Pitch Offset Hz, Volume Offset %, Style)
VARIATION_TEMPLATES = {
    "Calm":         (0, 0, 0, "general"),
    "Excited":      (10, 2, 25, "cheerful"),
    "Stressed":     (10, 5, 10, "unfriendly"),
    "Whisper":      (-10, 0, -90, "whispering"),
    "Angry":        (15, 0, 50, "angry"),
    "Loud":         (0, 0, 30, "shouting"),
    "Depressed":    (-15, -5, -10, "sad"),
    "Frustrated":   (5, 5, 10, "unfriendly"),
    "Happy":        (10, 5, 5, "cheerful"),
    "Inside Voice": (-5, -5, -40, "general"),
    "Desperate":    (20, 15, 25, "terrified")
}

# Map of language codes to full names
LANGUAGE_NAMES = {
    "af": "Afrikaans", "am": "Amharic", "ar": "Arabic", "az": "Azerbaijani",
    "bg": "Bulgarian", "bn": "Bengali", "bs": "Bosnian", "ca": "Catalan",
    "cs": "Czech", "cy": "Welsh", "da": "Danish", "de": "German",
    "el": "Greek", "en": "English", "es": "Spanish", "et": "Estonian",
    "fa": "Persian", "fi": "Finnish", "fil": "Filipino", "fr": "French",
    "ga": "Irish", "gl": "Galician", "gu": "Gujarati", "he": "Hebrew",
    "hi": "Hindi", "hr": "Croatian", "hu": "Hungarian", "id": "Indonesian",
    "is": "Icelandic", "it": "Italian", "iu": "Inuktitut", "ja": "Japanese",
    "jv": "Javanese", "ka": "Georgian", "kk": "Kazakh", "km": "Khmer",
    "kn": "Kannada", "ko": "Korean", "lo": "Lao", "lt": "Lithuanian",
    "lv": "Latvian", "mk": "Macedonian", "ml": "Malayalam", "mn": "Mongolian",
    "mr": "Marathi", "ms": "Malay", "mt": "Maltese", "my": "Burmese",
    "nb": "Norwegian Bokmål", "ne": "Nepali", "nl": "Dutch", "pl": "Polish",
    "ps": "Pashto", "pt": "Portuguese", "ro": "Romanian", "ru": "Russian",
    "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian", "so": "Somali",
    "sq": "Albanian", "sr": "Serbian", "su": "Sundanese", "sv": "Swedish",
    "sw": "Swahili", "ta": "Tamil", "te": "Telugu", "th": "Thai",
    "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu", "uz": "Uzbek",
    "vi": "Vietnamese", "zh": "Chinese", "zu": "Zulu"
}

# Map of country codes to full names
COUNTRY_NAMES = {
    "AF": "Afghanistan", "AL": "Albania", "DZ": "Algeria", "AR": "Argentina",
    "AU": "Australia", "AT": "Austria", "AZ": "Azerbaijan", "BH": "Bahrain",
    "BD": "Bangladesh", "BE": "Belgium", "BO": "Bolivia",
    "BA": "Bosnia and Herzegovina", "BR": "Brazil", "BG": "Bulgaria", "MM": "Myanmar",
    "CA": "Canada", "CL": "Chile", "CN": "China", "CO": "Colombia",
    "CR": "Costa Rica", "HR": "Croatia", "CU": "Cuba", "CZ": "Czech Republic",
    "DK": "Denmark", "DO": "Dominican Republic", "EC": "Ecuador", "EG": "Egypt",
    "SV": "El Salvador", "GQ": "Equatorial Guinea", "EE": "Estonia", "ET": "Ethiopia",
    "FI": "Finland", "FR": "France", "GE": "Georgia", "DE": "Germany",
    "GR": "Greece", "GT": "Guatemala", "HN": "Honduras", "HK": "Hong Kong SAR",
    "HU": "Hungary", "IS": "Iceland", "IN": "India", "ID": "Indonesia",
    "IR": "Iran", "IQ": "Iraq", "IE": "Ireland", "IL": "Israel",
    "IT": "Italy", "JP": "Japan", "JO": "Jordan", "KZ": "Kazakhstan",
    "KE": "Kenya", "KH": "Cambodia", "KR": "South Korea", "KW": "Kuwait",
    "LA": "Laos", "LV": "Latvia", "LB": "Lebanon", "LY": "Libya",
    "LT": "Lithuania", "MK": "North Macedonia", "MY": "Malaysia", "MT": "Malta",
    "MX": "Mexico", "MN": "Mongolia", "MA": "Morocco", "NP": "Nepal",
    "NL": "Netherlands", "NZ": "New Zealand", "NI": "Nicaragua", "NG": "Nigeria",
    "NO": "Norway", "OM": "Oman", "PK": "Pakistan", "PA": "Panama",
    "PY": "Paraguay", "PE": "Peru", "PH": "Philippines", "PL": "Poland",
    "PT": "Portugal", "PR": "Puerto Rico", "QA": "Qatar", "RO": "Romania",
    "RU": "Russia", "SA": "Saudi Arabia", "RS": "Serbia",
    "SG": "Singapore", "SK": "Slovakia", "SI": "Slovenia", "SO": "Somalia",
    "ZA": "South Africa", "ES": "Spain", "LK": "Sri Lanka", "SE": "Sweden",
    "CH": "Switzerland", "SY": "Syria", "TW": "Taiwan", "TZ": "Tanzania",
    "TH": "Thailand", "TN": "Tunisia", "TR": "Turkey",
    "UA": "Ukraine", "AE": "United Arab Emirates", "GB": "United Kingdom", "US": "United States",
    "UY": "Uruguay", "UZ": "Uzbekistan", "VE": "Venezuela", "VN": "Vietnam",
    "YE": "Yemen"
}

def parse_val(s):
    """Parses a string like '+10%' or '-5Hz' into (number, unit)."""
    if not s:
        return 0, ""
    m = re.match(r"([+-]?\d+)(.*)", s)
    if m:
        return int(m.group(1)), m.group(2)
    return 0, ""

def apply_offset(base_s, offset):
    """Applies an integer offset to a value string."""
    val, unit = parse_val(base_s)
    new_val = val + offset
    sign = "+" if new_val >= 0 else ""
    return f"{sign}{new_val}{unit}"

#=====================================================================================================
#--- Custom Widgets ---
#=====================================================================================================
class LimitedComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setView(QListView())

    def showPopup(self):
        super().showPopup()
        popup = self.view().window()

        # --- Calculate Height ---
        rect = self.view().visualRect(self.view().model().index(0, 0))
        row_height = rect.height() if rect.height() > 0 else self.view().fontMetrics().lineSpacing()
        max_items = 15
        items_to_show = min(self.count(), max_items)
        total_height = (items_to_show * row_height) + 4

        # --- Calculate Position ---
        # Get the point for the top-left of the popup, which is the bottom-left of the combo box
        point = self.mapToGlobal(QPoint(0, self.height()))

        # Get current popup geometry to preserve width
        current_geo = popup.geometry()
        popup.setGeometry(point.x(), point.y(), current_geo.width(), total_height)

#=====================================================================================================
#--- Worker Thread ---
#=====================================================================================================
class GenerationWorker(QThread):
    finished = Signal(bool, str)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self.process = None
        self._is_running = True

    def run(self):
        try:
            # Use Popen to have control over the process
            self.process = subprocess.Popen(
                self.cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                # Hide console window on Windows
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            stdout, stderr = self.process.communicate()

            # If stop() was called, _is_running will be False.
            if not self._is_running:
                self.finished.emit(True, "Operation cancelled by user.")
                return

            if self.process.returncode == 0:
                self.finished.emit(True, "")
            else:
                self.finished.emit(False, stderr or stdout or f"Process failed with return code {self.process.returncode}")
        
        except Exception as e:
            if self._is_running:
                self.finished.emit(False, str(e))

    def stop(self):
        self._is_running = False
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.process.kill()
#=====================================================================================================
#--- Playback Worker Thread ---
#=====================================================================================================
class PlaybackWorker(QThread):
    def __init__(self, files):
        super().__init__()
        self.files = files
        self.current_process = None
        self.is_running = True

    def run(self):
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "play_audio.py")
        for file_path in self.files:
            if not self.is_running:
                break
            try:
                self.current_process = subprocess.Popen(
                    [sys.executable, script_path, file_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.current_process.wait()
            except Exception:
                pass

    def stop(self):
        self.is_running = False
        if self.current_process and self.current_process.poll() is None:
            self.current_process.terminate()

#=====================================================================================================
#--- Main Application Class ---
#=====================================================================================================
class TextToSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize Settings
        self.settings = QSettings("Wheelhouser", "TextToSpeech")

        self.setWindowTitle("Text to Speech Tool")
        self.setGeometry(100, 100, 900, 700)
        
        # --- Set Window Icon using resource_path ---
        icon_path = resource_path(os.path.join("assets", "icons", "icon.ico"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # --- Main Tabs ---
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tab 1: General (Manual Controls)
        self.general_tab = QWidget()
        self.setup_general_tab()
        self.tabs.addTab(self.general_tab, "General")

        # Tab 2: Characters (Library)
        self.char_tab = QWidget()
        self.setup_char_tab()
        self.tabs.addTab(self.char_tab, "Characters")

        # Tab 3: Playback
        self.playback_tab = QWidget()
        self.setup_playback_tab()
        self.tabs.addTab(self.playback_tab, "Playback")

        # Data storage
        self.characters_data = []
        self.all_voices = []
        self.language_map = {}

        # Load Data
        self.load_voices()
        self.load_characters()
        
        self.worker = None
        self.playback_worker = None
        
        # Restore playback folder
        self.current_playback_folder = self.settings.value("last_playback_dir", "")
        if self.current_playback_folder and os.path.exists(self.current_playback_folder):
            self.folder_label.setText(self.current_playback_folder)
            self.refresh_file_list()
        else:
            self.current_playback_folder = ""

        # Timer for auto-saving variation changes
        self.variation_update_timer = QTimer(self)
        self.variation_update_timer.setSingleShot(True)
        self.variation_update_timer.setInterval(750)  # 750ms delay after last change
        self.variation_update_timer.timeout.connect(self._perform_variation_update)

    def setup_general_tab(self):
        # Main layout for the tab
        tab_layout = QVBoxLayout(self.general_tab)
        
        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        tab_layout.addWidget(scroll_area)
        
        # Content Widget inside Scroll Area
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        
        layout = QVBoxLayout(content_widget)
        
        # --- Top Control Bar ---
        top_bar_layout = QHBoxLayout()
        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.show_about_dialog)
        
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.about_button)
        layout.addLayout(top_bar_layout)
        
        # --- Voice Selection ---
        voice_group = QGroupBox("Voice Settings")
        voice_layout = QVBoxLayout()
        
        # Gender Filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Gender:"))
        self.gender_group = QButtonGroup(self)
        self.radio_all = QRadioButton("All")
        self.radio_male = QRadioButton("Male")
        self.radio_female = QRadioButton("Female")
        self.radio_all.setChecked(True)
        
        self.gender_group.addButton(self.radio_all)
        self.gender_group.addButton(self.radio_male)
        self.gender_group.addButton(self.radio_female)
        self.gender_group.buttonClicked.connect(lambda _: self.update_voice_list())
        
        filter_layout.addWidget(self.radio_all)
        filter_layout.addWidget(self.radio_male)
        filter_layout.addWidget(self.radio_female)
        
        # Language Filter
        filter_layout.addSpacing(15)
        filter_layout.addWidget(QLabel("Language:"))
        self.language_filter_combo = LimitedComboBox()
        self.language_filter_combo.addItem("All")
        self.language_filter_combo.currentIndexChanged.connect(self.on_language_changed)
        filter_layout.addWidget(self.language_filter_combo)

        # Country Filter
        filter_layout.addSpacing(15)
        filter_layout.addWidget(QLabel("Country:"))
        self.country_filter_combo = LimitedComboBox()
        self.country_filter_combo.addItem("All")
        self.country_filter_combo.currentIndexChanged.connect(lambda: self.update_voice_list())
        filter_layout.addWidget(self.country_filter_combo)
        
        filter_layout.addStretch()
        voice_layout.addLayout(filter_layout)
        
        self.voice_combo = LimitedComboBox()
        
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("Select Voice:"))
        combo_layout.addWidget(self.voice_combo)
        combo_layout.addStretch()
        voice_layout.addLayout(combo_layout)
        
        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)

        # --- Text Input ---
        text_group = QGroupBox("Input Text")
        text_layout = QVBoxLayout()
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter the text you want to convert to speech here...")
        text_layout.addWidget(self.text_input)
        text_group.setLayout(text_layout)
        layout.addWidget(text_group, 1)

        # --- Audio Controls ---
        controls_group = QGroupBox("Audio Controls")
        controls_layout = QHBoxLayout()

        # Pitch
        self.pitch_spin = QSpinBox()
        self.pitch_spin.setRange(-100, 100)
        self.pitch_spin.setSuffix(" Hz")
        self.pitch_spin.setValue(0)
        controls_layout.addWidget(QLabel("Pitch:"))
        controls_layout.addWidget(self.pitch_spin)

        # Rate
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(-100, 100)
        self.rate_spin.setSuffix(" %")
        self.rate_spin.setValue(0)
        controls_layout.addWidget(QLabel("Rate:"))
        controls_layout.addWidget(self.rate_spin)

        # Volume
        self.vol_spin = QSpinBox()
        self.vol_spin.setRange(-100, 100)
        self.vol_spin.setSuffix(" %")
        self.vol_spin.setValue(0)
        controls_layout.addWidget(QLabel("Volume:"))
        controls_layout.addWidget(self.vol_spin)

        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)

        # --- Action Buttons ---
        action_layout = QHBoxLayout()
        self.preview_btn = QPushButton("Preview (Play)")
        self.preview_btn.setMinimumHeight(40)
        self.preview_btn.clicked.connect(lambda: self.preview_audio(mode="general"))
        
        self.save_btn = QPushButton("Save to File...")
        self.save_btn.setMinimumHeight(40)
        self.save_btn.clicked.connect(lambda: self.save_audio(mode="general"))
        
        self.create_char_btn = QPushButton("Create Character")
        self.create_char_btn.setMinimumHeight(40)
        self.create_char_btn.clicked.connect(self.create_character)

        action_layout.addWidget(self.preview_btn)
        action_layout.addWidget(self.save_btn)
        action_layout.addWidget(self.create_char_btn)
        layout.addLayout(action_layout)

    def setup_char_tab(self):
        layout = QVBoxLayout(self.char_tab)

        # --- Selection Area ---
        sel_group = QGroupBox("Character Selection")
        sel_layout = QGridLayout()
        
        self.char_combo = LimitedComboBox()
        self.char_combo.currentIndexChanged.connect(self.on_character_changed) # This will trigger on_variation_changed
        self.var_combo = LimitedComboBox()
        self.var_combo.currentIndexChanged.connect(self.on_variation_changed)
        
        sel_layout.addWidget(QLabel("Character:"), 0, 0)
        sel_layout.addWidget(self.char_combo, 0, 1)
        sel_layout.addWidget(QLabel("Variation:"), 1, 0)
        sel_layout.addWidget(self.var_combo, 1, 1)
        sel_layout.setColumnStretch(2, 1)
        
        sel_group.setLayout(sel_layout)
        layout.addWidget(sel_group)

        # --- Info Area ---
        self.char_desc_label = QLabel("Description: ")
        self.char_desc_label.setWordWrap(True)
        self.char_desc_label.setStyleSheet("color: #aaa; font-style: italic; margin-bottom: 10px;")
        layout.addWidget(self.char_desc_label)

        # --- Variation Controls ---
        var_controls_group = QGroupBox("Variation Settings")
        var_controls_layout = QHBoxLayout()

        # Pitch
        self.char_pitch_spin = QSpinBox()
        self.char_pitch_spin.setRange(-100, 100)
        self.char_pitch_spin.setSuffix(" Hz")
        var_controls_layout.addWidget(QLabel("Pitch:"))
        var_controls_layout.addWidget(self.char_pitch_spin)

        # Rate
        self.char_rate_spin = QSpinBox()
        self.char_rate_spin.setRange(-100, 100)
        self.char_rate_spin.setSuffix(" %")
        var_controls_layout.addWidget(QLabel("Rate:"))
        var_controls_layout.addWidget(self.char_rate_spin)
        
        # Volume
        self.char_vol_spin = QSpinBox()
        self.char_vol_spin.setRange(-100, 100)
        self.char_vol_spin.setSuffix(" %")
        var_controls_layout.addWidget(QLabel("Volume:"))
        var_controls_layout.addWidget(self.char_vol_spin)

        self.char_pitch_spin.valueChanged.connect(self.schedule_variation_update)
        self.char_rate_spin.valueChanged.connect(self.schedule_variation_update)
        self.char_vol_spin.valueChanged.connect(self.schedule_variation_update)
        var_controls_group.setLayout(var_controls_layout)
        layout.addWidget(var_controls_group)

        # --- Text Input ---
        text_group = QGroupBox("Lines")
        text_layout = QVBoxLayout()
        self.char_text_input = QTextEdit()
        self.char_text_input.setPlaceholderText("Character lines...")
        text_layout.addWidget(self.char_text_input)
        text_group.setLayout(text_layout)
        layout.addWidget(text_group, 1)

        # --- Action Buttons ---
        action_layout = QHBoxLayout()
        self.char_preview_btn = QPushButton("Preview (Play)")
        self.char_preview_btn.setMinimumHeight(40)
        self.char_preview_btn.clicked.connect(lambda: self.preview_audio(mode="character"))
        
        self.char_save_btn = QPushButton("Save to File...")
        self.char_save_btn.setMinimumHeight(40)
        self.char_save_btn.clicked.connect(lambda: self.save_audio(mode="character"))
        
        self.delete_char_btn = QPushButton("Delete Character")
        self.delete_char_btn.setMinimumHeight(40)
        self.delete_char_btn.clicked.connect(self.delete_character)

        action_layout.addWidget(self.char_preview_btn)
        action_layout.addWidget(self.char_save_btn)
        action_layout.addWidget(self.delete_char_btn)
        layout.addLayout(action_layout)

    def setup_playback_tab(self):
        layout = QVBoxLayout(self.playback_tab)
        
        # Top bar
        top_layout = QHBoxLayout()
        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.clicked.connect(self.open_playback_folder)
        self.folder_label = QLabel("No folder selected")
        self.folder_label.setObjectName("PathLabel")
        top_layout.addWidget(self.open_folder_btn)
        top_layout.addWidget(self.folder_label, 1)
        layout.addLayout(top_layout)
        
        # List
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.file_list.itemDoubleClicked.connect(self.play_single_item)
        layout.addWidget(self.file_list)
        
        # Controls
        ctrl_layout = QHBoxLayout()
        self.play_selected_btn = QPushButton("Play Selected")
        self.play_selected_btn.clicked.connect(self.play_selected)
        
        self.play_all_btn = QPushButton("Play All")
        self.play_all_btn.clicked.connect(self.play_all)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_playback)
        
        ctrl_layout.addWidget(self.play_selected_btn)
        ctrl_layout.addWidget(self.play_all_btn)
        ctrl_layout.addWidget(self.stop_btn)
        layout.addLayout(ctrl_layout)

    def open_playback_folder(self):
        last_dir = self.settings.value("last_playback_dir", "")
        folder = QFileDialog.getExistingDirectory(self, "Select Audio Folder", last_dir)
        if folder:
            self.settings.setValue("last_playback_dir", folder)
            self.current_playback_folder = folder
            self.folder_label.setText(folder)
            self.refresh_file_list()

    def refresh_file_list(self):
        self.file_list.clear()
        if not self.current_playback_folder:
            return
            
        exts = ('.mp3', '.wav', '.ogg', '.m4a')
        try:
            files = [f for f in os.listdir(self.current_playback_folder) 
                     if f.lower().endswith(exts)]
            files.sort()
            self.file_list.addItems(files)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to list files: {e}")

    def play_single_item(self, item):
        self.start_playback([item.text()])

    def play_selected(self):
        items = self.file_list.selectedItems()
        if not items:
            return
        files = [i.text() for i in items]
        self.start_playback(files)

    def play_all(self):
        count = self.file_list.count()
        if count == 0:
            return
        files = [self.file_list.item(i).text() for i in range(count)]
        self.start_playback(files)

    def start_playback(self, filenames):
        if self.playback_worker and self.playback_worker.isRunning():
            self.playback_worker.stop()
            self.playback_worker.wait()
            
        full_paths = [os.path.join(self.current_playback_folder, f) for f in filenames]
        self.playback_worker = PlaybackWorker(full_paths)
        self.playback_worker.start()

    def stop_playback(self):
        # Stop playback from the Playback tab
        if self.playback_worker and self.playback_worker.isRunning():
            self.playback_worker.stop()
        
        # Also stop any active generation/preview from other tabs
        if self.worker and self.worker.isRunning():
            self.worker.stop()
    def on_language_changed(self):
        """Updates the country filter when the language changes."""
        selected_language_code = self.language_filter_combo.currentData()
        
        self.country_filter_combo.blockSignals(True)
        self.country_filter_combo.clear()
        self.country_filter_combo.addItem("All")
        
        if selected_language_code and selected_language_code in self.language_map:
            country_codes = self.language_map.get(selected_language_code, [])
            
            country_list = []
            for code in country_codes:
                name = COUNTRY_NAMES.get(code, code)
                country_list.append((name, code))
            
            country_list.sort(key=lambda x: x[0])

            for name, code in country_list:
                self.country_filter_combo.addItem(name, code)
            self.country_filter_combo.setEnabled(True)
        else:
            # If "All" languages, disable country filter as it's not meaningful
            self.country_filter_combo.setEnabled(False)
            
        self.country_filter_combo.blockSignals(False)
        
        # Trigger an update of the voice list
        self.update_voice_list()

    def load_voices(self):
        """Loads voices from voices.json."""
        # Look in src/ or project root
        paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "voices.json"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "voices.json")
        ]
        
        voices = []
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, 'r', encoding='utf-8') as f:
                        voices = json.load(f)
                    break
                except Exception as e:
                    print(f"Failed to load voices from {p}: {e}")
        
        if not voices:
            self.voice_combo.addItem("Error: voices.json not found")
            self.voice_combo.setEnabled(False)
            return
        
        # Process locales to build language and country maps
        for v in voices:
            locale = v.get("Locale")
            if not locale:
                continue
            parts = locale.split('-')
            if len(parts) >= 1:
                lang = parts[0]
                country = None
                # Find the country code, which is usually a 2-letter uppercase string
                for part in parts[1:]:
                    if len(part) == 2 and part.isupper():
                        country = part
                        break
                
                if not country:
                    continue

                if lang not in self.language_map:
                    self.language_map[lang] = set()
                self.language_map[lang].add(country)

        # Convert sets to sorted lists
        for lang in self.language_map:
            self.language_map[lang] = sorted(list(self.language_map[lang]))

        # Populate Language Filter
        language_list = []
        for code in self.language_map.keys():
            name = LANGUAGE_NAMES.get(code, code)
            language_list.append((name, code))
        
        language_list.sort(key=lambda x: x[0])

        self.language_filter_combo.blockSignals(True)
        self.language_filter_combo.clear()
        self.language_filter_combo.addItem("All")
        for name, code in language_list:
            self.language_filter_combo.addItem(name, code)
        self.language_filter_combo.blockSignals(False)

        # Sort voices by ID
        voices.sort(key=lambda x: x.get("ID", 0))
        self.all_voices = voices
        
        # Set initial state of country combo and trigger initial voice list update
        self.on_language_changed()
    
    def format_voice_display_name(self, voice_data):
        """Formats the voice data into a user-friendly display name."""
        voice_id = voice_data.get("ID", "?")
        short_name = voice_data.get("ShortName", "Unknown")
        locale = voice_data.get("Locale", "")
        gender = voice_data.get("Gender", "")

        # 1. Extract name from ShortName
        # Example: en-US-AndrewNeural -> Andrew
        # Example: zh-CN-liaoning-XiaobeiNeural -> Xiaobei
        name_part = short_name.split('-')[-1]
        if name_part.endswith("Neural"):
            name_part = name_part[:-6]
        # Split CamelCase: e.g., HsiaoChen -> Hsiao Chen
        person_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name_part)

        # 2. Extract language and country from Locale
        lang_code = ""
        country_code = ""
        locale_parts = locale.split('-')
        if len(locale_parts) >= 1:
            lang_code = locale_parts[0]
        
        # Find the country code, which is usually a 2-letter uppercase string
        for part in locale_parts[1:]:
            if len(part) == 2 and part.isupper():
                country_code = part
                break
        
        lang_name = LANGUAGE_NAMES.get(lang_code, lang_code)
        country_name = COUNTRY_NAMES.get(country_code, "") # Return empty string if not found

        # 3. Construct display string
        details_parts = []
        if gender:
            details_parts.append(gender)
        if country_name:
            details_parts.append(country_name)
        if lang_name:
            details_parts.append(lang_name)
        
        details_str = " - ".join(details_parts)

        return f"{voice_id} \t {person_name} \t ({details_str})"

    def update_voice_list(self):
        """Filters and populates the voice combo box."""
        self.voice_combo.clear()
        
        filter_gender = "All"
        if self.radio_male.isChecked():
            filter_gender = "Male"
        if self.radio_female.isChecked():
            filter_gender = "Female"
            
        filter_language_code = self.language_filter_combo.currentData()
        filter_country_code = self.country_filter_combo.currentData()

        for v in self.all_voices:
            if filter_gender != "All" and v.get("Gender") != filter_gender:
                continue
            
            locale = v.get("Locale", "")

            # Filter by language, then by country
            if filter_language_code and filter_language_code != "All":
                if not locale.startswith(filter_language_code + '-'):
                    continue
                if filter_country_code and filter_country_code != "All" and f"-{filter_country_code}" not in locale:
                    continue

            display_text = self.format_voice_display_name(v)
            self.voice_combo.addItem(display_text, v.get("ShortName"))

    def load_characters(self):
        """Loads characters from characters.json."""
        # Path relative to src/ or project root
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "voice-library", "characters.json")
        
        if not os.path.exists(path):
            self.char_combo.addItem("Error: characters.json not found")
            self.char_combo.setEnabled(False)
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.characters_data = json.load(f)
        except Exception as e:
            print(f"Failed to load characters: {e}")
            return

        # Sort characters by ReferenceID
        self.characters_data.sort(key=lambda x: x.get("ReferenceID", 0))

        self.char_combo.clear()
        for char in self.characters_data:
            alias = char.get("Alias", "Unknown")
            self.char_combo.addItem(alias, char)

        # Trigger update for first item
        if self.characters_data:
            self.on_character_changed(0)

    def create_character(self):
        """Creates a new character based on current General tab settings."""
        # 1. Get Basic Info
        alias_dialog = QInputDialog(self)
        alias_dialog.setWindowTitle("Create Character")
        alias_dialog.setLabelText("Character Alias (e.g. 'Yoda'):")
        alias_dialog.setInputMode(QInputDialog.TextInput)
        
        # Find the QLineEdit and set its minimum width to accommodate ~64 characters
        line_edit = alias_dialog.findChild(QLineEdit)
        if line_edit:
            font_metrics = line_edit.fontMetrics()
            line_edit.setMinimumWidth(font_metrics.averageCharWidth() * 64)

        ok = alias_dialog.exec()
        alias = alias_dialog.textValue()
        if not ok or not alias.strip():
            return
        
        desc_dialog = QInputDialog(self)
        desc_dialog.setWindowTitle("Create Character")
        desc_dialog.setLabelText("Description:")
        desc_dialog.setInputMode(QInputDialog.TextInput)

        # Find the QLineEdit and set its minimum width
        line_edit = desc_dialog.findChild(QLineEdit)
        if line_edit:
            font_metrics = line_edit.fontMetrics()
            line_edit.setMinimumWidth(font_metrics.averageCharWidth() * 64)

        ok = desc_dialog.exec()
        desc = desc_dialog.textValue()
        if not ok:
            return

        # 2. Get Current Settings
        voice_shortname = self.voice_combo.currentData()
        if not voice_shortname:
            QMessageBox.warning(self, "Error", "No voice selected.")
            return

        pitch_str = f"{self.pitch_spin.value():+d}Hz"
        rate_str = f"{self.rate_spin.value():+d}%"
        vol_str = f"{self.vol_spin.value():+d}%"
        sample_text = self.text_input.toPlainText().strip() or "Hello, I am ready to speak."

        # 3. Find Full Voice Data (Need ID, Gender, Locale)
        paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "voices.json"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "voices.json")
        ]
        voice_data = None
        for p in paths:
            if os.path.exists(p):
                try:
                    with open(p, 'r', encoding='utf-8') as f:
                        voices = json.load(f)
                        voice_data = next((v for v in voices if v.get("ShortName") == voice_shortname), None)
                    if voice_data:
                        break
                except Exception:
                    pass
        
        if not voice_data:
            QMessageBox.critical(self, "Error", "Could not find voice details in voices.json.")
            return

        # 4. Load Library to determine ID
        lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "voice-library", "characters.json")
        library = []
        if os.path.exists(lib_path):
            try:
                with open(lib_path, 'r', encoding='utf-8') as f:
                    library = json.load(f)
            except Exception: 
                pass

        next_id = 1
        if library:
            next_id = max((c.get("ReferenceID", 0) for c in library), default=0) + 1

        # 5. Generate Variations
        variations = {}
        for name, (rate_off, pitch_off, vol_off, style) in VARIATION_TEMPLATES.items():
            variations[name] = {
                "Rate": apply_offset(rate_str, rate_off),
                "Pitch": apply_offset(pitch_str, pitch_off),
                "Volume": apply_offset(vol_str, vol_off),
                "Style": style,
                "Image": ""
            }

        # 6. Construct Object
        new_character = {
            "ReferenceID": next_id,
            "Alias": alias,
            "Engine": "edge-tts",
            "VoiceID": voice_data.get("ID", 0),
            "ShortName": voice_data.get("ShortName"),
            "Gender": voice_data.get("Gender"),
            "Locale": voice_data.get("Locale"),
            "Description": desc,
            "SampleText": sample_text,
            "Baseline": {
                "Rate": rate_str,
                "Pitch": pitch_str,
                "Volume": vol_str
            },
            "Variations": variations
        }

        # 7. Save (Update if exists, else append)
        existing_index = next((i for i, c in enumerate(library) if c["Alias"] == alias), -1)
        if existing_index >= 0:
            new_character["ReferenceID"] = library[existing_index]["ReferenceID"]
            library[existing_index] = new_character
        else:
            library.append(new_character)

        with open(lib_path, 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=4)

        self.load_characters() # Refresh UI
        QMessageBox.information(self, "Success", f"Character '{alias}' saved successfully!")

    def delete_character(self):
        """Deletes the currently selected character after confirmation."""
        current_index = self.char_combo.currentIndex()
        if current_index < 0:
            QMessageBox.warning(self, "No Character Selected", "Please select a character to delete.")
            return

        char_data = self.char_combo.currentData()
        alias = char_data.get("Alias", "Unknown")

        reply = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to permanently delete the character '{alias}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Remove from the internal list
            self.characters_data.pop(current_index)

            # Save the updated library back to the file
            lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "voice-library", "characters.json")
            try:
                with open(lib_path, 'w', encoding='utf-8') as f:
                    json.dump(self.characters_data, f, indent=4)
                self.load_characters() # Refresh UI
                QMessageBox.information(self, "Success", f"Character '{alias}' has been deleted.")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to update characters.json.\n\n{e}")
                self.load_characters() # Re-sync on failure

    def on_character_changed(self, index):
        """Updates variations and text when character changes."""
        if index < 0 or index >= len(self.characters_data):
            return
        
        char = self.char_combo.currentData()
        if not char:
            return

        # Update Description
        desc = char.get("Description", "")
        self.char_desc_label.setText(f"Description: {desc}")

        # Update Sample Text
        sample = char.get("SampleText", "")
        self.char_text_input.setText(sample)

        # Update Variations
        self.var_combo.clear()
        variations = char.get("Variations", {})
        for var_name in sorted(variations.keys()):
            self.var_combo.addItem(var_name)
        
        # Select 'Calm' by default if exists
        idx = self.var_combo.findText("Calm")
        if idx >= 0:
            self.var_combo.setCurrentIndex(idx)

    def on_variation_changed(self, index):
        """Updates the variation spin boxes when the variation changes."""
        if index < 0:
            return

        char = self.char_combo.currentData()
        var_name = self.var_combo.currentText()

        if not char or not var_name:
            return

        variation = char.get("Variations", {}).get(var_name)
        if not variation:
            return

        # Block signals to prevent loops
        self.char_pitch_spin.blockSignals(True)
        self.char_rate_spin.blockSignals(True)
        self.char_vol_spin.blockSignals(True)

        pitch_val, _ = parse_val(variation.get("Pitch", "+0Hz"))
        rate_val, _ = parse_val(variation.get("Rate", "+0%"))
        vol_val, _ = parse_val(variation.get("Volume", "+0%"))

        self.char_pitch_spin.setValue(pitch_val)
        self.char_rate_spin.setValue(rate_val)
        self.char_vol_spin.setValue(vol_val)

        # Unblock signals
        self.char_pitch_spin.blockSignals(False)
        self.char_rate_spin.blockSignals(False)
        self.char_vol_spin.blockSignals(False)

    def schedule_variation_update(self):
        """Schedules a delayed update to the character variation to avoid rapid file writes."""
        self.variation_update_timer.start()

    def _perform_variation_update(self):
        """Saves the current variation settings to characters.json. Called by a timer."""
        char_data = self.char_combo.currentData()
        var_name = self.var_combo.currentText()

        if not char_data or not var_name:
            return

        # Find the character in the main data list to ensure we modify the source
        char_to_update = next((c for c in self.characters_data if c.get("ReferenceID") == char_data.get("ReferenceID")), None)
        if not char_to_update:
            return

        # Get the new values from spin boxes and format them
        pitch_str = f"{self.char_pitch_spin.value():+d}Hz"
        rate_str = f"{self.char_rate_spin.value():+d}%"
        vol_str = f"{self.char_vol_spin.value():+d}%"

        # Update the dictionary in memory
        if var_name in char_to_update["Variations"]:
            char_to_update["Variations"][var_name]["Pitch"] = pitch_str
            char_to_update["Variations"][var_name]["Rate"] = rate_str
            char_to_update["Variations"][var_name]["Volume"] = vol_str
        else:
            return

        # Save the entire library back to the file
        lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "voice-library", "characters.json")
        try:
            with open(lib_path, 'w', encoding='utf-8') as f:
                json.dump(self.characters_data, f, indent=4)
            # Also update the data stored in the combobox item to keep it in sync
            self.char_combo.setItemData(self.char_combo.currentIndex(), char_to_update)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save characters.json.\n\n{e}")

    def get_generation_args(self, output_file, mode="general"):
        """Helper to construct arguments for generate_speech_edge.py"""
        
        if mode == "general":
            text = self.text_input.toPlainText().strip()
            voice_id = self.voice_combo.currentData()
            pitch_str = f"{self.pitch_spin.value():+d}Hz"
            rate_str = f"{self.rate_spin.value():+d}%"
            vol_str = f"{self.vol_spin.value():+d}%"
        
        elif mode == "character":
            text = self.char_text_input.toPlainText().strip()
            char = self.char_combo.currentData()
            var_name = self.var_combo.currentText()
            
            if not char or not var_name:
                QMessageBox.warning(self, "Selection Error", "Please select a character and variation.")
                return None
            
            voice_id = char.get("ShortName")
            
            # Get settings from variation (assuming absolute values as per your JSON structure)
            variations = char.get("Variations", {})
            settings = variations.get(var_name, {})
            
            pitch_str = settings.get("Pitch", "+0Hz")
            rate_str = settings.get("Rate", "+0%")
            vol_str = settings.get("Volume", "+0%")

        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter some text.")
            return None

        if not voice_id:
            QMessageBox.warning(self, "Voice Error", "Please select a valid voice.")
            return None

        # Path to the generation script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_speech_edge.py")

        return [
            sys.executable, script_path,
            text, output_file,
            "--voice", voice_id,
            f"--pitch={pitch_str}",
            f"--rate={rate_str}",
            f"--volume={vol_str}"
        ]

    def preview_audio(self, mode="general"):
        """Generates audio to a temp file and plays it."""
        # Use a temporary file in the current directory or temp dir
        temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_preview.mp3")
        
        cmd = self.get_generation_args(temp_file, mode=mode)
        if not cmd:
            return

        # Add --play flag
        cmd.append("--play")

        btn = self.preview_btn if mode == "general" else self.char_preview_btn
        
        btn.setEnabled(False)
        original_text = btn.text()
        btn.setText("Generating...")

        self.worker = GenerationWorker(cmd)
        self.worker.finished.connect(lambda success, msg: self.on_preview_finished(success, msg, btn, original_text))
        self.worker.start()

    def on_preview_finished(self, success, msg, btn, original_text):
            btn.setEnabled(True)
            btn.setText(original_text)
            if not success:
                QMessageBox.critical(self, "Generation Error", f"Failed to generate audio.\n\n{msg}")

    def save_audio(self, mode="general"):
        """Opens save dialog and generates audio file."""
        last_dir = self.settings.value("last_save_dir", "")
        
        # Generate default filename from text
        text = self.text_input.toPlainText() if mode == "general" else self.char_text_input.toPlainText()
        text = text.strip()
        
        default_name = "output.mp3"
        if text:
            # Sanitize: keep alphanumeric, spaces, hyphens
            safe_text = re.sub(r'[^\w\s-]', '', text)
            # Replace spaces/hyphens with underscores
            safe_text = re.sub(r'[-\s]+', '_', safe_text).strip('_')
            # Truncate to 24 chars
            safe_text = safe_text[:24]
            if safe_text:
                default_name = f"{safe_text}.mp3"

        if mode == "character":
            char = self.char_combo.currentData()
            if char:
                alias = char.get("Alias", "character")
                # Sanitize alias for filename
                safe_alias = re.sub(r'[^\w\s-]', '', alias).strip()
                safe_alias = re.sub(r'[-\s]+', '_', safe_alias)
                default_name = f"{safe_alias}_{default_name}"

        initial_path = os.path.join(last_dir, default_name) if last_dir else default_name
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Audio", initial_path, "MP3 Files (*.mp3);;WAV Files (*.wav)")
        if not file_path:
            return

        self.settings.setValue("last_save_dir", os.path.dirname(file_path))

        cmd = self.get_generation_args(file_path, mode=mode)
        if not cmd:
            return

        btn = self.save_btn if mode == "general" else self.char_save_btn
        
        btn.setEnabled(False)
        original_text = btn.text()
        btn.setText("Saving...")

        self.worker = GenerationWorker(cmd)
        self.worker.finished.connect(lambda success, msg: self.on_save_finished(success, msg, btn, original_text, file_path))
        self.worker.start()

    def on_save_finished(self, success, msg, btn, original_text, file_path):
            btn.setEnabled(True)
            btn.setText(original_text)
            if success:
                # Don't show success message if user cancelled
                if "cancelled by user" not in msg.lower():
                    QMessageBox.information(self, "Success", f"Audio saved to:\n{file_path}")
            else:
                QMessageBox.critical(self, "Generation Error", f"Failed to save audio.\n\n{msg}")

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
        about_dlg.setText("<h3>Text to Speech</h3>")
        about_dlg.setInformativeText(
            "<div style='font-size: 14px; font-weight: normal;'>"
            "This application uses Microsoft Edge TTS to build out audio phrases.<br><br>"
            "Supported output formats: MP3<br><br>"
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
    app.setStyle("Fusion")

    # --- Dark Palette for correct Fusion rendering of controls like QSpinBox ---
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    # --- Prepare and set stylesheet with correct resource paths ---
    css_icon_path = resource_path(os.path.join("assets", "icons", "checkmark.png")).replace("\\", "/")
    app.setStyleSheet(DARK_STYLESHEET.replace("{css_icon_path}", css_icon_path))

    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec())
