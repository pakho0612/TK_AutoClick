import pyautogui
import datetime
import pygetwindow
import time
import json
from const import *
import GUI
import os
#windows click
# GUI to set troops


#################### Debug/Error Functions
class TimeOutError(Exception):
    pass

class InvalidValueError(Exception):
    pass

def debug_message(*args, **kwargs):
    if debug == 1:
        print("    " + " ".join(map(str,args)), **kwargs);
#################### System Functions
def ActivateWindow(default_window_pos, default_window_size, process_name):
    # for later: may rescale cv image instead
    # 
    win_handle = pygetwindow.getWindowsWithTitle(process_name)[0];
    win_handle.activate();#try both to get the window active
    win_handle.restore(); #
    win_handle.moveTo(default_window_pos[0], default_window_pos[1]);
    win_handle.resizeTo(default_window_size[0], default_window_size[1]);

def Init():
    # Load constants from JSON
    print('Init..');
    task_list = AllTasks();
    ActivateWindow(c_default_window_pos, c_default_window_size, c_process_name);
    return task_list;

def InitTimer():
    print('Started Timeout timer');
    return time.time();
    
def DelayAndTimeOut(start_time):
    # Reduce CPU usage while polling for locate functions
    if time.time() > (start_time + c_timeout):
        debug_message(time.time(),' vs ', start_time + c_timeout);
        return True; ## timed out
    time.sleep(c_delay);
    return False;

#################### User Functions    
def locate(picture, conf = 0.9):
    try:
        search_region = (c_default_window_pos[0],c_default_window_pos[1], c_default_window_size[0], c_default_window_size[1]);
        button_location = pyautogui.locateOnScreen(picture, confidence = conf, grayscale = True, region = search_region);
        debug_message("@locate bbox ", button_location);
        return button_location;
    except :
        debug_message("Unexpected error in locate function");

def locateCoordinateBox(picture, conf = 0.95):
    try:
        #Searching only at bottom right quarter
        search_region = (c_default_window_pos[0]+round(c_default_window_size[0]/2),c_default_window_pos[1]+round(c_default_window_size[1]/2), c_default_window_size[0], c_default_window_size[1]);
        button_location = pyautogui.locateAllOnScreen(picture, confidence = conf, region = search_region);
        debug_message("@locateCoordinateBox bbox ", button_location);
        return button_location;
    except :
        debug_message("Unexpected error in locateCoordinateBox function");
        return False;
        
def Button_exists(button_image):
    start_time = InitTimer();
    while DelayAndTimeOut(start_time) is False:
        button_bbox = locate(button_image);
        if button_bbox is not None:
            return button_bbox;
    debug_message('button not exists');
    return False; ## button not found within timeout
    
def ClickOnButton(button_image):
    # Finding the button to press
    button_bbox = Button_exists(button_image);
    if button_bbox is False:
        return False; ## button not found within timeout
    button_x, button_y = pyautogui.center(button_bbox);
    debug_message('button found at ', (button_x, button_y));
    pyautogui.click(button_x, button_y)
    return True;
        
def click(button_bbox, x_offset = 0, y_offset = 0):
    button_x, button_y = pyautogui.center(button_bbox);
    button_x = button_x + x_offset;
    button_y = button_y + y_offset;
    debug_message("button click on ",button_x, button_y)
    pyautogui.click(button_x, button_y)

def clean_textbox():
    pyautogui.press('delete');
    pyautogui.press('delete');
    pyautogui.press('delete');
    pyautogui.press('delete');
    pyautogui.press('backspace');
    pyautogui.press('backspace');
    pyautogui.press('backspace');
    pyautogui.press('backspace');

def write_number(number):
    pyautogui.write(str(number));

def GoHomeTown(location):
    ActivateWindow(c_default_window_pos, c_default_window_size, c_process_name);
    Navigate_map(location);
    if ClickOnButton(enter_home_button) is False:
        raise TimeOutError({'message':'Finding enter_home Error: TimedOut'});

def Navigate_map(location):
    #open map
    print('Finding map button');
    if ClickOnButton(map_button) is False:
        raise TimeOutError({'message':'Finding map button Error: TimedOut'});
    
    #Enter coordinate
    print('Locating coordinate buttons');
    start_time = InitTimer();
    while True:
        coordinate_list = list(locateCoordinateBox(map_coordinate_box));
        if len(coordinate_list) ==2: ## x and y coordinate box found
            break;
        if DelayAndTimeOut(start_time) is True:
            raise TimeOutError({'message':'Locating coordinate buttons Error: TimedOut'});
    print("Entering Coordinate", (location[0],location[1]));
    for i in range(2):
        click(coordinate_list[i], 30, 0);## offset to the actual coordinate field ,since the image used is the icon only
        clean_textbox();
        pyautogui.write(str(location[i]));
        
    #Confirm goto target
    print("Finding goto button");
    if ClickOnButton(map_goto_button) is False:
        raise TimeOutError({'message':'Finding goto Error: TimedOut'});

def FindTroopsImg(HomeLocation):
        try:
            GoHomeTown(HomeLocation);
            time.sleep(1);
            # this function find and capture img of troops for pyautogui to locate
            for i in range(len(c_troops)):
                #capture 5 available troops at specific location
                #if the capture image is invalid(no troop)
                troop_img_path = c_troops[i];
                troop_bbox = c_troops_bbox[i];
                if os.path.isfile(troop_img_path):
                    print('Removing existing troop image...');
                    os.remove(troop_img_path);
                img = pyautogui.screenshot(region=troop_bbox);
                isinvalid = pyautogui.locate(c_invalid_troop, img, grayscale=True, confidence = 0.9);
                if isinvalid is not None:
                    print('Invalid troop not added', troop_img_path);
                else:
                    print('saving image to ', troop_img_path);
                    img.save(troop_img_path);
        except TimeOutError as e:
            details = e.args[0];
            print(details['message']);
            return;
    
def SetNumberTimes(number_of_times):
    if number_of_times == -1:
        print('Selected nonstop attacking')
    else:
        if ClickOnButton(numbertimes_button) is False:
            raise TimeOutError({'message':'Finding numbertimes_button Error: TimedOut'});
        if ClickOnButton(numbertimes_button_list[number_of_times]) is False:
            raise TimeOutError({'message':'Finding number_of_times Error: TimedOut'});
        print('Selected attacking for ', number_of_times, ' times');
        
def AttackReturnHome(go_home_after_attack):
    if go_home_after_attack:
        if Button_exists(not_return_home_button): # not return home is currently selected, else its already set
            if ClickOnButton(not_return_home_button) is False: #checking the return home button 
                raise TimeOutError({'message':'Finding not_return_home_button Error: TimedOut'});
        print('Returning home after attack is selected');
    else:
        if Button_exists(return_home_button): # return home is currently selected, else its already set
            if ClickOnButton(return_home_button) is False:# Unchecking the return home button
                raise TimeOutError({'message':'Finding return_home_button Error: TimedOut'});
        print('Not returning home after attack is selected');

#click target
#find and click attack
def OrderToAttackTile(troop, return_home):
    print('Finding attack tile button...');
    if ClickOnButton(attack_tile_button) is False:
        raise TimeOutError({'message':'Finding attack_tile_button Error: TimedOut'});
        
    print('Selecting troop...');
    if ClickOnButton(troop) is False:
        raise TimeOutError({'message':'Finding troop Error: TimedOut'});
        
    print('Selecting return home option');
    AttackReturnHome(return_home);
    
    print('Finding confirm button...');
    if ClickOnButton(attack_tile_confirm_button) is False:
        raise TimeOutError({'message':'Finding attack_tile_confirm_button Error: TimedOut'});
        
    CheckForceAttack();
    print('Attacking Tile');
    
def OrderToAttackCity(troop, return_home, number_of_times = -1):
    print('Finding attack city button...');
    if ClickOnButton(attack_city_button) is False:
        raise TimeOutError({'message':'Finding attack_city_button Error: TimedOut'});
        
    print('Finding troop...');
    if ClickOnButton(troop) is False:
        raise TimeOutError({'message':'Finding troop Error: TimedOut'});
        
    print('Setting number of times...');
    SetNumberTimes(number_of_times);    
    
    print('Selecting return home option');
    AttackReturnHome(return_home);
    
    print('Finding confirm button...');
    if ClickOnButton(attack_city_confirm_button) is False:
        raise TimeOutError({'message':'Finding attack_city_confirm_button Error: TimedOut'});
        
    print('Attacking City');
    
def OrderToMove(troop):
    print('Find move button...');
    if ClickOnButton(move_button) is False:
        raise TimeOutError({'message':'Finding move_button Error: TimedOut'});
        
    print('Finding troop...');
    if ClickOnButton(troop) is False:
        raise TimeOutError({'message':'Finding troop Error: TimedOut'});
    
    print('Find confirm button...');
    if ClickOnButton(move_confirm_button) is False:
        raise TimeOutError({'message':'Finding move_confirm_button Error: TimedOut'});
        
    print('Moving Troop');
    
def CheckForceAttack():
    # ?????????????????? ????????????
    # appear only at some ocations
    # skipped after timeout
    print('Finding Force attack button');
    if ClickOnButton(force_attack_button) is False:
        raise TimeOutError({'message':'CheckForceAttack Error: TimedOut'});
    return True;

####################### Task Class
class Task:
    def __init__(self, mode, time, troop, target, delay, repeat, return_home):
        self.mode = mode;
        self.time = time;
        self.troop = troop;
        self.target = target;
        self.delay = delay;
        self.repeat = repeat;
        self.return_home = return_home;
        
    def task_handler(self):
        # logic of attacking or moving based of task
        # check mode then does sth
        # task : [mode, time, delay, target, troop]
        if self.mode == c_mode_city:
            Navigate_map(self.target);
            OrderToAttackCity(self.troop, self.return_home, self.repeat);
        elif self.mode == c_mode_tile:
            Navigate_map(self.target);
            OrderToAttackTile(self.troop, self.return_home);
        elif self.mode == c_mode_move:
            Navigate_map(self.target);
            OrderToMove(self.troop);
        else:
            raise InvalidValueError({'message':'InvalidValueError: Undefined Mode'});
            
    def check_time(self):
        #check current time and scheduled time
        start_time = self.time + datetime.timedelta(seconds = self.delay);
        print('waiting for time : ', start_time);
        while True:
            now = datetime.datetime.now();
            if start_time < now:
                print('Start Script : ', now);
                return True;
            print('waiting...');
            time.sleep((start_time-now).total_seconds()); 

#################
        
class AllTasks:
    def __init__(self):
        self.task_list = [];
        
    def AddTask(self, mode, time, troop, target, delay, repeat, return_home):
        newtask = Task(mode, time, troop, target, delay, repeat, return_home);
        #self.task_list.append(newtask);
        time_epsilon = datetime.timedelta(seconds = 0.001);
        newtask_time = time + datetime.timedelta(seconds = delay);
        for i in range(len(self.task_list)):
            thistask_time = self.task_list[i].time + datetime.timedelta(seconds = self.task_list[i].delay);
            if newtask_time >= thistask_time - time_epsilon and newtask_time <= thistask_time + time_epsilon:
                if False:
                    self.task_list.insert(i, newtask);## this section for sorting by troop name
                    print('task inserted at location ', i)
                    return;
            elif newtask_time < thistask_time:
                self.task_list.insert(i, newtask);
                print('task inserted at location ', i)
                return;
        self.task_list.append(newtask);
        
    def PrintTasks(self):
         for task in self.task_list:
            print('Remaining task. Mode:', task.mode, ' Time:',task.time, ' Troop:',task.troop, ' Target:',task.target, ' Delay:',task.delay, ' Repeat:',task.repeat, ' Return Home:',task.return_home);
        
    def RemoveTaskbyIndex(self, task_index):
         self.task_list.remove(self.task_list[task_index]);
         self.PrintTasks();
            
    def tasks_management(self):
        try:
            while self.task_list:
                task = self.task_list.pop(0);
                print('Handling task. Mode:', task.mode, ' Time:',task.time);
                # when time is due for the first task
                # execute it 
                if task.check_time() is True:
                    ActivateWindow(c_default_window_pos, c_default_window_size, c_process_name);
                    task.task_handler();
                    print('Task ', task.mode, task.time, ' is finished.');
        except InvalidValueError as e:
            details = e.args[0];
            print(details['message']);
        except TimeOutError as e:
            details = e.args[0];
            print(details['message']);
            
def SetTasks_JSON(file):
    alltasks = AllTasks();
    print('Loading Tasks');
    with open(file,'r') as file_object:  
        data = json.load(file_object);
    for task in data[c_json_task]:
        debug_message('Adding new task', task);
        task_time = [int(i) for i in task[c_time]];
        task_datetime = datetime.datetime(task_time[0], task_time[1], task_time[2], task_time[3], task_time[4], task_time[5]);
        alltasks.AddTask(task[c_mode], task_datetime, task[c_troop], task[c_target], task[c_attackdelay], task[c_repeat], task[c_return_home]);
    return alltasks;

alltasks = Init();

def main():
    alltasks = SetTasks_JSON(json_file_location);
    alltasks.tasks_management();

