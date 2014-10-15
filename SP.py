__version__ = 'classic_secretary_problem_1.0, with pygame_version_1.9.2a0_fromUCI, python2.7.3, Win64'
#---------experiment setting info-----------------
# before decision search cost is a fixed value as 5
# No limit on the number of PE in each trial
# all the disitrbutions are uniform
# Black 25-100-175 as no information disclosure
# white 50-100-150
# Turns = 20
# trials = 48 in total, each has 12 trials
# all the 48 trials shuffled into a random order
# all other distributions:
# 40-80-120(0.5*80--1.5*80) ;20-80-140(0.25*80--1.75*80)
# 80-160-240 ; 40-160-280 ; 100-200-300 ;50-200-350 ; 120-240-360 ;60-240-420
# 150-300-450; 75-300-525
# -------------guidelines for the coding -----------------
# first make the whole procedures integral, then if necessary adding the try part
# add instruction windows and interface
# modulize the runing part, add trials and conditions
# add function to tracking clicking time!
# add details about the experiment above
# save the data 
# how to properly quit the csv writer object and save the data with integrity
# ----------------------to do list---------------------------------
# check the prompt window from Tkinter
# revise the prompt window on the instruction and also on INTERFACE

import pygame, sys
import math, time, string
import pygbutton
import random
import csv
from Tkinter import *
#import pyganim

#######experiment settings###########################
#uniform distribution values, L and H are closed interval
#card value's range
LOWEST,HIGHEST = 25, 170
#card's width and height
CARDWIDTH, CARDHEIGHT =  40, 50
BACKGROUND_COLOR  = (30, 98, 50)
#the window's width and height
WIDTH, HEIGHT = 800, 600
FPS = 30
TURN = 20
#ANIMATION_ON = True




def introprompt():
    """asks the user to read a document and type in a subject id, then click ok."""
    def saveclose():
        global _Subject_id
        _Subject_id = entry.get()
        #print id
        #root.quit()
    introtext = "Welcome.   In this experiment, your goal is to choose a set of numbered cards so that you get \n\
the **highest total score** that you can in each game. You have a deck of cards at the bottom of the screen, \n\
and on each turn, you can pick a new card from that deck by clicking on it,or you can pick one of the cards\n\
you have already gotten from the deck, by clicking on that card in the set of cards displayed above the deck.\n\
If you pick a new card from the deck, you will get the number of points on that card added to your score, and\n\
if you pick an old card shown on the screen, you will get the number of points shown on it--but then that card's\n\
value will decrease by 3 points. If you choose that card next time, you will get the decreased number of points\n\
added to your score, and the value will go down by another 3 points.  The cards in the deck have numbers between\n\
1 and 99, with each number being equally likely to turn up. In each game, the total number of turns is uncertain \n\
and may vary from game to game. And you will get to play the game 32 times--the first-two game is a practice. The \n\
highest value of cards on your table will be painted red. Your total score for the current game is shown at the \n\
bottom of the screen, along with how many turns you already have had, and what numbers you have picked so far.  \n\
\n\
At the end of each game, you will be told your total amount of points and total number of turns at that game. \n\
Please ask if you have any questions now, or give it a try!\n"
    root = Tk()
    root.title = "Instructions"
    label = Label(root, text = introtext, font=("Helvetica", 16),justify=LEFT,anchor=NE)
    label.pack()
    entry = Entry(root)
    #entry.insert(0, "Type Subject ID Here.")
    entry.pack()
    button = Button(root, text = "Experimenter: Enter Subject ID above and click here to save it, then click the upper right red X button of THIS window to start the game.", font=("Helvetica", 12), command = saveclose)
    button.pack()
    root.mainloop()
    
    
def writeinit(subjectid):
    """preps the file object, writes the initial header line"""
    global csvwriter    
    filename = subjectid + "-data.csv"
    fileobj = open(filename, 'wb')
    csvwriter = csv.writer(fileobj)
    header = ['subjectid','trial','turn','explore0_exploit1','switch_exploit?','switch_PE?', 'timeofclick','timesincelastclick','numberofcards','cardvalue','exploitCards','maxvalueontable','totalpoint']
    csvwriter.writerow(header)
    #fileobj.close()



class Game_info:
    
    def __init__(self, num_card, current_value_set, surface):
        self.turn = num_card
        self.left_turn = TURN - self.turn
        if len(current_value_set) == 0:
            self.current_value = 'Not Applicable'
        else:
            self.current_value = current_value_set[-1]
        self.surface = surface
        

        
    def draw_game_info(self):
        game_info_text1 = 'The current turn is:'
        game_info_text1 += str(self.turn)
        #game_info_text += '\n'
        game_info_text2 = 'The number of turns left is:'
        game_info_text2 += str(self.left_turn)
        #game_info_text += '\n'
        game_info_text3 = 'The current card value available is:'
        game_info_text3 += str(self.current_value)
        
        #first draw the area for text, and erase the previous game info
        
        self.surface.fill(pygame.Color(30, 98, 50), (300,500,500,90))
        #self.surface.fill(pygame.Color('white'), (300,500,500,90))
        #draw on the surface
        font_instance = pygame.font.SysFont('helvetica',25)
        #helvetica, times
        #font_instance = pygame.font.SysFont("comicsansms",25)
        #text1 is a new surface
        text1 = font_instance.render(game_info_text1,True,(0,0,0))     
        text2 = font_instance.render(game_info_text2,True,(0,0,0))
        text3 = font_instance.render(game_info_text3,True,(0,0,0))
        #render the new surface on the game interface
        self.surface.blit(text1, (300,500))
        self.surface.blit(text2, (300,530))
        self.surface.blit(text3, (300,560))
        #self.surface.blit(text1, (self.width_pos, self.height_pos))        

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
    Num_card = 0
    Card_value_set = []
    #control whether the flip is before or post Exploration
    #every time the game starts, this is False; every time PE decision, this is True then
    Post_exploration = False
    Selected_rect = None
    
    def __init__(self, clicker_counter, value, surface):
        
        self.card_value = value
        self.cardwidth = CARDWIDTH
        self.cardheight = CARDHEIGHT
        self.surface = surface
        self.click_time = clicker_counter
        #above is an instance attribute
        #Click_Times is starting from 0
        #Click_Times += 1???---local variable 'Click_Times' referenced before assignment!!!  The python frame and variables apply here in class and its methods. Click_Times will be a local variable, rather than a global variable in terms of the Rect class
        Rect.Click_Times += 1
        #Num_card is from 0, and recording the number of card flipped over
        Rect.Num_card  += 1
        #put all the card value into a list
        Rect.Card_value_set.append(self.card_value)
        #initialize the max number of card per row
        Rect.Max_card_per_row = Rect.compute_max_num_card_per_row()
        #print  Rect.Max_card_per_row
        self.width_pos, self.height_pos = self.compute_width_heigh_pos(clicker_counter)
        #print self.width_pos, self.height_pos
    
    @staticmethod
    def reset_Rect_Class_attributes():
        '''
        reset the class attributes
        NOTE THAT, YOU HAVE TO refer to Rect. , otherwise, all the variables below would be treated as local variables within this method
        '''
        Rect.Click_Times = -1
        Rect.Num_card = 0
        Rect.Card_value_set = []
        #control whether the flip is before or post Exploration
        #every time the game starts, this is False; every time PE decision, this is True then
        Rect.Post_exploration = False
        Rect.Selected_rect = None        
        
    @classmethod
    def set_post_exp_and_sel_rect(cls, post_exploration = False, selected_rect = None):
        cls.Post_exploration = post_exploration
        cls.Selected_rect = selected_rect
        
    @classmethod
    def get_current_value(cls):
        return cls.Card_value_set[-1]
    
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
        '''
        Before Decision, the current value is highlighted, and the previous value is shaded
        
        After decision, the selected value is highlighted, and the PE cards are shaded
        
        Rect.Post_exploration is originally False, after decision,set it as True. and Every new game should initialize it as False again
        '''
        if Rect.Post_exploration == False:
            if self.click_time == Rect.Click_Times:
                pygame.draw.rect(self.surface, (255,255,255), (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
            else:
                pygame.draw.rect(self.surface, (150,150,150), (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
        else:
            if self == Rect.Selected_rect:
                pygame.draw.rect(self.surface, (255,255,255), (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
            else:
                pygame.draw.rect(self.surface, (150,150,150), (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
                
    def draw(self):
        '''
        draw the rect instance and update its corresponding value
        '''
        
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
FPSCLOCK = pygame.time.Clock()
Window0 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A Decision Task')
Window0.fill(BACKGROUND_COLOR)
#pygame.display.flip()
#Deck = pygame.image.load('deck.jpg')
#Deck1 = pygame.transform.smoothscale(Deck, (60,80))
#Window0.blit(Deck1, (0,520))
introprompt()
writeinit(_Subject_id)

pygame.draw.rect(Window0,(31,31,31), (0,520, 60, 80), 0)
pygame.draw.rect(Window0, (6,113,148), (5,525,50,70), 3)
button_Before_Ex = pygbutton.PygButton((70, 490, 150, 30), 'Flip A New Card')
button_Decision = pygbutton.PygButton((70, 530, 150, 30), 'Make A Decision')
button_Next = pygbutton.PygButton((70, 570, 150, 30), 'Next Round')
button_Before_Ex.draw(Window0)
#button_Decision.draw(Window0)
#button_Next.draw(Window0)
pygame.display.flip()



running = True
click_counter = 0
rect_set = []
buttonDecision_visMode = True
button_Next_visMode = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            pygame.quit()
            sys.exit()        
        # button_Before_Ex.handleEvent(event) is a queue
        if 'click' in button_Before_Ex.handleEvent(event):
            
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
            #Window0.scroll will move the surface 
            #Window0.scroll(40,-70)
            #print rect_set
            
            
            #write into the csv file
            exp_turn = click_counter
            exp_trial = 1
            ##the right way is to set selected as an instance attribute!
            if rect == Rect.Selected_rect:
                exp_picked_rect = 1
            else:
                exp_picked_rect = 0
            exp_ex_ex = 0
            row = [_Subject_id, exp_trial, exp_turn, exp_ex_ex, rect.card_value,exp_picked_rect]
            csvwriter.writerow(row)
            
            
            ###########################
            click_counter += 1
            
        if 'click' in button_Decision.handleEvent(event):
            '''
            click on the decision button will:
            make the current value be highlighted until the end of this game
            activate the next round button
            disable itself
            when there is no card on the scree, do nothing
            '''
            #when there is no card, do nothing when clicking the decision button
            if len(rect_set) == 0:
                pass
            else:
                Rect.set_post_exp_and_sel_rect(post_exploration = True, selected_rect = rect_set[-1])
                #pygame.draw.rect(Window0, (30, 98, 50), (70, 530, 150, 30), 0)
                #pygame.draw.rect(Window0, (0, 0, 0), (70, 530, 150, 30), 2)
                #Window0.fill(pygame.Color(0, 0, 0), (70, 530, 180, 30))
                ##to cover the Decsion button area, to cover the previous drawn decsion button
                Window0.fill((30, 98, 50), (60, 520, 200, 40))
                #Window0.fill(pygame.Color(30, 98, 50), (70, 530, 150, 30))
                
                buttonDecision_visMode = False
                
                # make the Decision button disable; draw colors or rect doesnot work
                #buttonDecision_visMode= False
                button_Next_visMode = True
                #button_Next_visMode = True
                #set the button_Next active
                button_Decision.visible = buttonDecision_visMode
                button_Next.visible = button_Next_visMode  
                
                           
                
        
        if 'click' in button_Next.handleEvent(event):
            '''
            reset the game 
            write a re-set function to do this??
            '''
            Window0.fill(BACKGROUND_COLOR)
            button_Next_visMode = False
            buttonDecision_visMode = True
            button_Decision.visible = buttonDecision_visMode
            button_Next.visible = button_Next_visMode             
            #change the setting of Rect attributes, might not be the most proper way, should set some method in Rect class
            Rect.reset_Rect_Class_attributes()
            
            rect_set = []
            click_counter = 0
            pygame.draw.rect(Window0,(31,31,31), (0,520, 60, 80), 0)
            pygame.draw.rect(Window0, (6,113,148), (5,525,50,70), 3)            
            pygame.display.update()
            
        
    game_info = Game_info(Rect.Num_card, Rect.Card_value_set, Window0)
    game_info.draw_game_info()
    #in order to show the clicking effect, you have to draw the button instance to the surface for every event, not every CLICK(within the above if statement)!!
    button_Before_Ex.draw(Window0)
    button_Decision.draw(Window0)
    button_Next.draw(Window0)
    pygame.display.update()
    FPSCLOCK.tick(FPS)        


def main():
    pass

