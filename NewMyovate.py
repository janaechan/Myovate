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


class CustomizedButton(Button):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))


class Row(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv_data = ObjectProperty(None)
    rv = ObjectProperty(None)

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
        self.rv = rv
        self.rv_data = rv.data
        self.index = index
        self.selected = is_selected
        print(self.index)

    def remove(self):
        print('REMOVE ENTRY')
        if self.rv:
            self.rv.data.pop(self.index)

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plot.points = [(i, j / 5) for i, j in enumerate(levels)]


class RunningScreenRow(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv_data = ObjectProperty(None)
    rv = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RunningScreenRow, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(RunningScreenRow, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(RunningScreenRow, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.rv = rv
        self.rv_data = rv.data
        self.index = index
        self.selected = is_selected
        print(self.index)

    def remove(self):
        print('REMOVE ENTRY')
        if self.rv:
            self.rv.data.pop(self.index)

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plot.points = [(i, j / 5) for i, j in enumerate(levels)]


class SessionHistoryRow(RecycleDataViewBehavior, GridLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 2

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SessionHistoryRow, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SessionHistoryRow, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class ConfirmDeletePopup(Popup):
    remove_status = BooleanProperty(False)

    def __init__(self, root, **kwargs):
        super(ConfirmDeletePopup, self).__init__(**kwargs)
        self.root = root

    def remove(self):
        print('update remove status')
        self.remove_status = True
        self.root.remove()


class AddSensorPopup(Popup):
    rv_data = ObjectProperty()
    txt_input = ObjectProperty()
    rv = ObjectProperty()
    index = 0
    date = datetime.date.today().strftime('%m/%d/%y')

    # TODO Channel Number
    def __init__(self, sensor_data=None, **kwargs):
        if sensor_data is not None:
            self.rv_data = sensor_data.rv_data
            self.index = sensor_data.index
            print(sensor_data.rv_data)
        super(AddSensorPopup, self).__init__(**kwargs)

    def clear_text_input(self):
        self.ids.sensor_name_input.text = ''
        self.ids.sensor_loc_input.text = ''
        self.ids.but_mapping_input.text = ''
        self.dismiss()
        return CalibrationSetupPopup().open()

    def cancel_adding_sensor(self):
        self.ids.sensor_name_input.text = ''
        self.ids.sensor_loc_input.text = ''
        self.ids.but_mapping_input.text = ''
        self.dismiss()

    def on_text(self):
        # print(self.ids.keyboard_toggle.state, self.ids.game_pad_toggle.state)
        if self.ids.keyboard_toggle.state == 'normal':
            matches = ['A', 'B', 'X', 'Y']
        else:
            matches = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

        # display the data in the recycleview
        display_data = []
        for i in matches:
            display_data.append({'text': i})
        # self.ids.rv.data = display_data

        # ensure the size is okay
        if len(matches) <= 3:
            self.parent.height = 30


class DropDownWidget(BoxLayout):
    txt_input = ObjectProperty()
    rv = ObjectProperty()


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)


class MyTextInput(TextInput):
    txt_input = ObjectProperty()
    flt_list = ObjectProperty()
    word_list = ListProperty()
    # this is the variable storing the number to which the look-up will start
    starting_no = NumericProperty(3)
    suggestion_text = ''

    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        # print(self.parent.parent.parent.parent.ids)
        return super(MyTextInput, self).on_touch_down(touch)

    def on_text(self, instance, value):
        # find all the occurrence of the word
        self.parent.ids.rv.data = []
        matches = [self.word_list[i] for i in range(len(self.word_list)) if
                   self.word_list[i][:self.starting_no] == value[:self.starting_no]]
        matches = ['A', 'B', 'X', 'Y']
        matches = []
        # display the data in the recycleview
        display_data = []
        for i in matches:
            display_data.append({'text': i})
        self.parent.ids.rv.data = display_data

        # ensure the size is okay
        if len(matches) <= 10:
            self.parent.height = (50 + (len(matches) * 20))
        else:
            self.parent.height = 240


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
        # 1500 data points
        if self.cp.value >= 100:  # Checks to see if progress_bar.value has met 100
            self.add_next_button()
            time.sleep(1)
            self.r_cal.text = 'Current Calibration Complete'
            return False  # Returning False schedule is canceled and won't repeat

        # get new value from arduino global
        self.cp.value += 1  # Updates progress_bar's progress

    def add_next_button(self):
        ok_button = CustomizedButton(text='Next', pos_hint={'center_x': 0.75, 'center_y': 0.15},
                           size=(self.ids.layout.width / 2, self.ids.layout.height / 5),
                           size_hint=(None, None)
                           )
        ok_button.bind(on_press=self.clk)
        self.ids.layout.add_widget(ok_button)

    def clk(self, obj):
        popup = CalibrationContractPopup()
        popup.open()
        return super(CalibrationRelaxPopup, self).dismiss()
        # self.dismiss()

    def puopen(self):  # Called from bind.
        Clock.schedule_interval(self.next, .0005)  # Creates Clock event scheduling next() every 5-1000th of a second.


class CalibrationContractPopup(Popup):
    progress_bar = ObjectProperty()
    cp = ObjectProperty()

    def __init__(self, **kwargs):
        super(CalibrationContractPopup, self).__init__(**kwargs)
        self.progress_bar = ProgressBar()  # instance of ProgressBar created.
        Clock.schedule_once(self.progress_bar_start)

    def progress_bar_start(self, instance):  # Provides initial value of of progress bar and lanches popup
        self.cp.value = 1  # Initial value of progress_bar

    def next(self, dt):  # Updates Project Bar
        # 1500 data points
        if self.cp.value >= 100:  # Checks to see if progress_bar.value has met 100
            self.add_next_button()
            time.sleep(1)
            self.c_cal.text = 'Current Calibration Complete'
            return False  # Returning False schedule is canceled and won't repeat

        # get new value from arduino global
        self.cp.value += 1  # Updates progress_bar's progress

    def add_next_button(self):
        ok_button = CustomizedButton(text='Next', pos_hint={'center_x': 0.75, 'center_y': 0.15},
                           size=(self.ids.layout.width / 2, self.ids.layout.height / 5),
                           size_hint=(None, None)
                           )
        ok_button.bind(on_press=self.clk)
        self.ids.layout.add_widget(ok_button)

    def clk(self, obj):
        popup = CalibrationCompletePopup()
        popup.open()
        return super(CalibrationContractPopup, self).dismiss()
        # self.dismiss()

    def puopen(self):  # Called from bind.
        Clock.schedule_interval(self.next, .0005)  # Creates Clock event scheduling next() every 5-1000th of a second.


class CalibrationCompletePopup(Popup):
    pass


class MissingFieldPopup(Popup):
    pass


# class DropDownMenu(DropDown):
#     pass


class MainScreen(Screen):
    pass


class StartSessionScreen(Screen):
    # TODO Add another popup: Input Arduino Serial Number
    session_date = datetime.date.today().strftime('%m/%d/%y')

    def __init__(self, **kwargs):
        super(StartSessionScreen, self).__init__(**kwargs)
        self.add_sensor_popup = AddSensorPopup()

    def insert(self, sensor_name, sensor_loc, but_mapping):
        self.rv.data.insert(0, {'sensor_name': sensor_name or 'default value',
                                'sensor_loc': sensor_loc or 'default value',
                                'but_mapping': but_mapping or 'default value',
                                'need_calibration': True})

    def clear_text_input(self):
        self.manager.get_screen('session_history').insert(self.ids.session_name_input.text,
                                                          self.ids.session_date_input.text, self.ids.rv.data)
        self.manager.get_screen('running_session').insert(self.ids.session_name_input.text,
                                                          self.ids.session_date_input.text, self.ids.rv.data)

        self.ids.session_name_input.text = ''
        self.ids.rv.data = []
        self.parent.current = 'running_session'


class SessionHistoryScreen(Screen):
    def insert(self, session_name, session_date, rv_data):
        self.rv_progress.data.insert(0, {'session_name': session_name or 'default value',
                                         'session_date': session_date or 'default value',
                                         })
        print("DATA FROM ADDING SENSORS", rv_data)

    def print_log(self):
        print(self.rv_progress.data)


class RunningSessionScreen(Screen):
    session_name = ObjectProperty()
    session_date = ObjectProperty()
    # rv = ObjectProperty()

    # TODO End session saves it to session history
    def __init__(self, **kwargs):
        super(RunningSessionScreen, self).__init__(**kwargs)
        self.session_name = ''
        self.session_date = ''
        # self.rv = []

    def insert(self, session_name, session_date, rv):
        print('session_name: ', session_name)
        print('session_date: ', session_date)
        print('rv_sensors: ', rv)
        self.session_name = session_name
        self.session_date = session_date
        self.rv.data = rv
        # self.rv.data.insert(0, {'session_name': session_name or 'default value',
        #                         'session_date': session_date or 'default value',
        #                         'rv': rv or 'default value'})


class ProgressScreen(Screen):
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
    MyvoateApp().run()
    """
    Gamepad: +/- x; +/- y
    Keyboard: 
    Confirm Arduino when you start session
    """
