import shutil
import sys
import random
import requests
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCalendarWidget, QLabel, \
    QMessageBox, QFileDialog, QProgressDialog, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap, QPalette, QColor, QImage, QBrush, QImageReader
from PyQt6.QtCore import Qt, QDate, QObject, pyqtSignal, QSize, QThread
from datetime import datetime
import config

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        developer = QLabel("created by C0dJUggL")
        layout.addWidget(developer)
        about_label = QLabel("the application was created to generate a picture of the earth on any given day.  generation takes 5-30 seconds.  It depends on the size of the picture.")
        layout.addWidget(about_label)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Earth Viewer")
        self.setGeometry(100, 100, 600, 350)
        self.setFixedSize(600,350)

        self.layout = QVBoxLayout()

        self.start_button = QPushButton("Start")
        self.info_button = QPushButton("About")
        self.exit_button = QPushButton("Exit")

        button_size = QSize(150, 60)
        self.start_button.setMinimumSize(button_size)
        self.info_button.setMinimumSize(button_size)
        self.exit_button.setMinimumSize(button_size)

        button_style = """
    QPushButton {
        font-size: 16px;
        color: white;
        border: none;
        border-radius: 20px; /* Increase the border-radius for rounded corners */
        padding: 10px 15px; /* Adjust padding for a more compact button */
        margin: 5px 0px; /* Add margin to separate buttons vertically */
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 rgba(63,19,140,1),
                                          stop:0.28 rgba(63,19,140,1),
                                          stop:1 rgba(20,111,215,1));
    }

    QPushButton:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 rgba(33,9,80,1),
                                          stop:0.28 rgba(33,9,80,1),
                                          stop:1 rgba(10,61,155,1));
    }
"""
        self.start_button.setStyleSheet(button_style)
        self.info_button.setStyleSheet(button_style)
        self.exit_button.setStyleSheet(button_style)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.info_button)
        self.layout.addWidget(self.exit_button)



        self.start_button.clicked.connect(self.show_earth_photo)
        self.info_button.clicked.connect(self.show_about_window)
        self.exit_button.clicked.connect(self.exit_application)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        palette = QPalette()
        background_image = QImage("background_menu.jpg")
        background_brush = QBrush(background_image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        palette.setBrush(QPalette.ColorRole.Window, background_brush)
        self.setPalette(palette)

        self.setLayout(self.layout)
    def show_earth_photo(self):
        self.hide()
        self.earth_photo_window = EarthPhoto()
        self.earth_photo_window.show()
        self.earth_photo_window.closed.connect(self.show)

    def show_about_window(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def exit_application(self):
        QApplication.quit()

class LoadImageThread(QThread):
    loaded = pyqtSignal(bool)

    def __init__(self, selected_date_str, get_image_path_method ,parent=None):
        super().__init__(parent)
        self.image_path = None
        self.selected_date_str = selected_date_str
        self.get_image_path_for_date = get_image_path_method

    def run(self):
        self.image_path = self.get_image_path_for_date(self.selected_date_str)
        self.loaded.emit(self.image_path is not None)

class EarthPhoto(QWidget):
    closed = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Earth Viewer")
        self.setGeometry(100, 100, 422, 300)
        self.setFixedSize(422,300)
        #self.setMinimumSize(422, 300)
        #self.setMaximumSize(750, 350)
        self.layout = QVBoxLayout()
        self.date_layout = QHBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.date_layout.addWidget(self.calendar)
        self.calendar.setFixedSize(400, 220)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_layout.addWidget(self.image_label)
        self.layout.addLayout(self.date_layout)

        # ... (продолжайте добавлять другие кнопки и элементы в расположение)
        button_style = """
    QPushButton {
        font-size: 16px;
        color: white;
        border: none;
        border-radius: 20px; /* Increase the border-radius for rounded corners */
        padding: 10px 15px; /* Adjust padding for a more compact button */
        margin: 5px 0px; /* Add margin to separate buttons vertically */
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 rgba(63,19,140,1),
                                          stop:0.28 rgba(63,19,140,1),
                                          stop:1 rgba(20,111,215,1));
    }

    QPushButton:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 rgba(33,9,80,1),
                                          stop:0.28 rgba(33,9,80,1),
                                          stop:1 rgba(10,61,155,1));
    }
"""
        palette = QPalette()
        background_image = QImage("/home/dolche/PycharmProjects/NasaApp/photo_2023-08-14_00-17-11.jpg")
        background_brush = QBrush(background_image)
        palette.setBrush(QPalette.ColorRole.Window, background_brush)
        self.setPalette(palette)
        self.button = QPushButton("Show picture")
        self.button.clicked.connect(self.show_image)
        self.layout.addWidget(self.button)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_image)
        self.download_button.hide()  # Скрыть кнопку по умолчанию
        self.layout.addWidget(self.download_button)
        self.button.setStyleSheet(button_style)
        self.download_button.setStyleSheet(button_style)

        self.setLayout(self.layout)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
    def show_image(self):
        selected_date = self.calendar.selectedDate()
        selected_date_str = selected_date.toString("yyyy-MM-dd")

        if selected_date >= QDate.currentDate():
            self.load_image(selected_date_str)
        else:
            self.loading_dialog = QMessageBox(self)
            self.loading_dialog.setIcon(QMessageBox.Icon.Information)
            self.loading_dialog.setWindowTitle("Loading Image")
            self.loading_dialog.setText("Please wait while the image is loading...")
            self.loading_dialog.setStandardButtons(QMessageBox.StandardButton.NoButton)
            self.loading_dialog.show()

            self.load_image_thread = LoadImageThread(selected_date_str, self.get_image_path_for_date)
            self.load_image_thread.loaded.connect(self.image_loaded)
            self.load_image_thread.finished.connect(self.loading_dialog.accept)
            self.load_image_thread.start()

    def image_loaded(self, success):
        self.loading_dialog.accept()

        if success:
            selected_date = self.calendar.selectedDate()
            selected_date_str = selected_date.toString("yyyy-MM-dd")
            image_path = self.get_image_path_for_date(selected_date_str)

            if image_path:
                self.load_image(image_path)

    def load_image(self, image_path):
        if QImageReader(image_path).size().isValid():
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaledToWidth(300)
            self.setFixedSize(750, 400)
            self.image_label.setPixmap(pixmap)
            self.download_button.show()
        else:
            QMessageBox.critical(self, "Error", "Selected date is not available")


    def get_image_path_for_date(self, date):
        nasa_image_url = self.get_earth_image(date)
        return nasa_image_url

    def get_image_path_for_date(self, date):
        nasa_image_url = self.get_earth_image(date)
        return nasa_image_url


    def get_earth_image(self, date: str):
        items = requests.get(f"https://api.nasa.gov/EPIC/api/natural/date/{date}",
                            params={"api_key": f"{config.nasa_token}"})
        items = items.json()
        if not items:
            QMessageBox.critical(self, "Error", "Selected date is not available")
        else:
            with open('items.json', 'w') as f:
                json.dump(items, f, indent=4)
            item = items[random.randint(0, len(items) - 1)]

            image_src = item["image"]
            year, month, day = date.split("-")[0], date.split("-")[1], date.split("-")[2]
            img_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_src}.png?api_key={config.nasa_token}"
            resp = requests.get(img_url)

            if resp.status_code == 200:
                self.resize(750, 400)
                with open('img.png', 'wb') as f:
                    f.write(resp.content)
                    return 'img.png'
            else:
                print("error")
                return None
    def download_image(self):
        selected_date = self.calendar.selectedDate()
        selected_date_str = selected_date.toString("yyyy-MM-dd")
        image_path = self.get_image_path_for_date(selected_date_str)

        if image_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save picture", "", "Pictures (*.png *.jpg)")
            if save_path:
                shutil.copyfile(image_path, save_path)
                QMessageBox.information(self, "Saved", "Picture saved successfully!")
            else:
                QMessageBox.warning(self, "Error", "Choose a location for saving")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec())
