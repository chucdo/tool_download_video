import sys
import pyttsx3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QSlider, QComboBox, QFileDialog
)
from PyQt6.QtCore import Qt


class TextToSpeechApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text to Speech App")
        self.setFixedSize(500, 400)

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")

        # GUI Elements
        self.label = QLabel("Nhập văn bản:")
        self.text_edit = QTextEdit()

        # Voice selection
        self.voice_label = QLabel("Chọn giọng đọc:")
        self.voice_combo = QComboBox()
        self.populate_voices()

        # Speed control
        self.speed_label = QLabel("Tốc độ đọc:")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(50, 300)
        self.speed_slider.setValue(150)
        self.speed_slider.valueChanged.connect(self.update_rate)

        # Volume control
        self.volume_label = QLabel("Âm lượng:")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.update_volume)

        # Buttons
        self.speak_button = QPushButton("Đọc văn bản")
        self.save_button = QPushButton("Lưu thành file .wav")

        self.speak_button.clicked.connect(self.speak_text)
        self.save_button.clicked.connect(self.save_to_file)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)

        layout.addWidget(self.voice_label)
        layout.addWidget(self.voice_combo)

        layout.addWidget(self.speed_label)
        layout.addWidget(self.speed_slider)

        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.speak_button)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Init settings
        self.update_rate()
        self.update_volume()

    def populate_voices(self):
        for voice in self.voices:
            lang = voice.languages[0] if voice.languages else 'unknown'
            self.voice_combo.addItem(f"{voice.name} - {lang}", userData=voice.id)

    def update_rate(self):
        rate = self.speed_slider.value()
        self.engine.setProperty('rate', rate)

    def update_volume(self):
        volume = self.volume_slider.value() / 100.0
        self.engine.setProperty('volume', volume)

    def speak_text(self):
        text = self.text_edit.toPlainText().strip()
        if text:
            self.engine.setProperty('voice', self.voice_combo.currentData())
            self.update_rate()
            self.update_volume()
            self.engine.say(text)
            self.engine.runAndWait()

    def save_to_file(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Lưu file", "", "WAV files (*.wav)")
        if not file_path:
            return
        self.engine.setProperty('voice', self.voice_combo.currentData())
        self.update_rate()
        self.update_volume()
        self.engine.save_to_file(text, file_path)
        self.engine.runAndWait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec())
