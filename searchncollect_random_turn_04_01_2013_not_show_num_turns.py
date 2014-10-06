


#Things to fix
# 1)why it doesnot transfer to questions and save the data:
#now after you escape and kill the IDLE, the data can be saved fully!
#but I donot know what would happen after being transferred to a EXE file
# 2) transfer it to EXE file
#3) change the final instruction to fit
'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: Search & Collect'

import time, math, string
import pyglet
from string import strip,replace
from pyglet import font
from pyglet.window import mouse
from pyglet.window import key
from pyglet import image
import random
from math import sqrt
from Tkinter import *
from Canvas import Rectangle, Group, Window
window = pyglet.window.Window(1024,800)



#try:
#    sys.stdout.write("\n")
#    sys.stdout.flush()
#except IOError:
#    class dummyStream:
#        ''' dummyStream behaves like a stream but does nothing. '''
#        def __init__(self): pass
#        def write(self,data): pass
#        def read(self,data): pass
#        def flush(self): pass
#        def close(self): pass
#    # and now redirect all default streams to this dummyStream:
#    sys.stdout = dummyStream()
#   sys.stderr = dummyStream()
#    sys.stdin = dummyStream()
#   sys.__stdout__ = dummyStream()
#   sys.__stderr__ = dummyStream()
#    sys.__stdin__ = dummyStream()





class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [200, 200, 220, 255] * 4)
        )

class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), 
            dict(color=(0, 0, 0, 255))
        )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

class Window(pyglet.window.Window):
    global error
    def __init__(self, *args, **kwargs):
        error=0
        super(Window, self).__init__(960, 600, caption='Post-experiment Questionaire')

        self.batch = pyglet.graphics.Batch()
        self.labels = [
            pyglet.text.Label('We would like to ask you about your general strategy for doing this task.  At different points in the game, you may have felt that',
                anchor_y='top', color=(0, 0, 0, 255), x=10, y=580, 
                batch=self.batch),
            pyglet.text.Label('if you had a large enough card value showing on the table,then you would be satisfied with it, and would pick it instead of.',
                anchor_y='top', color=(0, 0, 0, 255), x=10, y=540, 
                batch=self.batch),     
            pyglet.text.Label('drawing a new card from the deck. For example, on the first round, if you happened to draw a 99, then you may have been',
                anchor_y='top', color=(0, 0, 0, 255), x=10, y=500, 
                batch=self.batch),  
            pyglet.text.Label('satisfied enough with it to pick it for the rest of the game.  For each of the rounds listed below, what was the LOWEST value',
                anchor_y='top', color=(0, 0, 0, 255), x=10, y=460, 
                    batch=self.batch),
            pyglet.text.Label('for a card that would been enough for you to pick it for the rest of the game?',
                anchor_y='top', color=(0, 0, 0, 255), x=10, y=420, 
                    batch=self.batch),
            pyglet.text.Label('When you are finished, click the <space bar> to submit your numbers.',
                anchor_y='top', color=(0, 0, 0, 255), x=10, y=380, 
                    batch=self.batch),

            pyglet.text.Label('For the 2nd round out of 20, the lowest card that would be enough was', x=10, y=220, anchor_y='bottom',
                color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('For the 5th round out of 20, the lowest card that would be enough was', x=10, y=180, anchor_y='bottom',
                color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('For the 9th round out of 20, the lowest card that would be enough was', x=10, y=140, 
                anchor_y='bottom', color=(0, 0, 0, 255), 
                batch=self.batch),
            pyglet.text.Label('For the 13th round out of 20, the lowest card that would be enough was', x=10, y=100, 
                anchor_y='bottom', color=(0, 0, 0, 255), 
                batch=self.batch),
            pyglet.text.Label('For the 17th round out of 20, the lowest card that would be enough was', x=10, y=60, 
                anchor_y='bottom', color=(0, 0, 0, 255), 
                batch=self.batch),
            pyglet.text.Label('For the 20th round out of 20, the lowest card that would be enough was', x=10, y=20, 
                anchor_y='bottom', color=(0, 0, 0, 255), 
                batch=self.batch)
                ]
               
                    
        self.widgets = [ #to access the actual contents of these text boxes, use         print self.widgets[x].document.text
            TextWidget('', 550, 220, 40, self.batch),
            TextWidget('', 550, 180, 40, self.batch),   
            TextWidget('', 550, 140, 40, self.batch),#instead of 40, was self.width - 210 - but that extended all the way to the right edge
            TextWidget('', 550, 100, 40, self.batch),
            TextWidget('', 550, 60, 40, self.batch),
            TextWidget('', 550, 20, 40, self.batch)
        ]
        self.text_cursor = self.get_system_mouse_cursor('text')

                    
        self.focus = None
        self.set_focus(self.widgets[0])

    def on_resize(self, width, height):
        super(Window, self).on_resize(width, height)
        for widget in self.widgets:
            widget.width = width - 110

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)
      
    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)
            
    def on_key_press(self, symbol, modifiers):
        global thresholds
        global error
        global subjectid
        if symbol==pyglet.window.key.SPACE:
            error = 0
            for i in range(6):
                an_error=0
                try: float(self.widgets[i].document.text.strip())  #The strip () gets rids of any spaces in the number
                except ValueError:
                    error = error + 1 # an error on any of the six inputs should abort
                    an_error=1
                if an_error == 0:
                    thresholds[i]=float(self.widgets[i].document.text)
                else:
                     thresholds[i]='?'                
                 #convert the strings to numbers
            if error >0:
                 self.labels.append (pyglet.text.Label('Not all of your inputs are numbers',
                     anchor_y='top', color=(255, 0, 0, 255), x=10, y=340, 
                         batch=self.batch))
            else:           
                self.labels.append (pyglet.text.Label('Thanks again for your participation!  You are done!',
                    anchor_y='top', color=(255, 0, 0, 255), x=10, y=300, 
                        batch=self.batch))
                csvwriter.writerow([subjectid,999]+ thresholds)
                #print thresholds
                pyglet.app.exit()
        
        if symbol == pyglet.window.key.TAB:
            if modifiers & pyglet.window.key.MOD_SHIFT:
                dir = -1
            else:
                dir = 1

            if self.focus in self.widgets:
                i = self.widgets.index(self.focus)
            else:
                i = 0
                dir = 0

            self.set_focus(self.widgets[(i + dir) % len(self.widgets)])

        elif symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        
    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)


def introprompt():
    """asks the user to read a document and type in a subject id, then click ok."""
    def saveclose():
        global subjectid
        subjectid = entry.get()
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


def secondprompt():
    """displays a prompt telling the user the first game is coming"""
    text = 'To start the first game, click the red X button in the corner of THIS window when you are ready.'
    root = Tk()
    root.title = "Please read"
    label = Label(root, text = text, font=("Helvetica", 18))
    label.pack()
    sys.stdout.write('\a')
    sys.stdout.flush()
    root.mainloop()



def interimprompt():
    """displays a prompt telling the user another game is coming"""
    text = 'Well done!  Now please take a moment to prepare for the next game.\nClick the red X button in the upper right corner of THIS window when you are ready.'
    root = Tk()
    root.title = "Please read"
    label = Label(root, text = text, font=("Helvetica", 18))
    label.pack()
    sys.stdout.write('\a')
    sys.stdout.flush()
    root.mainloop()


def finalprompt():
    """displays a prompt telling the user the games are all over"""
    text = 'Great--that was the last game.  Thank you for your participation.\nClick the red X button in the upper right corner of THIS window to end the program.'
    root = Tk()
    root.title = "Please read"
    label = Label(root, text = text, font=("Helvetica", 18))
    label.pack()
    sys.stdout.write('\a')
    sys.stdout.flush()
    root.mainloop()


class Sprite(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        self.image.blit(self.x, self.y)

class Card (Sprite):
    image=pyglet.resource.image('card.jpg')
 #   def on_mouse_motion(self, x, y, dx, dy):   #This is if we want to move the card
 #        self.x += dx
 #        self.x = min(max(0, self.x), window.width - self.image.width)



def draw_deck(cards,reallydraw=1):
    global cards_coords
    x_pos=0
    y_pos=0
    label.draw()
    if len(cards)>0:
        max_value=max(cards)
    else:
        max_value=0
    cards_coords=[]
    for i in range (len(cards)):
        if cards[i]==max_value:
            value_color=(255,0,0,255)
        else:
            value_color=(0,100,100,255)
        if i==clicked_card:
            font_bigness=24
        else:
            font_bigness=18
        card_value=pyglet.text.Label(str(cards[i]),font_name='Times New Roman', color=value_color,
        font_size=font_bigness,x=x_pos*down_card.width*2+x_offset-10+down_card.width/2, y=window.height-y_pos*down_card.height*2+y_offset+down_card.height/2,
        halign='center', anchor_y='center')
        if reallydraw or (i<len(cards)-1):
            down_card.blit(x_pos*down_card.width*2+x_offset,window.height-y_pos*down_card.height*2+y_offset)
            card_value.draw()
        cards_coords.append((x_pos*down_card.width*2+x_offset+down_card.width/2,window.height-y_pos*down_card.height*2+y_offset+down_card.height/2))
        x_pos=x_pos+1
        if (x_pos+1)*down_card.width*2+x_offset > window.width:
            x_pos=0
            y_pos=y_pos+1


def distance(x1,y1,x2,y2):
    return (math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)))
            
def move_value(which_card):
    global turn_number
    global accumulated_points1
    global accumulated_points2
    global moving_card
    global something_happened
    
    for i in range(num_frames,0,-1):
        x_position=(((turn_number%values_per_row)*37+120)*(num_frames-i)+cards_coords[which_card][0]*i)/num_frames  # first part is destination, second is original location
        if turn_number<values_per_row:
            y_position = (100*(num_frames-i)+cards_coords[which_card][1]*i)/num_frames
        else:
            y_position = (70*(num_frames-i)+cards_coords[which_card][1]*i)/num_frames
        card_value=pyglet.text.Label(str(cards[which_card]),font_name='Times New Roman', color=(125,125,125,255),
        font_size=18,x=x_position, y=y_position,halign='center', anchor_y='center')
        card_value.draw()
        window.flip()
    if turn_number<values_per_row:
        selected_cards1.append(cards[which_card])         
        accumulated_points1=pyglet.text.Label(string.strip (string.replace(str(selected_cards1),',','+'),'[ ]'),font_name='Times New Roman', color=(125,125,125,255),
        font_size=18,x=120, y=100,halign='left', anchor_y='center')
    else:
        selected_cards2.append(cards[which_card])         
        accumulated_points2=pyglet.text.Label(string.strip (string.replace(str(selected_cards2),',','+'),'[ ]'),font_name='Times New Roman', color=(125,125,125,255),
        font_size=18,x=120, y=70,halign='left', anchor_y='center')
    moving_card = 0
    something_happened = 1
    
@window.event
def on_mouse_press (x, y, button, modifiers):
        global clicked_card
        global cards_in_deck
        global timeoflastclick
        global timeoflastclickdelta
        global something_happened
        global exploit
        global max_before_turn
        global last_table_card_clicked
        global cards
        global table_card
        global moving_card # by making this global, I declare that I mean the globally declared moving_card
        clicked_card=-1
        something_happened = 1
        if (button == mouse.LEFT) and ((moving_card == 0) and (break_taking ==0)):
            timeoflastclickdelta = time.time() - timeoflastclick
            timeoflastclick = time.time()
             #       print(x)
            if distance (x,y,my_card.x+(my_card.image.width/2),my_card.y+(my_card.image.height/2)) < acceptable_distance:
                if len(cards) > 0:
                    max_before_turn=max(cards)    
                #window.pop_handlers()
                moving_card=1 # moving a card from deck
                cards.append(card_series[len(cards)])
                 
            else: #subjects may be exploiting a card on the table
                for i in range(len(cards)):
                    x_position=cards_coords[i][0]
                    y_position=cards_coords[i][1]
                    if (distance(x,y,x_position,y_position)<(acceptable_distance/2)):
                        if len(cards) > 0:
                            table_card=i
                           # clicked_card=i
                           # if cards[table_card] > 0:
                    # decrement the value of the clicked card if it's not zero yet:
                           #     cards[table_card] -= DEPLETION_RATE
                      
                        max_before_turn=max(cards)    
                        moving_card=2 # moving a table card
                        

        
        #while moving_card == 1:  #I thought this might wait around until the moving is done
          #  i=1
       
       # window.push_handlers(on_mouse_press)   # if don't include on_mouse_press, all events are gone.  If include it, then mouse presses are recognized again

@window.event
def on_key_press(symbol,modifiers):
    global continued
    if symbol == key.A:
           continued = 1
    ## add on to exit the program and save the data??
    #if symbol == key.ESCAPE:
    #       pyglet.app.exit()
def list2str(ls):
    """converts a list to a string without commas or brackets"""
    return " ".join(map(str, ls))
            


def writeinit(subjectid):
    """preps the file object, writes the initial header line"""
    filename = subjectid + "-data.csv"
    fileobj = open(filename, 'wb')
    import csv
    global csvwriter
    csvwriter = csv.writer(fileobj)
    header = ['subjectid','trial','turn','exploit','switch_exploit?','timeofclick','timesincelastclick','numberofcards','cardvalue','exploitCards','maxvalueontable','totalpoint',
         'optimalthreshold','totaloptimalpoints','optimalcardnumber','maxvalonoptimaltable','isoptimalexploiting','optimalcardvalue']
    csvwriter.writerow(header)
    #fileobj.close()

def break_between_games():
    global optimal_points
    global continued
    global trialnumber
    global trials
    #global total_turns
    #current_total_turns = total_turns
    window.clear()
    label = pyglet.text.Label('Press the "A" key to Continue to the next game', 
                              font_name='Times New Roman', 
                              font_size=20,
                              x=50, y=window.height-280,
                              halign='center', anchor_y='bottom')
    label.draw()
    label = pyglet.text.Label('You got ' +str(sum(selected_cards1)+sum(selected_cards2))+ ' points', # + 'and ' + str(current_total_turns)+' turns in this game', 
                            # 1) you might want to fix the above to show the current_total_turns after finishing every trial--currently no presence
                            font_name='Times New Roman', 
                            font_size=20,
                            x=50, y=window.height-40,
                            halign='center', anchor_y='bottom')
    label.draw()
    #label = pyglet.text.Label('The computer got ' +str(optimal_points)+ ' points',
    #                        font_name='Times New Roman', 
    #                        font_size=20,
    #                        x=50, y=window.height-80,
    #                        halign='center', anchor_y='bottom')
    #label.draw()
    #if sum(selected_cards1)+sum(selected_cards2) == optimal_points:
    #    label = pyglet.text.Label('Congratulations!  You did as well as the best strategy!',
    #                            font_name='Times New Roman', 
    #                            font_size=20,color=(255, 0, 0, 255),
    #                            x=50, y=window.height-120,
    #                            halign='center', anchor_y='bottom')
    #    label.draw()
    #if sum(selected_cards1)+sum(selected_cards2) > optimal_points:
    #        label = pyglet.text.Label('Congratulations!  You beat the best strategy (with some luck, maybe)!',
    #                                font_name='Times New Roman', 
    #                                font_size=20,color=(255, 0, 0, 255),
    #                                x=50, y=window.height-120,
    #                                halign='center', anchor_y='bottom')
    #        label.draw()
    if at_end:
        window.clear()
        label = pyglet.text.Label('Please donot press any key now and turn to the experimenter for further instructions',
                              font_name='Times New Roman', 
                              font_size=20,
                              x=50, y=window.height-280,
                              halign='center', anchor_y='bottom')
        label.draw()
        label = pyglet.text.Label('You got ' +str(sum(selected_cards1)+sum(selected_cards2))+ ' points', # + 'and ' + str(current_total_turns)+' turns in this game', 
                            # 1) you might want to fix the above to show the current_total_turns after finishing every trial--currently no presence
                            font_name='Times New Roman', 
                            font_size=20,
                            x=50, y=window.height-40,
                            halign='center', anchor_y='bottom')
        label.draw()
        label = pyglet.text.Label('You are now finished with the experiment.',
                                font_name='Times New Roman', 
                                font_size=20,
                                x=50, y=window.height-160,
                                halign='center', anchor_y='bottom')
        label.draw()
        label = pyglet.text.Label('Thank you for your participation!',
                                font_name='Times New Roman', 
                                font_size=20,
                                x=50, y=window.height-200,
                                halign='center', anchor_y='bottom')
        label.draw()
        #label = pyglet.text.Label('There are just six follow-up questions now',
        #                        font_name='Times New Roman', 
        #                        font_size=20,
        #                        x=50, y=window.height-240,
        #                        halign='center', anchor_y='bottom')
        #label.draw()
        
    window.flip()
    if continued == 1:
        window.clear()
        continued=0

if __name__ == '__main__':
    DEPLETION_RATE = 3  # rate at which the value of the chosen card depletes each time it is clicked on
                    #  Set this value to 0 to have the original non-depleting version

    trials = 2 #number of trial should be 30
    
    # number of games to be played
    subjectid = -1
    moving_card=0
    trialnumber = 0
    exploit = -1 # -1 init, 0 explore, 1 exploit
    timeoflastclick = 0
    timeoflastclickdelta = 0
    x_offset=20
    y_offset=-140
    lowest_card=1 #should be 1
    highest_card=99
    table_card=0
    error=0
    continued = 0
    thresholds=[0,0,0,0,0,0]
    at_end=0
    optimal_exploit=-1
    break_taking=0
    num_frames = 10 #Number of frames of animation
    acceptable_distance=50
    window.clear()
    introprompt()
    writeinit(subjectid)
    down_card=image.load('cardspot.jpg')
    window.clear()

    
    #secondprompt()
    for trialnumber in range(trials):
        window.clear()
        clicked_card=-1
        turn_number=0
        threshold=0
        optimal_card_number=0 # this is number of cards that the optimal strategy has taken
        highest_table_card_optimal=0 #this is the highest card on optimal's table.  Start low so sure to take from deck
        earlier_highest_card=0
        values_per_row=21 #How many cards will fit on one line of screen
        total_turns= random.randint(5,35)#20   # number of cards to be selected (from deck or exposed stack) per game
        #current_total_turns = total_turns
        cards_in_deck=total_turns
        ''''''
        if trialnumber >= 1:
            break_taking=1
            break_between_games()
            while continued == 0:
                window.dispatch_events()
        break_taking=0
        continued = 0
        optimal_points=0
        card_series=[]
        for i in range(0,total_turns,1):
            card_series.append(int(random.uniform(1,highest_card+1)))   #to give 1-N, need to add one more
        label = pyglet.text.Label('Click on the deck or an uncovered card', 
                                  font_name='Times New Roman',  
                                  font_size=20,
                                  x=window.width//4, y=window.height-40, #window.width//2
                                  halign='center', anchor_y='bottom')

        ''''''
        cards=[] #list of all cards that are on the table
        cards_coords=[]
        selected_cards1=[]
        selected_cards2=[]
        max_before_turn=0
        last_exploit_status=-1 #used to determine if switch explore/exploit status.  This is whether the subject exploited on LAST turn
        last_table_card_clicked=-1
        my_card=Card(10,10) #give initial X and Y positions
        accumulated_points1=pyglet.text.Label('',font_name='Times New Roman', color=(125,125,125,255),font_size=18,x=20, y=20,halign='center', anchor_y='center')
        accumulated_points2=pyglet.text.Label('',font_name='Times New Roman', color=(125,125,125,255),font_size=18,x=20, y=20,halign='center', anchor_y='center')
        #window.push_handlers(my_card)  # with this line, we can control the card
        something_happened = 1
        ''''''
        while turn_number < total_turns:
            window.dispatch_events()

            if something_happened == 1: #if the following is not in this conditional, then wasteful redrawing will often occur, which slows things down
                window.clear()
                my_card.draw()
                draw_deck(cards)
                cards_left=pyglet.text.Label('99 cards in deck',font_name='Times New Roman', color=(250,250,250,255),  # str(cards_in_deck)+
                 font_size=18,x=10, y=150,halign='left', anchor_y='center')
                information =pyglet.text.Label('Game '  +str(trialnumber+1)+ ' out of ' +str(trials)+ '     Turns taken = '+str(turn_number)+'     Total Points= '+str(sum(selected_cards1)+sum(selected_cards2)),font_name='Times New Roman', color=(250,250,250,255), #'        Turns left = '+str(total_turns-turn_number)+
                   font_size=18,x=120, y=40,halign='left')
#                optimal_information =pyglet.text.Label('Last Threshold= '  +str(threshold)+ '      Total optimal points= ' +str(optimal_points)+ '   num cards on optimal table= ' +str(optimal_card_number),font_name='Times New Roman', color=(250,250,250,255),
#                      font_size=18,x=120, y=20,halign='left')
                cards_left.draw()
                information.draw()
#                optimal_information.draw()
                accumulated_points1.draw()
                accumulated_points2.draw()
                something_happened = 0

            if moving_card == 1 :  #Move from deck to table
                exploit = 0
                clicked_card=len(cards)-1
                cards_in_deck=cards_in_deck-1
                draw_deck(cards,0)
                for i in range (num_frames,0,-1):
                     x_position=(cards_coords[clicked_card][0]*(num_frames-i)+70*i)/num_frames
                     y_position=(cards_coords[clicked_card][1]*(num_frames-i)+90*i)/num_frames
                     card_value=pyglet.text.Label(str(cards[clicked_card]),font_name='Times New Roman', color=(125,125,125,255),font_size=18,x=x_position, y=y_position,halign='center', anchor_y='center')
                     card_value.draw()
                     window.flip()        
                draw_deck(cards)
                window.flip()

            if moving_card == 2: # just move from table to accumulated points.  Before this used to be in on_mouse_press, but the global variable
                                # wasn't always updated in time if table card were selected very quickly.
                clicked_card=table_card
                exploit = 1
                
                
                
            if moving_card > 0 :  #earlier also had and clicked_card >-1
                #Note, for the calculation of optima, turn_number goes from 0 to total_turns - 1.
                #But, when we output the turn number, we output this number + 1
                
                turn_number=turn_number+1
                A=(total_turns-turn_number)*(highest_card*highest_card+highest_card)
                B=(highest_card+lowest_card)*(highest_card-lowest_card+1)
                C=(total_turns-turn_number)*(2*highest_card+1)+2*(highest_card-lowest_card+1)
                if turn_number==total_turns:
                    threshold=round(float(highest_card+lowest_card)/2,3)
                else:
                    threshold=round((C-math.sqrt(C*C-4*(total_turns-turn_number)*(A+B)))/(2*(total_turns-turn_number)),3)
                #print threshold
                if threshold > highest_table_card_optimal:#If table card is not juicy enough, then draw a new card
                    optimal_points = optimal_points + card_series[optimal_card_number]
                    earlier_highest_card=highest_table_card_optimal #remember what old best value was because this is what determined decision
                    if card_series[optimal_card_number]>highest_table_card_optimal:
                        highest_table_card_optimal=card_series[optimal_card_number]
                    opt_card_value=card_series[optimal_card_number]
                    optimal_card_number=optimal_card_number + 1
                    optimal_exploit=0
                else: #go with the highest card on the table
                    optimal_points = optimal_points + highest_table_card_optimal
                    earlier_highest_card=highest_table_card_optimal #remember what old best value was because this is what determined decision
                    opt_card_value=highest_table_card_optimal
                    optimal_exploit=1
                move_value(clicked_card) #move from table to accumulated points
                if cards[clicked_card] > (DEPLETION_RATE - 1): #?????/
                    Current_Card_To_Add  = cards[clicked_card]
                    # save cards[clicked_card] to Current_Card_To_Add, as values gotten at every turn, and write it to the csv file
                    cards[clicked_card] -= DEPLETION_RATE
                     
                #if cards[clicked_card] < DEPLETION_RATE:
                else:
                    Current_Card_To_Add = cards[clicked_card]
                    cards[clicked_card]  = 0
                selected_cards = selected_cards1 + selected_cards2
                if (exploit == 0):
                    clicked_card = -1
                #print len(selected_cards), list2str(selected_cards)
                #print "=" * 20
                if (last_exploit_status == exploit):
                    switch_exploit=0
                else:
                    switch_exploit=1
                last_exploit_status = exploit
                row = [subjectid, trialnumber+1, turn_number, exploit, switch_exploit, timeoflastclick, timeoflastclickdelta, len(cards),
                    Current_Card_To_Add,clicked_card, max_before_turn,sum(selected_cards1)+sum(selected_cards2),threshold, optimal_points,optimal_card_number,earlier_highest_card,optimal_exploit,opt_card_value]
                    #cards[clicked_card]+DEPLETION_RATE
                csvwriter.writerow(row)
            #  game_over.draw()
            #if moving_card == 0:
            window.flip()
    #csvwriter.close()
    break_taking=1
    at_end=1
    break_between_games() #need to call with ()s, otherwise its ISN'T called
    while continued == 0:
        window.dispatch_events()
    ####finalprompt()
    #End_questions=Window(resizable=True)
    pyglet.app.run()         
#    if cards==[]:
 #       max_before_turn=0
 #   else:
 #       max_before_turn=max(cards)
        

        
