from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser
from hashlib import new
from tokenize import String
from os import system


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(500, 500)
        self.label1 = QLabel("Enter your host IP:", self)
        self.text = QLineEdit(self)
        self.text.move(20, 60)
        self.label2 = QLabel("api_key:", self)
        self.text1 = QLineEdit(self)
        self.label2.move(20, 120)
        self.text1.move(20, 160)
        self.label3 = QLabel("IP :", self)
        self.text2 = QLineEdit(self)
        self.label3.move(30, 110)
        self.text2.move(30, 130)
        self.label4 = QLabel("Answer:", self)
        self.label4.move(30, 160)
        self.button = QPushButton("Send", self)
        self.button.move(30, 210)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        hostname = self.text.text()
        api_key = self.text1.text()
        IP = self.text2.text()

        if hostname == "" or api_key == "" or IP == "":
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__query(hostname,api_key,IP)
            if res or res and type(res)==dict:
                lat=str(res["latitude"])
                long=str(res["longitude"])
                self.label4.setText("Answer%s" % (res["Organization"]+"\n latitude :"+lat+"\n longitude :"+long))
                self.label4.adjustSize()
                self.show()
                webbrowser.open( url = "https://www.openstreetmap.org/?mlat="+lat+"&mlon="+long+"#map=12",new =0 )
                
 #    if res

    def __query(self, hostname,api_key,IP):
        url = "http://"+hostname+"/ip/"+IP+"?key="+api_key
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()