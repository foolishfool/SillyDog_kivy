__author__ = 'Frank.Fu'

import  kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock

from kivy.vector import Vector
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.layout import Layout
from kivy.core.audio import SoundLoader




#from functools import partial
class Fist(Widget):
    sound_punch = SoundLoader.load('punch.wav')
    sound_whiff = SoundLoader.load('whiff.wav')
    def punch(self,dog):
        if self.collide_widget(dog):
            self.sound_punch.play()
            dog.spinning = 1
            dog.spin()
            dog.resize()
        else:
            self.sound_whiff.play()
            pass



class Dog(Scatter):
    spinning = 0
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    speed = ReferenceListProperty(velocity_x,velocity_y)
    angle = NumericProperty(0)
    initial_size = [100,100]
    initial_speed = (5,0)
    background_music_relax = SoundLoader.load('background_music_relax.mp3')
    background_music_nervous = SoundLoader.load('background_music_nerverous.mp3')
    def move(self):
        self.pos =   Vector(*self.speed) + self.pos
    def crazy(self):
        self.background_music_relax.stop()
        self.background_music_nervous.play()
        if abs(self.velocity_x) > abs(self.initial_speed[0]) * 1.5 :
                self.velocity_x *= 1.05

    def spin(self):
        if self.spinning == 1:
            self.angle += 20
            if self.angle >= 360:
                self.angle = 0
                self.spinning = 0

    def resize(self):

         if self.size[0] / self.initial_size[0] >= 0.4:
             self.size[0] *= 0.95
         if self.size[1] / self.initial_size[1] >= 0.4:
             self.size[1] *= 0.95



class SillyDogGame(Widget):
    fist = ObjectProperty(None)
    dog = ObjectProperty(None)

    def build_dog(self):
        self.dog.background_music_relax.play()
        self.dog.center = self.center
        self.dog.speed = self.dog.initial_speed

    def upgrade(self,dt):

        self.fist.center_x =  Window.mouse_pos[0]
        self.fist.center_y =  Window.mouse_pos[1]
        if (self.dog.center_x < 0 ) or (self.dog.center_x * 2 > self.width):
            self.dog.velocity_x *= -1
        self.dog.spin()
        self.dog.move()
        if self.dog.size[0]/self.dog.initial_size[0] <= 0.6:
            self.dog.crazy()



    def on_touch_down(self, touch):
         self.fist.center_x = touch.x + 10
         self.fist.center_y = touch.y + 20
         self.fist.punch(self.dog)


class Background(Widget):
    pass



class SillyDog(App):
    def build(self):
        game = SillyDogGame()
        game.build_dog()
        Clock.schedule_interval(game.upgrade,1.0 / 60.0)
        return game


if __name__ == '__main__':
    SillyDog().run()