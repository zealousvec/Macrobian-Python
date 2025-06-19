import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

class WindowManager(ScreenManager):
    pass

class MainLayout(ScreenManager): # this is my first window basically my home scren
    pass

class MainScreen(Screen):
    pass

class SecondWindow(Screen): # this is my second window basically the UI for my languages
    pass

class RoundedImage(Button):
    image = BooleanProperty(False)
    
kv = Builder.load_file('main.kv')

class MainApp(App):
    
    def build(self):
        return Builder.load_file('main.kv')

    def on_button_press(self, instance):
        print("Pressed:", instance.text)
    
    def copy(self):
        print("copied")
        
    def change_language(self):
        print("changed the language")
        
    def switch_language(self):
        print("switched languages")
        

if __name__ == '__main__':
    MainApp().run()
    



