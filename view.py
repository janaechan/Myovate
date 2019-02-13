from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.base import runTouchApp

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class MainScreen:

    def __init__(self):
        self.drop_down_menu = DropDown()

    def build(self):
        # Main menu text
        myovate_menu_text = "Myovate Menu"

        # Layout
        layout_drop = AnchorLayout(anchor_x='left', anchor_y='top')
        layout_myovate = AnchorLayout(anchor_x='center', anchor_y='center')
        layout_main = FloatLayout()

        # Welcome text
        welcome_text = "Welcome to Myovate"
        welcome_label = Label(text=welcome_text, font_size='40sp')
        layout_myovate.add_widget(welcome_label)

        # Make buttons
        calibration_button = Button(text='Calibration', size_hint_y=None, height=150)
        calibration_button.bind(on_release=lambda btn: self.drop_down_menu.select(myovate_menu_text))

        progress_button = Button(text='Progress', size_hint_y=None, height=150)
        progress_button.bind(on_release=lambda btn: self.drop_down_menu.select(myovate_menu_text))
        calibration_button.on_press()

        # Add buttons to layout
        self.drop_down_menu.add_widget(calibration_button)
        self.drop_down_menu.add_widget(progress_button)

        # Menu button
        menu_button = Button(text=myovate_menu_text, size_hint=(0.2, 0.2))
        menu_button.bind(on_release=self.drop_down_menu.open)
        self.drop_down_menu.bind(on_select=lambda instance, x: setattr(menu_button,'text', x))
        layout_drop.add_widget(menu_button)

        # Add to main layout
        layout_main.add_widget(layout_drop)
        layout_main.add_widget(layout_myovate)

        # return layout_main, self.drop_down_menu
        return runTouchApp(layout_main)


# screen_manager = ScreenManager()
# screen_manager.add_widget(CalibrationScreen(name='calibration_screen'))

