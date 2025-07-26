from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QFormLayout, QSpinBox
)
from PyQt5.QtCore import Qt

class RecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Record New Gesture")
        self.setMinimumWidth(400)

        # Form fields
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(20)
        self.name_edit.setPlaceholderText("Gesture name (max 20 chars)")

        self.desc_edit = QLineEdit()
        self.desc_edit.setMaxLength(60)
        self.desc_edit.setPlaceholderText("Description (optional, max 60 chars)")

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Select type", "volume", "brightness", "open file", "run command", "open url"])
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)

        # Value field: QLineEdit for most, QComboBox for volume/brightness
        self.value_line = QLineEdit()
        self.value_line.setPlaceholderText("")
        self.value_line.setEnabled(False)
        self.value_line.setVisible(True)
        self.value_line.textChanged.connect(self.validate_form)

        self.value_combo = QComboBox()
        self.value_combo.addItems(["up", "down"])
        self.value_combo.setVisible(False)
        self.value_combo.currentIndexChanged.connect(self.validate_form)

        self.step_spin = QSpinBox()
        self.step_spin.setRange(0, 100)
        self.step_spin.setEnabled(False)

        # Button
        self.record_button = QPushButton("Record Gesture")
        self.record_button.setEnabled(False)
        self.record_button.clicked.connect(self.on_record_clicked)

        # Layout
        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_edit)
        form_layout.addRow("Description:", self.desc_edit)
        form_layout.addRow("Type:", self.type_combo)
        form_layout.addRow("Value:", self.value_line)
        form_layout.addRow("", self.value_combo)
        form_layout.addRow("Step:", self.step_spin)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.record_button)
        self.setLayout(main_layout)

        # Connect field changes to validation
        self.name_edit.textChanged.connect(self.validate_form)
        self.desc_edit.textChanged.connect(self.validate_form)
        self.step_spin.valueChanged.connect(self.validate_form)

    def on_type_changed(self, idx):
        # Clear value and step fields
        self.value_line.clear()
        self.value_combo.setCurrentIndex(0)
        self.step_spin.setValue(0)
        self.value_line.setEnabled(False)
        self.value_combo.setVisible(False)
        self.value_line.setVisible(True)
        self.step_spin.setEnabled(False)

        type_text = self.type_combo.currentText()
        if type_text in ["volume", "brightness"]:
            self.value_line.setVisible(False)
            self.value_combo.setVisible(True)
            self.value_combo.setEnabled(True)
            self.step_spin.setEnabled(True)
        elif type_text == "open file":
            self.value_line.setPlaceholderText("local system path to the file")
            self.value_line.setEnabled(True)
            self.value_line.setVisible(True)
            self.value_combo.setVisible(False)
            self.step_spin.setEnabled(False)
        elif type_text == "run command":
            self.value_line.setPlaceholderText("cmd command to execute")
            self.value_line.setEnabled(True)
            self.value_line.setVisible(True)
            self.value_combo.setVisible(False)
            self.step_spin.setEnabled(False)
        elif type_text == "open url":
            self.value_line.setPlaceholderText("url to open")
            self.value_line.setEnabled(True)
            self.value_line.setVisible(True)
            self.value_combo.setVisible(False)
            self.step_spin.setEnabled(False)
        else:
            self.value_line.setPlaceholderText("")
            self.value_line.setEnabled(False)
            self.value_line.setVisible(True)
            self.value_combo.setVisible(False)
            self.step_spin.setEnabled(False)
        self.validate_form()

    def validate_form(self):
        type_text = self.type_combo.currentText()
        name_filled = bool(self.name_edit.text().strip())
        value_filled = False
        step_valid = True
        if type_text in ["volume", "brightness"]:
            value_filled = True  # always one selected in combo
            step_valid = self.step_spin.value() > 0
        elif type_text in ["open file", "run command", "open url"]:
            value_filled = bool(self.value_line.text().strip())
            step_valid = True
        else:
            value_filled = False
            step_valid = False
        self.record_button.setEnabled(name_filled and value_filled and step_valid)

    def on_record_clicked(self):
        # Placeholder for next interface
        if self.type_combo.currentText() in ["volume", "brightness"]:
            value = self.value_combo.currentText()
        else:
            value = self.value_line.text().strip()
        print(f"Proceed to gesture recording interface... Value: {value}")
        self.accept()
