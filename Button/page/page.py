import pygame
import cv2
from Button import Button

pygame.init()
video = cv2.VideoCapture(r"..\background\hackingTheme.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)
#============================
# SIZE = (1000, 700)
screen = pygame.display.set_mode(video_image.shape[1::-1])
clock = pygame.time.Clock()
button = 0
fontIntro = pygame.font.Font(r'..\PygameTest\page\OCRAEXT.TTF',30)

start_img = pygame.image.load('startButton.jpg').convert_alpha()

running = True
desired_width = 100

# Adjust the size of the image
# Calculate the corresponding height to maintain the aspect ratio
aspect_ratio = start_img.get_width() / start_img.get_height()
desired_height = int(desired_width / aspect_ratio)

start_img = pygame.image.load('startButton.jpg').convert_alpha()

# Scale the image
scaled_img = pygame.transform.scale(start_img, (desired_width, desired_height))
# start_button = Button(100, 200, scaled_img)


def drawIntro(screen):
    #start
    if button == 0:  # == 0
        screen.fill((0, 0, 0))
        text = fontIntro.render("Sigle click to start", True, (23, 201, 21))
        
        screen.blit(text, (300, 300, 500, 500))
        screen.blit(text, (301, 301, 500, 500))
    elif button == 1:  #page1
        screen.fill((0, 0, 0))
        text = fontIntro.render("page 1", True, (23, 201, 21))
        screen.blit(text, (300, 300, 500, 500))
    elif button == 2:  #page2
        screen.fill((0, 0, 0))
        text = fontIntro.render("page 2", True, (26, 201, 23))
        screen.blit(text, (300, 300, 500, 500))
    elif button == 3:  #page3
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            running = False
        screen.blit(video_surf, (0, 0))
        # pass


while running:
    clock.tick(fps)
    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            running = False
        if evnt.type == pygame.MOUSEBUTTONDOWN:  # Once per click.
            button += 1

    drawIntro(screen)
    pygame.display.flip()

pygame.quit()
