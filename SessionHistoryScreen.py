from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.gridlayout import GridLayout
import Misc


class SessionHistoryScreen(Screen):
    def insert(self, session_name, session_date, rv_data):
        self.rv_progress.data.insert(0, {'session_name': session_name or 'default value',
                                         'session_date': session_date or 'default value',
                                         })
        print("DATA FROM ADDING SENSORS", rv_data)

    def print_log(self):
        print(self.rv_progress.data)


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