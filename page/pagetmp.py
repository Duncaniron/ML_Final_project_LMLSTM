import pygame
from Button.Button_main import Button
import cv2
import subprocess

pygame.init()
fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 15)
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
    global running, global_clicked
    # init
    rectangle_width, rectangle_height = 750,400
    rectangle_x = (screen_width - rectangle_width) // 2
    rectangle_y = (screen_height - rectangle_height) // 2
    screen.fill((0, 0, 0))
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
    # Draw the text
    text = fontIntro.render("Password:  _______********_______", True, (23, 201, 21))
    screen.blit(text, (rectangle_x + 80, rectangle_y + 110))
    # Draw the text
    login_button = Button('login', rectangle_x + 200, rectangle_y + 200, 150, 50, fontIntro, 'LoginWarning')
    landmarkbutton = Button('LM-LSTM' , rectangle_x + 420, rectangle_y + 200, 150, 50, fontIntro, 'LM-LSTM')
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
Warning_content = ["The current username-password login method is deprecated and insecure. ",
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
    screen.blit(text, ( 650, 400))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 25)
    y = 480
    for text in Warning_content:
        text = fontIntro.render(text, False, (255,69,0))
        screen.blit(text, ( 650, y))
        y += 30
    # Draw the text
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
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    admin_tmp_button = Button('admin', rectangle_x + 200, rectangle_y + 200, 150, 50, fontIntro, 'admin')
    user_tmp_button = Button('user' , rectangle_x + 420, rectangle_y + 200, 150, 50, fontIntro, 'login')
    # Draw the text for different user
    stage = admin_tmp_button.draw(screen, stage)
    stage = user_tmp_button. draw(screen, stage)

    return stage

# Admin stage
def AdminStage(stage, screen):
    # init 
    screen.fill((0, 0, 0))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    admin_tmp_button = Button('Add user', rectangle_x + 100, rectangle_y + 200, 150, 50, fontIntro, 'admin')
    user_tmp_button = Button('Check Intruder' , rectangle_x + 420, rectangle_y + 200, 350, 50, fontIntro, 'admin')
    # Draw the text for different user
    stage = admin_tmp_button.draw(screen, stage)
    stage = user_tmp_button. draw(screen, stage)

    return stage


LMLSTM_text = ['We shall employ Face Landmark technology for the purpose of identity verification.', 
               'This advanced system will enable us to discern and confirm individual identities', 
               'with precision and reliability']

def LMLSTM(stage, screen):
    # init
    y = 400
    screen.fill((0, 0, 0))
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    for text in LMLSTM_text:    
        text = fontIntro.render(text, False, (255,69,0))
        screen.blit(text, ( 250, y))
        y += 30
    # Draw the text
    fontIntro = pygame.font.Font(r'page/OCRAEXT.TTF', 30)
    fontIntro.set_bold(True)
    verifybutton = Button('Understand and Verify' , rectangle_x + 120, rectangle_y + 400, 500, 50, fontIntro, 'Verify')

    return verifybutton.draw(screen,stage)




def Login(stage, screen):
    # read the login video
    success, video_image = video.read()
    if success:
        video_surf = pygame.image.frombuffer(
        video_image.tobytes(), (1280, 720), "BGR")
        video_surf = pygame.transform.scale(video_surf, (1920, 1080))
    else:
        running = False
    screen.blit(video_surf, (0, 0))
    
    return stage