import pygame
import sys
from pygame.locals import *
import pyganim
pygame.init()

#windowSurface = pygame.display.set_mode((320, 240), 0, 32)
#surf1 = pygame.Surface((100, 100))
#pygame.draw.rect(surf1, (255, 0, 0), (50, 50, 20, 20))

#while True: # main loop
    #for event in pygame.event.get():
        #if event.type == QUIT:
            #pygame.quit()
            #sys.exit()
    #windowSurface.blit(surf1, (50,50))
    #pygame.display.update()

windowSurface = pygame.display.set_mode((320, 240), 0, 32)

# make some Surface objects for the animation frames:
surf1 = pygame.Surface((100, 100))
pygame.draw.rect(surf1, (255, 0, 0), (0, 0, 20, 20))

surf2 = pygame.Surface((100, 100))
pygame.draw.rect(surf2, (255, 0, 0), (80, 80, 20, 20))

surf3 = pygame.Surface((100, 100))
pygame.draw.circle(surf3, (0, 0, 255), (50, 50), 20)

# create the PygAnimation object
animObj = pyganim.PygAnimation([(surf1, 0.2), (surf2, 0.2), (surf3, 0.2)],loop=False)
animObj.play()

while True: # main loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    animObj.blit(windowSurface, (0, 0))
    pygame.display.update()