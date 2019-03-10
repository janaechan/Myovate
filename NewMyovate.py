from kivy.app import App
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager
from threading import Thread
import audioop


import AboutUsScreen
import AwardsScreen
import JournalScreen
import SessionHistoryScreen
import RunningSessionScreen
import StartSessionScreen
import MainScreen
import ProgressScreen
import MicrophoneThread
import Misc


# class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
#                                  RecycleBoxLayout):
#     ''' Adds selection and focus behaviour to the view. '''


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.drop_down = Misc.DropDownMenu()


class NewMyovateApp(App):
    pass


if __name__ == '__main__':
    # TODO create arduino instance
    # TODO start arduino thread when you start new session so you can call find_, set_, get_data
    # levels = []  # store levels of microphone

    # get_arduino_thread = Thread(target=Arduino)
    Window.fullscreen = 'auto'
    NewMyovateApp().run()
