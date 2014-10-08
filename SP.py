__version__ = 'classic_secretary_problem_1.0, with pygame_version_1.9.2a0_fromUCI'

# 
# 
# show turns used and left information
# and also show all other information subjects need to know on the surface
# show the value that you would get on the board for the left turns
# animation of flipping over a card
# three buttons, first two and then later one.

import pygame, sys
import math, time, string
import pygbutton
import random

#######experiment settings###########################
#uniform distribution values, L and H are closed interval
#card value's range
LOWEST,HIGHEST = 1, 100
#card's width and height
CARDWIDTH, CARDHEIGHT =  40, 50
BACKGROUND_COLOR  = (30, 98, 50)
#the window's width and height
WIDTH, HEIGHT = 800, 600
FPS = 30


class Rect:
    '''
    Rect is a class showing the card values
    '''
    #class attributes
    Click_Times = -1
    #Max_card_per_row = 0
    Gap = 20
    Initial_width_pos = 10
    Initial_height_pos = 10
    
    
    def __init__(self, clicker_counter, value, surface):
        
        self.card_value = value
        self.cardwidth = CARDWIDTH
        self.cardheight = CARDHEIGHT
        self.surface = surface
        self.click_time = clicker_counter
        #above is an instance attribute
        Rect.Click_Times += 1
        #initialize the max number of card per row
        Rect.Max_card_per_row = Rect.compute_max_num_card_per_row()
        #print  Rect.Max_card_per_row
        self.width_pos, self.height_pos = self.compute_width_heigh_pos(clicker_counter)
        #print self.width_pos, self.height_pos
   
    @staticmethod
    def compute_max_num_card_per_row():
        '''
        static method to compute the number of card per row
        '''
        i = 1
        while Rect.Initial_width_pos + i*(Rect.Gap + CARDWIDTH) <= WIDTH :
            i += 1
        return (i - 1)
        
        
        
    def compute_width_heigh_pos(self, click_counter):
        '''
        compute the starting pos of width and height for each rect given the click times of the button
        this might have bugs!!!!!
        And also have to switch to the next lines when necessary!!!!!
        
        '''
        # assign the class attributes to the local variables
        initial_width_pos = Rect.Initial_width_pos
        initial_height_pos = Rect.Initial_height_pos
        gap = Rect.Gap
        
        #click_counter is starting from 0; so donot have to add 1 to the end in the following line
        num_card_on_left = (click_counter % Rect.Max_card_per_row) 
        num_row_on_top = (click_counter // Rect.Max_card_per_row)
        
        #compute the starting position for each card instance
        rect_width_pos = initial_width_pos + num_card_on_left*(CARDWIDTH+gap)
        rect_height_pos = initial_height_pos + num_row_on_top*(CARDHEIGHT+gap)
        
        return rect_width_pos,rect_height_pos
        
        
    def regular_or_highlight(self):
        #print 'Rect.Click_Times', Rect.Click_Times
        #print 'self.click_time', self.click_time
        if self.click_time == Rect.Click_Times:
            pygame.draw.rect(self.surface, (255,255,255), (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
        else:
            pygame.draw.rect(self.surface, (150,150,150), (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
            
    def draw(self):
        '''
        draw the rect instance and update its corresponding value
        '''
        color = (0, 139, 0)
        Rect = (self.width_pos, self.height_pos, self.cardwidth, self.cardheight)
        self.regular_or_highlight()
        #the following code is drawing a frame of the card
        pygame.draw.rect(self.surface, (6,113,148), (self.width_pos + 3,self.height_pos + 3, CARDWIDTH-6, CARDHEIGHT-6), 3)
        self.draw_card_value()
        pygame.display.flip()
        #you can actually only update part of the surface, using a rect tuple
        #pygame.display.update((10,10,20,20))
    def draw_card_value(self):
        '''
        draw the card value on the Rect instance for each click
        '''
        #self.card_value
        #first creat a Font instace
        font_instance = pygame.font.SysFont("comicsansms",20)
        #text1 is a new surface
        text1=font_instance.render(str(self.card_value),True,(77,77,77))     
        #render the new surface on the game interface
        self.surface.blit(text1, (self.width_pos + self.cardwidth/5, self.height_pos+ self.cardheight/5))
        #self.surface.blit(text1, (self.width_pos, self.height_pos))
    

pygame.init()
#Do we need this clock object in this game??
#FPSCLOCK = pygame.time.Clock()
Window0 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A Decision Task')
Window0.fill(BACKGROUND_COLOR)
pygame.display.flip()
Deck = pygame.image.load('deck.jpg')
Deck1 = pygame.transform.smoothscale(Deck, (60,80))
Window0.blit(Deck1, (0,520))
buttonObj = pygbutton.PygButton((70, 500, 90, 30), 'Flip Over')
buttonObj.draw(Window0)
pygame.display.flip()






running = True
click_counter = 0
rect_set = []
while running:
    for event in pygame.event.get():
        # buttonObj.handleEvent(event) is a queue
        if 'click' in buttonObj.handleEvent(event):
            
            #width_pos = 10
            #height_pos =
            card_value_generated = random.randint(LOWEST, HIGHEST)
            #print random.randint(LOWEST, HIGHEST)
            
            rect = Rect(click_counter, card_value_generated, Window0)
            if len(rect_set) == 0:
                pass #pass here, execute nothing, but the control flow continue to the following statements
            else:
                rect_set[-1].draw()
            rect.draw()
            rect_set.append(rect)
            #print rect_set
            
            
            click_counter += 1
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        
        #in order to show the clicking effect, you have to draw the button instance to the surface for every event, not every CLICK(within the above if statement)!!
        buttonObj.draw(Window0)
        pygame.display.update()
        #FPSCLOCK.tick(FPS)        


def main():
    pass

