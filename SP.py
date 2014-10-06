__version__ = 'classic_secretary_problem_1.0, with pygame_version_1.9.2a0_fromUCI'


# create a button
# create a random generator

import pygame
import math, time, string
import pygbutton
import random
#uniform distribution values, L and H are closed interval
LOWEST = 1
HIGHEST = 100
CARDWIDTH =  40
CARDHEIHT = 50
BACKGROUND_COLOR  = (34, 139, 34)

class Rect:
    '''
    Rect is a class showing the card values
    '''
    def __init__(self, clicker_counter, value, surface):
        self.width_pos, self.height_pos = self.compute_width_heigh_pos(clicker_counter)
        self.card_value = value
        self.cardwidth = CARDWIDTH
        self.cardheight = CARDHEIHT
        self.surface = surface
        
    def compute_width_heigh_pos(self, click_counter):
        '''
        compute the starting pos of width and height for each rect given the click times of the button
        this might have bugs!!!!!
        And also have to switch to the next lines when necessary!!!!!
        
        '''
        initial_width_pos = 10
        initial_height_pos = 10
        gap = 20
        rect_width_pos = initial_width_pos + click_counter*(CARDWIDTH+gap)
        rect_height_pos = initial_height_pos
        return rect_width_pos,rect_height_pos
        
        
    def draw(self):
        '''
        draw the rect instance and update its corresponding value
        '''
        color = (0, 139, 0)
        Rect = (self.width_pos, self.height_pos, self.cardwidth, self.cardheight)
        pygame.draw.rect(self.surface, (255,255,255), (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIHT), 0)
        self.draw_card_value()
        pygame.display.flip()
    
    def draw_card_value(self):
        '''
        draw the card value on the Rect instance for each click
        '''
        self.card_value
        #first creat a Font instace
        font_instance = pygame.font.SysFont("comicsansms",20)
        #text1 is a new surface
        text1=font_instance.render(str(self.card_value),True,(120,120,120))        
        #render the new surface on the game interface
        self.surface.blit(text1, (self.width_pos + self.cardwidth/5, self.height_pos+ self.cardheight/5))
        #self.surface.blit(text1, (self.width_pos, self.height_pos))
    
pygame.init()
#Background_color  = (255,255,255)


Width, Height = 800, 600
Window0 = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('A Decision Task')
Window0.fill(BACKGROUND_COLOR)
pygame.display.flip()
Deck = pygame.image.load('deck.jpg')
Deck1 = pygame.transform.smoothscale(Deck, (60,80))
Window0.blit(Deck1, (0,520))
#pygame.display.flip()
buttonObj = pygbutton.PygButton((150, 550, 60, 30), 'Click')
buttonObj.draw(Window0)
pygame.display.flip()

#pygame.draw.rect(Window0, (0,255,0), (10,10,60,40), width = 2)
#pygame.display.flip()




running = True
click_counter = 0

while running:
    for event in pygame.event.get():
        if 'click' in buttonObj.handleEvent(event):
            #width_pos = 10
            #height_pos =
            random.randint(LOWEST, HIGHEST)
            #print random.randint(LOWEST, HIGHEST)
            rect = Rect(click_counter, random.randint(LOWEST, HIGHEST), Window0)
            rect.draw()
            click_counter += 1
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()




def main():
    pass

