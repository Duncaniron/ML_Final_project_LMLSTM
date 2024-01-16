import pygame
import cv2

video = cv2.VideoCapture(r"C:\Users\User\Desktop\python\PygameTest\background\hackingTheme.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)

window = pygame.display.set_mode(video_image.shape[1::-1])
clock = pygame.time.Clock()

run = success
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    clock.tick(fps)
    success, video_image = video.read()
    if success:
        video_surf = pygame.image.frombuffer(
            video_image.tobytes(), video_image.shape[1::-1], "BGR")
    else:
        run = False
    window.blit(video_surf, (0, 0))
    pygame.display.flip()

pygame.quit()
exit()