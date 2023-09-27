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

#Verschillende schermen benoemen
class Navbar(Screen):
    pass
class Dashboard(Screen):
    pass
class Huiswerk(Screen):
    pass
class Toetsen(Screen):
    pass
class Vakken(Screen):
    pass
class Cijfers(Screen):
    pass

class WindowManager(ScreenManager):
    pass
        
class Scorro(App):
    def build(self):
        kv = Builder.load_file('my.kv')
        return kv
    
Window.size = (350, 600)

if __name__ == "__main__":
    Scorro().run()