from kivy.app import App
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager
from threading import Thread
import audioop
import pyaudio

import AboutUsScreen
import AwardsScreen
import JournalScreen
import SessionHistoryScreen
import RunningSessionScreen
import StartSessionScreen
import MainScreen
import ProgressScreen
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


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.drop_down = Misc.DropDownMenu()


class NewMyovateApp(App):
    pass


if __name__ == '__main__':
    # TODO create arduino instance
    levels = []  # store levels of microphone
    get_level_thread = Thread(target=get_microphone_level)
    get_level_thread.daemon = True
    get_level_thread.start()
    Window.fullscreen = 'auto'
    NewMyovateApp().run()