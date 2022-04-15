import sys
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

class GUI(QtWidgets.QWidget):
    def __init__(self):
       super().__init__(); # invoke init of super class(QtWidgets.QWidget), GUI() is child class of QtWidgets.QWidget

       LoadTroopsButton = QtWidgets.QPushButton(self);
       LoadTroopsButton.setText("Load Troops");
       LoadTroopsButton.move(50,20);
       LoadTroopsButton.clicked.connect(self.LoadTroops);
            
       self.setGeometry(10,10,300,200);
       self.setWindowTitle('PyQt');
       self.show();

    def LoadTroops(self):
        print('Loading Troops');

def GUI_Init():
    app = QtWidgets.QApplication(sys.argv);# contain the GUI application object
    gui = GUI();
    sys.exit(app.exec_())
    return gui;
	
if __name__ == '__main__':
   gui = GUI_Init();
