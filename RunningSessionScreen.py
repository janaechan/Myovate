from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import MeshLinePlot
from kivy.clock import Clock
import MicrophoneThread
import Misc


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
        self.plot.points = [(i, j / 5) for i, j in enumerate(MicrophoneThread.levels)]
