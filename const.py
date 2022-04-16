
#################### Internal constant
c_process_name = '三國志';
c_default_window_pos = (10,10);
c_default_window_size = (1104,651);
c_GUI_size = (1440,300);
c_timeout = 5;#seconds
c_forceattack_timeout = 2;
c_verify_timeout = 2;
c_delay = 0.25;#seconds
debug = 1;

c_mode_city = 'attack_city';
c_mode_tile = 'attack_tile';
c_mode_move = 'move';
c_mode = 'mode';
c_time = 'time';
c_troop = 'troop';
c_target = 'target';
c_attackdelay = 'delay';
c_repeat = 'repeat';
c_return_home = 'return_home';

img_location = './src/';
usrdata_location = './usr/';
tasks_file = 'tasks.json';
c_json_task = 'Tasks';
c_troop1 = usrdata_location + 'troop1.PNG';
c_troop2 = usrdata_location + 'troop2.PNG';
c_troop3 = usrdata_location + 'troop3.PNG';
c_troop4 = usrdata_location + 'troop4.PNG';
c_troop5 = usrdata_location + 'troop5.PNG';
c_invalid_troop = img_location + 'invalid_troop.PNG';
c_troops = [c_troop1, c_troop2, c_troop3, c_troop4, c_troop5];
c_troops_imgsize = (85,83); #110,605
c_troop1_bbox = (25,518,c_troops_imgsize[0],c_troops_imgsize[1]);
c_troop2_bbox = (241,518,c_troops_imgsize[0],c_troops_imgsize[1]);
c_troop3_bbox = (458,518,c_troops_imgsize[0],c_troops_imgsize[1]);
c_troop4_bbox = (675,518,c_troops_imgsize[0],c_troops_imgsize[1]);
c_troop5_bbox = (893,518,c_troops_imgsize[0],c_troops_imgsize[1]);
c_troops_bbox = [c_troop1_bbox,c_troop2_bbox,c_troop3_bbox,c_troop4_bbox,c_troop5_bbox];
##################### Source 
map_button = img_location + 'map_button.png';
map_coordinate_box = img_location + 'map_coordinate_box.png';
map_goto_button = img_location + 'map_goto_button.png';

attack_city_button = img_location + 'attack_button.png';
attack_city_confirm_button = img_location + 'attack_confirm_button.png';
attack_tile_button = img_location + 'attack_tile_button.png';
attack_tile_confirm_button = img_location + 'attack_tile_confirm_button.png';
return_home_button = img_location + 'return_home_button.PNG';
not_return_home_button = img_location + 'not_return_home_button.PNG';
force_attack_button = img_location + 'force_attack_button.PNG';
enter_home_button = img_location + 'enterhome.PNG';

numbertimes_button = img_location + 'number_times.PNG';
once_button = img_location + 'once.PNG';
twice_button = img_location + 'twice.PNG';
threetimes_button = img_location + 'three_times.PNG';
numbertimes_button_list = {1:once_button, 2:twice_button, 3:threetimes_button};

move_button = img_location + 'move_button.PNG';
move_confirm_button = img_location + 'move_confirm_button.PNG';