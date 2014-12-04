__version__ = 'classic_secretary_problem_1.0, with pygame_version_1.9.2a0_fromUCI, python2.7.3, Win64'
#---------experiment setting info-----------------
# before decision search cost is a fixed value as 5
# The limit on the number of PE in each trial is Total turn is 80
# all the disitrbutions are uniform
# Black 100-150-200 as no information disclosure
# white 50-100-150--this is to let the Black and White decks have the same variance
# trials = 48 in total, each has 12 trials
# all the 48 trials shuffled into a random order
# 
# ------------------------to do list---------------------------------
# 
########--------------------------------------------------------=-----
"""
PygButton v0.1.0

PygButton (pronounced "pig button") is a module that implements UI buttons for Pygame.
PygButton requires Pygame to be installed. Pygame can be downloaded from http://pygame.org
PygButton was developed by Al Sweigart (al@inventwithpython.com)
https://github.com/asweigart/pygbutton


Simplified BSD License:

Copyright 2012 Al Sweigart. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Al Sweigart ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Al Sweigart OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Al Sweigart.
"""
import pygame
from pygame.locals import *

pygame.font.init()
PYGBUTTON_FONT = pygame.font.Font('freesansbold.ttf', 14)

BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)

class PygButton(object):
    def __init__(self, rect=None, caption='', bgcolor=LIGHTGRAY, fgcolor=BLACK, font=None, normal=None, down=None, highlight=None):
        """Create a new button object. Parameters:
            rect - The size and position of the button as a pygame.Rect object
                or 4-tuple of integers.
            caption - The text on the button (default is blank)
            bgcolor - The background color of the button (default is a light
                gray color)
            fgcolor - The foreground color (i.e. the color of the text).
                Default is black.
            font - The pygame.font.Font object for the font of the text.
                Default is freesansbold in point 14.
            normal - A pygame.Surface object for the button's normal
                appearance.
            down - A pygame.Surface object for the button's pushed down
                appearance.
            highlight - A pygame.Surface object for the button's appearance
                when the mouse is over it.

            If the Surface objects are used, then the caption, bgcolor,
            fgcolor, and font parameters are ignored (and vice versa).
            Specifying the Surface objects lets the user use a custom image
            for the button.
            The normal, down, and highlight Surface objects must all be the
            same size as each other. Only the normal Surface object needs to
            be specified. The others, if left out, will default to the normal
            surface.
            """
        if rect is None:
            self._rect = pygame.Rect(0, 0, 30, 60)
        else:
            self._rect = pygame.Rect(rect)

        self._caption = caption
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor

        if font is None:
            self._font = PYGBUTTON_FONT
        else:
            self._font = font

        # tracks the state of the button
        self.buttonDown = False # is the button currently pushed down?
        self.mouseOverButton = False # is the mouse currently hovering over the button?
        self.lastMouseDownOverButton = False # was the last mouse down event over the mouse button? (Used to track clicks.)
        self._visible = True # is the button visible
        self.customSurfaces = False # button starts as a text button instead of having custom images for each surface

        if normal is None:
            # create the surfaces for a text button
            self.surfaceNormal = pygame.Surface(self._rect.size)
            self.surfaceDown = pygame.Surface(self._rect.size)
            self.surfaceHighlight = pygame.Surface(self._rect.size)
            self._update() # draw the initial button images
        else:
            # create the surfaces for a custom image button
            self.setSurfaces(normal, down, highlight)

    def handleEvent(self, eventObj):
        """Note that this handleEvent method generates a queue!!!
        All MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN event objects
        created by Pygame should be passed to this method. ---pygame will generates these variables, and they are constant passed to handleEvent method here by call.And judged by the first line of Code.
        handleEvent() will
        detect if the event is relevant to this button and change its state.

        There are two ways that your code can respond to button-events. One is
        to inherit the PygButton class and override the mouse*() methods. The
        other is to have the caller of handleEvent() check the return value
        for the strings 'enter', 'move', 'down', 'up', 'click', or 'exit'.

        Note that mouseEnter() is always called before mouseMove(), and
        mouseMove() is always called before mouseExit(). Also, mouseUp() is
        always called before mouseClick().

        buttonDown is always True when mouseDown() is called, and always False
        when mouseUp() or mouseClick() is called. lastMouseDownOverButton is
        always False when mouseUp() or mouseClick() is called."""

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return []

        retVal = []

        hasExited = False
        if not self.mouseOverButton and self._rect.collidepoint(eventObj.pos):
            # if mouse has entered the button:
            self.mouseOverButton = True
            self.mouseEnter(eventObj)
            retVal.append('enter')
        elif self.mouseOverButton and not self._rect.collidepoint(eventObj.pos):
            # if mouse has exited the button:
            self.mouseOverButton = False
            hasExited = True # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

        if self._rect.collidepoint(eventObj.pos):
            # if mouse event happened over the button:
            if eventObj.type == MOUSEMOTION:
                self.mouseMove(eventObj)
                retVal.append('move')
            elif eventObj.type == MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True
                self.mouseDown(eventObj)
                retVal.append('down')
        else:
            if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self.lastMouseDownOverButton = False

        # mouse up is handled whether or not it was over the button
        doMouseClick = False
        if eventObj.type == MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                doMouseClick = True
            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False
                self.mouseUp(eventObj)
                retVal.append('up')

            if doMouseClick:
                self.buttonDown = False
                self.mouseClick(eventObj)
                retVal.append('click')

        if hasExited:
            self.mouseExit(eventObj)
            retVal.append('exit')

        return retVal

    def draw(self, surfaceObj):
        """Blit the current button's appearance to the surface object."""
        if self._visible:
            if self.buttonDown:
                surfaceObj.blit(self.surfaceDown, self._rect)
            elif self.mouseOverButton:
                surfaceObj.blit(self.surfaceHighlight, self._rect)
            else:
                surfaceObj.blit(self.surfaceNormal, self._rect)


    def _update(self):
        """Redraw the button's Surface object. Call this method when the button has changed appearance."""
        if self.customSurfaces:
            self.surfaceNormal    = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
            self.surfaceDown      = pygame.transform.smoothscale(self.origSurfaceDown, self._rect.size)
            self.surfaceHighlight = pygame.transform.smoothscale(self.origSurfaceHighlight, self._rect.size)
            return

        w = self._rect.width # syntactic sugar
        h = self._rect.height # syntactic sugar

        # fill background color for all buttons
        self.surfaceNormal.fill(self.bgcolor)
        self.surfaceDown.fill(self.bgcolor)
        self.surfaceHighlight.fill(self.bgcolor)

        # draw caption text for all buttons
        captionSurf = self._font.render(self._caption, True, self.fgcolor, self.bgcolor)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceDown.blit(captionSurf, captionRect)

        # draw border for normal button
        pygame.draw.rect(self.surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.surfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw border for down button
        pygame.draw.rect(self.surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self.surfaceDown, DARKGRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceDown, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self.surfaceDown, GRAY, (2, 2), (w - 3, 2))

        # draw border for highlight button
        self.surfaceHighlight = self.surfaceNormal


    def mouseClick(self, event):
        pass # This class is meant to be overridden.
    def mouseEnter(self, event):
        pass # This class is meant to be overridden.
    def mouseMove(self, event):
        pass # This class is meant to be overridden.
    def mouseExit(self, event):
        pass # This class is meant to be overridden.
    def mouseDown(self, event):
        pass # This class is meant to be overridden.
    def mouseUp(self, event):
        pass # This class is meant to be overridden.


    def setSurfaces(self, normalSurface, downSurface=None, highlightSurface=None):
        """Switch the button to a custom image type of button (rather than a
        text button). You can specify either a pygame.Surface object or a
        string of a filename to load for each of the three button appearance
        states."""
        if downSurface is None:
            downSurface = normalSurface
        if highlightSurface is None:
            highlightSurface = normalSurface

        if type(normalSurface) == str:
            self.origSurfaceNormal = pygame.image.load(normalSurface)
        if type(downSurface) == str:
            self.origSurfaceDown = pygame.image.load(downSurface)
        if type(highlightSurface) == str:
            self.origSurfaceHighlight = pygame.image.load(highlightSurface)

        if self.origSurfaceNormal.get_size() != self.origSurfaceDown.get_size() != self.origSurfaceHighlight.get_size():
            raise Exception('foo')

        self.surfaceNormal = self.origSurfaceNormal
        self.surfaceDown = self.origSurfaceDown
        self.surfaceHighlight = self.origSurfaceHighlight
        self.customSurfaces = True
        self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))



    def _propGetCaption(self):
        return self._caption


    def _propSetCaption(self, captionText):
        self.customSurfaces = False
        self._caption = captionText
        self._update()


    def _propGetRect(self):
        return self._rect


    def _propSetRect(self, newRect):
        # Note that changing the attributes of the Rect won't update the button. You have to re-assign the rect member.
        self._update()
        self._rect = newRect


    def _propGetVisible(self):
        return self._visible


    def _propSetVisible(self, setting):
        self._visible = setting


    def _propGetFgColor(self):
        return self._fgcolor


    def _propSetFgColor(self, setting):
        self.customSurfaces = False
        self._fgcolor = setting
        self._update()


    def _propGetBgColor(self):
        return self._bgcolor


    def _propSetBgColor(self, setting):
        self.customSurfaces = False
        self._bgcolor = setting
        self._update()


    def _propGetFont(self):
        return self._font


    def _propSetFont(self, setting):
        self.customSurfaces = False
        self._font = setting
        self._update()


    caption = property(_propGetCaption, _propSetCaption)
    rect = property(_propGetRect, _propSetRect)
    visible = property(_propGetVisible, _propSetVisible)
    fgcolor = property(_propGetFgColor, _propSetFgColor)
    bgcolor = property(_propGetBgColor, _propSetBgColor)
    font = property(_propGetFont, _propSetFont)


########---------------------------------------------------------------


import pygame, sys
import math, time, string
#import pygbutton
import random
import csv
import numpy as np
from Tkinter import * 
#above: use the module of Tkinter without calling Tkinter.
#import pyganim

#######experiment settings###########################
#uniform distribution values, L and H are closed interval
#card value's range
#LOWEST,HIGHEST = 25, 170---oblete
#card's width and height
CARDWIDTH, CARDHEIGHT =  60, 80
BACKGROUND_COLOR  = (30, 98, 50)
#the window's width and height
WIDTH, HEIGHT = 1200, 800
FPS = 30
NUM_TRIAL = 48
#NUM_TRIAL = 4
NUM_TURN = 80
NUM_CONDITIONS = ['BLACK','WHITE','BLUE','YELLOW']
#ANIMATION_ON = True
SEARCH_COST = 5
###color settings:
BLACK = (31,31,31)
WHITE = (255,255,255)
BLUE = (0,0,139)
YELLOW = (255,215,0)
LIGHTBLUE = (6,113,148)
RED = (255,0,0)
ALPHA = (150,150,150)
#deck card range setting for BLACK and WHITE
BLACK_RANGE = (100,200)
WHITE_RANGE = (50, 150)



def generate_condition_seq(total_num_trial):
	'''
	generate a condition sequence for each subj; we want the sequence is different for each  subj; so DONOT seed
	and each condition has equal number of trials (total_num_trial/NUM_CONDITIONS) in the sequence
	'''
	raw_seq_conditions = NUM_CONDITIONS * (total_num_trial/len(NUM_CONDITIONS))
	random.shuffle(raw_seq_conditions)
	shuffled_seq_conditions = raw_seq_conditions
	return shuffled_seq_conditions


def generate_uniform_dis(num_unique_uniform_distribution):

	N = num_unique_uniform_distribution # 12 distribution needed in the original setting
	#for integer value, arange is the same as range, for non-integer value, it is better to use linspace function
	values_pool = np.arange(25, 1005, 25)
	#final_list is a list containing all the uniform distributions for the BLUE and YELLOW conditions
	final_list = []
	num_values = len(values_pool)
	#in numpy, seed will make all the following random event predictable, which is cool; you donot have to reseed again if you are going to 
	# do randomization for several times--all the following random events will be set.
	np.random.seed(007)
	i = 1
	while i <= N:
		index_mean = np.random.randint(num_values)
		index_half_range = np.random.randint(num_values)
		while index_half_range >= index_mean:
			index_half_range = np.random.randint(num_values)

		para_values = (values_pool[index_mean], values_pool[index_half_range])
		if para_values not in final_list:
			final_list.append(para_values)
			i += 1

	return final_list

def generate_uniform_distributions_list(unique_uniform_distributions, sequence_conditions):
	#print sequence_conditions
	uniform_distributions_list = []
	#dummry_range = (99,99)
	##assign the original uniform distributions to either BLUE or YELLOW, then shuffle both, to randomly list the uniform dis sequence
	BLUE_unique_uniform_distributions = unique_uniform_distributions[:]
	random.shuffle(BLUE_unique_uniform_distributions)
	#-----python list mutable, you canNOT assign directly, otherwise Blue and Yellow will point to the same list
	#use a copy of the original list would work; this doesnot happen to tuples or scalar, but happen to dict! and list!
	YELLOW_unique_uniform_distributions = unique_uniform_distributions[:]
	random.shuffle(YELLOW_unique_uniform_distributions)
	#print 'BLUE_unique_uniform_distributions' , BLUE_unique_uniform_distributions
	#print 'YELLOW_unique_uniform_distributions', YELLOW_unique_uniform_distributions
	##generate the uniform list for each condition in the sequence_conditions
	for item in sequence_conditions:
		if item == 'BLACK':
			uniform_distributions_list.append(BLACK_RANGE)
		elif item == 'WHITE':
			uniform_distributions_list.append(WHITE_RANGE)
		elif item == 'BLUE':
			uniform_distributions_list.append(BLUE_unique_uniform_distributions[0])
			BLUE_unique_uniform_distributions.pop(0)
		else: 
			uniform_distributions_list.append(YELLOW_unique_uniform_distributions[0])
			YELLOW_unique_uniform_distributions.pop(0)
	return uniform_distributions_list


def generate_card_values(sequence_state, uniform_distribution_parameters):
	'''
	this function return two things: the range of the deck values as a list
	second, a value generated from this range by random.randint function
	'''
	if sequence_state == "BLACK":
		cardvalue_range = list(BLACK_RANGE)
		cardvalue = random.randint(cardvalue_range[0],cardvalue_range[1])
	elif sequence_state == "WHITE":
		cardvalue_range = list(WHITE_RANGE)
		cardvalue = random.randint(cardvalue_range[0],cardvalue_range[1])
	elif sequence_state == "BLUE":
		cardvalue_range = [uniform_distribution_parameters[0] - uniform_distribution_parameters[1], uniform_distribution_parameters[0] + uniform_distribution_parameters[1]]
		cardvalue = random.randint(cardvalue_range[0],cardvalue_range[1])
	else: 
		cardvalue_range = [uniform_distribution_parameters[0] - uniform_distribution_parameters[1], uniform_distribution_parameters[0] + uniform_distribution_parameters[1]]
		cardvalue = random.randint(cardvalue_range[0],cardvalue_range[1])
	return cardvalue_range, cardvalue


def introprompt():
	"""asks the user to read a document and type in a subject id, then click ok."""
	
	def saveclose():
		global _Subject_id
		_Subject_id = entry.get()
		
	introtext = '''
	Welcome!
	In this experiment, you will play 48 games. In each game, your goal is to achieve a score as highest as you can.
	In each game, there is a card deck. At the first turn, you have to flip over a card from the deck, by clicking on
	the 'Flip A New Card' button. After this, you can continue to flip over new cards by clicking on the 'Flip A New 
	Card' button; or you can choose the most recent card by clicking on the 'Make A Decision' button. Note that, you 
	can ONLY choose the most recent/latest card; if you reject one card, you can NOT go back and choose it again. 

	However, after you make your decision for choosing a card, you can continue flip over cards from the deck by clicking on the 
	'Flip A New Card' button. The difference is that:
	Before you make a decision, each time you flip over a card from the deck, there a 'Search Cost' applied to your final score of
	each game. The 'Search Cost' is 5 every time you flip over a card. Your total search cost would be the number of times you 
	flip over a card multiplying the 'Search Cost' 5. And your total score in one game will be the card value you choose minusing 
	your total search cost.
	After you make a decision, there is no additional search cost applied to your final score in the game. You can flip over cards
	freely from the deck without considering the 'Search Cost'.

	In each game, the card values of the deck have a specific range. The range varies for different colored decks. 
	Particularly:
	All the White card decks have the samge range; and in the experiment, the computer will show you the range of White decks.
	All the Black card decks have the same range; BUT in the experiment, the computer will NOT show you the range of Black decks.
	Each Yellow card deck has a unique range; and in the experiment, the computer will show you each range of Yellow decks.
	Each Blue card deck also has a unique range; BUT in the experiment, the computer will NOT show you any range of Blue decks.

	In addition, whenever you flip over a card from a deck, each card value in the range of the deck has equal probability to be
	draw and shown on the screen. That is, in each game, every time you flip over a card from a deck, you have equal probability
	to get every value within the range of the deck. So every flip is the same in one game for you.

	In each game, when you flip over a card from the deck, this is called one 'Turn'. In one game, you can flip over cards at most 
	to 80 times; so there are 80 turns in one game. The used turn and left turn information, with the trial number, the total search 
	cost will be shown at the lower right corner of the game screen. In addition, after you make a decision, the card value you choose
	and your final score in the game, will also be shown at the lower right corner.

	Please ask questions now if you have; Or start to play the games!	
	'''
	root = Tk()
	root.resizable(width=False, height=False)
	root.geometry('{}x{}'.format(1300,1000))
	root.title = "Instructions"
	label = Label(root, text = introtext, font=("Helvetica", 16),justify=LEFT,anchor=NE)
	label.pack()
	entry = Entry(root, borderwidth= 3)
	entry.insert(9999, "Enter Subject ID Here.")
	entry.pack(ipady = 8, padx = 5, pady = 5)
	button0 = Button(root, text = "Save Subject ID", font=("Helvetica", 12), command = saveclose, borderwidth= 3)
	button0.pack(padx = 5, pady = 5)
	button1 = Button(root, text = "Start  the  Game", font=("Helvetica", 12), command = root.destroy, borderwidth= 3)
	#NOT add button1 and click on close window will work; 
	#if you use root.quit, then the interface disabled, but it still will be shown, and the close window button not working, note the difference
	button1.pack(padx = 5, pady = 5)
	root.mainloop()

def post_game_prompt():
	'''
	after the game, tell subjects the game information briefly and ask them go to the experimenter
	'''
	def quit_game_sys():
		root.destroy
		#print 'whether it will be carried out here after root.destroy? YES!!'
		sys.exit()

	end_text = '''
	Congratulations! You have finished the experiment! 
	Please turn to the experimenter for further instructions!
	'''
	root = Tk()
	root.resizable(width=False, height=False)
	root.geometry('{}x{}'.format(900,600))
	root.title = "Game Information"
	label = Label(root, text = end_text, font=("Helvetica", 26),justify=LEFT,anchor=NE)
	label.pack(padx=15, pady=15)
	button1 = Button(root, text = "Quit the Game", font=("Helvetica", 15), command = quit_game_sys , borderwidth= 3)
	button1.pack(padx=15, pady=100, ipady = 10, ipadx = 30)
	root.mainloop()

   
def writeinit(subjectid):
	"""preps the file object, writes the initial header line"""
	global _Csvwriter, _Fileobj    
	filename = subjectid + "-data.csv"
   
   
   #create a fileobj
	_Fileobj = open(filename, 'wb')
	#create a csv.writer object
	_Csvwriter = csv.writer(_Fileobj)

	header = ['subject_id', 'trial', 'turn', 'card_value', 'selected_or_not','timeoflastclick', 'timeoflastclickdelta', 'deck_state', 'deck_range', 'search_cost', 'total_search_cost']
	#csv.writer write data into rows
	_Csvwriter.writerow(header)
	# in order to quit writing and the file, you need to close the file obj
	# but close the _Fileobj here will stop the further writing in the program
	#_Fileobj.close()



class Game_info:

	Decision_turn = 0
	
	def __init__(self, trial_number, num_card, current_value_set, surface):
		self.trial_number = trial_number
		self.turn = num_card
		self.left_turn = NUM_TURN - self.turn
		if len(current_value_set) == 0:
			self.current_value = 'Not Applicable'
		else:
			self.current_value = current_value_set[-1]
		self.surface = surface
		

	@staticmethod
	def set_Decision_turn(value):
		Game_info.Decision_turn = value

	def draw_game_info(self):
		game_info_wid_pos = 700
		game_info_height_pos = 620
		game_info_each_text_height = 30

		game_info_text0 = 'Current game is: ' + str(self.trial_number) +' of total ' + str(NUM_TRIAL) + ' games'
		game_info_text1 = 'Current turn is: '
		game_info_text1 += str(self.turn)
		#game_info_text += '\n'
		game_info_text2 = 'Number of turns left is: '
		game_info_text2 += str(self.left_turn)
		#game_info_text += '\n'
		game_info_text3 = 'Total search cost so far is: '
		if _Decision_or_not == False:
			game_info_text3 +=  str(SEARCH_COST) + str(' * ') + str(self.turn) + str(' = ') + str(SEARCH_COST * self.turn)
		else:
			game_info_text3 +=  str(SEARCH_COST) + str(' * ') + str(Game_info.Decision_turn) + str(' = ') + str(SEARCH_COST * Game_info.Decision_turn)
		
		#first draw the area for text, and erase the previous game info
		#self.surface.fill(pygame.Color(30, 98, 50), (game_info_wid_pos,game_info_height_pos,WIDTH - game_info_wid_pos,HEIGHT - game_info_height_pos))
		self.surface.fill(BACKGROUND_COLOR, (game_info_wid_pos,game_info_height_pos,WIDTH - game_info_wid_pos,HEIGHT - game_info_height_pos))
		#self.surface.fill(pygame.Color('white'), (300,500,500,90))
		#draw on the surface
		font_instance = pygame.font.SysFont('helvetica',25)
		#helvetica, times
		#font_instance = pygame.font.SysFont("comicsansms",25)
		#text1 is a new surface
		text0 = font_instance.render(game_info_text0,True,BLACK)
		text1 = font_instance.render(game_info_text1,True,BLACK)     
		text2 = font_instance.render(game_info_text2,True,BLACK)
		text3 = font_instance.render(game_info_text3,True,BLACK)
		
		#render the new surface on the game interface
		self.surface.blit(text0, (game_info_wid_pos,game_info_height_pos))
		self.surface.blit(text1, (game_info_wid_pos,game_info_height_pos+game_info_each_text_height))
		self.surface.blit(text2, (game_info_wid_pos,game_info_height_pos+game_info_each_text_height*2))
		self.surface.blit(text3, (game_info_wid_pos,game_info_height_pos+game_info_each_text_height*3))
		if _Decision_or_not == True:
			game_info_text4 = 'Card value you chose is: '
			game_info_text4 += str(Rect.Selected_rect.card_value) 
			game_info_text5 = 'Your final score in this game is: '
			game_info_text5 += str(Rect.Selected_rect.card_value) + str(' - ') + str(SEARCH_COST * Game_info.Decision_turn) + str(' = ') + str(Rect.Selected_rect.card_value - SEARCH_COST * Game_info.Decision_turn)
			text4 = font_instance.render(game_info_text4,True,BLACK)
			text5 = font_instance.render(game_info_text5,True,BLACK)
			self.surface.blit(text4, (game_info_wid_pos,game_info_height_pos+game_info_each_text_height*4))
			self.surface.blit(text5, (game_info_wid_pos,game_info_height_pos+game_info_each_text_height*5))
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
		#selected_or_not means whether subjs picked this card, 0 means NO and 1 means YES
		self.selected_or_not = 0
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
				pygame.draw.rect(self.surface, WHITE, (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
			else:
				pygame.draw.rect(self.surface, ALPHA, (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
		else:
			if self == Rect.Selected_rect:
				pygame.draw.rect(self.surface, WHITE, (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
			else:
				pygame.draw.rect(self.surface, ALPHA, (self.width_pos,self.height_pos,CARDWIDTH,CARDHEIGHT), 0)
				
	def draw(self):
		'''
		draw the rect instance and update its corresponding value
		'''
		rect_gap = 10
		self.regular_or_highlight()
		#the following code is drawing a frame of the card
		pygame.draw.rect(self.surface, LIGHTBLUE, (self.width_pos + rect_gap/2,self.height_pos + rect_gap/2, CARDWIDTH-rect_gap, CARDHEIGHT-rect_gap), 3)
		self.draw_card_value()
		pygame.display.flip()
		#you can actually only update part of the surface, using a rect tuple
	   
	   
	   #pygame.display.update((10,10,20,20))
	def draw_card_value(self):
		'''
		draw the card value on the Rect instance for each click
		second, before the exploit decision has been made, draw the total search cost on each card value in the lower of the card face
		'''
		#self.card_value
		#first creat a Font instace
		font_instance = pygame.font.SysFont("comicsansms",20)
		font_instance_search_cost = pygame.font.SysFont("comicsansms",13)
		#text1 is a new surface
		text1=font_instance.render(str(self.card_value),True,(77,77,77))     
		#render the new surface on the game interface
		self.surface.blit(text1, (self.width_pos + self.cardwidth/4, self.height_pos+ self.cardheight*3/10))
		#self.surface.blit(text1, (self.width_pos, self.height_pos))
		if Rect.Post_exploration == False:
			total_search_cost_text = '-' + str((self.click_time + 1) * SEARCH_COST)
			total_search_cost_surface =  font_instance_search_cost.render(total_search_cost_text, True, (220,20,60))
			self.surface.blit(total_search_cost_surface, (self.width_pos + self.cardwidth/2, self.height_pos+ self.cardheight))

	
def draw_card_deck(surface,condition,uniform_dis):
	'''
	draw the deck given the four conditions: ['BLACK','WHITE','DARKBLUE','LIGHTYELLOW']
	and also put the text above the deck to give information to subjects
	'''
	#card_range here, for black and white, is NOT right, because the ranges for them is already computed 
	card_range = [uniform_dis[0] - uniform_dis[1], uniform_dis[0] + uniform_dis[1]]
	font_size = 22
	deck_width = 90
	deck_height = 120
	deck_wid_pos = 0
	deck_height_pos = HEIGHT - deck_height

	deck_rect_width = 75
	deck_rect_height = 105
	deck_rect_width_pos = (deck_width - deck_rect_width)/2
	deck_rect_height_pos = deck_height_pos + (deck_height - deck_rect_height)/2
	deck_rect_border = 4

	text_font_type = 'Helvetica'

	text_wid_pos = 2
	text_height_pos1 = deck_height_pos - font_size*1.5
	text_height_pos2 = deck_height_pos - font_size*2.5
	text_width = 450
	text_height = deck_rect_height_pos - text_height_pos2

	Window0 = surface
	if condition == 'BLACK':
		pygame.draw.rect(Window0, BLACK, (deck_wid_pos,deck_height_pos, deck_width, deck_height), 0)
		pygame.draw.rect(Window0, LIGHTBLUE, (deck_rect_width_pos,deck_rect_height_pos,deck_rect_width,deck_rect_height), deck_rect_border)  
		deck_info = pygame.font.SysFont(text_font_type, font_size)
		range_info = pygame.font.SysFont(text_font_type, font_size)
		deck_window = deck_info.render('All BLACK decks have the same card range', 0, BLACK)
		range_window = range_info.render('This deck\'s range is the same as before', 0, BLACK)
		#Window0.fill(BACKGROUND_COLOR, (text_wid_pos, text_height_pos2, text_width, text_height))
		Window0.blit(deck_window, (text_wid_pos, text_height_pos2))
		Window0.blit(range_window, (text_wid_pos, text_height_pos1))
	elif condition == 'WHITE':
		pygame.draw.rect(Window0, WHITE, (deck_wid_pos,deck_height_pos, deck_width, deck_height), 0)
		pygame.draw.rect(Window0, LIGHTBLUE,  (deck_rect_width_pos,deck_rect_height_pos,deck_rect_width,deck_rect_height), deck_rect_border) 
		deck_info = pygame.font.SysFont(text_font_type, font_size)
		range_info = pygame.font.SysFont(text_font_type, font_size)
		deck_window = deck_info.render('All WHITE decks have the same card range:', 0, WHITE)
		range_window = range_info.render('The range is always: ' + str(list(WHITE_RANGE)), 0, WHITE)
		#Window0.fill(BACKGROUND_COLOR, (text_wid_pos, text_height_pos2, text_width, text_height))
		Window0.blit(deck_window, (text_wid_pos, text_height_pos2))
		Window0.blit(range_window, (text_wid_pos, text_height_pos1))

	elif condition == 'BLUE':
		pygame.draw.rect(Window0, BLUE, (deck_wid_pos,deck_height_pos, deck_width, deck_height), 0)
		pygame.draw.rect(Window0, LIGHTBLUE,  (deck_rect_width_pos,deck_rect_height_pos,deck_rect_width,deck_rect_height), deck_rect_border) 
		deck_info = pygame.font.SysFont(text_font_type, font_size)
		range_info = pygame.font.SysFont(text_font_type, font_size)
		deck_window = deck_info.render('Each BLUE deck has a unique card range', 0, BLUE)
		range_window = range_info.render('This deck\'s range is different from previous BLUEs', 0, BLUE)
		#Window0.fill(BACKGROUND_COLOR, (text_wid_pos, text_height_pos2, text_width, text_height))
		Window0.blit(deck_window, (text_wid_pos, text_height_pos2))
		Window0.blit(range_window, (text_wid_pos, text_height_pos1))
	else:
		pygame.draw.rect(Window0, YELLOW, (deck_wid_pos,deck_height_pos, deck_width, deck_height), 0)
		pygame.draw.rect(Window0, LIGHTBLUE, (deck_rect_width_pos,deck_rect_height_pos,deck_rect_width,deck_rect_height), deck_rect_border)
		deck_info = pygame.font.SysFont(text_font_type, font_size)
		range_info = pygame.font.SysFont(text_font_type, font_size)
		deck_window = deck_info.render('Each YELLOW deck has a unique card range', 0, YELLOW)
		range_window = range_info.render('This deck\'s range is: ' + str(card_range), 0, YELLOW)
		#Window0.fill(BACKGROUND_COLOR, (text_wid_pos, text_height_pos2, text_width, text_height))
		Window0.blit(deck_window, (text_wid_pos, text_height_pos2))
		Window0.blit(range_window, (text_wid_pos, text_height_pos1))




pygame.init()
######first introduction window
introprompt()
##write in the subject information into CSV file 
writeinit(_Subject_id)

#generate the sequence of conditions beforehand
sequence_conditions = generate_condition_seq(total_num_trial = NUM_TRIAL) 
#sequence_state is the variable deciding what condition of the current trial is
sequence_state = sequence_conditions[0]
num_unique_uniform_distribution = NUM_TRIAL/len(NUM_CONDITIONS)
#num_unique_uniform_distribution = 12
unique_uniform_distributions = generate_uniform_dis(num_unique_uniform_distribution)
uniform_distributions_list = generate_uniform_distributions_list(unique_uniform_distributions, sequence_conditions)
#uniform_distributions_list contains all the uniform distributions in the experiment, each element corresponding to the sequence_conditions, canNOT mis-match
#the following uniform_dis_state is the corresponding uniform distribution state for each sequence_state
uniform_dis_state = uniform_distributions_list[0]



#Do we need this clock object in this gamet to keep the updating controlable?
FPSCLOCK = pygame.time.Clock()
Window0 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A Decision Task')
Window0.fill(BACKGROUND_COLOR)
#pygame.display.flip()
#Deck = pygame.image.load('deck.jpg')
#Deck1 = pygame.transform.smoothscale(Deck, (60,80))
#Window0.blit(Deck1, (0,520))
draw_card_deck(Window0, sequence_state, uniform_dis_state)

button_width_pos = 110
button_width = 150
button_height = 30
button_gap = 10
button_height_pos1 = 680
button_height_pos2 = button_height_pos1 + button_height + button_gap
button_height_pos3 = button_height_pos2 + button_height + button_gap
button_Before_Ex =  PygButton((button_width_pos, button_height_pos1, button_width, button_height), 'Flip A New Card')
button_Decision =  PygButton((button_width_pos, button_height_pos2, button_width, button_height), 'Make A Decision')
button_Next =  PygButton((button_width_pos, button_height_pos3, button_width, button_height), 'Next Round')


buttonDecision_visMode = True
button_Next_visMode = False
button_Before_Ex_visMode = True
#has to assign the visMode to the buttons first before you draw it.  NOTE: visMode has to be assign, otherwise...
button_Decision.visible = buttonDecision_visMode
button_Next.visible = button_Next_visMode
button_Before_Ex.visible = button_Before_Ex_visMode
# button_Before_Ex.draw(Window0)
# button_Decision.draw(Window0)	
# button_Next.draw(Window0)
# pygame.display.flip()


#global variable _Decision_or_not , to record whether each game has been made decision or not yet
_Decision_or_not = False
running = True
click_counter = 0
rect_set = []
exp_trial = 1

#global timeoflastclick
#global timeoflastclickdelta
timeoflastclick = time.time()
timeoflastclickdelta = 0




while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			_Fileobj.close()
			pygame.quit()
			sys.exit()        
		# button_Before_Ex.handleEvent(event) is a queue
		if 'click' in button_Before_Ex.handleEvent(event):
			'''
			if click on the exploration buttion
			'''
			#card value generated function here:  

			#note that in the 'random' package, randint includes both ends; but in the numpy.random package, randint is [ ), not includes the highest value
			#card_value_generated = random.randint(LOWEST, HIGHEST)
			cardvalue_range, card_value_generated = generate_card_values(sequence_state = sequence_state, uniform_distribution_parameters = uniform_dis_state)
			#print cardvalue_range

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
			exp_turn = click_counter + 1
			##the right way is to set selected as an instance attribute!

			#let us say last is the recent one, and timeoflastclick is the recent happening time; and the timeoflastclickdelta is
			#the delta time from the second recent to the recent one; first save the happening time to a transit variable, get the
			#delta time, and then save the transit time to the timeoflastclick
			transit_click_time = time.time()
			timeoflastclickdelta = transit_click_time - timeoflastclick
			timeoflastclick = transit_click_time
			#in this way, in the output data: 1) each row's lasttime - the prevous row's will get the delta time in the same row
			#2) for the first row, we canNOT because we didnot save the original time.time() for the last time
			#3)from the second trial, the first row's delta time includes two parts: a) RT for clicking on the 'NEXT'button and RT for clicking on the flipover button in the following trial
			#4)for the last trial, we canNOT record the RT for clicking on the NEXT Round button(when the game is quitting), SO for study 'NEXT' RT, just exclude 1s row of the first trial
			
			#other variables to save:search cost, total search cost; BUT NOT: final score---will be computed afterhand,not saved in the data
			#card value range is very important to save; so is the deck condition(sequence_state)
			if _Decision_or_not == 0:
				total_search_cost = SEARCH_COST * exp_turn
			else:
				total_search_cost = SEARCH_COST * Game_info.Decision_turn


			row = [_Subject_id, exp_trial, exp_turn, rect.card_value, rect.selected_or_not, timeoflastclick, timeoflastclickdelta, sequence_state, cardvalue_range, SEARCH_COST,total_search_cost]
			_Csvwriter.writerow(row)
			
			
			###########################
			click_counter += 1
			#there is mis-match by 1 between click_counter and NUM_TURN::
			if click_counter + 1 > NUM_TURN:
				button_Before_Ex_visMode = False
				button_Before_Ex.visible = button_Before_Ex_visMode
				Window0.fill(BACKGROUND_COLOR, (button_width_pos, button_height_pos1, button_width+button_gap, button_height+button_gap))
				#next_game_message = 'Please go to next game'
				next_game_message = pygame.font.SysFont('Helvetica', 30)
				next_game_message_window = next_game_message.render('Please go to next game', 0, RED)
				Window0.blit(next_game_message_window, (button_width_pos, button_height_pos1))
			
		if 'click' in button_Decision.handleEvent(event):
			'''
			click on the decision button will:
			make the current value be highlighted until the end of this game
			activate the next round button
			disable itself
			when there is no card on the scree, do nothing;

			There are 4 variable to indicate whether the decision has been made or not:
			1) rect.selected_or_not = 1 --for the specific rect
			2)_Decision_or_not--global variable to indicate
			3)Rect.set_post_exp_and_sel_rect(post_exploration = True....---indicate this in the Rect Class
			4) Game_info.Decision_turn is a real number
			'''
			#when there is no card, do nothing when clicking the decision button
			if len(rect_set) == 0:
				pass
			else:
				#save the selected card data's attributes AGAIN in the data file, for one new row
				#set the current rect been selected as 1: directly or could create a method in the class
				#originally, rect.selected_or_not is 0 by default for each rect
				rect.selected_or_not = 1
				#change the global variable _Decision_or_not to 1
				_Decision_or_not = True
				#change the Game_info class's Decision_turn value
				Game_info.set_Decision_turn(exp_turn)
				total_search_cost = SEARCH_COST * Game_info.Decision_turn
				# there is absolute 'turn' meaning for selection/exploitation time
				# so keep exp_turn the same, easy to tell when the selection happens and at which turn
				# also keep rect.card_value the same
				transit_click_time = time.time()
				timeoflastclickdelta = transit_click_time - timeoflastclick
				timeoflastclick = transit_click_time

				row = [_Subject_id, exp_trial, exp_turn, rect.card_value, rect.selected_or_not,timeoflastclick, timeoflastclickdelta,sequence_state, cardvalue_range, SEARCH_COST,total_search_cost]
				_Csvwriter.writerow(row)

				Rect.set_post_exp_and_sel_rect(post_exploration = True, selected_rect = rect_set[-1])
				# make the Decision button disable; draw colors or rect on it not working; have to cover the previous drawn Decsion button area, and draw a new invisiable button onto Window0
				Window0.fill(BACKGROUND_COLOR, (button_width_pos, button_height_pos2, button_width+button_gap, button_height+button_gap))
				buttonDecision_visMode= False
				button_Next_visMode = True
				#assign the button mode to  the two button Objects
				button_Decision.visible = buttonDecision_visMode
				button_Next.visible = button_Next_visMode  
				
		
		if 'click' in button_Next.handleEvent(event):
			'''
			clicking on the NEXT BUTTON will reset the experiment to the Next game
			'''
			Window0.fill(BACKGROUND_COLOR)
			button_Next_visMode = False
			buttonDecision_visMode = True
			button_Before_Ex_visMode = True
			button_Decision.visible = buttonDecision_visMode
			button_Next.visible = button_Next_visMode     
			button_Before_Ex.visible = button_Before_Ex_visMode
			#reset the Rect attributes to start a new game
			Rect.reset_Rect_Class_attributes()
			
			rect_set = []
			click_counter = 0
			_Decision_or_not = 0
			Game_info.set_Decision_turn(0)
			
			exp_trial += 1
			#when the trial_num exceeds the NUM_TRIAL in this experiment, quit the pygame, close the file and quit the system
			if exp_trial > NUM_TRIAL:
				running = False
				#if not need further data, should use following to securely save data
				_Fileobj.close()
				pygame.quit()
				post_game_prompt()
				#yes, from the below line:it will prompt the Tkinter loop forever because of the 'root.mainloop()'
				#and before you kill it, the following statement would NOT be executed
				#print pygame.version.ver 
				#most safe way to quit the system, you can actually add one button in the last prompt to quit the system
				#in case something wrong in the prompt, add sys.exit() here so you can still safely quit the system
				sys.exit()

			#update the card deck conditions, if the game is still on
			#because the exp_trial is move one step forward, so in the sequence_conditions list, has to use exp_trial - 1 
			sequence_state = sequence_conditions[exp_trial-1]
			uniform_dis_state = uniform_distributions_list[exp_trial-1]

			draw_card_deck(Window0, sequence_state, uniform_dis_state)
			pygame.display.update()
			#print pygame.version.ver 
			  
	game_info = Game_info(exp_trial, Rect.Num_card, Rect.Card_value_set, Window0)
	game_info.draw_game_info()
	#in order to show the clicking effect, you have to draw the button instance to the surface for every event, not every CLICK(within the above 'if' statement)!!
	button_Before_Ex.draw(Window0)
	button_Decision.draw(Window0)
	button_Next.draw(Window0)
	pygame.display.update()
	FPSCLOCK.tick(FPS)        


