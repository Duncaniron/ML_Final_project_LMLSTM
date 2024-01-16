import pygame
import shutil

class Button():
    def __init__(self, context, x, y, w, h, fontIntro, nxt_stage):
        self.context = context
        self.rect.topleft = (x, y)
        self.clicked = False
        self.fontintro = fontIntro
        self.nxt_stage = nxt_stage
        self.rect = pygame.Rect(x, y, w, h) 
        self.context_x_point = x + (w/ 2) - (18 * len(context) / 2) 
        self.context_y_point = y + (h / 2) - (fontIntro.get_height() / 2) 

    def draw(self, screen, stage):
        # get mouse position
        pos = pygame.mouse.get_pos()
        
        # Check if the mouse is over the button 
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, (23, 255, 21), self.rect)
            text = self.fontintro.render(self.context, True, (0, 0, 0))
            screen.blit(text, (self.context_x_point, self.context_y_point))
            # Check if the mouse is clicked
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                print('clicked')
                stage = self.nxt_stage
        else:
            pygame.draw.rect(screen, (23, 201, 21), self.rect, width=2)
            text = self.fontintro.render(self.context, True, (23, 201, 21))
            screen.blit(text, (self.context_x_point, self.context_y_point))
        
        # Check if the mouse is over the button and left mouse button is released
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                print('released')
        
        return stage

class adminButton():
    def __init__(self, context, x, y, w, h, fontIntro, nxt_stage):
        self.context = context
        
        self.rect.topleft = (x, y)
        self.clicked = False
        self.fontintro = fontIntro
        self.nxt_stage = nxt_stage
        self.rect = pygame.Rect(x, y, w, h)  
        self.context_x_point = x + (w/ 2) - (18 * len(context) / 2) 
        self.context_y_point = y + (h / 2) - (fontIntro.get_height() / 2) 

    def draw(self, screen, stage, global_clicked):
        # get mouse position
        pos = pygame.mouse.get_pos()
        
        # Check if the mouse is over the button
        if self.rect.collidepoint(pos):
            text = self.fontintro.render(self.context + ' <' , True, (23, 201, 21))
            screen.blit(text, self.rect)
            # Check if the mouse is clicked
            if pygame.mouse.get_pressed()[0] == 1 and not global_clicked:
                global_clicked = True
                print('clicked')
                stage = self.nxt_stage
        else:
            text = self.fontintro.render(self.context, True, (23, 201, 21))
            screen.blit(text, self.rect)
        # Check if the mouse is over the button and left mouse button is released
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                print('released')
        
        return stage, global_clicked



class delButton():
    def __init__(self, context, x, y, w, h, fontIntro, nxt_stage):
        self.context = context
        self.rect = pygame.Rect(x, y, w, h)  
        self.rect.topleft = (x, y)
        self.fontintro = fontIntro
        self.nxt_stage = nxt_stage
        self.dirpath = ["degree_data_4/0/", "degree_data_4/1/", "degree_data_4/2/", "degree_data_4/3/"]


    def draw(self, screen, stage, global_clicked):
        #get mouse position
        pos = pygame.mouse.get_pos()
        

        # Check if the mouse is over the button and left mouse button is clicked
        if self.rect.collidepoint(pos):
            # pygame.draw.rect(screen, (23, 255, 21), self.rect)
            # pygame.draw.rect(screen, (23, 255, 21), (self.x, self.y, self.w, self.h), width=2)
            text = self.fontintro.render('[-] ' + self.context + ' <', True, (23, 255, 21))
            screen.blit(text, self.rect)

            if pygame.mouse.get_pressed()[0] == 1 and not global_clicked:
                for i in self.dirpath:
                    directory_path = i + self.context
                    try:
                        shutil.rmtree(directory_path)
                        print(f"Directory '{directory_path}' removed successfully.")
                    except OSError as e:
                        print(f"Error: {e}")
                
                stage = self.nxt_stage
                global_clicked = True
            
        else:
            # pygame.draw.rect(screen, (23, 201, 21), self.rect, width=2)
            text = self.fontintro.render('[-] ' + self.context, True, (23, 201, 21))
            screen.blit(text, self.rect)
        
        if pygame.mouse.get_pressed()[0] == 0  and global_clicked:
                print('released')
        
        return stage, global_clicked
    

class chkIntruButton():
    def __init__(self, context, x, y, w, h, fontIntro):
        self.context = context
        self.rect = pygame.Rect(x, y, w, h)  
        self.rect.topleft = (x, y)
        self.fontintro = fontIntro
        self.context_x_point = x + (w/ 2) - (18 * len(context) / 2) 
        self.context_y_point = y + (h / 2) - (fontIntro.get_height() / 2) 

    def draw(self, screen, Inturder_index, global_clicked, move, len):
        #get mouse position
        pos = pygame.mouse.get_pos()

        # Check if the mouse is over the button 
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, (23, 255, 21), self.rect)
            text = self.fontintro.render(self.context, True, (0, 0, 0))
            screen.blit(text, (self.context_x_point, self.context_y_point))
            # Check if the mouse is clicked
            if pygame.mouse.get_pressed()[0] == 1 and not global_clicked:
                global_clicked = True
                print('clicked')
                if(Inturder_index + move >= 0 and Inturder_index + move < len):
                    Inturder_index += move
        else:
            pygame.draw.rect(screen, (23, 201, 21), self.rect, width=2)
            text = self.fontintro.render(self.context, True, (23, 201, 21))
            screen.blit(text, (self.context_x_point, self.context_y_point))
        # Check if the mouse is over the button and left mouse button is released
        if pygame.mouse.get_pressed()[0] == 0 and global_clicked:
                global_clicked = False
                print('released')
        
        return Inturder_index, global_clicked