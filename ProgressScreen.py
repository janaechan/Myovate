
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import MeshLinePlot


class ProgressScreen(Screen):
    def __init__(self, **kwargs):
        super(ProgressScreen, self).__init__(**kwargs)
        self.session_date = ''
        self.arduino = None

    def info(self, session_date):
        self.session_date = session_date
        self.arduino = self.manager.get_screen('start_session').arduino
        for channel in self.arduino.muscle_info:
            self.rv.data.insert(0, {'sensor_loc': self.arduino.muscle_info[channel],
                                    'sensor_date': self.session_date,
                                    'data_points': self.arduino.cal[channel][1]
                                    })
            #self.rv.data[0].add_plot()


class ProgressScreenRow(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv_data = ObjectProperty(None)
    rv = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ProgressScreenRow, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        #self.ids.graph.add_plot(self.plot)
        #self.plot.points(self.sensor_date, self.data_points)
        return super(ProgressScreenRow, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(ProgressScreenRow, self).on_touch_down(touch):
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

    def add_plot(self):
        self.ids.graph.add_plot(self.plot)
        self.plot.points(self.sensor_date, self.data_points)
