import kivy

from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class WindowManager(ScreenManager):
    pass

class Sc(MDApp):
    def build(self):
        kv = Builder.load_file('mein.kv')
        return kv


if __name__ == '__main__':
    Sc().run()