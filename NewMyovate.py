from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import Label as CoreLabel
from kivy.lang.builder import Builder
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.recycleview import RecycleView
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty


class AddSensorPopup(Popup):
    pass


class CalibrationSetupPopup(Popup):
    pass


class CalibrationRelaxPopup(Popup):
    progress_bar = ObjectProperty()
    cp = ObjectProperty()

    def __init__(self, **kwargs):
        super(CalibrationRelaxPopup, self).__init__(**kwargs)
        self.progress_bar = ProgressBar()  # instance of ProgressBar created.
        Clock.schedule_once(self.progress_bar_start)

    def progress_bar_start(self, instance):  # Provides initial value of of progress bar and lanches popup
        self.cp.value = 1  # Initial value of progress_bar

    def next(self, dt):  # Updates Project Bar
        if self.cp.value >= 100:  # Checks to see if progress_bar.value has met 100
            return False  # Returning False schedule is canceled and won't repeat
        self.cp.value += 1  # Updates progress_bar's progress

    def puopen(self):  # Called from bind.
        Clock.schedule_interval(self.next, .0005)  # Creates Clock event scheduling next() every 5-1000th of a second.


class CalibrationContractPopup(Popup):
    cp = ObjectProperty()

    def __init__(self, **kwargs):
        super(CalibrationContractPopup, self).__init__(**kwargs)
        self.progress_bar = ProgressBar()  # instance of ProgressBar created.
        Clock.schedule_once(self.progress_bar_start)

    def progress_bar_start(self, instance):  # Provides initial value of of progress bar and lanches popup
        self.cp.value = 1  # Initial value of progress_bar

    def next(self, dt):  # Updates Project Bar
        if self.cp.value >= 100:  # Checks to see if progress_bar.value has met 100
            return False  # Returning False schedule is canceled and won't repeat
        self.cp.value += 1  # Updates progress_bar's progress

    def puopen(self):  # Called from bind.
        Clock.schedule_interval(self.next, .0005)  # Creates Clock event scheduling next() every 5-1000th of a second.


class CalibrationCompletePopup(Popup):
    pass


class DropDownMenu(DropDown):
    pass


class AboutUsScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class StartSessionScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(StartSessionScreen, self).__init__(*args, **kwargs)
        self.add_sensor_popup = AddSensorPopup()

    def insert(self, value, sensor_loc):
        print(value, sensor_loc)
        self.rv.data.insert(0, {'value': value or 'default value',
                                'sensor_loc': sensor_loc or 'default value'})


class RunningSessionScreen(Screen):
    rv = ObjectProperty()


class ProgressScreen(Screen):
    def insert(self, value):
        self.rv_progress.data.insert(0, {'value': value or 'default value'})
        print(self.rv_progress.data, value)

    def print_log(self):
        print(self.rv_progress.data)


class ScreenManagement(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(ScreenManagement, self).__init__(*args, **kwargs)
        self.drop_down = DropDownMenu()


presentation = Builder.load_file("NewMyovate.kv")


class MyvoateApp(App):
    def build(self):
        return presentation


if __name__ == '__main__':
    MyvoateApp().run()
