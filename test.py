import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

#Verschillende schermen benoemen
class Dashboard(Screen):
    pass

kv = Builder.load_file('app.kv')
        
class Scorro(App):
    def build(self):
        return kv

Window.size = (400, 750)

if __name__ == "__main__":
    Scorro().run()