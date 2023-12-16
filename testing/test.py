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
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
import sqlite3

lijst_dagen = []
dagen_popup = []

#Verschillende schermen benoemen
class Navbar(Screen):
    pass
class Dashboard(Screen):
    pass
class Planning(Screen):
    pass
class Schoolwerk(Screen):
    def on_enter(self):
        pw_lijst = Scorro.show_proefwerken(self)
        self.ids.BoxHwPw.clear_widgets()
        for item in pw_lijst:
            replace = str(item).replace("(", "")
            replace = replace.replace(")", "")
            replace = replace.replace("'", "")
            button = Button(text=str(replace))
            self.ids.BoxHwPw.add_widget(button)
            
        hw_lijst = Scorro.show_huiswerk(self)
        for item in hw_lijst:
            replace = str(item).replace("(", "")
            replace = replace.replace(")", "")
            replace = replace.replace("'", "")
            button = Button(text=str(replace))
            self.ids.BoxHwPw.add_widget(button)

class PopupVak(Popup):
    def on_open(self):
        dagen_popup.clear()
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM vakken WHERE naam = '{naam}'")
        records = c.fetchall()

        conn.commit()
        conn.close()

        colour_selec = (0,1,0,1)
        colour_deselec = (1,0,0,1)

        try:
            dagen = records[0][1].replace("[", "").replace("]", "").replace(" ", "").replace("'", "").split(",")
            for dag in dagen:
                dagen_popup.append(dag)
            
            for dag in dagen_popup:
                self.ids[dag].background_color = colour_selec
        except:
            print("Geen dagen gevonden")

    def Savedag(self, dag):
        colour_selec = (0,1,0,1)
        colour_deselec = (1,0,0,1)
        if dag in dagen_popup:
            dagen_popup.remove(dag)
            self.ids[dag].background_color = colour_deselec
        else:
            dagen_popup.append(dag)
            self.ids[dag].background_color = colour_selec

    def OW_klas(self):
        text = self.ids.naam_vakAP.text
        old_name = self.title.split(" - ")[0]

        if dagen_popup != []:
            if text != "":
                conn = sqlite3.connect('ScorroDB.db')
                c = conn.cursor()
            
                dagen = str(dagen_popup)
                c.execute("""UPDATE vakken SET
                    naam = :naam,
                    dag = :dag
                    WHERE naam = :old_name""",
                    {
                    'naam': text,
                    'dag': str(dagen_popup),
                    'old_name': old_name,
                })

                conn.commit()
                conn.close()
                print("vak opgeslagen")

                dagen_popup.clear()
                
                vakken_screen = App.get_running_app().root.get_screen("vakken").ids.BoxVakken
                for vak in vakken_screen.children:
                    if vak.text == old_name:
                        vak.text = text
                
                sorted_buttons = sorted(vakken_screen.children, key=lambda x: x.text)
                vakken_screen.clear_widgets()
                for button in sorted_buttons:
                    vakken_screen.add_widget(button)
            else:
                print("Geen tekst")
        else:
            print("Geen dagen")

    def verwijderKlas(self):
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"DELETE FROM vakken WHERE naam = '{naam}'")

        conn.commit()
        conn.close()

        vakken_screen = App.get_running_app().root.get_screen("vakken").ids.BoxVakken
        
        for vak in vakken_screen.children:
            if vak.text == naam:
                vakken_screen.remove_widget(vak)

class Vakken(Screen):
    def popupVak(self, naam):
        popup = PopupVak(title=f"{naam} - vak aanpassen")
        popup.ids.naam_vakAP.text = naam
        popup.open()

    def on_enter(self):
        window_size = int(Window.size[1]) / 10
        vakken_lijst = Scorro.show_klassen(self)
        self.ids.BoxVakken.clear_widgets()

        for vak in vakken_lijst:
            button = Button(text=str(vak[0]), size_hint_y=None, height=window_size)
            button.bind(on_press=lambda button: self.popupVak(button.text))
            self.ids.BoxVakken.add_widget(button)
        
        sorted_buttons = sorted(self.ids.BoxVakken.children, key=lambda x: x.text)
        self.ids.BoxVakken.clear_widgets()
        for button in sorted_buttons:
            self.ids.BoxVakken.add_widget(button)


class Cijfers(Screen):
    def on_enter(self):
        print(Scorro.show_cijfers(self))

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
    def on_enter(self):
        for item in lijst_dagen:
            lijst_dagen.remove(item)
        self.ids.maandag.background_color = (1,0,0,1)
        self.ids.dinsdag.background_color = (1,0,0,1)
        self.ids.woensdag.background_color = (1,0,0,1)
        self.ids.donderdag.background_color = (1,0,0,1)
        self.ids.vrijdag.background_color = (1,0,0,1)
        self.ids.zaterdag.background_color = (1,0,0,1)
        self.ids.zondag.background_color = (1,0,0,1)
        
    def hide_message(self):
        self.ids.BoxMessage.remove_widget(self.ids.BoxMessage.children[0])

    def SavedVak(self):
        text = self.ids.naam_vak.text
        if lijst_dagen != []:
            if text != "":
                message = Label(text="Vak opgeslagen!")
                self.ids.BoxMessage.add_widget(message)
                Clock.schedule_once(lambda x: self.hide_message(), 1.5)

    def Savedag(self, dag):
        colour_selec = (0,1,0,1)
        colour_deselec = (1,0,0,1)
        if dag in lijst_dagen:
            lijst_dagen.remove(dag)
            self.ids[dag].background_color = colour_deselec
        else:
            lijst_dagen.append(dag)
            self.ids[dag].background_color = colour_selec

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
            weging text,
            beschrijving text,
            vak text)
        """)

        c.execute("""CREATE TABLE if not exists proefwerken(
            naam text,
            datum text,
            beschrijving text,
            vak text)
        """)

        c.execute("""CREATE TABLE if not exists huiswerk(
            naam text,
            datum text,
            beschrijving text,
            vak text)
        """)

        conn.commit()
        conn.close()

        kv = Builder.load_file('testdl.kv')
        return kv


    #functies voor klassen
    def submit_klas(self):
        global lijst_dagen
        text = self.root.get_screen('nieuw vak').ids.naam_vak.text
        if lijst_dagen != []:
            if text != "":
                #connect to database
                conn = sqlite3.connect('ScorroDB.db')
                c = conn.cursor()
            
                c.execute("INSERT INTO vakken VALUES (:naam, :dag)",
                {
                    'naam': self.root.get_screen('nieuw vak').ids.naam_vak.text,
                    'dag': str(lijst_dagen),
                })

                conn.commit()
                conn.close()
                
                #reset buttons
                lijst_dagen = []
                self.root.get_screen('nieuw vak').ids.maandag.background_color = (1,0,0,1)
                self.root.get_screen('nieuw vak').ids.dinsdag.background_color = (1,0,0,1)
                self.root.get_screen('nieuw vak').ids.woensdag.background_color = (1,0,0,1)
                self.root.get_screen('nieuw vak').ids.donderdag.background_color = (1,0,0,1)
                self.root.get_screen('nieuw vak').ids.vrijdag.background_color = (1,0,0,1)
                self.root.get_screen('nieuw vak').ids.zaterdag.background_color = (1,0,0,1)
                self.root.get_screen('nieuw vak').ids.zondag.background_color = (1,0,0,1)

                self.root.get_screen('nieuw vak').ids.naam_vak.text = ''
                print("vak opgeslagen")

            else:
                print("Geen tekst")
        else:
            print("Geen dagen")

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
        naam = self.root.get_screen('nieuw cijfer').ids.welkCF.text
        weging = self.root.get_screen('nieuw cijfer').ids.wegingCF.text
        vak = self.root.get_screen('nieuw cijfer').ids.kiesvakCF.text
        if naam != "":
            if weging != "":
                if vak != "Selecteer een vak":
                    conn = sqlite3.connect('ScorroDB.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO cijfers VALUES (:cijfer, :weging, :beschrijving, :vak)",
                    {
                        'cijfer': self.root.get_screen('nieuw cijfer').ids.welkCF.text,
                        'weging': self.root.get_screen('nieuw cijfer').ids.wegingCF.text,
                        'beschrijving': self.root.get_screen('nieuw cijfer').ids.infoCF.text,
                        'vak': self.root.get_screen('nieuw cijfer').ids.kiesvakCF.text,
                    })


                    self.root.get_screen('nieuw cijfer').ids.welkCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.wegingCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.infoCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.kiesvakCF.text = 'Selecteer een vak'

                    conn.commit()
                    conn.close()
                else:
                    print("Selecteer een vak")
            else:
                print("Geef je cijfer een weging")
        else:
            print("Geef je cijfer")

    def show_cijfers(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM cijfers")
        records = c.fetchall()

        conn.commit()
        conn.close()
        return records
    

    #functies voor proefwerken
    def submit_proefwerk(self):
        naam = self.root.get_screen('nieuw proefwerk').ids.welkPW.text
        datum = self.root.get_screen('nieuw proefwerk').ids.datumPW.text
        vak = self.root.get_screen('nieuw proefwerk').ids.kiesvakPW.text
        if naam != "":
            if datum != "":
                if vak != "Selecteer een vak":
                    conn = sqlite3.connect('ScorroDB.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO proefwerken VALUES (:naam, :datum, :beschrijving, :vak)",
                    {
                        'naam': self.root.get_screen('nieuw proefwerk').ids.welkPW.text,
                        'datum': self.root.get_screen('nieuw proefwerk').ids.datumPW.text,
                        'beschrijving': self.root.get_screen('nieuw proefwerk').ids.infoPW.text,
                        'vak': self.root.get_screen('nieuw proefwerk').ids.kiesvakPW.text,
                    })


                    self.root.get_screen('nieuw proefwerk').ids.welkPW.text = ''
                    self.root.get_screen('nieuw proefwerk').ids.datumPW.text = ''
                    self.root.get_screen('nieuw proefwerk').ids.infoPW.text = ''
                    self.root.get_screen('nieuw proefwerk').ids.kiesvakPW.text = 'Selecteer een vak'

                    conn.commit()
                    conn.close()
                else:
                    print("Selecteer een vak")
            else:
                print("Geef je proefwerk een datum")
        else:
            print("Geef je proefwerk een naam")
            
            
    def show_proefwerken(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM proefwerken")
        records = c.fetchall()

        conn.commit()
        conn.close()
        return records
    

    #functies voor huiswerk
    def submit_huiswerk(self):
        naam = self.root.get_screen('nieuw huiswerk').ids.welkHW.text
        datum = self.root.get_screen('nieuw huiswerk').ids.datumHW.text
        vak = self.root.get_screen('nieuw huiswerk').ids.kiesvakHW.text
        if naam != "":
            if datum != "":
                if vak != "Selecteer een vak":
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
                else:
                    print("Selecteer een vak")
            else:
                print("Geef je toets een datum")
        else:
            print("Geef je toets een naam")

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