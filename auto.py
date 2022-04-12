import pyautogui
import datetime
import pygetwindow
#windows click
# GUI to set troops

map_button = './src/map_button.png';
map_coordinate_box = './src/map_coordinate_box.png';
map_goto_button = './src/map_goto_button.png';
attack_button = './src/attack_button.png';
attack_confirm_button = './src/attack_confirm_button.png';
attack_tile_button = './src/attack_tile_button.png';
attack_tile_confirm_button = './src/attack_tile_confirm_button.png';
numbertimes_button = './src/number_times.PNG';
once_button = './src/once.PNG';
twice_button = './src/twice.PNG';
threetimes_button = './src/three_times.PNG';
numbertimes_button_list = {1:once_button, 2:twice_button, 3:threetimes_button};

troop1 = './src/troop1.png';
troop2 = './src/troop2.png';
#city
target_location = (1465,454);
attack_time_offset = 120; #seconds
attack_time = ['2022','04','11','09','00','00'];
number_of_times = 3; # -1=inf 
#tiles
target_location2 = (1475,455);
attack_time_offset2 = 0; #seconds
attack_time2 = ['2022','04','11','07','05','50'];

#################### Internal constant
process_name = '三國志';
default_window_pos = (10,10);
default_window_size = (1104,651);
debug = 1;

####################
def WindowResizing(default_window_pos, default_window_size):
    # for later: may rescale cv image instead
    # 
    win_handle = pygetwindow.getWindowsWithTitle('三國志')[0];
    win_handle.activate();#try both to get the window active
    win_handle.restore(); #
    win_handle.moveTo(default_window_pos[0], default_window_pos[1]);
    win_handle.resizeTo(default_window_size[0], default_window_size[1]);

def Init():
    # Load constants from JSON
    WindowResizing(default_window_pos, default_window_size);

def debug_message(*args, **kwargs):
    if debug == 1:
        print("    " + " ".join(map(str,args)), **kwargs);

#################### User Functions    
def locate(picture, conf = 0.9):
    #pyautogui.locateOnScreen('someButton.png', region=(0,0, 300, 400))
    # return None
    try:
        map_button_location = pyautogui.locateOnScreen(picture, confidence = conf, grayscale=True, region=(default_window_pos[0],default_window_pos[1], default_window_size[0], default_window_size[1]));
        debug_message("map bbox ", map_button_location);
        return map_button_location;
    except :
        debug_message("Unexpected error");
        return False;

def locateAll(picture, conf = 0.87):
    #pyautogui.locateOnScreen('someButton.png', region=(0,0, 300, 400))
    # return None
    try:
        map_button_location = pyautogui.locateAllOnScreen(picture, confidence = conf, region=(default_window_pos[0],default_window_pos[1], default_window_size[0], default_window_size[1]));
        debug_message("map bbox ", map_button_location);
        return map_button_location;
    except :
        debug_message("Unexpected error");
        return False;

def ClickOnButton(image):
    while True:
        button = locate(image);
        if button is not None:
            break;
    debug_message('button found at ', button);
    click(button);
        
def click(button_bbox):
    button_x, button_y = pyautogui.center(button_bbox);
    debug_message("button click on ",button_x, button_y)
    pyautogui.click(button_x, button_y)
    debug_message("button clicked")

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

#攻城
#1時間,2地點,3出擊,4隊伍,4確定

#1
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
    else:
        debug_message('Invalid timestamp');
        return False;
#2
def Navigate_map(location):
    #open map
    ClickOnButton(map_button);
    print("map opened")
    
    #Enter coordinate
    while True:
        coordinate_list = list(locateAll(map_coordinate_box));
        if len(coordinate_list) ==2:
            print(coordinate_list);
            print(len(coordinate_list));
            break;
    print("Entering Coordinate")
    for i in range(2):
        click(coordinate_list[i]);
        clean_textbox();
        pyautogui.write(str(location[i]));
        
    #Confirm goto target
    ClickOnButton(map_goto_button);
    print("Going to target location");

def SetNumberTimes(number_of_times):
    if number_of_times == -1:
        print('nonstop attacking')
        return ;
    else:
        ClickOnButton(numbertimes_button);
        ClickOnButton(numbertimes_button_list[number_of_times]);
        print('attacking for ', number_of_times, ' times');
        return;

#click target
#find and click attack
def OrderToAttack(attack, troop, confirm, number_of_times):
    ClickOnButton(attack);
    ClickOnButton(troop);
    SetNumberTimes(number_of_times)
    ClickOnButton(confirm);
    print('Attacking... 1/1');

def MultipleAttack(target_location, attack, troops, confirm, number_of_times):
    Navigate_map(target_location);
    count = 0;
    total = len(troops);
    for troop in troops:
        OrderToAttack(attack, troop, confirm, number_of_times);
        count = count + 1;
        print('Attacking... ', count, '/', total);
        
def main():
    Init();
    check_time(attack_time, attack_time_offset);
    Navigate_map(target_location);
    OrderToAttack(attack_button, troop1, attack_confirm_button, number_of_times);

    ## for attack a specific tile
    #check_time(attack_time2, attack_time_offset2);
    #Navigate_map(target_location2);
    #OrderToAttack(attack_tile_button, troop2, attack_tile_confirm_button);

main();
