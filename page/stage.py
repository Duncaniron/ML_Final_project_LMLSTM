import pygame
from Button.Button_main import Button, delButton,adminButton, chkIntruButton
import cv2
import subprocess
import time 
import os

# init the parameters
pygame.init()
fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
video = cv2.VideoCapture(r"background/hackingTheme.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)
screen_width, screen_height = 1920, 1080
LOGIN_font =[
"      _                _            ",    
"     | |    ___   __ _(_)_ __       ",
"     | |   / _ \ / _` | | '_ \     ", 
"     | |__| (_) | (_| | | | | |     ",
"     |_____\___/ \__, |_|_| |_|     ",
"                 |___/              ",
"                                    ",
"  "
]
rectangle_width, rectangle_height = 750,400
rectangle_x = (screen_width - rectangle_width) // 2
rectangle_y = (screen_height - rectangle_height) // 2

# WaitingStage
def waitingStage(stage, screen):
    global running, global_clicked, start_switch, name, flag, process, stdout, BUTTON_verify
    # init
    name = ''
    flag = 0
    process = ''
    stdout = ''
    global_clicked = False
    BUTTON_verify = 0
    start_switch = False
    rectangle_width, rectangle_height = 750,400
    rectangle_x = (screen_width - rectangle_width) // 2
    rectangle_y = (screen_height - rectangle_height) // 2
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (23, 255, 21), (rectangle_x, rectangle_y, rectangle_width, rectangle_height) , width=1)
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 15)
    for text in LOGIN_font:
        rectangle_y += 15
        text = fontIntro.render(text, True, (23, 201, 21))
        screen.blit(text, (rectangle_x + 220, rectangle_y))
    # Draw the rectangle
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 20)
    text = fontIntro.render("=========================================================", True, (23, 201, 21))
    screen.blit(text, (rectangle_x + 40, rectangle_y))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    text = fontIntro.render("Username:  ________admin_________", True, (23, 201, 21))
    screen.blit(text, (rectangle_x + 80, rectangle_y + 60))
    text = fontIntro.render("Password:  _______********_______", True, (23, 201, 21))
    screen.blit(text, (rectangle_x + 80, rectangle_y + 110))
    # Draw the button
    login_button = Button('login', rectangle_x + 200, rectangle_y + 200, 150, 50, fontIntro, 'LoginWarning')
    landmarkbutton = Button('LM-LSTM' , rectangle_x + 420, rectangle_y + 200, 150, 50, fontIntro, 'LM-LSTM')
    # print(fontIntro.get_height())
    stage = login_button.draw(screen, stage)
    stage = landmarkbutton. draw(screen, stage)

    return stage

# Login Warning sign
Warning_sign = [
"                                 .i;;;;i.                                  ",
"                               iYcviii;vXY:                                ",
"                            .YXi       .i1c.                               ",
"                            .YC.     .    in7.                             ",
"                           .vc.   ......   ;1c.                            ",
"                           i7,   ..        .;1;                            ",
"                          i7,   .. ...      .Y1i                           ",
"                         ,7v     .6MMM@;     .YX,                          ",
"                        .7;.   ..IMMMMMM1     :t7.                         ",
"                       .;Y.     ;$MMMMMM9.     :tc.                        ",
"                       vY.   .. .nMMM@MMU.      ;1v.                       ",
"                      i7i   ...  .#MM@M@C. .....:71i                       ",
"                     it:   ....   $MMM@9;.,i;;;i,;tti                      ",
"                    :t7.  .....   0MMMWv.,iii:::,,;St.                     ",
"                   .nC.   .....   IMMMQ..,::::::,.,czX.                    ",
"                  .ct:   ....... .ZMMMI..,:::::::,,:76Y.                   ",
"                  c2:   ......,i..Y$M@t..:::::::,,..inZY                   ",
"                 vov   ......:ii..c$MBc..,,,,,,,,,,..iI9i                  ",
"                i9Y   ......iii:..7@MA,..,,,,,,,,,....;AA:                 ",
"               iIS.  ......:ii::..;@MI....,............;Ez.                ",
"              .I9.  ......:i::::...8M1..................C0z.               ",
"             .z9;  ......:i::::,.. .i:...................zWX.              ",
"             vbv  ......,i::::,,.      ................. :AQY              ",
"            c6Y.  .,...,::::,,..:t0@@QY. ................ :8bi             ",
"           :6S. ..,,...,:::,,,..EMMMMMMI. ............... .;bZ,            ",
"          :6o,  .,,,,..:::,,,..i#MMMMMM#v.................  YW2.           ",
"         .n8i ..,,,,,,,::,,,,.. tMMMMM@C:.................. .1Wn           ",
"         7Uc. .:::,,,,,::,,,,..   i1t;,..................... .UEi          ",
"         7C...::::::::::::,,,,..        ....................  vSi.         ",
"         ;1;...,,::::::,.........       ..................    Yz:          ",
"          v97,.........                                     .voC.          ",
"           izAotX7777777777777777777777777777777777777777Y7n92:            ",
"             .;CoIIIIIUAA666666699999ZZZZZZZZZZZZZZZZZZZZ6ov.              ",                                                                           
]
# Login Warning content
Warning_content = ["The current username-password login method is deprecated",
                   "and insecure. ",
                   " ",
                   "Please use LM-LSTM instead!"]

def LoginWarning(stage, screen):
    # init
    rectangle_width, rectangle_height = 750,400
    rectangle_x = (screen_width - rectangle_width) // 2
    rectangle_y = (screen_height - rectangle_height) // 2
    y = 400
    screen.fill((0, 0, 0))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 10)
    fontIntro.set_bold(True)
    for text in Warning_sign:
        text = fontIntro.render(text, True, (255,69,0))
        screen.blit(text, ( 220, y))
        y += 10
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 50)
    text = fontIntro.render('Warning', False, (255,69,0))
    screen.blit(text, ( 650, 350))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 25)
    y = 450
    for text in Warning_content:
        text = fontIntro.render(text, False, (255,69,0))
        screen.blit(text, ( 650, y))
        y += 30
    # Draw the button
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    landmarkbutton = Button('LM-LSTM' , rectangle_x + 920, rectangle_y + 500, 150, 50, fontIntro, 'LM-LSTM')
    
    return  landmarkbutton.draw(screen, stage)
    


# Verify stage
def VerifyStage(stage, screen):
    # init
    screen.fill((0, 0, 0))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    text = fontIntro.render('Go to admin or login based on the result of KNN', False, (255,69,0))
    screen.blit(text, ( 550, 400))
    # Draw the button
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    admin_tmp_button = Button('admin', rectangle_x + 200, rectangle_y + 200, 150, 50, fontIntro, 'admin')
    user_tmp_button = Button('user' , rectangle_x + 420, rectangle_y + 200, 150, 50, fontIntro, 'login')
    # button reflect the page and return the stage
    stage = admin_tmp_button.draw(screen, stage)
    stage = user_tmp_button. draw(screen, stage)

    return stage

# init the parameters
Greeting_Admin = ">  Welcome Admin. What would you like to do today?"
start_switch = False
typing_speed = 20  
start_time = 0
cursor_blink_speed = 0.5
cursor_last_toggle = 0
cursor_visible = True

# Admin stage
def AdminStage(stage, screen):
    global start_switch, typing_speed, start_time, cursor_visible, cursor_last_toggle, global_clicked
    # init
    cursor_blink_speed = 0.5
    screen.fill((0, 0, 0))
    global_clicked = False
    if(start_switch == False):
        start_time = time.time()
        start_switch = True
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    # Calculate the number of characters to display based on elapsed time
    characters_to_display = int(elapsed_time * typing_speed)
    visiable_text = Greeting_Admin[:characters_to_display]
    # Toggle cursor visibility based on the blink speed
    if time.time() - cursor_last_toggle > cursor_blink_speed:
        cursor_visible = not cursor_visible
        cursor_last_toggle = time.time()
    # Append cursor to visible text
    if cursor_visible:
        visiable_text += '|'
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 35)
    text_surface = fontIntro.render(visiable_text, True, (23, 201, 21))
    screen.blit(text_surface, (250, 200))
    # Draw the button
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    adduser_button = adminButton('[+] Add user', 315, 290, 350,  35, fontIntro, 'addingUser')
    chk_intruder_button = adminButton('[+] Check Intruder' , 315, 330, 350, 35, fontIntro, 'chkIntruder')
    del_usre_button = adminButton('[+] Delete user', 315, 370, 350, 35, fontIntro, 'delUser')
    logout_button = adminButton('[+] Logout', 315, 410, 350, 35, fontIntro, 'waiting')

    # button reflect the page and return the stage
    stage,global_clicked = adduser_button.draw(screen, stage, global_clicked)
    stage, global_clicked = del_usre_button. draw(screen, stage, global_clicked)
    stage, global_clicked = chk_intruder_button.draw(screen, stage, global_clicked)
    stage, global_clicked = logout_button.draw(screen, stage, global_clicked)

    return stage


LMLSTM_text = ['We shall employ Face Landmark technology for the purpose of identity verification.', 
               'This advanced system will enable us to discern and confirm individual identities', 
               'with precision and reliability...']

def LMLSTM(stage, screen):
    # init
    y = 400
    screen.fill((0, 0, 0))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 27)
    for text in LMLSTM_text:    
        text = fontIntro.render(text, False, (255,69,0))
        screen.blit(text, ( 330, y))
        y += 30
    # Draw the button
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    fontIntro.set_bold(True)
    verifybutton = Button('Understand and Verify' , rectangle_x + 120, rectangle_y + 400, 500, 50, fontIntro, 'Verify')
    return verifybutton.draw(screen,stage)


buttontime = 0
Enterlogin = False

def Login(stage, screen):
    global Inturder_index, start_switch, typing_speed, start_time, cursor_visible, cursor_last_toggle, global_clicked
    # init
    Inturder_index = 0
    Greeting_User = ">  Welcome User. What would you like to do today?"
    cursor_blink_speed = 0.5
    screen.fill((0, 0, 0))
    global_clicked = False
    if(start_switch == False):
        start_time = time.time()
        start_switch = True
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    # Calculate the number of characters to display based on elapsed time
    characters_to_display = int(elapsed_time * typing_speed)
    visiable_text = Greeting_User[:characters_to_display]
    # Toggle cursor visibility based on the blink speed
    if time.time() - cursor_last_toggle > cursor_blink_speed:
        cursor_visible = not cursor_visible
        cursor_last_toggle = time.time()
    # Append cursor to visible text
    if cursor_visible:
        visiable_text += '|'
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 35)
    text_surface = fontIntro.render(visiable_text, True, (23, 201, 21))
    screen.blit(text_surface, (250, 200))
    # Draw the button
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    adduser_button = adminButton('[+] Check Intruder', 315, 290, 350,  35, fontIntro, 'chkIntruderUsr')
    presentation_button = adminButton('[+] Presentation' , 315, 330, 350, 35, fontIntro, 'presentation')
    del_usre_button = adminButton('[+] Logout', 315, 370, 350, 35, fontIntro, 'waiting')
    stage,global_clicked = adduser_button.draw(screen, stage, global_clicked)
    stage, global_clicked = del_usre_button. draw(screen, stage, global_clicked)
    stage, global_clicked = presentation_button.draw(screen, stage, global_clicked)

    return stage

# init the parameters
face_path = './demo_webcam_smooth.py'
name = ''
flag = 0
process = ''
stdout = ''
global_clicked = False
BUTTON_verify = 0

def verifyStage(stage, screen):
    global BUTTON_verify, global_clicked, name, face_path, flag, process, stdout

    # Check if the mouse is clicked and calculate the number of clicks
    if pygame.mouse.get_pressed()[0] == 1 and not global_clicked:
        global_clicked = True
        print("clicked")
        if BUTTON_verify < 3:
            BUTTON_verify += 1
    if pygame.mouse.get_pressed()[0] == 0 and global_clicked:
        global_clicked = False
        print('released')
    # the stage of verify according to the number of clicks
    if BUTTON_verify == 0:
        screen.fill((0, 0, 0))
        fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
        text = fontIntro.render("click to verify", True, (23, 201, 21))
        screen.blit(text, (300, 300))
    elif BUTTON_verify == 1:
        screen.fill((0, 0, 0))
        fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
        if flag == 0:
            stdout = 'n'
            process = subprocess.Popen(['python3', face_path], stdout=subprocess.PIPE, text=True)
            time.sleep(1)
            flag = 1
        elif flag == 1:
            stdout, _ = process.communicate()
            stdout = (stdout.splitlines())[-1]
            flag = 2
        elif flag == 2:
            if(stdout == 'Intruder'):
                BUTTON_verify = 2
            fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 40)
            Text = "Login as " + stdout + "...."
            text = fontIntro.render(Text, True, (23, 201, 21))
            screen.blit(text, (750, 500))
            pass
    elif BUTTON_verify == 2:
        if(stdout != 'Intruder'):
            if(stdout == 'Duncan'):
                stage = 'admin'
            else:
                stage = 'login'
        else:
            stage = "IntruderDetected"
    elif BUTTON_verify == 3:
        stage = 'quit'

    return stage

def AddUser(stage,screen, input_string):
    global flag, cursor_last_toggle, cursor_visible
    # init
    cursor_blink_speed = 0.5
    flag = 0
    screen.fill((0, 0, 0))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 35)
    text = fontIntro.render('Enter the name of new user : ', True, (23, 201, 21))
    screen.blit(text, (250, 200))
    # Render the input string
    input_string = '> ' + input_string 

    # Toggle cursor visibility based on the blink speed
    if time.time() - cursor_last_toggle > cursor_blink_speed:
        cursor_visible = not cursor_visible
        cursor_last_toggle = time.time()
    # Append cursor to visible text
    if cursor_visible:
        input_string += '|'
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    text = fontIntro.render(input_string, True, (23, 201, 21))
    screen.blit(text, (315, 290))
    # Draw the button and return the stage
    admin_tmp_button = Button('Go back', 1400, 900, 150, 50, fontIntro, 'admin')
    stage = admin_tmp_button.draw(screen, stage)

    return stage


def ActAdduser(stage , screen, input_string):
    global flag, process
    # use flag to control the process
    if flag == 0:
        process = subprocess.Popen(['python3', face_path, '-name', input_string], stdout=subprocess.PIPE, text=True)
        time.sleep(1)
        flag = 1
    elif flag == 1:
        process.wait()
        flag = 2
    elif flag == 2:
        stage = "admin"
        pass
    # init
    screen.fill((0, 0, 0))
    # Render the input string
    text = fontIntro.render(input_string, True, (23, 201, 21))
    screen.blit(text, (300, 300, 500, 500))
    return stage

def get_current_user():
    dir_path = 'degree_data_4/0'
    all_user = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    all_user.remove('Duncan')
    return all_user


def delUser(stage, screen):
    global global_clicked
    all_user = get_current_user()

    # init
    screen.fill((0, 0, 0))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 35)
    text = fontIntro.render('> Choose the user you want to delete: ', True, (23, 201, 21))
    screen.blit(text, (250, 200))
    
    # Draw the button for different user
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    for i, usr in enumerate(all_user):
        if pygame.mouse.get_pressed()[0] == 0 and global_clicked:
            global_clicked = False
        delusrbutton = delButton(usr , 315, 290 + i * 35, 300, 32, fontIntro, 'delUser')
        stage , global_clicked = delusrbutton.draw(screen,stage, global_clicked)
    # Draw the button and return the stage
    admin_tmp_button = Button('Go back', 1400, 800, 150, 50, fontIntro, 'admin')
    stage = admin_tmp_button.draw(screen, stage)
    return stage

def get_all_intruder():
    dir_path = 'intruder'
    all_intruder = [f for f in os.listdir(dir_path) if f.lower().endswith('.png')]

    return all_intruder


Inturder_num = 0
Inturder_index = 0

def chkIntruder(stage, screen):  
    global Inturder_num, Inturder_index, global_clicked
    # init
    screen.fill((0, 0, 0))
    all_intruder = get_all_intruder()
    Inturder_num = len(all_intruder)
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 35)
    text = fontIntro.render('> Threat Alert Center', True, (23, 201, 21))
    screen.blit(text, (250, 200))
    # Draw the image
    image = pygame.image.load("intruder/" + all_intruder[Inturder_index])
    image_rect = image.get_rect()
    x_position = (1920 - image_rect.width) // 3 
    y_position = ((1080 - image_rect.height) // 2 )
    image_rect.x = x_position
    image_rect.y = y_position
    screen.blit(image, image_rect)
    # Draw the button and get the return stage
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    admin_tmp_button = Button('Go back', 1400, 800, 150, 50, fontIntro, 'admin')
    stage = admin_tmp_button.draw(screen, stage)
    # Draw the button for switching the image
    go_right =  chkIntruButton('>', 850, 800, 150, 50, fontIntro)
    go_left = chkIntruButton('<', 450, 800, 150, 50, fontIntro)
    Inturder_index, global_clicked =  go_right.draw(screen,Inturder_index,global_clicked, 1, Inturder_num)
    Inturder_index, global_clicked = go_left.draw(screen, Inturder_index, global_clicked, -1, Inturder_num)
    pos = str(Inturder_index + 1) + '/' + str(Inturder_num)
    text = fontIntro.render(pos , True, (23, 201, 21))
    screen.blit(text, (700, 810))
    return stage

intruder_text = ["Intruder", "Alert!!!"]
intruder_timer = 0
inturder_bool = False

def IntruderDetected(stage, screen):
    global intruder_text, intruder_timer, inturder_bool
    if(not inturder_bool):
        intruder_timer = time.time()
        inturder_bool = True
    # init
    y = 400
    screen.fill((0, 0, 0))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 80)
    fontIntro.set_bold(True)
    for text in intruder_text:
        text = fontIntro.render(text, True, (255,69,0))
        screen.blit(text, ( 750, y))
        y += 100
    y += 100
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 40)
    text = fontIntro.render("Return to main page in " + \
                            str(int(7 - (time.time() - intruder_timer)))  \
                            +" sec.." , True, (255,69,0))
    screen.blit(text, ( 600, y))
    # if the time is over 7 sec, return to the main page
    if(time.time() - intruder_timer > 7):
        stage = 'waiting'
        inturder_bool = False

    return stage


def get_all_slide():
    dir_path = 'presentation'
    all_slide = [f for f in os.listdir(dir_path) if f.lower().endswith('.png')]

    return all_slide

def presentation(stage, screen):  
    global Inturder_num, Inturder_index, global_clicked
    # init
    screen.fill((0, 0, 0))
    all_slide = get_all_slide()
    Inturder_num = len(all_slide)
    # Draw the image
    image = pygame.image.load("presentation/" + all_slide[Inturder_index])
    image_rect = image.get_rect()
    x_position = (1920 - image_rect.width) // 2 
    y_position = (1080 - image_rect.height) // 2 
    image_rect.x = x_position
    image_rect.y = y_position
    screen.blit(image, image_rect)
    # Draw the button and get the return stage
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    admin_tmp_button = Button('<<', 200, 110 , 50, 30, fontIntro, 'login')
    stage = admin_tmp_button.draw(screen, stage)
    # Draw the button for switching the image
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    go_left = chkIntruButton('<', 750, 870, 150, 50, fontIntro)
    go_right =  chkIntruButton('>', 1070 , 870, 150, 50, fontIntro)
    Inturder_index, global_clicked =  go_right.draw(screen,Inturder_index,global_clicked, 1, Inturder_num)
    Inturder_index, global_clicked = go_left.draw(screen, Inturder_index, global_clicked, -1, Inturder_num)
    pos = str(Inturder_index + 1) + '/' + str(Inturder_num)
    text = fontIntro.render(pos , True, (23, 201, 21))
    screen.blit(text, (960, 880))
    return stage


def chkIntruderUsr(stage, screen):  
    global Inturder_num, Inturder_index, global_clicked
    # init
    screen.fill((0, 0, 0))
    all_intruder = get_all_intruder()
    Inturder_num = len(all_intruder)
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 35)
    text = fontIntro.render('> Threat Alert Center', True, (23, 201, 21))
    screen.blit(text, (250, 200))
    # Draw the image
    image = pygame.image.load("intruder/" + all_intruder[Inturder_index])
    image_rect = image.get_rect()
    x_position = (1920 - image_rect.width) // 3 
    y_position = ((1080 - image_rect.height) // 2 )
    image_rect.x = x_position
    image_rect.y = y_position
    screen.blit(image, image_rect)
    # Draw the button and get the return stage
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    admin_tmp_button = Button('Go back', 1400, 800, 150, 50, fontIntro, 'login')
    stage = admin_tmp_button.draw(screen, stage)
    # Draw the button for switching the image
    go_right =  chkIntruButton('>', 850, 800, 150, 50, fontIntro)
    go_left = chkIntruButton('<', 450, 800, 150, 50, fontIntro)
    Inturder_index, global_clicked =  go_right.draw(screen,Inturder_index,global_clicked, 1, Inturder_num)
    Inturder_index, global_clicked = go_left.draw(screen, Inturder_index, global_clicked, -1, Inturder_num)
    pos = str(Inturder_index + 1) + '/' + str(Inturder_num)
    text = fontIntro.render(pos , True, (23, 201, 21))
    screen.blit(text, (700, 810))
    return stage