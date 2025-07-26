from src.detector.detection_service import DetectionService

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QFont

from src.gestures.gesture_manager import GestureManager

class DetectionThread(QThread):
    status_changed = pyqtSignal(str)

    def __init__(self, detection_service):
        super().__init__()
        self.detection_service = detection_service

    def run(self):
        self.status_changed.emit("running")
        self.detection_service.run()

    def stop(self):
        self.detection_service.stop()
        self.status_changed.emit("stopped")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Handler")
        self.resize(600, 500)

        self.detection_service = DetectionService()
        self.detection_thread = DetectionThread(self.detection_service)
        self.detection_thread.status_changed.connect(self.update_status)

        self.status_label = QLabel("Estado: Iniciando detección…")
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.set_status_color("yellow")

        title = QLabel("Handler")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))

        self.gesture_table = QTableWidget()
        self.gesture_table.setColumnCount(3)
        self.gesture_table.setHorizontalHeaderLabels(["Name", "Type", "Value"])
        self.gesture_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_gestures()

        self.record_button = QPushButton("Record New Gesture")
        self.record_button.clicked.connect(self.on_record_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.status_label)
        layout.addWidget(self.gesture_table)
        layout.addWidget(self.record_button)
        self.setLayout(layout)

        self.detection_thread.start()


    def set_status_color(self, color):
        colors = {
            "green": "#4CAF50",
            "red": "#F44336",
            "yellow": "#FFC107"
        }
        self.status_label.setStyleSheet(f"color: {colors.get(color, 'black')};")

    @pyqtSlot(str)
    def update_status(self, status):
        if status == "starting":
            self.status_label.setText("State: Starting detection…")
            self.set_status_color("yellow")
        elif status == "running":
            self.status_label.setText("State: Detecting…")
            self.set_status_color("green")
        elif status == "stopped":
            self.status_label.setText("State: Detection paused")
            self.set_status_color("red")

    def load_gestures(self):
        gestures = GestureManager().gestures
        self.gesture_table.setRowCount(len(gestures))
        for row, gesture in enumerate(gestures):
            self.gesture_table.setItem(row, 0, QTableWidgetItem(gesture.name))
            self.gesture_table.setItem(row, 1, QTableWidgetItem(gesture.type))
            self.gesture_table.setItem(row, 2, QTableWidgetItem(gesture.value.get("command")))

    def on_record_button_clicked(self):
        self.detection_thread.stop()
        from src.gui.record_dialog import RecordDialog
        dialog = RecordDialog(self)
        dialog.exec_()
        self.detection_thread.start()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
