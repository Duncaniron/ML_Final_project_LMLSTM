import pygame
import cv2
from Button import Button

pygame.init()
# init the parameters
video = cv2.VideoCapture(r"..\background\hackingTheme.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)
screen = pygame.display.set_mode(video_image.shape[1::-1])
clock = pygame.time.Clock()
button = 0
fontIntro = pygame.font.Font(r'..\PygameTest\page\OCRAEXT.TTF',30)
start_img = pygame.image.load('startButton.jpg').convert_alpha()
running = True
# Adjust the size of the image to fit the aspect ratio
desired_width = 100
aspect_ratio = start_img.get_width() / start_img.get_height()
desired_height = int(desired_width / aspect_ratio)

start_img = pygame.image.load('startButton.jpg').convert_alpha()
# Scale the image
scaled_img = pygame.transform.scale(start_img, (desired_width, desired_height))


def drawIntro(screen):
    # button reflect the page

    # start page
    if button == 0:  
        screen.fill((0, 0, 0))
        text = fontIntro.render("Sigle click to start", True, (23, 201, 21))
        screen.blit(text, (300, 300, 500, 500))
        screen.blit(text, (301, 301, 500, 500))
    # page1
    elif button == 1:  
        screen.fill((0, 0, 0))
        text = fontIntro.render("page 1", True, (23, 201, 21))
        screen.blit(text, (300, 300, 500, 500))
    #page2
    elif button == 2:  
        screen.fill((0, 0, 0))
        text = fontIntro.render("page 2", True, (26, 201, 23))
        screen.blit(text, (300, 300, 500, 500))
    #page3
    elif button == 3:  
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(
                video_image.tobytes(), video_image.shape[1::-1], "BGR")
        else:
            running = False
        screen.blit(video_surf, (0, 0))

# Run the main loop
while running:
    clock.tick(fps)
    # Handle the events
    for evnt in pygame.event.get():
        # Quit the game when the close button is pressed
        if evnt.type == pygame.QUIT:
            running = False
        # Check if the mouse is clicked
        if evnt.type == pygame.MOUSEBUTTONDOWN:  
            button += 1
    drawIntro(screen)
    pygame.display.flip()

pygame.quit()
