from PyQt5.QtWidgets import *
import sys,pickle
from PyQt5 import uic,QtWidgets

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('mainwindow.ui',self)
        
        self.launch_text = self.findChild(QLabel,'label')
        self.launch_button = self.findChild(QPushButton,'pushButton')
        
        self.launch_button.clicked.connect(self.launch_message)

    def launch_message(self):
        self.launch_text.setText("맛점하세요.")
    # self.show()

if __name__ =="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()

    sys.exit(app.exec_())