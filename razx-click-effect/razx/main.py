import json
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QColorDialog, QApplication
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle("RazX Cursor Effects Settings") 

        # Set fixed window size and remove maximize button
        self.setMaximumSize(427, 554)
        self.setFixedSize(427, 554)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # Connect buttons
        self.pick.clicked.connect(self.pick_color)
        self.pick_2.clicked.connect(self.pick_color_2)
        self.apply.clicked.connect(self.apply_clicked)
        self.exit.clicked.connect(self.Exit)

        # Init
        self.selected_color = None
        self.selected_color2 = None
        self.last_left_color = {}
        self.last_right_color = {}

        # Set fixed size for input fields
        self.leftSize.setFixedSize(100, 30)
        self.rightSize.setFixedSize(100, 30)

        self.load_saved_colors()

    def Exit(self):
        QApplication.quit()

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            r, g, b = color.red(), color.green(), color.blue()
            self.leftClick_colorBlock.setStyleSheet(
                f"background-color: rgb({r}, {g}, {b}); border: 1px solid #000;"
            )

    def pick_color_2(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color2 = color
            r, g, b = color.red(), color.green(), color.blue()
            self.rightClick_colorBlock.setStyleSheet(
                f"background-color: rgb({r}, {g}, {b}); border: 1px solid #000;"
            )

    def apply_clicked(self):
        # Use fallback color if none selected
        if not self.selected_color:
            self.selected_color = QColor(
                int(self.last_left_color.get("r", 0) * 255),
                int(self.last_left_color.get("g", 0) * 255),
                int(self.last_left_color.get("b", 0) * 255)
            )

        if not self.selected_color2:
            self.selected_color2 = QColor(
                int(self.last_right_color.get("r", 0) * 255),
                int(self.last_right_color.get("g", 0) * 255),
                int(self.last_right_color.get("b", 0) * 255)
            )

        r = round(self.selected_color.red() / 255, 3)
        g = round(self.selected_color.green() / 255, 3)
        b = round(self.selected_color.blue() / 255, 3)

        r2 = round(self.selected_color2.red() / 255, 3)
        g2 = round(self.selected_color2.green() / 255, 3)
        b2 = round(self.selected_color2.blue() / 255, 3)

        a = 0.7

        # Validate and show inline error
        self.leftSize.setStyleSheet("")
        self.rightSize.setStyleSheet("")
        self.leftSize.setToolTip("")
        self.rightSize.setToolTip("")
        error_found = False

        try:
            left_radius = int(self.leftSize.text())
            if left_radius > 50:
                self.leftSize.setStyleSheet("border: 2px solid red;")
                self.leftSize.setToolTip("Radius must not be greater than 50")
                error_found = True
        except ValueError:
            self.leftSize.setStyleSheet("border: 2px solid red;")
            self.leftSize.setToolTip("Invalid number")
            error_found = True

        try:
            right_radius = int(self.rightSize.text())
            if right_radius > 50:
                self.rightSize.setStyleSheet("border: 2px solid red;")
                self.rightSize.setToolTip("Radius must not be greater than 50")
                error_found = True
        except ValueError:
            self.rightSize.setStyleSheet("border: 2px solid red;")
            self.rightSize.setToolTip("Invalid number")
            error_found = True

        if error_found:
            return

        # Save data
        data = {
            "left_click": {
                "r": r,
                "g": g,
                "b": b,
                "a": a,
                "radius": left_radius,
                "diameter": 1000
            },
            "right_click": {
                "r": r2,
                "g": g2,
                "b": b2,
                "a": a,
                "radius": right_radius,
                "diameter": 1000
            }
        }

        with open("settings.json", "w") as f:
            json.dump(data, f, indent=2)

        print("Settings saved to settings.json.")

    def load_saved_colors(self):
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)

                # LEFT
                left = data.get("left_click", {})
                self.last_left_color = left
                r = int(left.get("r", 0) * 255)
                g = int(left.get("g", 0) * 255)
                b = int(left.get("b", 0) * 255)
                self.selected_color = QColor(r, g, b)
                self.leftClick_colorBlock.setStyleSheet(
                    f"background-color: rgb({r}, {g}, {b}); border: 1px solid #000;"
                )
                self.leftSize.setText(str(left.get("radius", 40)))

                # RIGHT
                right = data.get("right_click", {})
                self.last_right_color = right
                r2 = int(right.get("r", 0) * 255)
                g2 = int(right.get("g", 0) * 255)
                b2 = int(right.get("b", 0) * 255)
                self.selected_color2 = QColor(r2, g2, b2)
                self.rightClick_colorBlock.setStyleSheet(
                    f"background-color: rgb({r2}, {g2}, {b2}); border: 1px solid #000;"
                )
                self.rightSize.setText(str(right.get("radius", 40)))
        except Exception as e:
            print("Could not load settings.json:", e)
            self.last_left_color = {}
            self.last_right_color = {}

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
