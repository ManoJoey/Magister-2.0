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

Builder.load_file('my.kv')

class MyGridLayout(Widget):
    def yes(self):
        print("yes")
    

        
class test1(App):
    def build(self):
        return MyGridLayout()

Window.size = (450, 750)

if __name__ == "__main__":
    test1().run()