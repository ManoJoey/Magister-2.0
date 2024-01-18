import kivy
from kivymd.app import MDApp

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.widget import Widget 
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.clock import Clock

import matplotlib.pyplot as plt # matplotlib==3.6.3
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import sqlite3
from datetime import datetime, timedelta, date
import ast

lijst_dagen = []
dagen_popup = []
TotCF = ""


class Navbar(Screen):
    pass

class BootScreen(Screen):
    pass

class Dashboard(Screen):
    def on_touch_move(self, touch):
        threshold = float(Window.size[0] / 4)
        diff = float(touch.ox) - float(touch.x)
        
        if touch.x < touch.ox:
            if diff > threshold:
                MDApp.get_running_app().swipe_right()
        
        if touch.x > touch.ox:
            if diff < threshold * -1:
                MDApp.get_running_app().swipe_left()

    def change(self):
        app = MDApp.get_running_app()
        app.call_cf()

    def on_enter(self):
        cijferlijst = Scorro.show_cijfers(self)
        cijferlijst.sort(key=lambda x: x[4], reverse=True)

        lay = self.ids.LayCf
        lay.clear_widgets()
        cf_size = int(int(Window.size[1]) / 20)
        vak_size = int(int(Window.size[1]) / 50)
        w = int(int(Window.size[0]) / 3)

        if cijferlijst != []:
            if len(cijferlijst) >= 3:
                lay.cols = 3
                l1 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[0][0], vak_size, cijferlijst[0][3]),
                halign="center", valign="center", background_color="white", background_normal="", color="gray")
                l1.bind(on_release=lambda x: self.change())
                lay.add_widget(l1)

                l2 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[1][0], vak_size, cijferlijst[1][3]),
                halign="center", valign="center", background_color="white", background_normal="", color="gray")
                l2.bind(on_release=lambda x: self.change())
                lay.add_widget(l2)

                l3 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[2][0], vak_size, cijferlijst[2][3]),
                halign="center", valign="center", background_color="white", background_normal="", color="gray")
                l3.bind(on_release=lambda x: self.change())
                lay.add_widget(l3)
            elif len(cijferlijst) == 2:
                lay.cols = 2
                l1 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[0][0], vak_size, cijferlijst[0][3]),
                halign="center", valign="center", background_color="white", background_normal="", color="gray")
                l1.bind(size=l1.setter('text_size'))
                l1.bind(on_release=lambda x: self.change())
                lay.add_widget(l1)

                l2 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[1][0], vak_size, cijferlijst[1][3]),
                halign="center", valign="center", background_color="white", background_normal="", color="gray")
                l2.bind(size=l2.setter('text_size'))
                l2.bind(on_release=lambda x: self.change())
                lay.add_widget(l2)
            elif len(cijferlijst) == 1:
                lay.cols = 3
                l2 = Button(background_color="white", background_normal="", color="gray")
                lay.add_widget(l2)

                l1 = Button(markup=True, text="[size={}]{}[/size]\n[size={}]{}[/size]".format(cf_size, cijferlijst[0][0], vak_size, cijferlijst[0][3]),
                halign="center", valign="center", background_color="white", background_normal="", color="gray")
                l1.bind(size=l1.setter('text_size'))
                l1.bind(on_release=lambda x: self.change())
                lay.add_widget(l1)

                l3 = Button(background_color="white", background_normal="", color="gray")
                lay.add_widget(l3)
        else:
            l1 = Button(markup=True, text="Nog geen cijfers",
            halign="center", valign="center", background_color="white", background_normal="", color="gray", font_size=Window.size[0]/10)
            l1.bind(size=l1.setter('text_size'))
            l1.bind(on_release=lambda x: self.change())
            lay.add_widget(l1)


class PopupSW(Popup):
    def on_open(self):
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM huiswerk WHERE naam = '{naam}'")
        records = c.fetchall()

        conn.commit()
        conn.close()
        if str(records) != "[]":
            records = ast.literal_eval(str(records).replace("(","").replace(")",""))
            self.ids.naam_hwP.text = records[0]
            self.ids.datum_hwP.text = records[1]
            self.ids.kiesvakHwP.text = records[3]
            self.ids.info_hwP.text = records[2]
        else:
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM proefwerken WHERE naam = '{naam}'")
            records = c.fetchall()

            conn.commit()
            conn.close()
            
            records = ast.literal_eval(str(records).replace("(","").replace(")",""))
            self.ids.naam_hwP.text = records[0]
            self.ids.datum_hwP.text = records[1]
            self.ids.kiesvakHwP.text = records[3]
            self.ids.info_hwP.text = records[2]

    #functies datepicker
    def get_date(self, instance, value, date_range):
        d = str(value).split("-")
        d1 = d[2]
        d2 = d[1]
        d3 = d[0]
        date = str(d1 + "-" + d2 + "-" + d3)
        self.ids.datum_hwP.text = date

    def kies_datum_HwP(self):
        date = self.ids.datum_hwP.text.split("-")
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        date_dialog = MDDatePicker(year=year, month=month, day=day)
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()
    
    #functies bewerken
    def verwijderHw(self):
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM huiswerk WHERE naam = '{naam}'")
        records = c.fetchall()
        if str(records) != "[]":
            c.execute(f"DELETE FROM huiswerk WHERE naam = '{naam}'")
        else:
            c.execute(f"DELETE FROM proefwerken WHERE naam = '{naam}'")

        conn.commit()
        conn.close()
        
        # bouw scherm opnieuw op
        if str(MDApp.get_running_app().current_ScreenName()) == "planning":
            MDApp.get_running_app().root.get_screen("planning").on_enter()
        elif str(MDApp.get_running_app().current_ScreenName()) == "schoolwerk":
            MDApp.get_running_app().root.get_screen("schoolwerk").on_enter()
        
        self.dismiss()
    
    def OW_hw(self):
        old_name = self.title.split(" - ")[0]
        new_name = self.ids.naam_hwP.text
        new_date = self.ids.datum_hwP.text
        new_vak = self.ids.kiesvakHwP.text
        new_info = self.ids.info_hwP.text

        if new_name != "" and new_date != "" and new_vak != "":
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM huiswerk WHERE naam = '{old_name}'")
            r = c.fetchall()
            if str(r) != "[]":
        
                c.execute("""UPDATE huiswerk SET
                    naam = :naam,
                    datum = :datum,
                    beschrijving = :info,
                    vak = :vak
                    WHERE naam = :old_name""",
                    {
                    'naam': new_name,
                    'datum': new_date,
                    'info': new_info,
                    'vak': new_vak,
                    'old_name': old_name,
                })
            else:
                c.execute("""UPDATE proefwerken SET
                    naam = :naam,
                    datum = :datum,
                    beschrijving = :info,
                    vak = :vak
                    WHERE naam = :old_name""",
                    {
                    'naam': new_name,
                    'datum': new_date,
                    'info': new_info,
                    'vak': new_vak,
                    'old_name': old_name,
                })

            conn.commit()
            conn.close()
            
            # bouw scherm opnieuw op
            if str(MDApp.get_running_app().current_ScreenName()) == "planning":
                MDApp.get_running_app().root.get_screen("planning").on_enter()
            elif str(MDApp.get_running_app().current_ScreenName()) == "schoolwerk":
                MDApp.get_running_app().root.get_screen("schoolwerk").on_enter()

            self.dismiss()
        else:
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Je vergeet iets!")
    
    #functie spinner
    def spinnerHwP_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakHwP
        spinner.values = [str(item[0]) for item in data]

class Planning(Screen):
    def on_touch_move(self, touch):
        threshold = float(Window.size[0] / 4)
        diff = float(touch.ox) - float(touch.x)

        if touch.x < touch.ox:
            if diff > threshold:
                MDApp.get_running_app().swipe_right()
        
        if touch.x > touch.ox:
            if diff < threshold * -1:
                MDApp.get_running_app().swipe_left()
    
    def popupSW(self, text):
        naam = text.split("\n")[0]
        popup = PopupSW(title=f"{naam} - aanpassen")
        popup.open()
    
    def on_enter(self):
        window_size = int(Window.size[1]) / 10

        for grid in self.ids.boxmains.children:
            if isinstance(grid, Label):
                # voor verwijderen van label 'niks te doen'
                self.ids.boxmains.remove_widget(grid)
            else:
                for item in grid.children:
                    if isinstance(item, GridLayout):
                        item.clear_widgets()

        pw_lijst = Scorro.show_proefwerken(self)
        hw_lijst = Scorro.show_huiswerk(self)
        pw_lijst.sort(key=lambda x: x[1])
        hw_lijst.sort(key=lambda x: x[1])
        lijst_pw_kort = []
        lijst_pw_lang = []
        lijst_pw_red = []
        lijst_hw = []
        c1 = 0
        c2 = 0
        c3 = 0
        for item in pw_lijst:
            date1 = datetime.strptime(item[1], "%d-%m-%Y")
            cdate = str(date.today())
            cdate = datetime.strptime(cdate, "%Y-%m-%d")
            dif = str(date1 - cdate).split(" ")[0]
            if dif == "0:00:00" or int(dif) < 0:
                naam = item[0]
                conn = sqlite3.connect('ScorroDB.db')
                c = conn.cursor()
                c.execute(f"DELETE FROM proefwerken WHERE naam = '{naam}'")
                conn.commit()
                conn.close()
            elif int(dif) <= 3:
                lijst_pw_kort.append(item)
                c1 += 1
            elif int(dif) <= 8:
                lijst_pw_red.append(item)
                c2 += 1
            elif int(dif) <= 11:
                lijst_pw_lang.append(item)
                c3 += 1
        try: 
            lijst_hw.append(hw_lijst[0])
        except: 
            pass
        try:
            lijst_hw.append(hw_lijst[1])
        except: 
            pass
            
        if c3 > 0:
            self.ids.StudeerGlobaal.text = "Bestudeer globaal de stof van:"
            for item in lijst_pw_lang:
                replace = str(item).replace("(", "").replace(")", "").replace("'", "").split(", ")
                button = Button(text=str(replace[0] + "\n" + replace[3] + " - " + replace[1]), size_hint=(None, None), height=window_size, width=Window.size[0],
                    on_press=lambda button: self.popupSW(button.text), background_normal="", background_color=(1,133/255,39/255,1), font_size=int(int(Window.size[0])/20))
                button.text_size = (button.width-(Window.size[0]/10), None)
                button.bind(size=button.setter('text_size'))
                self.ids.boxmains_pwL.add_widget(button)
        else:
            # 8-11
            self.ids.StudeerGlobaal.text = "Volgende week geen proefwerken!"
        if c2 > 0:
            self.ids.StudeerGoed.text = "Bestudeer goed de stof van:"
            for item in lijst_pw_red:
                replace = str(item).replace("(", "").replace(")", "").replace("'", "").split(", ")
                button = Button(text=str(replace[0] + "\n" + replace[3] + " - " + replace[1]), size_hint=(None, None), height=window_size, width=Window.size[0],
                    on_press=lambda button: self.popupSW(button.text), background_normal="", background_color=(1,133/255,39/255,1), font_size=int(int(Window.size[0])/20))
                button.text_size = (button.width-(Window.size[0]/10), None)
                button.bind(size=button.setter('text_size'))
                self.ids.boxmains_pwRL.add_widget(button)
        else:
            # 3-8
            self.ids.StudeerGoed.text = "Geen proefwerken over 3-8 dagen!"
        if c1 > 0:
            self.ids.LastigeStof.text = "Bestudeer de lastige stof van:"
            for item in lijst_pw_kort:
                replace = str(item).replace("(", "").replace(")", "").replace("'", "").split(", ")
                button = Button(text=str(replace[0] + "\n" + replace[3] + " - " + replace[1]), size_hint=(None, None), height=window_size, width=Window.size[0],
                    on_press=lambda button: self.popupSW(button.text), background_normal="", background_color=(1,133/255,39/255,1), font_size=int(int(Window.size[0])/20))
                button.text_size = (button.width-(Window.size[0]/10), None)
                button.bind(size=button.setter('text_size'))
                self.ids.boxmains_pwK.add_widget(button)
        else:
            # 0-3
            self.ids.LastigeStof.text = "Geen proefwerken binnenkort!"
        if str(lijst_hw) != "[]":
            self.ids.GaVerderMet.text = "Ga verder met:"
            for item in lijst_hw:
                replace = str(item).replace("(", "").replace(")", "").replace("'", "").split(", ")
                button = Button(text=str(replace[0] + "\n" + replace[3] + " - " + replace[1]), size_hint=(None, None), height=window_size, width=Window.size[0],
                    on_press=lambda button: self.popupSW(button.text), background_normal="", background_color=(0, 163/255, 130/255,), font_size=int(int(Window.size[0])/20))
                button.text_size = (button.width-(Window.size[0]/10), None)
                button.bind(size=button.setter('text_size'))
                self.ids.boxmains_hw.add_widget(button)
        else:
            self.ids.GaVerderMet.text = "Er staat geen huiswerk op de planning!"


class Schoolwerk(Screen):
    def on_touch_move(self, touch):
        threshold = float(Window.size[0] / 4)
        diff = float(touch.ox) - float(touch.x)

        if touch.x < touch.ox:
            if diff > threshold:
                MDApp.get_running_app().swipe_right()
        
        if touch.x > touch.ox:
            if diff < threshold * -1:
                MDApp.get_running_app().swipe_left()
    
    def popupSW(self, text):
        naam = text.split("\n")[0]
        popup = PopupSW(title=f"{naam} - aanpassen")
        popup.open()

    def on_enter(self):
        window_size = int(Window.size[1]) / 10
        self.ids.BoxHwPw.clear_widgets()

        pw_lijst = Scorro.show_proefwerken(self)
        hw_lijst = Scorro.show_huiswerk(self)
        if str(pw_lijst) != "[]" or str(hw_lijst) != "[]":
            for item in pw_lijst:
                replace = str(item).replace("(", "").replace(")", "").replace("'", "").split(", ")
                button = Button(text=str(replace[0] + "\n" + replace[3] + " - " + replace[1]), size_hint=(None, None), height=window_size, width=Window.size[0],
                    on_press=lambda button: self.popupSW(button.text), background_normal="", background_color=(1,133/255,39/255,1), font_size=int(int(Window.size[0])/20))
                button.text_size = (button.width-(Window.size[0]/10), None)
                button.bind(size=button.setter('text_size'))
                self.ids.BoxHwPw.add_widget(button)
                
            for item in hw_lijst:
                replace = str(item).replace("(", "").replace(")", "").replace("'", "").split(", ")
                button = Button(text=str(replace[0] + "\n" + replace[3] + " - " + replace[1]), size_hint=(None, None), height=window_size, width=Window.size[0],
                    on_press=lambda button: self.popupSW(button.text), background_normal="", background_color=(0, 163/255, 130/255,), font_size=int(int(Window.size[0])/20))
                button.text_size = (button.width-(Window.size[0]/10), None)
                button.bind(size=button.setter('text_size'))
                self.ids.BoxHwPw.add_widget(button)
            
            self.ids.BoxHwPw.children.sort(reverse=True, key=lambda date: datetime.strptime(date.text.split("\n")[1].split(" - ")[1], "%d-%m-%Y"))
        else:
            label = Label(text="Geen schoolwerk.\nDoe iets leuks met je dag!", size_hint=(None, None), width=Window.size[0], height=window_size,
                font_size=int(int(Window.size[0])/15), color=(0,0,0,1), valign="middle", halign="left")
            label.text_size = (label.width-(Window.size[0]/10), None)
            label.bind(size=label.setter('text_size'))
            
            self.ids.BoxHwPw.add_widget(label)


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
            dagen = records[0][1].replace("[", "").replace("]", "").replace("'", "").split(", ")
            for dag in dagen:
                dagen_popup.append(dag)
            
            for dag in dagen_popup:
                self.ids[dag].background_color = colour_selec
        except:
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Geen dagen gevonden.")

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

                dagen_popup.clear()
                
                vakken_screen = MDApp.get_running_app().root.get_screen("vakken").ids.BoxVakken
                for vak in vakken_screen.children:
                    if vak.text == old_name:
                        vak.text = text
                
                vakken_screen.children.sort(reverse=True, key=lambda x: x.text.lower())
                self.dismiss()
            else:
                popup = Notification(title="Fout")
                popup.open()

                popup.update_text("Geen naam.")
        else:
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Geen dagen.")

    def verwijderKlas(self):
        naam = self.title.split(" - ")[0]

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"DELETE FROM vakken WHERE naam = '{naam}'")

        conn.commit()
        conn.close()

        vakken_screen = MDApp.get_running_app().root.get_screen("vakken").ids.BoxVakken
        
        for vak in vakken_screen.children:
            if vak.text == naam:
                vakken_screen.remove_widget(vak)
        
        self.dismiss()


class Vakken(Screen):
    def on_touch_move(self, touch):
        threshold = float(Window.size[0] / 4)
        diff = float(touch.ox) - float(touch.x)

        if touch.x < touch.ox:
            if diff > threshold:
                MDApp.get_running_app().swipe_right()
        
        if touch.x > touch.ox:
            if diff < threshold * -1:
                MDApp.get_running_app().swipe_left()
    
    def popupVak(self, naam):
        popup = PopupVak(title=f"{naam} - Aanpassen")
        popup.ids.naam_vakAP.text = naam
        popup.open()

    def on_enter(self):
        window_size = int(Window.size[1]) / 10
        vakken_lijst = Scorro.show_klassen(self)
        self.ids.BoxVakken.clear_widgets()
        if str(vakken_lijst) != "[]":
            for vak in vakken_lijst:
                button = Button(text=str(vak[0]), size_hint_y=None, height=window_size, background_color=(0.11, 0.792, 1, 1), font_size=int(int(Window.size[0])/15))
                button.bind(on_press=lambda button: self.popupVak(button.text))
                self.ids.BoxVakken.add_widget(button)
        else: 
            label = Label(text="Geen vakken!", size_hint_y=None, height=window_size, font_size=int(int(Window.size[0])/10), color=(0,0,0,1))
            self.ids.BoxVakken.add_widget(label)
        
        self.ids.BoxVakken.children.sort(reverse=True, key=lambda x: x.text.lower())


class PopupCF(Popup):
    def on_open(self):
        global TotCF
        vak = self.title.split(" | ")[0]
        cijfer = self.title.split(" | ")[1]
        weging = self.title.split(" | ")[2].split(" - ")[0].replace("x", "")
        self.title = vak + " - cijfer aanpassen"

        TotCF = vak + "|" + cijfer + "|" + weging
    
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM cijfers WHERE cijfer = '{cijfer}' AND weging = '{weging}' AND vak = '{vak}'")
        records = c.fetchall()

        conn.commit()
        conn.close()

        records = str(records).replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "").split(", ")
        self.ids.welkCF_p.text = records[0]
        self.ids.wegingCF_p.text = records[1] + "x"
        self.ids.infoCF_p.text = records[2]
        self.ids.kiesvakCF_p.text = records[3]

    def OW_cf(self):
        Ovak = TotCF.split("|")[0]
        Ocijfer = TotCF.split("|")[1]
        Oweging = TotCF.split("|")[2]

        cf = self.ids.welkCF_p.text
        weging = self.ids.wegingCF_p.text.replace("x", "")
        info = self.ids.infoCF_p.text
        vak = self.ids.kiesvakCF_p.text

        try:
            float(cf.replace(",", "."))
            float(weging.replace(",", "."))

            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()
        
            c.execute("""UPDATE cijfers SET
                cijfer = :cijfer,
                weging = :weging,
                beschrijving = :info,
                vak = :vak
                WHERE cijfer = :Ocijfer AND vak = :Ovak AND weging = :Oweging""",
                {
                'cijfer': cf,
                'weging': weging,
                'info': info,
                'vak': vak,
                'Ocijfer': Ocijfer,
                'Oweging': Oweging,
                'Ovak': Ovak,
            })

            conn.commit()
            conn.close()

            
            cijfers_box = MDApp.get_running_app().root.get_screen("cijfers").ids.BoxCfVak
        
            for bu in cijfers_box.children:
                if bu.text.split(" - ")[0] == Ocijfer and bu.text.split(" - ")[1] == Ovak and bu.text.split(" - ")[2] == str(Oweging + "x"):
                    bu.text = cf + " - " + vak + " - " + weging + "x"
            
            cijfers_box.children.sort(reverse=True, key=lambda x: x.text)

            MDApp.get_running_app().root.get_screen("cijfers").on_enter()

            self.dismiss()
        except:
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Je vergeet iets!")

    def verwijdercf(self):
        vak = TotCF.split("|")[0]
        cijfer = TotCF.split("|")[1]
        weging = TotCF.split("|")[2]
        
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"DELETE FROM cijfers WHERE cijfer = '{cijfer}' AND weging = '{weging}' AND vak = '{vak}'")

        conn.commit()
        conn.close()

        cijfers_box = MDApp.get_running_app().root.get_screen("cijfers").ids.BoxCfVak
        
        for cf in cijfers_box.children:
            if cf.text.split(" - ")[0] == cijfer and cf.text.split(" - ")[1] == vak and cf.text.split(" - ")[2] == str(weging + "x"):
                cijfers_box.remove_widget(cf)

        MDApp.get_running_app().root.get_screen("cijfers").on_enter()

        self.dismiss()

    def spinnerCFp_clicked(self):
        data = Scorro.show_klassen(self)
        spinner = self.ids.kiesvakCF_p
        spinner.values = [str(item[0]) for item in data]


class Cijfers(Screen):
    def on_touch_move(self, touch):
        threshold = float(Window.size[0] / 2)
        diff = float(touch.ox) - float(touch.x)

        if touch.x < touch.ox:
            if diff > threshold:
                MDApp.get_running_app().swipe_right()
        
        if touch.x > touch.ox:
            if diff < threshold * -1:
                MDApp.get_running_app().swipe_left()

    def popupCF(self, naam):
        vak = naam.split(" - ")[1]
        cijfer = naam.split(" - ")[0]
        weging = naam.split(" - ")[2]
        popup = PopupCF(title=f"{vak} | {cijfer} | {weging} - cijfer aanpassen")
        popup.open()
    
    def update_TotGem(self):
        cijferlijst = Scorro.show_cijfers(self)
        if cijferlijst != []:
            tot = 0
            weg_t = 0
            for item in cijferlijst:
                tot += float(item[0].replace(",", ".")) * float(item[1].replace(",", "."))
                weg_t += float(item[1].replace(",", "."))
            
            tot2 = tot / weg_t
            self.ids.tot_gem.text = "Totale gemiddelde: " + str(round(tot2, 1)).replace(".", ",")
            if tot2 >= 5.5:
                self.ids.tot_gem.bg_colour = (0, 163/255, 130/255,1)
            else:
                self.ids.tot_gem.bg_colour = (1, 0.329, 0.341, 1)
        else:
            self.ids.tot_gem.text = "Geen cijfers gevonden."
            self.ids.tot_gem.bg_colour = (0, 163/255, 130/255,1)
    
    def on_enter(self):
        self.ids.BoxCfVak.clear_widgets()
        window_size = int(Window.size[1]) / 20
        cijferlijst = Scorro.show_cijfers(self)
        cijferlijst.sort(key=lambda x: x[3].lower())
        
        if str(cijferlijst) != "[]":
            self.ids.alle_cf.height = Window.size[1] / 20
            self.ids.alle_cf.font_size = Window.size[0] / 15
            for item in cijferlijst:
                if float(item[0].replace(",", ".")) >= 5.5:
                    button = Button(text=str(item[0] + " - " + item[3] + " - " + item[1] + "x"), size_hint_y=None, height=window_size,
                        background_normal="", background_color=(0, 163/255, 130/255,1), font_size=int(int(Window.size[0])/20))
                    button.bind(on_press=lambda button: self.popupCF(button.text))
                    self.ids.BoxCfVak.add_widget(button)
                else: 
                    button = Button(text=str(item[0] + " - " + item[3] + " - " + item[1] + "x"), size_hint_y=None, height=window_size,
                        background_normal="", background_color=(1, 0.329, 0.341, 1), font_size=int(int(Window.size[0])/20))
                    button.bind(on_press=lambda button: self.popupCF(button.text))
                    self.ids.BoxCfVak.add_widget(button)
        else:
            self.ids.alle_cf.height = 0
            self.ids.alle_cf.font_size = 0
        
        self.update_TotGem()

        chart = self.ids.chart
        chart.clear_widgets()
        self.ids.CircleBox.clear_widgets()
        plt.cla()

        cijfers = Scorro.show_cijfers(self)
        cijfers.sort(key=lambda x: x[3].lower())

        vakken = []
        gemiddelde = []
        cf_only = []
        vold_count = 0
        onvold_count = 0

        for item in cijfers:
            if item[3] not in vakken:
                vakken.append(item[3])
            
            cf_only.append(item[0])
        
        for item in cf_only:
            if float(item.replace(",",".")) >= 5.5:
                vold_count += 1
            else:
                onvold_count += 1

        self.ids.L_vov.text = f"[color=00a382]Voldoendes: {vold_count}[/color]\n\n[color=ff5457]Onvoldoendes: {onvold_count}[/color]"

        for vak in vakken:
            tot = 0
            totweg = 0
            for item in cijfers:
                if item[3] == vak:
                    cf = float(item[0].replace(",", "."))
                    we = float(item[1])
                    tot += cf * we
                    totweg += we
            gem = round(tot / totweg, 1)
            gemiddelde.append(str(str(gem) + " | " + vak))

        gemiddelde.sort(reverse=True, key=lambda x: float(x.split(" | ")[0]))

        x = []
        y = []
        for item in gemiddelde:
            item = item.split(" | ")
            x.append(item[1])
            y.append(float(item[0]))

        if vold_count != 0 or onvold_count != 0:
            cijf = [vold_count, onvold_count]
        else:
            cijf = [1]

        fig, ax1 = plt.subplots()
        ax1.pie(cijf, colors=[(0, 163/255, 130/255,1), (1, 0.329, 0.341, 1)], shadow=True)
        ax1.axis('equal')
        
        fig.patch.set_alpha(0)
        canvas = FigureCanvasKivyAgg(fig)
        self.ids.CircleBox.add_widget(canvas)
        

        plt.rcParams.update({'font.size': int(Window.size[0]/35)})

        fig, ax2 = plt.subplots()
        ax2.bar(x,y, width=0.5, color=(0, 116/255, 1, 0.8))
        ax2.set_ylim([0,11])
        ax2.set_ylabel("Gemiddelde")
        ax2.set_title("Gemiddelde per vak", loc='left')
        fig.patch.set_alpha(0)

        
        chart_width = 0.4 * len(gemiddelde)
        chart.size_hint_x = chart_width
        self.ids.chart_parent.width = Window.size[0] + (Window.size[0] / 8.75) * len(gemiddelde)

        for i, value in enumerate(y):
            ax2.text(i, value, str(value).replace(".", ","), ha='center', va='bottom')


        chart.add_widget(FigureCanvasKivyAgg(fig))

dutch_to_numeric = {'maandag': 0, 'dinsdag': 1, 'woensdag': 2, 'donderdag': 3, 'vrijdag': 4, 'zaterdag': 5, 'zondag': 6}

def get_next_weekday(current_date, target_weekday):
    days_until_target = (target_weekday - current_date.weekday() + 7) % 7
    next_weekday = current_date + timedelta(days=days_until_target)
    return next_weekday

class NieuwHuiswerk(Screen):
    def get_date(self, instance, value, date_range):
        d = str(value).split("-")
        d1 = d[2]
        d2 = d[1]
        d3 = d[0]
        date = str(d1 + "-" + d2 + "-" + d3)
        self.ids.date_picker.text = date

    def kies_datumHW(self):
        date = self.ids.date_picker.text.split("-")
        year = int(date[2])
        month = int(date[1])
        day = int(date[0])
        date_dialog = MDDatePicker(year=year, month=month, day=day)
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()

    def spinnerHW_clicked(self):
        data = Scorro.show_klassen(self)
        if data != []:
            spinner = self.ids.kiesvakHW
            spinner.values = [str(item[0]) for item in data]
        else: 
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Je hebt nog geen vakken.")

    def enable_date(self):
        vak = self.ids.kiesvakHW.text
        if vak != "Selecteer een vak":
            self.ids.date_picker.disabled = False
        
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM vakken WHERE naam = '{vak}'")
            records = c.fetchall()

            conn.commit()
            conn.close()
            
            records = list(records[0])
            records[1] = ast.literal_eval(records[1])

            current_date = datetime.now()

            list_dates_days = []
            for day in records[1]:
                next_instance_day = get_next_weekday(current_date, target_weekday=dutch_to_numeric[day])
                list_dates_days.append(next_instance_day)
            
            closest_date = min(list_dates_days, key=lambda date: date - current_date).strftime("%d-%m-%Y")
            self.ids.date_picker.text = closest_date


class NieuwProefwerk(Screen):
    def get_date(self, instance, value, date_range):
        d = str(value).split("-")
        d1 = d[2]
        d2 = d[1]
        d3 = d[0]
        date = str(d1 + "-" + d2 + "-" + d3)
        self.ids.date_pickerPW.text = date

    def kies_datumPW(self):
        date = self.ids.date_pickerPW.text.split("-")
        year = int(date[2])
        month = int(date[1])
        day = int(date[0])
        date_dialog = MDDatePicker(year=year, month=month, day=day)
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()

    def spinnerPW_clicked(self):
        data = Scorro.show_klassen(self)
        if data != []:
            spinner = self.ids.kiesvakPW
            spinner.values = [str(item[0]) for item in data]
        else: 
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Je hebt nog geen vakken.")
    
    def enable_date(self):
        vak = self.ids.kiesvakPW.text
        if vak != "Selecteer een vak":
            self.ids.date_pickerPW.disabled = False
            
            conn = sqlite3.connect('ScorroDB.db')
            c = conn.cursor()

            c.execute(f"SELECT * FROM vakken WHERE naam = '{vak}'")
            records = c.fetchall()

            conn.commit()
            conn.close()
            
            records = list(records[0])
            records[1] = ast.literal_eval(records[1])

            current_date = datetime.now()

            list_dates_days = []
            for day in records[1]:
                next_instance_day = get_next_weekday(current_date, target_weekday=dutch_to_numeric[day])
                list_dates_days.append(next_instance_day)
            
            closest_date = min(list_dates_days, key=lambda date: date - current_date).strftime("%d-%m-%Y")
            self.ids.date_pickerPW.text = closest_date


class NieuwCijfer(Screen):
    def spinnerCF_clicked(self):
        data = Scorro.show_klassen(self)
        if data != []:
            spinner = self.ids.kiesvakCF
            spinner.values = [str(item[0]) for item in data]
        else: 
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Je hebt nog geen vakken.")

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
    def on_enter(self):
        self.refresh()

    def spinnerCFB_clicked(self):
        data = Scorro.show_klassen(self)
        if data != []:
            spinner = self.ids.kiesvakCFB
            spinner.values = [str(item[0]) for item in data]
        else: 
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Je hebt nog geen vakken.")
    
    def refresh(self):
        self.ids.BoxCF_WE.clear_widgets()
        self.ids.kiesvakCFB.text = "Selecteer een vak"
        self.ids.CF_BH.text = ""
        self.ids.welkCFW.text = ""
        self.ids.welkWEW.text = ""
        self.ids.welkCFW.disabled = True
        self.ids.welkWEW.disabled = True
        self.ids.bereken.disabled = True


    def vak_gekozen(self):
        vak = self.ids.kiesvakCFB.text
        self.ids.BoxCF_WE.clear_widgets()

        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute(f"SELECT * FROM cijfers WHERE vak = '{vak}'")
        records = c.fetchall()

        conn.commit()
        conn.close()
        
        window_size = int(Window.size[1]) / 20
        for item in records:
            l = Label(text=item[0], color=(0,0,0,1), size_hint_y=None, height=window_size)
            e = Label(text=str(item[1] + "x"), color=(0,0,0,1), size_hint_y=None, height=window_size)
            self.ids.BoxCF_WE.add_widget(l)
            self.ids.BoxCF_WE.add_widget(e)
        
        self.ids.welkCFW.disabled = False
        self.ids.welkWEW.disabled = False
        self.ids.bereken.disabled = False
        
    def bereken_cf(self):
        if self.ids.kiesvakCFB.text != "Selecteer een vak":
            try:
                goal = float(self.ids.welkCFW.text.replace(",", "."))
                weg = float(self.ids.welkWEW.text.replace(",", ".").replace("x", "").replace("X", ""))

                conn = sqlite3.connect('ScorroDB.db')
                c = conn.cursor()

                c.execute(f"SELECT * FROM cijfers WHERE vak = '{self.ids.kiesvakCFB.text}'")
                records = c.fetchall()

                conn.commit()
                conn.close()

                tot = 0
                weg_t = 0
                for item in records:
                    tot += float(item[1]) * float(item[0].replace(",", "."))
                    weg_t += float(item[1])
                weg_t += weg
                grade_weg = goal * weg_t - tot
                grade_to_get = grade_weg / weg

                self.ids.CF_BH.text = str(round(grade_to_get, 1)).replace(".", ",")
            except:
                popup = Notification(title="Fout")
                popup.open()

                popup.update_text("Fout bij invoer.")
        else:
                popup = Notification(title="Fout")
                popup.open()

                popup.update_text("Selecteer een vak.")


class Notification(Popup):
    def update_text(self, new_text):
        self.ids.LabelNoti.text = new_text

    def on_open(self):
        Clock.schedule_once(lambda dt: self.dismiss(), 1)


class WindowManager(ScreenManager):
    pass


screen_order = ["dashboard", "planning", "schoolwerk", "cijfers", "vakken"]

class Scorro(MDApp):
    def current_ScreenName(self):
        return self.root.current

    def call_cf(self):
        self.root.current = "nieuw cijfer"

    def on_start(self):
        self.root.current = "dashboard"

    def swipe_right(self):
        cur =  self.root.current
        if cur != "vakken":
            for screen in screen_order:
                if screen == cur:
                    next_scr = int(screen_order.index(screen))+1
                    self.root.transition = SlideTransition()
                    self.root.transition.direction = 'left'
                    self.root.current = screen_order[next_scr]
    
    def swipe_left(self):
        cur =  self.root.current
        if cur != "dashboard":
            for screen in screen_order:
                if screen == cur:
                    next_scr = int(screen_order.index(screen))-1
                    self.root.transition = SlideTransition()
                    self.root.transition.direction = 'right'
                    self.root.current = screen_order[next_scr]


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
            vak text,
            date text)
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

        kv = Builder.load_file('main_kv.kv')
        return kv


    #functies voor klassen
    def submit_klas(self):
        global lijst_dagen
        text = self.root.get_screen('nieuw vak').ids.naam_vak.text
        
        if text != "":
            if lijst_dagen != []:
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
                origin = self.root.get_screen('nieuw vak')
                origin.ids.maandag.background_color = (1,0,0,1)
                origin.ids.dinsdag.background_color = (1,0,0,1)
                origin.ids.woensdag.background_color = (1,0,0,1)
                origin.ids.donderdag.background_color = (1,0,0,1)
                origin.ids.vrijdag.background_color = (1,0,0,1)
                origin.ids.zaterdag.background_color = (1,0,0,1)
                origin.ids.zondag.background_color = (1,0,0,1)

                self.root.get_screen('nieuw vak').ids.naam_vak.text = ''
                
                popup = Notification(title="Gelukt!")
                popup.open()

                popup.update_text("Vak opgeslagen!")
            else:
                popup = Notification(title="Fout")
                popup.open()

                popup.update_text("Selecteer minstens 1 dag.")
        else:
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Geef je vak een naam.")

    def show_klassen(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM vakken")
        records = c.fetchall()

        conn.commit()
        conn.close()
        records.sort(key=lambda x: x[0].lower())
        return records

    #functies voor cijfers
    def submit_cijfer(self):
        naam = self.root.get_screen('nieuw cijfer').ids.welkCF.text
        weging = self.root.get_screen('nieuw cijfer').ids.wegingCF.text.replace("x", "").replace("X", "")
        vak = self.root.get_screen('nieuw cijfer').ids.kiesvakCF.text
        now = datetime.now()

        try:
            float(naam.replace(",", "."))
            float(weging.replace(",", "."))

            if vak != "Selecteer een vak":
                if float(naam.replace(",", ".")) <= 10.0 and float(naam.replace(",", ".")) >= 0.0:
                    conn = sqlite3.connect('ScorroDB.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO cijfers VALUES (:cijfer, :weging, :beschrijving, :vak, :date)",
                    {
                        'cijfer': naam,
                        'weging': weging,
                        'beschrijving': self.root.get_screen('nieuw cijfer').ids.infoCF.text,
                        'vak': vak,
                        'date': now,
                    })

                    conn.commit()
                    conn.close()


                    self.root.get_screen('nieuw cijfer').ids.welkCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.wegingCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.infoCF.text = ''
                    self.root.get_screen('nieuw cijfer').ids.kiesvakCF.text = 'Selecteer een vak'

                    popup = Notification(title="Gelukt!")
                    popup.open()

                    popup.update_text("Cijfer opgeslagen!")
                else:
                    popup = Notification(title="Fout")
                    popup.open()

                    popup.update_text("Je cijfer zit niet tussen 0 en 10.")
            else:
                popup = Notification(title="Fout")
                popup.open()

                popup.update_text("Selecteer een vak.")
        except:
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Fout bij invoer.")

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
        datum = self.root.get_screen('nieuw proefwerk').ids.date_pickerPW.text
        vak = self.root.get_screen('nieuw proefwerk').ids.kiesvakPW.text
        beschrijving = self.root.get_screen('nieuw proefwerk').ids.infoPW.text
        if naam != "":
            if vak != "Selecteer een vak":
                if datum != "Kies Datum":
                    conn = sqlite3.connect('ScorroDB.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO proefwerken VALUES (:naam, :datum, :beschrijving, :vak)",
                    {
                        'naam': naam,
                        'datum': datum,
                        'beschrijving': beschrijving,
                        'vak': vak,
                    })

                    conn.commit()
                    conn.close()

                    self.root.get_screen('nieuw proefwerk').ids.welkPW.text = ''
                    self.root.get_screen('nieuw proefwerk').ids.date_pickerPW.text = 'Kies Datum'
                    self.root.get_screen('nieuw proefwerk').ids.date_pickerPW.disabled = True
                    self.root.get_screen('nieuw proefwerk').ids.infoPW.text = ''
                    self.root.get_screen('nieuw proefwerk').ids.kiesvakPW.text = 'Selecteer een vak'
                    
                    popup = Notification(title="Gelukt!")
                    popup.open()

                    popup.update_text("Proefwerk opgeslagen!")
                else:
                    popup = Notification(title="Fout")
                    popup.open()

                    popup.update_text("Geef je proefwerk een datum.")
            else:
                popup = Notification(title="Fout")
                popup.open()

                popup.update_text("Selecteer een vak.")
        else:
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Geef je proefwerk een naam.")
            
            
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
        datum = self.root.get_screen('nieuw huiswerk').ids.date_picker.text
        vak = self.root.get_screen('nieuw huiswerk').ids.kiesvakHW.text
        beschrijving = self.root.get_screen('nieuw huiswerk').ids.infoHW.text

        if naam != "":
            if vak != "Selecteer een vak":
                if datum != "Kies Datum":
                    conn = sqlite3.connect('ScorroDB.db')
                    c = conn.cursor()

                    c.execute("INSERT INTO huiswerk VALUES (:naam, :datum, :beschrijving, :vak)",
                    {
                        'naam': naam,
                        'datum': datum,
                        'beschrijving': beschrijving,
                        'vak': vak,
                    })

                    conn.commit()
                    conn.close()

                    self.root.get_screen('nieuw huiswerk').ids.welkHW.text = ''
                    self.root.get_screen('nieuw huiswerk').ids.date_picker.text = 'Kies Datum'
                    self.root.get_screen('nieuw huiswerk').ids.date_picker.disabled = True
                    self.root.get_screen('nieuw huiswerk').ids.infoHW.text = ''
                    self.root.get_screen('nieuw huiswerk').ids.kiesvakHW.text = 'Selecteer een vak'

                    popup = Notification(title="Gelukt!")
                    popup.open()

                    popup.update_text("Huiswerk opgeslagen!")
                else:
                    popup = Notification(title="Fout")
                    popup.open()

                    popup.update_text("Geef je huiswerk een datum.")
            else:
                popup = Notification(title="Fout")
                popup.open()

                popup.update_text("Selecteer een vak.")
        else:
            popup = Notification(title="Fout")
            popup.open()

            popup.update_text("Geef je huiswerk een naam.")

    def show_huiswerk(self):
        conn = sqlite3.connect('ScorroDB.db')
        c = conn.cursor()

        c.execute("SELECT * FROM huiswerk")
        records = c.fetchall()

        conn.commit()
        conn.close()
        return records

#Window.size = (525, 900)   
Window.size = (350, 600)
#Window.size = (233, 400)

if __name__ == "__main__":
    Scorro().run()