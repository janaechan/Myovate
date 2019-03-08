from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, BooleanProperty
import datetime
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.garden.graph import MeshLinePlot
import CalibrationModule


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
        return CalibrationModule.CalibrationSetupPopup().open()

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
