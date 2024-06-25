from pytube import YouTube
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap
import requests


class Window(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("gui.ui", self)
        self.setWindowTitle("PyTuber")
        self.setFixedSize(self.size())
        self.downloadbtn.clicked.connect(self.download)
        self.link.textChanged.connect(self.refresh_status)
        self.downloadbtn.setEnabled(False)

    def refresh_status(self):
        video_url = self.link.text()
        if len(video_url) > 7:
            try:
                yt = YouTube(video_url)
                img_content = requests.get(yt.thumbnail_url).content
                with open("thum.png", "wb") as file:
                    file.write(img_content)
                self.video_title.setText(yt.title[:5] + '...')
                self.video_img.setPixmap(QPixmap("thum.png"))
                self.video_img.setScaledContents(True)
                self.downloadbtn.setEnabled(True)
            except Exception as error:
                self.video_img.clear()
                self.video_title.clear()
                self.downloadbtn.setEnabled(False)
                print(error)
        else:
            self.video_img.clear()
            self.video_title.clear()
            self.downloadbtn.setEnabled(False)

    def download(self):
        video_url = self.link.text()
        try:
            yt = YouTube(video_url)
            video = yt.streams.filter(res=self.selected_resolution).first()
            if video:
                video.download()
                QMessageBox.information(self, "Success", "Download completed successfully!")
            else:
                QMessageBox.warning(self, "Error", "Selected resolution not available.")
        except Exception as error:
            QMessageBox.critical(self, "Error", f"An error occurred: {error}")
            print(error)

    @property
    def selected_resolution(self):
        return self.resolution.currentText()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
