#
# This file is part of Dinamo project.
# 
# Copyright (C) 2009-2013 William Oliveira de Lagos <william@efforia.com.br>
#
# Dinamo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dinamo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dinamo.  If not, see <http://www.gnu.org/licenses/>.
#

from base import BaseHandler
from pygame import *
from pygame.locals import *

images = {}
modes = [(640,480),(800,600),(1024,768),(1280,800)]
screen = None

def load_graphics(name,local):
    global images,screen
    local = os.path.abspath(os.path.join("euphoria",local))
    if not images.has_key(name):
        images[name] = pygame.image.load(local).convert(screen)
    return images[name]
def get_image(name):
    global images
    return images[name]

class Image:
    '''Euphoria Image Class'''
    image = None
    posx = 0
    posy = 0
    def __init__(self,name,local):
        '''Initialize the image'''
        self.load_image(name,local)
    def image_position(self,x,y):
        self.image.set_colorkey(self.image.get_at((x,y)))
    def load_image(self,name,local):
        '''Load image attributes to class'''
        self.image = load_graphics(name,local)
        self.posx = self.image.get_width()
        self.posy = self.image.get_height()
    def position(self):
        '''Returns position of image'''
        return self.posy,self.posx
    def height(self):
        '''Height of image'''
        return self.posy
    def width(self):
        '''Width of image'''
        return self.posx
class Video:
    '''Euphoria Video Class'''
    def __init__(self,size,fullscreen = False):
        '''Initialize the video'''
        pygame.init()
        self.notify = []
        self.mode(size,fullscreen)
        self.imfont = pygame.font.Font(None,24)
        self.actual_mode = 1
    def add(self,function):
        '''Add notification'''
        self.notify.append(function)
    def notificate(self,message):
        '''Print notifications'''
        for m in self.notify:
            m(message)
    def mode(self,size,fullscreen = None):
        '''Set screen mode in size and type'''
        global screen
        self.size = size
        if fullscreen == None:
            fullscreen = self.fullscreen
        else:
            self.fullscreen = fullscreen
        flags = DOUBLEBUF | HWSURFACE
        if fullscreen:
            flags = flags | FULLSCREEN
        self.screen = pygame.display.set_mode(size,flags)
        screen = self.screen
        self.notificate(0)
    def next_mode(self):
        '''Get next screen mode'''
        self.actual_mode = (self.actual_mode + 1) % len(modes)
        self.mode(modes[self.actual_mode])
    def previous_mode(self):
        '''Get previous screen mode'''
        self.actual_mode -= 1
        if self.actual_mode < 0:
            self.actual_mode = len(modes) - 1
        self.mode(modes[self.actual_mode])
    def toggle_fullscreen(self,yes = None):
        '''Turn into fullscreen'''
        if sim == None:
            sim = ~ self.fullscreen
        self.mode(self.size, yes)
    def update(self):
        '''Animate the display'''
        pygame.display.flip()
    def clear(self, color = (0,0,0,0)):
        '''Clear the screen with black'''
        self.screen.fill(color)
    def draw(self,image,position):
        '''Draw image in screen'''
        self.screen.blit(image,position)
    def font(self,size):
        '''Change font size of text'''
        self.imfont = pygame.font.Font(None,size)
    def text(self,message,color):
        '''Print message to the screen'''
        image = self.imfont.render(message,True,color)
        return image
    def title(self,name):
        '''Set the window title'''
        pygame.display.set_caption(name)

class Handler(BaseHandler):
    def __init__(self):
        '''Initialize the game'''
        elements = []
        video = Video(size)
        video.add(self.reconfigure_video(0))
        width = size[0]
        height = size[1]
        gamespace = Space()
        pygame.display.set_caption("Zhockon SDL")
    def load_sound(self,archive):
        try:
            raise NotImplementedError
        except NotImplementedError, e:
            print "Option not already implemented."
    def stop_sound(self,archive):
        try:
            raise NotImplementedError
        except NotImplementedError, e:
            print "Option not already implemented."
    def start_sync(self):
        '''Controls the game time'''
        self.gamespace.start_sync()
    def stop_sync(self):
        '''Stops controlling the time'''
        self.gamespace.stop_sync()
    def reconfigure_video(self, message):
        ''''''
        if message == 0:
            self.width = self.video.size[0]
            self.height = self.video.size[1]
    def create_element(self, image, anim, position = [0,0], speed = [1,0]):
        '''Add a element in the game scenario'''
        element = Element(image,anim,position)
        element.which_speed(speed)
        self.elements.append(element)
        element.space = self
    def remove_element(self, element):
        '''Remove a element in the game scenario'''
        if element.type != None:
            self.collisions[element.type].remove(element)
        self.elements.remove(element)
    def draw_image(self,image,position=[0,0]):
        '''Draw a image in the game screen'''
        img = Image(image,image).image
        if position[0] == -1: position[0] = (self.width - image.get_width()) /2
        if position[1] == -1: position[1] = (self.height - image.get_height()) /2
        self.video.draw(img, position)
    def write_text(self, position, text, color, size = None):
        '''Write a text in the game screen'''
        if size != None:
            self.video.font(size)
        image = self.video.text(text,color)
        if position[0] == -1: position[0] = (self.width - image.get_width()) /2
        if position[1] == -1: position[1] = (self.height - image.get_height()) /2
        self.draw(position, image)
    def draw_background(self,figure):
        '''Draw a background image in the game screen'''
        self.video.clear()
        image = Image("bkg",figure)
        self.video.draw(get_image("bkg"),(0,0))
    def draw_elements(self):
        '''Draw the added elements to game display''' 
        for element in self.elements:
            if element.visible:
                self.video.screen.blit(element.image, element.pos)
    def update(self):
        '''Animate the game'''
        #self.video.clear()
        objects = pygame.sprite.RenderUpdates(self.elements)
        for element in self.elements:
            if len(self.gamespace.handle_collisions(element,objects)) > 1:
                if ~element.collided:
                    element.reverse_speed()
                element.collided = True
        objects.update(); objects.draw(self.video.screen)
        self.video.update()
        

