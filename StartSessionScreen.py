from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty, StringProperty
import datetime
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from threading import Thread
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
import time
from kivy.clock import Clock
from kivy.garden.graph import MeshLinePlot
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
import CalibrationModule
import MicrophoneThread
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
import CalibrationModule
import audioop
import GraphThread
import Arduino
from kivy.factory import Factory
from multiprocessing import Process
import Misc


class AddArduinoPopup(Misc.CustomizedPopup):

    def __init__(self, arduino=None, **kwargs):
        self.arduino = arduino
        super(AddArduinoPopup, self).__init__(**kwargs)

    def find_arduino_result(self):
        ops = self.arduino.find_arduino()
        if len(ops) == 0:
            NoArduinoFoundPopup(self.arduino).open()
        else:
            self.dismiss()
            ArduinoOptionsPopup(self.arduino, ops).open()


class NoArduinoFoundPopup(Misc.CustomizedPopup):
    def __init__(self, arduino=None, **kwargs):
        self.arduino = arduino
        super(NoArduinoFoundPopup, self).__init__(**kwargs)


class ArduinoConnectedPopup(Misc.CustomizedPopup):
    pass


class ArduinoUnsuccessfulPopup(Misc.CustomizedPopup):

    def __init__(self, arduino=None, arduino_ops=None, **kwargs):
        self.arduino = arduino
        self.arduino_ops = arduino_ops
        super(ArduinoUnsuccessfulPopup, self).__init__(**kwargs)


class ArduinoOptionsPopup(Misc.CustomizedPopup):

    def __init__(self, arduino=None, arduino_ops=None, **kwargs):
        self.arduino = arduino
        self.arduino_ops = arduino_ops
        super(ArduinoOptionsPopup, self).__init__(**kwargs)
        self.add_arduinos()

    def add_arduinos(self):
        for a in range(len(self.arduino_ops)):
            if a == 0:
                but = ToggleButton(text=self.arduino_ops[a], group='arduino_buts', state='down', pos_hint={'center_x': 0.5})
            else:
                but = ToggleButton(text=self.arduino_ops[a], group='arduino_buts', pos_hint={'center_x': 0.5})
            self.arduinos.add_widget(but)

    def update_arduino(self):
        buts = ToggleButtonBehavior.get_widgets('arduino_buts')
        a_id = ''
        for b in buts:
            if b.state == 'down':
                a_id = b.text
                print(b.text)
        self.dismiss()

        if self.arduino.set_arduino(a_id):
            ArduinoConnectedPopup().open()
        else:
            ArduinoUnsuccessfulPopup(self.arduino, self.arduino_ops).open()


class StartSessionScreen(Screen):
    # TODO Add another popup: Input Arduino Serial Number
    session_date = datetime.date.today().strftime('%m/%d/%y')

    def __init__(self, **kwargs):
        self.arduino = Arduino.Arduino()
        #GraphThread.init_arduino(self.arduino)
        self.get_graph_thread = None
        super(StartSessionScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.get_num_channels)
        self.add_sensor_popup = AddSensorPopup(None, self.arduino)

    def on_enter(self, *args):
        if len(self.rv.data) == 0:
            AddArduinoPopup(self.arduino).open()

    def insert(self, sensor_loc, but_mapping, channel_num):
        if 'KEY_' in but_mapping:
            but_mapping = ' '.join(but_mapping.split('_')[1:])
        self.rv.data.insert(0, {'sensor_loc': sensor_loc or 'default value',
                                'but_mapping': but_mapping or 'default value',
                                'channel_num': channel_num})

    # def insert(self, sensor_name, sensor_loc, but_mapping, channel_num):
    #     if 'KEY_' in but_mapping:
    #         but_mapping = ' '.join(but_mapping.split('_')[1:])
    #     self.rv.data.insert(0, {'sensor_name': sensor_name or 'default value',
    #                             'sensor_loc': sensor_loc or 'default value',
    #                             'but_mapping': but_mapping or 'default value',
    #                             'channel_num': channel_num})

    def clear_text_input(self):
        self.manager.get_screen('running_session').insert(self.ids.session_name_input.text,
                                                          self.ids.session_date_input.text, self.ids.rv.data)
        self.manager.get_screen('progress').info(self.ids.session_date_input.text)
        self.ids.session_name_input.text = ''
        self.ids.rv.data = []
        self.parent.current = 'running_session'
        SendingToArduinoPopup(self.arduino).open()

    # def start_graph_thread(self):
    #     print("START GRAPH THREAD")
    #     get_arduino_thread = Thread(target=GraphThread.get_data_test)
    #     # get_arduino_thread.daemon = True
    #     get_arduino_thread.start()
    #     process = Process(target=GraphThread.get_data_test)
    #     process.start()
    #     # GraphThread.get_data_test()
    #     # GraphThread.init_arduino(self.arduino)
    #     # self.get_graph_thread = Thread(target=GraphThread.get_data_test())
    #     # self.get_graph_thread.daemon = True
    #     # self.get_graph_thread.start()

    def get_num_channels(self, dt):
        try:
            self.add_sensor_popup.ids.channel_num_input.hint_text = \
                'Enter value between 0 and {}'.format(len(self.arduino.get_data()))
        except AttributeError:
            self.add_sensor_popup.ids.channel_num_input.hint_text = 'Enter value between 0 - 5'


class StartSessionRow(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv_data = ObjectProperty(None)
    rv = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(StartSessionRow, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.levels = []  # store levels of microphone

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(StartSessionRow, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(StartSessionRow, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.rv = rv
        self.rv_data = rv.data
        self.index = index
        self.selected = is_selected

    def remove(self):
        if self.rv:
            self.rv.data.pop(self.index)

    def start(self):
        #GraphThread.get_data()
        #self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        pass
        #GraphThread.get_data()
        #self.plot.points = [(i, j / 5) for i, j in GraphThread.graph_data]


class AddSensorPopup(Popup):
    container = ObjectProperty(None)
    rv_data = ObjectProperty()
    rv = ObjectProperty()
    index = 0
    date = datetime.date.today().strftime('%m/%d/%y')
    but_mapping = StringProperty()

    def __init__(self, sensor_data=None, arduino=None, **kwargs):
        if sensor_data is not None:
            self.rv_data = sensor_data.rv_data
            self.index = sensor_data.index
        self.arduino = arduino
        Clock.schedule_once(self.make_keyboard)
        super(AddSensorPopup, self).__init__(**kwargs)

    def clear_text_input(self):
        self.arduino.send_button_map(int(self.ids.channel_num_input.text), self.but_mapping)
        self.arduino.map_muscle(int(self.ids.channel_num_input.text), self.ids.sensor_loc_input.text)
        CalibrationModule.CalibrationSetupPopup(self.arduino, int(self.ids.channel_num_input.text)).open()
        self.ids.channel_num_input.text = ''
        # self.ids.sensor_name_input.text = ''
        self.ids.sensor_loc_input.text = ''
        self.ids.but_mapping_input.text = ''
        keys = ToggleButtonBehavior.get_widgets('keys')
        for but in keys:
            but.state = 'normal'
        self.dismiss()

    def cancel_adding_sensor(self):
        self.ids.channel_num_input.text = ''
        # self.ids.sensor_name_input.text = ''
        self.ids.sensor_loc_input.text = ''
        self.ids.but_mapping_input.text = ''
        keys = ToggleButtonBehavior.get_widgets('keys')
        for but in keys:
            but.state = 'normal'
        self.dismiss()

    def check_for_missing_fields(self):
        # if not self.ids.channel_num_input.text or not self.ids.sensor_name_input.text or not self.ids.sensor_loc_input.text:
        #     return False

        if not self.ids.channel_num_input.text or not self.ids.sensor_loc_input.text:
            return False

        has_but = False
        keys = ToggleButtonBehavior.get_widgets('keys')
        for but in keys:
            if but.state == 'down':
                has_but = True
        if self.ids.but_mapping_input.text and not has_but:
            return self.ids.but_mapping_input.text
        if not self.ids.but_mapping_input.text and has_but:
            return has_but

    def check_channel(self):
        if self.ids.channel_num_input.text in self.arduino.button_info:
            return False
        return True

    def reset_state(self):
        keys = ToggleButtonBehavior.get_widgets('keys')
        for but in keys:
            but.state = 'normal'

    def make_keyboard(self, dt):
        box1 = BoxLayout(orientation='horizontal')
        box2 = BoxLayout(orientation='horizontal')
        box3 = BoxLayout(orientation='horizontal')
        count = 0
        for i, j in self.arduino.button_code.items():
            if count < 7:
                box1.add_widget(ToggleKeys(text=' '.join(i.split('_')[1:]), group='keys', font_size='13sp', id=i))
            else:
                box2.add_widget(ToggleKeys(text=' '.join(i.split('_')[1:]), group='keys', font_size='13sp', id=i))
            count += 1
        for i, j in self.arduino.direction_code.items():
            box3.add_widget(ToggleKeys(text=' '.join(i.split('_')[1:]), group='keys', font_size='13sp', id=i))
        self.container.add_widget(box1)
        self.container.add_widget(box2)
        self.container.add_widget(box3)


class ButtonMapping(TextInput):
    def insert_text(self, substring, from_undo=False):
        substring = substring[:1 - len(self.text)]
        add_sensor_popup = self.parent.parent.parent.parent
        add_sensor_popup.reset_state()
        add_sensor_popup.but_mapping = substring
        print(add_sensor_popup.but_mapping)
        return super(ButtonMapping, self).insert_text(substring, from_undo=from_undo)


class ToggleKeys(ToggleButton):
    def on_state(self, widget, value):
        # clear any text ins but_mapping TextInput
        if value == 'down':
            try:
                add_sensor_popup = self.parent.parent.parent.parent
                add_sensor_popup.ids.but_mapping_input.text = ''
            except AttributeError:
                add_sensor_popup = widget.parent.parent.parent.parent.parent.parent
                add_sensor_popup.ids.but_mapping_input.text = ''
            add_sensor_popup.but_mapping = widget.id


class ConfirmDeletePopup(Misc.CustomizedPopup):

    def __init__(self, rv=None, sensor_data=None, arduino=None, **kwargs):
        self.rv = rv
        print(sensor_data)
        print(sensor_data.rv.data)
        print(sensor_data.rv_data)
        self.rv_data = sensor_data.rv_data
        self.index = sensor_data.index
        self.arduino = arduino
        super(ConfirmDeletePopup, self).__init__(**kwargs)

    def remove(self):
        print('update remove status')
        self.arduino.remove_electrode(self.rv.data[self.index]['channel_num'])
        self.rv.data.pop(self.index)


class MissingFieldPopup(Misc.CustomizedPopup):
    pass


class ChannelUsedPopup(Misc.CustomizedPopup):
    pass


class SendingToArduinoPopup(Misc.CustomizedPopup):
    progress_bar = ObjectProperty()
    cp = ObjectProperty()

    def __init__(self, arduino=None, **kwargs):
        self.arduino = arduino
        super(SendingToArduinoPopup, self).__init__(**kwargs)
        self.progress_bar = ProgressBar()  # instance of ProgressBar created.
        Clock.schedule_once(self.progress_bar_start)
        self.arduino.send_all_cals()

    def progress_bar_start(self, instance):  # Provides initial value of of progress bar and lanches popup
        self.cp.value = 1  # Initial value of progress_bar

    def next(self, dt):  # Updates Project Bar
        # 1500 data points
        if self.cp.value >= 100:  # Checks to see if progress_bar.value has met 100
            self.add_next_button()
            time.sleep(1)
            self.info.text = 'All information sent! Please proceed to play games.'
            return False  # Returning False schedule is canceled and won't repeat

        # get new value from arduino global
        self.cp.value += 1  # Updates progress_bar's progress

    def add_next_button(self):
        ok_button = Button(text='Next', pos_hint={'center_x': 0.5, 'center_y': 0.10},
                           size=(self.ids.layout.width, self.ids.layout.height / 5),
                           size_hint=(None, None), font_size='20sp')
        ok_button.bind(on_press=self.clk)
        self.ids.layout.add_widget(ok_button)

    def clk(self, obj):

        self.dismiss()

    def puopen(self):  # Called from bind.
        Clock.schedule_interval(self.next, .0005)  # Creates Clock event scheduling next() every 5-1000th of a second.


