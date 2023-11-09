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
    def on_enter(self):
        hw_lijst = Scorro.show_huiswerk(self)
        word = ""
        for item in hw_lijst:
            replace = str(item).replace("(", "")
            replace = replace.replace(")", "")
            replace = replace.replace("'", "")
            word = f"{word}\n{replace}"
            self.ids.hw_labelSW.text = f"{word}"
class Vakken(Screen):
    pass
class Cijfers(Screen):
    pass
class NieuwHuiswerk(Screen):
    def spinnerHW_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakHW
        spinner.values = [str(item[0]) for item in data]
class NieuwProefwerk(Screen):
    def spinnerPW_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakPW
        spinner.values = [str(item[0]) for item in data]
class NieuwCijfer(Screen):
    def spinnerCF_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakCF
        spinner.values = [str(item[0]) for item in data]
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

        c.execute("""CREATE TABLE if not exists cijfers(
            cijfer text,
            vak text,
            weging text,
            beschrijving text)
        """)

        c.execute("""CREATE TABLE if not exists proefwerken(
            naam text,
            datum text,
            beschrijving text)
        """)

        c.execute("""CREATE TABLE if not exists huiswerk(
            naam text,
            datum text,
            beschrijving text,
            vak text)
        """)

        conn.commit()
        conn.close()

        kv = Builder.load_file('main.kv')
        return kv
    

    #functies voor klassen
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
        return records
    

    #functies voor cijfers
    def submit_cijfer(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("INSERT INTO cijfers VALUES (:naam, :dag)",
        {
            'cijfer': self.root.get_screen('nieuw vak').ids.naam_vak.text,
            'vak': self.root.get_screen('nieuw vak').ids.naam_vak.text,
            'weging': self.root.get_screen('nieuw vak').ids.naam_vak.text,
            'beschrijving': self.root.get_screen('nieuw vak').ids.naam_vak.text,
        })


        self.root.get_screen('nieuw cijfer').ids.naam_vak.text = ''

        conn.commit()
        conn.close()

    def show_cijfers(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM cijfers")
        records = c.fetchall()

        conn.commit()
        conn.close()
    

    #functies voor proefwerken
    def submit_proefwerk(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("INSERT INTO proefwerken VALUES (:naam, :dag)",
        {
            'naam': self.root.get_screen('nieuw vak').ids.naam_vak.text,
            'datum': self.root.get_screen('nieuw vak').ids.naam_vak.text,
            'beschrijving': self.root.get_screen('nieuw vak').ids.naam_vak.text,
        })


        self.root.get_screen('nieuw vak').ids.naam_vak.text = ''

        conn.commit()
        conn.close()

    def show_proefwerken(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM proefwerken")
        records = c.fetchall()

        conn.commit()
        conn.close()
    

    #functies voor huiswerk
    def submit_huiswerk(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("INSERT INTO huiswerk VALUES (:naam, :datum, :beschrijving, :vak)",
        {
            'naam': self.root.get_screen('nieuw huiswerk').ids.welkHW.text,
            'datum': self.root.get_screen('nieuw huiswerk').ids.datumHW.text,
            'beschrijving': self.root.get_screen('nieuw huiswerk').ids.infoHW.text,
            'vak': self.root.get_screen('nieuw huiswerk').ids.kiesvakHW.text,
        })


        self.root.get_screen('nieuw huiswerk').ids.welkHW.text = ''
        self.root.get_screen('nieuw huiswerk').ids.datumHW.text = ''
        self.root.get_screen('nieuw huiswerk').ids.infoHW.text = ''
        self.root.get_screen('nieuw huiswerk').ids.kiesvakHW.text = 'Selecteer een vak'

        conn.commit()
        conn.close()

    def show_huiswerk(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM huiswerk")
        records = c.fetchall()

        conn.commit()
        conn.close()
        return records

        
Window.size = (350, 600)

if __name__ == "__main__":
    Scorro().run()