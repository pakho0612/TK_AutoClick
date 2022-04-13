import pyautogui
import datetime
import pygetwindow
import time
#windows click
# GUI to set troops


#################### Internal constant
c_process_name = '三國志';
c_default_window_pos = (10,10);
c_default_window_size = (1104,651);
c_timeout = 5;#seconds
c_forceattack_timeout = 2;
c_delay = 0.25;#seconds
debug = 0;

c_mode_city = 'attack_city';
c_mode_tile = 'attack_tile';
c_mode_move = 'move';
c_mode = 'mode';
c_troop = 'troop';
c_time = 'time';
c_attackdelay = 'delay';
c_target = 'target';
c_repeat = 'repeat';

img_location = './src/';

##################### Source 
map_button = img_location + 'map_button.png';
map_coordinate_box = img_location + 'map_coordinate_box.png';
map_goto_button = img_location + 'map_goto_button.png';
attack_city_button = img_location + 'attack_button.png';
attack_city_confirm_button = img_location + 'attack_confirm_button.png';
attack_tile_button = img_location + 'attack_tile_button.png';
attack_tile_confirm_button = img_location + 'attack_tile_confirm_button.png';
force_attack_button = img_location + 'force_attack_button.PNG';
numbertimes_button = img_location + 'number_times.PNG';
once_button = img_location + 'once.PNG';
twice_button = img_location + 'twice.PNG';
threetimes_button = img_location + 'three_times.PNG';
numbertimes_button_list = {1:once_button, 2:twice_button, 3:threetimes_button};

#################### Debug/Error Functions
class TimeOutError(Exception):
    pass

class InvalidValueError(Exception):
    pass

def debug_message(*args, **kwargs):
    if debug == 1:
        print("    " + " ".join(map(str,args)), **kwargs);
#################### System Functions
def WindowResizing(default_window_pos, default_window_size, process_name):
    # for later: may rescale cv image instead
    # 
    win_handle = pygetwindow.getWindowsWithTitle(process_name)[0];
    win_handle.activate();#try both to get the window active
    win_handle.restore(); #
    win_handle.moveTo(default_window_pos[0], default_window_pos[1]);
    win_handle.resizeTo(default_window_size[0], default_window_size[1]);

def Init():
    # Load constants from JSON
    WindowResizing(c_default_window_pos, c_default_window_size, c_process_name);

def InitTimer():
    print('Started Timeout timer');
    return time.time();

def DelayAndTimeOut(start_time):
    # Reduce CPU usage while polling for locate functions
    if time.time() > (start_time + c_timeout):
        raise TimeOutError({'message':'TimedOut'});
        return False;
    time.sleep(c_delay);

#################### User Functions    
def locate(picture, conf = 0.9):
    #pyautogui.locateOnScreen('someButton.png', region=(0,0, 300, 400))
    # return None
    try:
        search_region = (c_default_window_pos[0],c_default_window_pos[1], c_default_window_size[0], c_default_window_size[1]);
        button_location = pyautogui.locateOnScreen(picture, confidence = conf, grayscale = True, region = search_region);
        debug_message("@locate bbox ", button_location);
        return button_location;
    except :
        debug_message("Unexpected error in locate function");

def locateCoordinateBox(picture, conf = 0.87):
    #pyautogui.locateOnScreen('someButton.png', region=(0,0, 300, 400))
    # return None
    try:
        #Searching only at bottom right quarter
        search_region = (c_default_window_pos[0]+round(c_default_window_size[0]/2),c_default_window_pos[1]+round(c_default_window_size[1]/2), c_default_window_size[0], c_default_window_size[1]);
        #search_region = (c_default_window_pos[0],c_default_window_pos[1], c_default_window_size[0], c_default_window_size[1]);
        button_location = pyautogui.locateAllOnScreen(picture, confidence = conf, region = search_region);
        debug_message("@locateCoordinateBox bbox ", button_location);
        return button_location;
    except :
        debug_message("Unexpected error in locateCoordinateBox function");
        return False;

def ClickOnButton(image):
    # Finding an important button to press
    start_time = InitTimer();
    while True:
        button = locate(image);
        if button is not None:
            break;
        DelayAndTimeOut(start_time);
    debug_message('button found at ', button);
    click(button);
        
def click(button_bbox):
    button_x, button_y = pyautogui.center(button_bbox);
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
    
    
def check_time(attack_time, attack_time_offset):
#check current time and scheduled time
    if len(attack_time) == 6:
        time_num = [];
        for i in attack_time:
            time_num.append(int(i));
        print('waiting for time');
        start_time = datetime.datetime(time_num[0],time_num[1],time_num[2],time_num[3],time_num[4],time_num[5]);
        start_time = start_time + datetime.timedelta(seconds = attack_time_offset);
        print(start_time);
        while True:
            now = datetime.datetime.now();
            if start_time < now:
                print('Start Script');
                print(now);
                return True;
            time.sleep(c_delay); # Polling bad, calculate time diff and sleep until then
    else:
        raise InvalidValueError({'message':'time entry is missing'});
        return False;
        
#2
def Navigate_map(location):
    #open map
    print('Finding Map button');
    ClickOnButton(map_button);
    
    #Enter coordinate
    print('Locating coordinate buttons');
    start_time = InitTimer();
    while True:
        coordinate_list = list(locateCoordinateBox(map_coordinate_box));
        if len(coordinate_list) ==2:
            print(coordinate_list);
            print(len(coordinate_list));
            break;
        DelayAndTimeOut(start_time);
    print("Entering Coordinate")
    for i in range(2):
        click(coordinate_list[i]);
        clean_textbox();
        pyautogui.write(str(location[i]));
        
    #Confirm goto target
    print("Finding Goto button");
    ClickOnButton(map_goto_button);

def SetNumberTimes(number_of_times):
    if number_of_times == -1:
        print('Selected nonstop attacking')
        return ;
    else:
        ClickOnButton(numbertimes_button);
        ClickOnButton(numbertimes_button_list[number_of_times]);
        print('Selected attacking for ', number_of_times, ' times');
        return;

#click target
#find and click attack
def OrderToAttackTile(troop):
    print('Finding attack tile button...');
    ClickOnButton(attack_tile_button);
    print('Finding troop...');
    ClickOnButton(troop);
    print('Finding confirm button...');
    ClickOnButton(attack_tile_confirm_button);
    CheckForceAttack();
    print('Attacking Tile');
    
def OrderToAttackCity(troop, number_of_times = -1):
    print('Finding attack tile button...');
    ClickOnButton(attack_city_button);
    print('Finding troop...');
    ClickOnButton(troop);
    print('Setting number of times...');
    SetNumberTimes(number_of_times)
    print('Finding attack tile button...');
    ClickOnButton(attack_city_confirm_button);
    print('Attacking City');
    
def CheckForceAttack():
    # 兵力差距過大 堅持出征
    # appear only at some ocations
    # skipped after timeout
    print('Finding Force attack button');
    start_time = time.time();
    while True:
        button = locate(force_attack_button);
        if button is not None:
            break;
        if time.time() > (start_time + c_forceattack_timeout):
            print('No force attack button found');
            return;
        time.sleep(c_delay);
    click(button);

def task_handler(task):
    # logic of attacking or moving based of task
    # check mode then does sth
    # task : [mode, time, delay, target, troop]
    if task[c_mode] == c_mode_city:
        Navigate_map(task[c_target]);
        OrderToAttackCity(task[c_troop], task[c_repeat]);
    elif task[c_mode] == c_mode_tile:
        Navigate_map(task[c_target]);
        OrderToAttackTile(task[c_troop]);
    elif task[c_mode] == c_mode_move:
        print('moving troop')
    else:
        raise InvalidValueError({'message':'InvalidValueError: Undefined Mode'});
        return False;

def tasks_management(task_list):
    try:
        while task_list:
            task = task_list.pop(0);
            print('Handling task. Mode:', task[c_mode], ' Time:',task[c_time]);
            # when time is due for the first task
            # execute it 
            if check_time(task[c_time], task[c_attackdelay]) is True:
                task_handler(task);
                print('Task ', task[c_mode], task[c_time], ' is finished.');
    except InvalidValueError as e:
        details = e.args[0];
        print(details['message']);
    except TimeOutError as e:
        details = e.args[0];
        print(details['message']);
            
def main():
    Init();
    
    ##################
    troop1 = './src/troop1.png';
    troop2 = './src/troop2.png';
    #city
    target_location = (1304,667);
    attack_time_delay = 120; #seconds
    attack_time = ['2022','04','11','09','00','00'];
    number_of_times = 3; # -1=inf
    #tiles
    target_location2 = (1479,472);
    attack_time_delay2 = 0; #seconds
    attack_time2 = ['2022','04','11','07','05','50'];
    ###################
    # currently need to manually queue orders if the units currently on same tile outside home
    task_list = [];
    task1 = {c_mode:'attack_tile', c_time: attack_time2, c_attackdelay:attack_time_delay2, c_troop:troop1, c_target:target_location2, c_repeat:number_of_times};
    task2 = {c_mode:'attack_city', c_time: attack_time, c_attackdelay:attack_time_delay, c_troop:troop2, c_target:target_location, c_repeat:number_of_times};
    task_list.append(task1);
    task_list.append(task2);
    tasks_management(task_list);
    

main();
