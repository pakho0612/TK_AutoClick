import sys
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

class GUI(QtWidgets.QWidget):
    def __init__(self):
       super().__init__(); # invoke init of super class(QtWidgets.QWidget), GUI() is child class of QtWidgets.QWidget

       self.Troop1 = ''; ## store location to the PNG
       self.Troop2 = '';
       self.Troop3 = '';
       self.Troop4 = '';
       self.Troop5 = '';
       self.LoadTroopsButton = QtWidgets.QPushButton(self);
       self.LoadTroopsButton.setText("Load Troops");
       self.LoadTroopsButton.move(50,20);
       self.LoadTroopsButton.clicked.connect(self.LoadTroops);

       self.TaskTimeMenu = QtWidgets.QDateTimeEdit(self);
       self.TaskTimeMenu.setCalendarPopup(True); ## calendar pop up for date setting
       self.TaskTimeMenu.setDisplayFormat("yyyy-MM-dd hh:mm:ss ap");
       self.TaskTime = QtCore.QDateTime.currentDateTime();
       self.TaskTimeMenu.setDateTime(self.TaskTime);
       self.TaskTime = self.TaskTime.toPyDateTime();
       self.TaskTimeMenu.dateTimeChanged.connect(self.TaskTimeChanged);
            
       self.setGeometry(400,400,300,200); ##GUI window location and size
       self.setWindowTitle('TKAutoClick');
       self.show();

    def LoadTroops(self):
        print('Loading Troops');

    def TaskTimeChanged(self):
        self.TaskTime = self.TaskTimeMenu.dateTime().toPyDateTime();
        print('Task Time has changed to :', self.TaskTime);

def GUI_Init():
    app = QtWidgets.QApplication(sys.argv);# contain the GUI application object
    gui = GUI();
    sys.exit(app.exec_());
    return gui;
	
if __name__ == '__main__':
   gui = GUI_Init();
