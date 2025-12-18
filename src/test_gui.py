import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QComboBox, QLabel, QListView, QSizePolicy)
from PySide6.QtGui import QPalette, QColor, Qt

class LimitedComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # --- THE FIX: FORCE SCROLLBAR ---
        # This tells the internal view: "Use a real scrollbar, don't use menu arrows."
        self.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Optional: Set a consistent item delegate height if needed, 
        # but usually not required if styling is correct.

    def showPopup(self):
        super().showPopup()
        popup = self.view().window()
        
        rect = self.view().visualRect(self.view().model().index(0, 0))
        row_height = rect.height() if rect.height() > 0 else self.view().fontMetrics().lineSpacing()
        
        max_items = 15
        items_to_show = min(self.count(), max_items)
        
        total_height = (items_to_show * row_height) + 4
        current_geo = popup.geometry()
        
        popup.setGeometry(current_geo.x(), current_geo.y(), current_geo.width(), total_height)

class TestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test GUI - Scrollbar Fix")
        self.resize(600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignTop)
        
        label = QLabel("ComboBox (Real Scrollbar):")
        layout.addWidget(label, 0, Qt.AlignLeft)
        
        self.combo = LimitedComboBox()
        self.combo.setView(QListView())
        
        # 100 Items
        items = [f"Item {i}" for i in range(1, 101)]
        items[49] = "Item 50 - This is a very long entry to test width"
        self.combo.addItems(items)
        
        # --- STYLING ---
        # Added QScrollBar styling to make it look integrated and dark
        self.combo.setStyleSheet("""
            QComboBox QAbstractItemView {
                background-color: #191919;
                color: white;
                selection-background-color: #2A82DA;
                outline: 0px;
            }
            
            /* Vertical ScrollBar Style */
            QScrollBar:vertical {
                border: none;
                background: #191919;
                width: 10px; /* Width of the bar */
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #505050; /* Lighter grey handle */
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px; /* Hides the ugly top/bottom arrows on the scrollbar itself */
            }
        """)

        layout.addWidget(self.combo, 0, Qt.AlignLeft)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
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
    
    window = TestApp()
    window.show()
    sys.exit(app.exec())