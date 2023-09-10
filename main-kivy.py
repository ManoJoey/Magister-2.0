import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

#Homepage
#(Nieuw cijfer invullen / Nieuw vak toevoegen)
#Statistieken per vak
#Compleet cijferlijstoverzicht
#Algemene statistieken
#Huiswerkoverzicht/Kalender met notificaties
#Toetsplanner (met Google Agenda als er tijd is)

class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

        
class MyApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == "__main__":
    MyApp().run()