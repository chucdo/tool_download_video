import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QPushButton,
    QVBoxLayout, QMessageBox, QScrollArea
)
from transformers import pipeline


class AINarrator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 AI Viết Truyện Ngôn Tình")
        self.setFixedSize(600, 600)

        self.story_generator = pipeline("text-generation", 
                                        model="mistralai/Mistral-7B-Instruct-v0.1", 
                                        device_map="auto",
                                        max_new_tokens=500,
                                        do_sample=True,
                                        temperature=0.8)

        self.prompt_label = QLabel("📝 Nhập yêu cầu viết truyện:")
        self.prompt_input = QTextEdit()
        self.generate_button = QPushButton("🪄 Viết Truyện")
        self.generate_button.clicked.connect(self.generate_story)

        self.result_label = QLabel("📖 Truyện AI Sáng Tác:")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)
        self.setLayout(layout)

    def generate_story(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập yêu cầu.")
            return

        self.result_output.setPlainText("⏳ Đang sáng tác truyện...")
        QApplication.processEvents()

        try:
            full_prompt = f"Viết một truyện ngôn tình với yêu cầu: {prompt}"
            result = self.story_generator(full_prompt)[0]["generated_text"]
            self.result_output.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AINarrator()
    window.show()
    sys.exit(app.exec())
