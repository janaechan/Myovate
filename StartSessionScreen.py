from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty
import datetime
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.garden.graph import MeshLinePlot
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
import CalibrationModule
import MicrophoneThread
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.label import Label
import CalibrationModule
import audioop
import pyaudio
import Arduino
from kivy.factory import Factory


class AddArduinoPopup(Popup):

    def __init__(self, arduino=None, **kwargs):
        self.arduino = arduino
        super(AddArduinoPopup, self).__init__(**kwargs)

    def find_arduino_result(self):
        ops = self.arduino.find_arduino()
        if len(ops) == 0:
            NoArduinoFoundPopup().open()
        else:
            self.add_arduino_popup.dismiss()
            ArduinoOptionsPopup(self.arduino, ops).open()


class NoArduinoFoundPopup(Popup):
    pass


class ArduinoConnectedPopup(Popup):
    pass


class ArduinoUnsuccessfulPopup(Popup):

    def __init__(self, arduino=None, arduino_ops=None, **kwargs):
        self.arduino = arduino
        self.arduino_ops = arduino_ops
        super(ArduinoUnsuccessfulPopup, self).__init__(**kwargs)


class ArduinoOptionsPopup(Popup):

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
        super(StartSessionScreen, self).__init__(**kwargs)
        self.add_sensor_popup = AddSensorPopup()
        Clock.schedule_once(self.get_num_channels)

    def on_enter(self, *args):
        AddArduinoPopup(self.arduino).open()

    def insert(self, sensor_name, sensor_loc, but_mapping, channel_num):
        self.rv.data.insert(0, {'sensor_name': sensor_name or 'default value',
                                'sensor_loc': sensor_loc or 'default value',
                                'but_mapping': but_mapping or 'default value',
                                'channel_num': channel_num})

    def clear_text_input(self):
        self.manager.get_screen('running_session').insert(self.ids.session_name_input.text,
                                                          self.ids.session_date_input.text, self.ids.rv.data)

        self.ids.session_name_input.text = ''
        self.ids.rv.data = []
        self.parent.current = 'running_session'

    def get_num_channels(self, dt):
        try:
            self.add_sensor_popup.ids.channel_num_input.hint_text = 'Enter value between 1 and {}'.format(
                len(self.arduino.get_data()))
        except AttributeError:
            self.add_sensor_popup.ids.channel_num_input.hint_text = 'Enter value between 1 and {}'.format(10)


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
        # self.levels = []  # store levels of microphone

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
        print(self.index)

    def remove(self):
        if self.rv:
            self.rv.data.pop(self.index)

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plot.points = [(i, j / 5) for i, j in enumerate(MicrophoneThread.levels)]


class AddSensorPopup(Popup):
    rv_data = ObjectProperty()
    txt_input = ObjectProperty()
    rv = ObjectProperty()
    index = 0
    date = datetime.date.today().strftime('%m/%d/%y')

    def __init__(self, sensor_data=None, **kwargs):
        if sensor_data is not None:
            self.rv_data = sensor_data.rv_data
            self.index = sensor_data.index
            print(sensor_data.rv_data)
        super(AddSensorPopup, self).__init__(**kwargs)

    def clear_text_input(self):
        print('clear_text_input')
        print(self.ids.channel_num_input.text)
        self.ids.channel_num_input.text = ''
        self.ids.sensor_name_input.text = ''
        self.ids.sensor_loc_input.text = ''
        self.ids.but_mapping_input.text = ''
        self.dismiss()

        return CalibrationModule.CalibrationSetupPopup().open()

    def cancel_adding_sensor(self):
        self.ids.channel_num_input.text = ''
        self.ids.sensor_name_input.text = ''
        self.ids.sensor_loc_input.text = ''
        self.ids.but_mapping_input.text = ''
        self.dismiss()

    def check_for_missing_fields(self):
        if not self.ids.channel_num_input.text or not self.ids.sensor_name_input.text or not self.ids.sensor_loc_input.text:
            return False

        has_but = False
        arrow_but = ToggleButtonBehavior.get_widgets('arrows')
        for but in arrow_but:
            if but.state == 'down':
                has_but = True
        if self.ids.but_mapping_input.text and not has_but:
            return self.ids.but_mapping_input.text
        if not self.ids.but_mapping_input.text and has_but:
            return has_but

    def reset_state(self):
        arrow_but = ToggleButtonBehavior.get_widgets('arrows')
        for but in arrow_but:
            but.state = 'normal'


class ButtonMapping(TextInput):
    def insert_text(self, substring, from_undo=False):
        substring = substring[:1 - len(self.text)]
        self.parent.parent.parent.parent.reset_state()
        return super(ButtonMapping, self).insert_text(substring, from_undo=from_undo)


class ToggleArrow(ToggleButton):

    def on_state(self, widget, value):
        # clear any text in but_mapping TextInput
        if value == 'down':
            add_sensor_popup = self.parent.parent.parent.parent
            add_sensor_popup.ids.but_mapping_input.text = ''


class ConfirmDeletePopup(Popup):
    remove_status = BooleanProperty(False)

    def __init__(self, root, **kwargs):
        super(ConfirmDeletePopup, self).__init__(**kwargs)
        self.root = root

    def remove(self):
        print('update remove status')
        self.remove_status = True
        self.root.remove()


class MissingFieldPopup(Popup):
    pass
