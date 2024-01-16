import pygame
from page import stage
import subprocess

# Define the global attributes
pygame.init()
fps = 30.0
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
input_string = ""
# Login user info
USER_ID = ""
# Stage change variable
STAGE = "waiting"

# Run the main loop
while running:
    clock.tick(30.0)
    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            running = False
        
        elif evnt.type == pygame.KEYDOWN:
            # Check if the key pressed is a printable character
            if evnt.unicode.isprintable() and STAGE == 'addingUser':
                # Append the character to the input string
                input_string += evnt.unicode
            # Check if the key pressed is BACKSPACE
            elif evnt.key == pygame.K_BACKSPACE and STAGE == 'addingUser':
                # Handle backspace to remove the last character
                input_string = input_string[:-1]
            # Check if the key pressed is ENTER
            elif evnt.key == pygame.K_RETURN and STAGE == 'addingUser':
                STAGE = 'ActAdduser'
            # Check if the key pressed is ESCAPE
            if evnt.key == pygame.K_ESCAPE:
                running = False

    #select the stage
        
    if(STAGE == "waiting"):
        STAGE = stage.waitingStage(STAGE, screen)
    
    elif(STAGE == "LoginWarning"):
        STAGE = stage.LoginWarning(STAGE, screen)

    elif(STAGE == "Verify"):
        STAGE = stage.VerifyStage(STAGE, screen)

    elif(STAGE == "admin"):
        input_string = ''
        STAGE = stage.AdminStage(STAGE, screen)
    
    elif(STAGE == "login"):
        STAGE = stage.Login(STAGE, screen)
    
    elif(STAGE == "addingUser"):
        STAGE = stage.AddUser(STAGE, screen, input_string)

    elif(STAGE == "ActAdduser"):
        STAGE = stage.ActAdduser(STAGE, screen, input_string)

    elif(STAGE == "delUser"):
        STAGE = stage.delUser(STAGE, screen)
    
    elif(STAGE == "chkIntruder"):
        STAGE = stage.chkIntruder(STAGE, screen)

    elif(STAGE == "chkIntruderUsr"):
        STAGE = stage.chkIntruderUsr(STAGE, screen)

    elif(STAGE == "LM-LSTM"):
        STAGE = stage.LMLSTM(STAGE, screen)

    elif(STAGE == "IntruderDetected"):
        STAGE = stage.IntruderDetected(STAGE, screen)

    elif(STAGE == "presentation"):
        STAGE = stage.presentation(STAGE, screen)
    elif(STAGE == "quit"):
        running = False
    else:
        STAGE = stage.waitingStage(STAGE, screen)
        
    pygame.display.flip()

pygame.quit()
