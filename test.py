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
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
import sqlite3

#Verschillende schermen benoemen
class Navbar(Screen):
    pass
class Dashboard(Screen):
    pass
class Planning(Screen):
    pass
class Schoolwerk(Screen):
    pass
class Vakken(Screen):
    pass
class Cijfers(Screen):
    pass
class NieuwHuiswerk(Screen):
    def spinner_clicked(self, vak):
        print(vak)
class NieuwProefwerk(Screen):
    pass
class NieuwCijfer(Screen):
    pass
class NieuwVak(Screen):
    pass
class CijferBerekenen(Screen):
    pass
class WindowManager(ScreenManager):
    pass
        
class Scorro(App):
    def build(self):
        self.icon = "Images/Logo.png"
        
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE if not exists vakken(
            naam text,
            dag text)
        """)

        conn.commit()
        conn.close()

        kv = Builder.load_file('testdl.kv')
        return kv
    
    def submit_klas(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("INSERT INTO vakken VALUES (:naam, :dag)",
        {
            'naam': self.root.get_screen('nieuw vak').ids.naam_vak.text,
            'dag': self.root.get_screen('nieuw vak').ids.naam_vak.text,
        })


        self.root.get_screen('nieuw vak').ids.naam_vak.text = ''

        conn.commit()
        conn.close()
    
    

    def show_klassen(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM vakken")
        records = c.fetchall()

        conn.commit()
        conn.close()
    
Window.size = (350, 600)

if __name__ == "__main__":
    Scorro().run()