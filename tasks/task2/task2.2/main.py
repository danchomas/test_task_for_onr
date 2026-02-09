import sys
import re
import requests
from bs4 import BeautifulSoup
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

class PriceParser(QThread):
    finished = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                self.finished.emit(f"ошибка сайта - {response.status_code}")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            
            text = soup.get_text(separator=' ')

            pattern = r'\d[\d\s.,]*\s?(?:₽|руб\.?|р\.)'
            
            matches = re.findall(pattern, text, re.IGNORECASE)

            if matches:
                price = matches[0].strip()
                self.finished.emit(f"найденная цена: {price}")
            else:
                self.finished.emit("цена не была найдена")

        except Exception as e:
            self.finished.emit(f"ошибка: {str(e)}")

class Desktop(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("поиск цены")
        self.resize(400, 200)
        
        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("ссылка")
        layout.addWidget(self.url_input)

        self.btn = QPushButton("цена")
        self.btn.setStyleSheet("font-size: 14px; padding: 10px; background-color: #0078D7; color: white;")
        self.btn.clicked.connect(self.start_check)
        layout.addWidget(self.btn)

        self.result_label = QLabel("ссылка")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def start_check(self):
        url = self.url_input.text().strip()
        if not url:
            return

        self.result_label.setText("ищу цену")
        self.btn.setEnabled(False)

        self.worker = PriceWorker(url)
        self.worker.finished.connect(self.show_result)
        self.worker.start()

    def show_result(self, text):
        self.result_label.setText(text)
        self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Desktop()
    window.show()
    sys.exit(app.exec())