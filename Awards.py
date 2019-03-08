from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
import datetime
from kivy.properties import ObjectProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.lang.builder import Builder
import time


class AwardsApp(App):
    pass


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    AwardsApp().run()