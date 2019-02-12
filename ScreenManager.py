from kivy.app import App
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
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty

import view


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        drop_down_menu = DropDown()

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
        # calibration_button.bind(on_release=lambda btn: drop_down_menu.select(myovate_menu_text))
        calibration_button.bind(on_press=self.on_press_calibrate, on_release=lambda btn: drop_down_menu.select(myovate_menu_text))
        progress_button = Button(text='Progress', size_hint_y=None, height=150)
        calibration_button.bind(on_press=self.on_press_progress, on_release=lambda btn: drop_down_menu.select(myovate_menu_text))
        # progress_button.bind(on_release=lambda btn: drop_down_menu.select(myovate_menu_text))
        # calibration_button.on_press()

        # Add buttons to layout
        drop_down_menu.add_widget(calibration_button)
        drop_down_menu.add_widget(progress_button)

        # Menu button
        menu_button = Button(text=myovate_menu_text, size_hint=(0.2, 0.2))
        menu_button.bind(on_release=drop_down_menu.open)
        drop_down_menu.bind(on_select=lambda instance, x: setattr(menu_button, 'text', x))
        layout_drop.add_widget(menu_button)

        # Add to main layout
        # layout_main.add_widget(drop_down_menu)
        layout_main.add_widget(layout_drop)
        layout_main.add_widget(layout_myovate)
        self.add_widget(layout_main)
        self.add_widget(drop_down_menu)

    def on_press_calibrate(self, *args):
        self.manager.current = "calibration_screen"

    def on_press_progress(self, *args):
        self.manager.current = "progress_screen"


class CalibrationScreen(Screen):
    def __init__(self, **kwargs):
        super(CalibrationScreen, self).__init__(**kwargs)
        layout = BoxLayout()
        btn = Button(text="Go to screen 3")
        btn.bind(on_press=self.on_press)
        layout.add_widget(btn)
        self.add_widget(layout)

    def on_press(self, *args):
        self.manager.current = "progress_screen"


class ProgressScreen(Screen):
    def __init__(self, **kwargs):
        super(ProgressScreen, self).__init__(**kwargs)
        drop_down_menu = DropDown()

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
        # calibration_button.bind(on_release=lambda btn: drop_down_menu.select(myovate_menu_text))
        calibration_button.bind(on_press=self.on_press_calibrate,
                                on_release=lambda btn: drop_down_menu.select(myovate_menu_text))
        progress_button = Button(text='Progress', size_hint_y=None, height=150)
        calibration_button.bind(on_press=self.on_press_progress,
                                on_release=lambda btn: drop_down_menu.select(myovate_menu_text))
        # progress_button.bind(on_release=lambda btn: drop_down_menu.select(myovate_menu_text))
        # calibration_button.on_press()

        # Add buttons to layout
        drop_down_menu.add_widget(calibration_button)
        drop_down_menu.add_widget(progress_button)

        # Menu button
        menu_button = Button(text=myovate_menu_text, size_hint=(0.2, 0.2))
        menu_button.bind(on_release=drop_down_menu.open)
        drop_down_menu.bind(on_select=lambda instance, x: setattr(menu_button, 'text', x))
        layout_drop.add_widget(menu_button)

        # Add to main layout
        # layout_main.add_widget(drop_down_menu)
        layout_main.add_widget(layout_drop)
        layout_main.add_widget(layout_myovate)
        self.add_widget(layout_main)
        self.add_widget(drop_down_menu)

    def on_press_calibrate(self, *args):
        self.manager.current = "calibration_screen"

    def on_press_progress(self, *args):
        self.manager.current = "progress_screen"


class Screens(App):
    def build(self):
        my_screen_manager = ScreenManager(transition=NoTransition())
        main_screen = MainScreen(name='main_screen')
        calibration_screen = CalibrationScreen(name='calibration_screen')
        progress_screen = ProgressScreen(name='progress_screen')

        my_screen_manager.add_widget(main_screen)
        my_screen_manager.add_widget(calibration_screen)
        my_screen_manager.add_widget(progress_screen)

        # m = Manager(transition=NoTransition())
        return my_screen_manager
