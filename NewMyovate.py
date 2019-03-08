from kivy.app import App
from kivy.lang.builder import Builder
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
import datetime
import time

from kivy.garden.graph import MeshLinePlot
from threading import Thread
import audioop
import pyaudio
import AwardsScreen
import AboutUsScreen
import StartSessionScreen
import SessionHistoryScreen
import RunningSessionScreen
import JournalScreen
import Misc

def get_microphone_level():
    """
    source: http://stackoverflow.com/questions/26478315/getting-volume-levels-from-pyaudio-for-use-in-arduino
    audioop.max alternative to audioop.rms
    """
    chunk = 100
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 30000
    p = pyaudio.PyAudio()

    s = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=chunk)
    global levels
    while True:
        data = s.read(chunk)
        mx = audioop.rms(data, 2)
        if len(levels) >= 100:
            levels = []
        levels.append(mx)


class ScreenManagement(ScreenManager):

    def __init__(self, **kwargs):
        self.drop_down = Misc.DropDownMenu()
        super(ScreenManagement, self).__init__(**kwargs)


class MainScreen(Screen):
    pass


class NewMyovateApp(App):
    pass


# class AwardsScreen(Screen):
#     pass


class AboutUsScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.drop_down = Misc.DropDownMenu()


presentation = Builder.load_file("NewMyovate.kv")


class MyvoateApp(App):
    # TODO create arduino instance

    def build(self):
        return presentation


if __name__ == '__main__':
    levels = []  # store levels of microphone

    get_level_thread = Thread(target=get_microphone_level)
    get_level_thread.daemon = True
    get_level_thread.start()
    Window.fullscreen = 'auto'
    NewMyovateApp().run()
    """
    Gamepad: +/- x; +/- y
    Keyboard: 
    Confirm Arduino when you start session
    """
