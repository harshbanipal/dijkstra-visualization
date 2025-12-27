import pygame

pygame.init()   # initialize pygame

screen = pygame.display.set_mode((640,640))    # create window with dimensions x by y
pygame.display.set_caption("dijkstra")

white = (255,255,255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
    