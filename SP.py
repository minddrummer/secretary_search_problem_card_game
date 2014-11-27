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
# add TRY section?
# modulize the runing part, add trials and conditions
# add function to tracking clicking time!
# add details about the experiment above
# save the all NECESSARY data 
# 
# ------------------------to do list---------------------------------
# 1) add time tracking to the data writing
# 2)modulize the runing part, add conditions and draw the condition information on the surface
# :: set the condition information as one attribute to the rect instance? MAYBE....





import pygame, sys
import math, time, string
import pygbutton
import random
import csv
from Tkinter import * 
#above: use the module of Tkinter without calling Tkinter.
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
NUM_TRIAL = 2
NUM_CONDITIONS = 4
#ANIMATION_ON = True


def introprompt():
	"""asks the user to read a document and type in a subject id, then click ok."""
	
	def saveclose():
		global _Subject_id
		_Subject_id = entry.get()
		
	introtext = '''Welcome. 
	Black deck: repeated, no information
	White deck: repeated, with information
	Dark colored decks:one shot, no information
	Light colored decks: one shot, with information'''
	root = Tk()
	root.resizable(width=False, height=False)
	root.geometry('{}x{}'.format(1000,800))
	root.title = "Instructions"
	label = Label(root, text = introtext, font=("Helvetica", 16),justify=LEFT,anchor=NE)
	label.pack()
	entry = Entry(root)
	entry.insert(9999, "Enter Subject ID Here.")
	entry.pack(ipady = 8)
	button0 = Button(root, text = "Save Subject ID", font=("Helvetica", 12), command = saveclose)
	button0.pack()
	button1 = Button(root, text = "Start the Game", font=("Helvetica", 12), command = root.destroy)
	#NOT add button1 and click on close window will work; 
	#if you use root.quit, then the interface disabled, but it still will be shown, and the close window button not working, note the difference
	button1.pack()
	root.mainloop()

def post_game_prompt():
	'''
	after the game, tell subjects the game information briefly and ask them go to the experimenter
	'''
	def quit_game_sys():
		root.destroy
		#print 'whether it will be carried out here after root.destroy? YES!!'
		sys.exit()

	end_text = '''Congratulations!  You finish the game! Please turn to the experimenter
	for further instructions!'''
	root = Tk()
	root.resizable(width=False, height=False)
	root.geometry('{}x{}'.format(1000,800))
	root.title = "Game Information"
	label = Label(root, text = end_text, font=("Helvetica", 16),justify=LEFT,anchor=NE)
	label.pack()
	button1 = Button(root, text = "Quit the Game", font=("Helvetica", 12), command = quit_game_sys)
	button1.pack()
	root.mainloop()

   
def writeinit(subjectid):
	"""preps the file object, writes the initial header line"""
	global _Csvwriter, _Fileobj    
	filename = subjectid + "-data.csv"
   
   
   #create a fileobj
	_Fileobj = open(filename, 'wb')
	#create a csv.writer object
	_Csvwriter = csv.writer(_Fileobj)
	header = ['subjectid','trial','turn','explore0_exploit1','switch_exploit?','switch_PE?', 'timeofclick','timesincelastclick','numberofcards','cardvalue','exploitCards','maxvalueontable','totalpoint']
	#csv.writer write data into rows
	_Csvwriter.writerow(header)
	# in order to quit writing and the file, you need to close the file obj
	# but close the _Fileobj here will stop the further writing in the program
	#_Fileobj.close()



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
	
def draw_card_deck(surface):
	Window0 = surface
	pygame.draw.rect(Window0,(31,31,31), (0,520, 60, 80), 0)
	pygame.draw.rect(Window0, (6,113,148), (5,525,50,70), 3)    


pygame.init()
######first introduction window
introprompt()
##write in the subject information into CSV file 
writeinit(_Subject_id)

#Do we need this clock object in this gamet to keep the updating controlable?
FPSCLOCK = pygame.time.Clock()
Window0 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A Decision Task')
Window0.fill(BACKGROUND_COLOR)
#pygame.display.flip()
#Deck = pygame.image.load('deck.jpg')
#Deck1 = pygame.transform.smoothscale(Deck, (60,80))
#Window0.blit(Deck1, (0,520))
draw_card_deck(Window0)
button_Before_Ex = pygbutton.PygButton((70, 490, 150, 30), 'Flip A New Card')
button_Decision = pygbutton.PygButton((70, 530, 150, 30), 'Make A Decision')
button_Next = pygbutton.PygButton((70, 570, 150, 30), 'Next Round')


buttonDecision_visMode = True
button_Next_visMode = False
#has to assign the visMode to the buttons first before you draw it.  NOTE: visMode has to be assign, otherwise...
button_Decision.visible = buttonDecision_visMode
button_Next.visible = button_Next_visMode

# button_Before_Ex.draw(Window0)
# button_Decision.draw(Window0)
# button_Next.draw(Window0)
# pygame.display.flip()



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
			card_value_generated = random.randint(LOWEST, HIGHEST)
			
			
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

			row = [_Subject_id, exp_trial, exp_turn, rect.card_value, rect.selected_or_not, timeoflastclick, timeoflastclickdelta]
			_Csvwriter.writerow(row)
			
			
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
				#save the selected card data's attributes AGAIN in the data file, for one new row
				#set the current rect been selected as 1: directly or could create a method in the class
				rect.selected_or_not = 1
				# there is absolute 'turn' meaning for selection/exploitation time
				# so keep exp_turn the same, easy to tell when the selection happens and at which turn
				# also keep rect.card_value the same
				transit_click_time = time.time()
				timeoflastclickdelta = transit_click_time - timeoflastclick
				timeoflastclick = transit_click_time
				row = [_Subject_id, exp_trial, exp_turn, rect.card_value, rect.selected_or_not,timeoflastclick, timeoflastclickdelta]
				_Csvwriter.writerow(row)

				Rect.set_post_exp_and_sel_rect(post_exploration = True, selected_rect = rect_set[-1])
				# make the Decision button disable; draw colors or rect on it not working; have to cover the previous drawn Decsion button area, and draw a new invisiable button onto Window0
				Window0.fill(BACKGROUND_COLOR, (60, 520, 200, 40))
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
			button_Decision.visible = buttonDecision_visMode
			button_Next.visible = button_Next_visMode     

			#reset the Rect attributes to start a new game
			Rect.reset_Rect_Class_attributes()
			
			rect_set = []
			click_counter = 0
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

			draw_card_deck(Window0)
			pygame.display.update()
			#print pygame.version.ver 
			  
	game_info = Game_info(Rect.Num_card, Rect.Card_value_set, Window0)
	game_info.draw_game_info()
	#in order to show the clicking effect, you have to draw the button instance to the surface for every event, not every CLICK(within the above 'if' statement)!!
	button_Before_Ex.draw(Window0)
	button_Decision.draw(Window0)
	button_Next.draw(Window0)
	pygame.display.update()
	FPSCLOCK.tick(FPS)        


def main():
	pass

