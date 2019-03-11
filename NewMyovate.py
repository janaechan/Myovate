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
import GraphThread
<<<<<<< HEAD
import Arduino
=======
>>>>>>> c739216ded632301e165d9068c2672b59a7b27f6
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
<<<<<<< HEAD
    # get_microphone_thread = Thread(target=MicrophoneThread.get_microphone_level)
    # get_microphone_thread.start()
    # get_arduino_thread = Thread(target=GraphThread.get_data_test)
    Window.fullscreen = 'auto'
=======

    # get_arduino_thread = Thread(target=GraphThread)
    # get_arduino_thread.daemon = True
    # get_arduino_thread.start()
    # GraphThread.get_data_test()
    # Window.fullscreen = 'auto'
>>>>>>> c739216ded632301e165d9068c2672b59a7b27f6
    NewMyovateApp().run()
    # arduino = Arduino.Arduino()
