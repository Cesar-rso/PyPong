# PyPong
# This is a recreation of the classical game Pong
# in Python, using pygame. 
# The uagame.py is taken from the University of Alberta 
# course "Problem Solving, Python Programming and Video
# Games" available on Coursera. 


from uagame import Window
from random import randint
from math import sqrt
from pygame import QUIT, Color, MOUSEBUTTONUP, K_UP, K_DOWN, K_ESCAPE, K_w, K_s
from pygame.time import Clock, get_ticks
from pygame.event import get as get_events
from pygame.draw import circle as draw_circle
from pygame.draw import rect as draw_rect
from pygame.draw import lines as draw_lines
from pygame.key import get_pressed

# User-defined functions

def main():
    game = Game()
    game.play()
    
# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self):
        # Initialize a Game.
        # - self is the Game to initialize
        
        self._window = Window('PyPong', 500, 400)
        self._adjust_window()
        self._frame_rate = 90  # larger is faster game
        self._close_selected = False
        self._clock = Clock()
        self._small_dot = Dot('white', [50,75], 10, [1,2], self._window)
        self._left_pad = Pad('white', [30,150], [20,110], 5, self._window)
        self._right_pad = Pad('white', [455,150], [20,110], 5, self._window)
        self._small_dot.randomize()
        self._score_left = 0
        self._score_right = 0
        self._continue_game = True
        
    def _adjust_window(self):
        # Adjust the window for the game.
        # - self is the Game to adjust the window for
        
        self._window.set_font_name('ariel')
        self._window.set_font_size(64)
        self._window.set_font_color('white')
        self._window.set_bg_color('black')        
    
    def play(self):
        # Play the game until the player presses the close icon
        # and then close the window.
        # - self is the Game to play

        while not self._close_selected:
            # play frame
            self.handle_events()
            self.draw()
            self.update()
        self._window.close()
           
    def handle_events(self):
        # Handle the current game events by changing the game
        # state appropriately.
        # - self is the Game whose events will be handled

        event_list = get_events()
        for event in event_list:
            self.handle_one_event(event)
            
    def handle_one_event(self, event):
        # Handle one event by changing the game state
        # appropriately.
        # - self is the Game whose event will be handled
        # - event is the Event object to handle
        keys = get_pressed()
        if event.type == QUIT or keys[K_ESCAPE]:
            self._close_selected = True
        if self._continue_game:
        # Controls for the left pad
            if keys[K_w]:
                self._left_pad.move(0)
            if keys[K_s]:
                self._left_pad.move(1)
        #Controls for the right pad
            if keys[K_UP]:
                self._right_pad.move(0)
            if keys[K_DOWN]:
                self._right_pad.move(1)
 
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        self._window.clear()
        self.draw_score()
        draw_lines(self._window.get_surface(), Color('white'), False, [(245,0), (245,400)])
        self._small_dot.draw()
        self._left_pad.draw()
        self._right_pad.draw()
        if not self._continue_game:  # perform game over actions
            self.draw_game_over()
        self._window.update()
                        
    def update(self):
        # Update all game objects with state changes
        # that are not due to user events. Determine if
        # the game should continue.
        # - self is the Game to update

        if self._continue_game:
            # update during game
            self._small_dot.intersects(self._left_pad, 1)
            self._small_dot.intersects(self._right_pad, 0)
            position = self._small_dot.move()
            if position > 250:
                self._score_left += 1
            elif position > -1:
                self._score_right += 1
        self._clock.tick(self._frame_rate)
        

    def draw_game_over(self):
        # Draw GAME OVER in the lower left corner of the
        # surface, using the small dot's color for the font
        # and the big dot's color as the background.
        # - self is the Game to draw for
        
        string = 'GAME OVER'
        font_color = self._small_dot.get_color()
        bg_color = 'blue'
        original_font_color = self._window.get_font_color()
        original_bg_color = self._window.get_bg_color()
        self._window.set_font_color(font_color)
        self._window.set_bg_color(bg_color)
        height = self._window.get_height() - self._window.get_font_height()
        self._window.draw_string(string, 0, height)
        self._window.set_font_color(original_font_color)
        self._window.set_bg_color(original_bg_color)
        
    def draw_score(self):
        # Draw the time since the game began as a score.
        # - self is the Game to draw for.
        
        string_l = str(self._score_left)
        string_width = self._window.get_string_width(string_l)
        self._window.draw_string(string_l, 220 - string_width, 0)
        
        string_r = str(self._score_right)
        self._window.draw_string(string_r, 270, 0)

class Dot:
    # An object in this class represents a colored circle
    # that can move.

    def __init__(self, color, center, radius, velocity, window):
        # Initialize a Dot.
        # - self is the Dot to initialize
        # - color is the str color of the dot
        # - center is a list containing the x and y int
        # coords of the center of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - window is the game's Window

        self._color = color
        self._center = center
        self._radius = radius
        self._velocity = velocity
        self._window = window

    def move(self):
        # Change the location and the velocity of the Dot so it
        # remains on the surface by bouncing from its edges.
        # - self is the Dot

        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
            # update center at index
            self._center[index] = self._center[index] + self._velocity[index]
            # dot perimeter outside window?
            if (self._center[index] < self._radius) or (self._center[index] + self._radius > size[index]):
                # change direction
                self._velocity[index] = - self._velocity[index]
                if index == 0:
                    return self._center[index]
        return -1

    def draw(self):
        # Draw the dot on the surface.
        # - self is the Dot

        surface = self._window.get_surface()
        color = Color(self._color)
        draw_circle(surface, color, self._center, self._radius)

    def intersects(self, pad, side):
    # Checks if the Dot intersects with one of the pads
    # If it does, it bounces from the pad
    # - self is the Dot
        result = False
        if side == 1: # left pad
            if ((self._center[0] - self._radius < pad._start_pos[0] + pad._end_pos[0]) and (pad._start_pos[1] + pad._end_pos[1] > self._center[1] > pad._start_pos[1])):
                result = True
                self._velocity[0] = - self._velocity[0]
                self._velocity[1] = - self._velocity[1]
        if side == 0: # right pad
            if ((self._center[0] + self._radius > pad._start_pos[0]) and (pad._start_pos[1] + pad._end_pos[1] > self._center[1] > pad._start_pos[1])):
                result = True
                self._velocity[0] = - self._velocity[0]
                self._velocity[1] = - self._velocity[1]
        return result

    def get_color(self):
        # Return a str that represents the color of the dot.
        # - self is the Dot
        
        return self._color
        
    def randomize(self):
        # Change the dot so that its center is at a random
        # point on the surface. Ensure that no part of a dot
        # extends beyond the surface boundary.
        # - self is the Dot

        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
            self._center[index] = randint(self._radius, size[index] - self._radius)
    
            
class Pad:
# An object of this class represents a Pad
# that can move up or down and bounce the Dot.

    def __init__(self, color, start_pos, end_pos, velocity, window):
        self._color = color
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._velocity = velocity
        self._window = window
        
    def draw(self):
        # Draw the pad on the surface.
        # - self is the Pad

        surface = self._window.get_surface()
        color = Color(self._color)
        draw_rect(surface, color, (self._start_pos[0], self._start_pos[1], self._end_pos[0], self._end_pos[1]))
        
    def move(self, direction):
    # Moves the pad up or down
    # - self is the Pad
    
        if direction == 1:
            self._start_pos[1] += self._velocity
            
        if direction == 0:
            self._start_pos[1] -= self._velocity
    

main()
