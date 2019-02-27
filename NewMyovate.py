from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
import datetime

from kivy.garden.graph import MeshLinePlot
from threading import Thread
import audioop
import pyaudio


def get_microphone_level():
    """
    source: http://stackoverflow.com/questions/26478315/getting-volume-levels-from-pyaudio-for-use-in-arduino
    audioop.max alternative to audioop.rms
    """
    chunk = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
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


class Row(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv_data = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Row, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(Row, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(Row, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        # print(index, is_selected, rv.data[index])
        # self.selected = is_selected
        self.rv_data = rv.data
        self.index = index
        # if is_selected:
        #     rv.data.pop(index)
        #     rv.layout_manager.clear_selection()

    def remove(self, root):
        print(root.rv_data)
        print(self.ids)

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plot.points = [(i, j / 5) for i, j in enumerate(levels)]


class ConfirmDeletePopup(Popup):
    pass


class AddSensorPopup(Popup):
    rv_data = ObjectProperty()
    index = 0
    date = datetime.date.today().strftime('%m/%d/%y')

    def __init__(self, sensor_data=None, **kwargs):
        super(AddSensorPopup, self).__init__(**kwargs)

        if sensor_data is not None:
            self.rv_data = sensor_data.rv_data
            self.index = sensor_data.index
            print(sensor_data.rv_data)


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
    session_date = datetime.date.today().strftime('%m/%d/%y')

    def __init__(self, **kwargs):
        super(StartSessionScreen, self).__init__(**kwargs)
        self.add_sensor_popup = AddSensorPopup()

    def insert(self, sensor_name, sensor_loc, but_mapping):
        print(sensor_name, sensor_loc)
        self.rv.data.insert(0, {'sensor_name': sensor_name or 'default value',
                                'sensor_loc': sensor_loc or 'default value',
                                'but_mapping': but_mapping or 'default value'})


class RunningSessionScreen(Screen):
    rv = ObjectProperty()


class ProgressScreen(Screen):
    def insert(self, value, rv_data):

        self.rv_progress.data.insert(0, {'value': value or 'default value'})
        print("DATA FROM ADDING SENSORS", rv_data)

    def print_log(self):
        print(self.rv_progress.data)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.drop_down = DropDownMenu()


presentation = Builder.load_file("NewMyovate.kv")


class MyvoateApp(App):
    def build(self):
        return presentation


if __name__ == '__main__':
    levels = []  # store levels of microphone
    get_level_thread = Thread(target=get_microphone_level)
    get_level_thread.daemon = True
    get_level_thread.start()

    MyvoateApp().run()
