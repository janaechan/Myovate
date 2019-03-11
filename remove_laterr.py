from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
import Arduino


class MyScreenManager(ScreenManager):
    total_button = NumericProperty(2)


class Login(Screen):
    login = ObjectProperty(None)

    def on_pre_enter(self):
        Window.size = (400, 300)

    def check_password(self, instance, password):
        if password == "pwd":
            instance.current = "registers"


class Registers(Screen):
    container = ObjectProperty(None)

    def on_pre_enter(self):
        Window.size = (800, 600)

    def add_buttons(self, n):
        arduino = Arduino.Arduino()
        box1 = BoxLayout(orientation='horizontal')
        box2 = BoxLayout(orientation='horizontal')
        count = 0
        for i, j in arduino.button_code.items():
            if count < len(arduino.button_code) / 2:
                box1.add_widget(Button(text="{}".format(' '.join(i.split('_')[1:])), id=i))
            else:
                box2.add_widget(Button(text="{}".format(' '.join(i.split('_')[1:])), id=i))
            count += 1
        self.container.add_widget(box1)
        self.container.add_widget(box2)
        print("Registers: n={}".format(n))
        # for i in range(n):
        #     self.container.add_widget(Button(text="Button #{}".format(i), id=str(i)))

    def remove_buttons(self, *args):
        for child in [child for child in self.container.children]:
            self.container.remove_widget(child)


class Welcome(Screen):
    pass


class TestApp(App):
    title = "ScreenManager - Add Widgets Dynamically"

    def build(self):

        return MyScreenManager()


if __name__ == "__main__":
    TestApp().run()