import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class MultiGraphApp(App):
    def build(self):
        # Create a BoxLayout to hold the Matplotlib plots
        layout = BoxLayout(orientation='vertical')

        # Create sample data
        data1 = [10, 20, 15, 25]
        data2 = [5, 15, 10, 20]

        # Create the first subplot
        fig, ax1 = plt.subplots()
        ax1.bar(range(len(data1)), data1, color='blue')
        ax1.set_xlabel('Bars')
        ax1.set_ylabel('Values')
        ax1.set_title('Matplotlib Bar Chart 1')
        canvas1 = FigureCanvasKivyAgg(fig)
        layout.add_widget(canvas1)

        # Create the second subplot
        fig, ax2 = plt.subplots()
        ax2.bar(range(len(data2)), data2, color='green')
        ax2.set_xlabel('Bars')
        ax2.set_ylabel('Values')
        ax2.set_title('Matplotlib Bar Chart 2')
        canvas2 = FigureCanvasKivyAgg(fig)
        layout.add_widget(canvas2)

        return layout

if __name__ == '__main__':
    MultiGraphApp().run()