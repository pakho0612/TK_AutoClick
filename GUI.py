import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from const import *
from functools import partial
import auto

class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(); # invoke init of super class(QtWidgets.QWidget), GUI() is child class of QtWidgets.QWidget

        self.CurTroop = '';
        self.AllTroops = [];
        self.LoadTroopsButton = QtWidgets.QPushButton(self);
        self.LoadTroopsButton.setText("Load Troops");
        self.LoadTroopsButton.clicked.connect(self.LoadTroops);

        self.HomeLocationBox = QtWidgets.QLineEdit(self);
        self.HomeLocation = [0,0];
        self.HomeLocationBox.setPlaceholderText('Home Location ex: 123,456');
        self.HomeLocationBox.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,4},[0-9]{1,4}")));
        self.HomeLocationBox.editingFinished.connect(self.HomeLocationChanged);

        self.ReloadTroopsButton = QtWidgets.QPushButton("Reload Troops", self);
        self.ReloadTroopsButton.clicked.connect(self.ReloadTroopsImg);

        self.TaskTimeMenu = QtWidgets.QDateTimeEdit(self);
        self.TaskTimeMenu.setCalendarPopup(True); ## calendar pop up for date setting
        self.TaskTimeMenu.setDisplayFormat("yyyy-MM-dd hh:mm:ss ap");
        self.TaskTime = QtCore.QDateTime.currentDateTime();
        self.TaskTimeMenu.setDateTime(self.TaskTime);
        self.TaskTime = self.TaskTime.toPyDateTime();
        self.TaskTimeMenu.dateTimeChanged.connect(self.TaskTimeChanged);

        self.TroopsHboxlayout = QtWidgets.QHBoxLayout();
        self.TroopsBox = QtWidgets.QButtonGroup(self);

        self.ModeButton = QtWidgets.QComboBox(self);
        self.mode = c_mode_city; ## Default Mode Value
        self.ModeButton.addItem("攻城", QtCore.QVariant(c_mode_city));
        self.ModeButton.addItem("佔地", QtCore.QVariant(c_mode_tile));
        self.ModeButton.addItem("行軍", QtCore.QVariant(c_mode_move));
        self.ModeButton.currentIndexChanged.connect(self.ModeChanged);

        self.RepeatButton = QtWidgets.QComboBox(self);
        self.repeat = -1; ## Default Mode Value
        self.RepeatButton.addItem("不限次", QtCore.QVariant(-1));
        self.RepeatButton.addItem("1次", QtCore.QVariant(1));
        self.RepeatButton.addItem("2次", QtCore.QVariant(2));
        self.RepeatButton.addItem("3次", QtCore.QVariant(3));
        self.RepeatButton.currentIndexChanged.connect(self.RepeatChanged);

        self.DelayBox = QtWidgets.QLineEdit(self);
        self.delay = 0;
        self.DelayBox.setPlaceholderText('Delay : 0 seconds');
        self.DelayBox.setValidator(QtGui.QIntValidator());
        self.DelayBox.editingFinished.connect(self.DelayChanged);

        self.TargetBox = QtWidgets.QLineEdit(self);
        self.target = [0,0];
        self.TargetBox.setPlaceholderText('Target Location ex: 123,456');
        self.TargetBox.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,4},[0-9]{1,4}")));
        self.TargetBox.editingFinished.connect(self.TargetChanged);

        self.ReturnHomeBox = QtWidgets.QCheckBox('Return Home',self);
        self.return_home = False;
        self.ReturnHomeBox.setChecked(False);
        self.ReturnHomeBox.stateChanged.connect(self.ReturnHomeChanged);

        self.AddTaskButton = QtWidgets.QPushButton('Add Task', self);
        self.AddTaskButton.clicked.connect(self.AddTaskClicked);

        self.AllTasksTable = QtWidgets.QTableWidget(self);
        self.AllTasksTable.setRowCount(0);
        self.AllTasksTable.setColumnCount(7);
        self.AllTasksTable.setHorizontalHeaderLabels(['Mode', 'Time', 'Troop', 'Target', 'Delay', 'Repeat', 'ReturnHome']);
        self.AllTasksTable.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows);

        self.RemoveTaskButton = QtWidgets.QPushButton('Remove Task', self);
        self.RemoveTaskButton.clicked.connect(self.RemoveTaskClicked);

        self.RunButton = QtWidgets.QPushButton('Run', self);
        self.RunButton.clicked.connect(self.RunClicked);

        self.LoadTroopsHomeLocationLayout = QtWidgets.QHBoxLayout();        
        self.LoadTroopsHomeLocationLayout.addWidget(self.LoadTroopsButton);
        self.LoadTroopsHomeLocationLayout.addWidget(self.HomeLocationBox);
        self.LoadTroopsHomeLocationLayout.addWidget(self.ReloadTroopsButton);

        self.ModeTargetTimeLayout = QtWidgets.QHBoxLayout();
        self.ModeTargetTimeLayout.addWidget(QtWidgets.QLabel("Mode: "));
        self.ModeTargetTimeLayout.addWidget(self.ModeButton);
        self.ModeTargetTimeLayout.addWidget(self.TargetBox);
        self.ModeTargetTimeLayout.addWidget(self.TaskTimeMenu);

        self.DelayRepeatReturnHomeLayout = QtWidgets.QHBoxLayout();
        self.DelayRepeatReturnHomeLayout.addWidget(self.DelayBox);
        self.DelayRepeatReturnHomeLayout.addWidget(QtWidgets.QLabel("Repeat: "));
        self.DelayRepeatReturnHomeLayout.addWidget(self.RepeatButton);
        self.DelayRepeatReturnHomeLayout.addWidget(self.ReturnHomeBox);
        
        self.LeftHalfLayout = QtWidgets.QVBoxLayout();
        self.LeftHalfLayout.addLayout(self.LoadTroopsHomeLocationLayout);
        self.LeftHalfLayout.addLayout(self.TroopsHboxlayout);
        self.LeftHalfLayout.addLayout(self.ModeTargetTimeLayout);
        self.LeftHalfLayout.addLayout(self.DelayRepeatReturnHomeLayout);
        self.LeftHalfLayout.addWidget(self.AddTaskButton);
        
        self.RightHalfLayout = QtWidgets.QVBoxLayout();
        self.RightHalfLayout.addWidget(self.AllTasksTable);
        self.RightHalfLayout.addWidget(self.RemoveTaskButton);
        self.RightHalfLayout.addWidget(self.RunButton);
        self.Layout = QtWidgets.QGridLayout(self);
        self.Layout.addLayout(self.LeftHalfLayout, 0, 1);
        self.Layout.addLayout(self.RightHalfLayout, 0, 2);

        self.setGeometry(400,400,c_GUI_size[0],c_GUI_size[1]); ##GUI window location and size
        self.setWindowTitle('TKAutoClick');
        self.show();

    def ReloadTroopsImg(self):
        auto.FindTroopsImg(self.HomeLocation);
        self.LoadTroops();

    def LoadTroops(self):
        self.CurTroop = '';
        print('wind size', self.width(), self.height());

        print('current button group', self.TroopsBox.buttons());
        # Find all troop from game and create button for each
        for btn in self.TroopsBox.buttons():
            self.TroopsBox.removeButton(btn); ## Clear all existing buttons before recreate new ones
            btn.deleteLater();
            
        for troop in c_troops: ##
            troop_img = QtGui.QPixmap(troop);
            if troop_img.isNull() is False:
                btn = QtWidgets.QPushButton(checkable = True);
                btn.setStyleSheet("checked{background-color: blue;}"); # set push button color when selected
                
                print('Image size ', troop_img.width(), troop_img.height())
                btn.setFixedSize(troop_img.width(), troop_img.height());
                btn.setStyleSheet("background-image : url(" + troop + ");");
                btn.clicked.connect(partial(self.TroopSelected, troop)); #partial() create a new with argument replace by a constant(troop in this case)
                self.TroopsHboxlayout.addWidget(btn);
                self.TroopsBox.addButton(btn);
        print('Loading Troops');

    def TroopSelected(self, troop):
        self.CurTroop = troop;
        print('Troop selected : ', troop);

    def TaskTimeChanged(self):
        self.TaskTime = self.TaskTimeMenu.dateTime().toPyDateTime();
        print('Task Time has changed to :', self.TaskTime);

    def ModeChanged(self):
        self.mode = self.ModeButton.currentData();
        print('Mode Changed to : ', self.mode);

    def RepeatChanged(self):
        self.repeat = self.RepeatButton.currentData();
        print('Repeat Changed to : ', self.repeat);

    def DelayChanged(self):
        self.delay = int(self.DelayBox.text());
        print('Delay Changed to : ', self.delay, ' seconds');

    def TargetChanged(self):
        self.target = self.TargetBox.text().split(',');
        print('Target Changed to : ', self.target);

    def HomeLocationChanged(self):
        self.HomeLocation = self.HomeLocationBox.text().split(',');
        print('Home Location Changed to : ', self.HomeLocation);

    def ReturnHomeChanged(self):
        self.return_home = self.ReturnHomeBox.isChecked();
        print('ReturnHome Changed to : ', self.return_home);

    def AddTaskClicked(self):
        print('Adding Task');
        auto.debug_message('Added new task', self.mode, self.TaskTime, self.CurTroop, self.target, self.delay, self.repeat, self.return_home);
        auto.alltasks.AddTask(self.mode, self.TaskTime, self.CurTroop, self.target, self.delay, self.repeat, self.return_home);

        numrow = self.AllTasksTable.rowCount();
        self.AllTasksTable.insertRow(numrow);
        self.AllTasksTable.setItem(numrow, 0, QtWidgets.QTableWidgetItem(self.mode));
        self.AllTasksTable.setItem(numrow, 1, QtWidgets.QTableWidgetItem(self.TaskTime.strftime("%m/%d/%Y %H:%M:%S")));
        self.AllTasksTable.setItem(numrow, 2, QtWidgets.QTableWidgetItem(self.CurTroop));
        self.AllTasksTable.setItem(numrow, 3, QtWidgets.QTableWidgetItem(str(self.target[0])+','+str(self.target[1])));
        self.AllTasksTable.setItem(numrow, 4, QtWidgets.QTableWidgetItem(str(self.delay)));
        self.AllTasksTable.setItem(numrow, 5, QtWidgets.QTableWidgetItem(str(self.repeat)));
        self.AllTasksTable.setItem(numrow, 6, QtWidgets.QTableWidgetItem(str(self.return_home)));

    def RemoveTaskClicked(self):
        rowToRemove = self.AllTasksTable.currentRow();
        self.AllTasksTable.removeRow(rowToRemove);
        print('Removing Task : ', rowToRemove);
        auto.alltasks.RemoveTaskbyIndex(rowToRemove);

    def RunClicked(self):
        auto.alltasks.tasks_management();

def GUI_Init():
    app = QtWidgets.QApplication(sys.argv);# contain the GUI application object
    gui_data = GUI();
    sys.exit(app.exec_());
    return gui;
	
if __name__ == '__main__':  #only run when as main
    #auto.Init();
    print(auto.alltasks)
    gui = GUI_Init();
