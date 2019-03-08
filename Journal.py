from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
import datetime
from kivy.properties import ObjectProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.lang.builder import Builder
import time


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class JournalEntry(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv_data = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(JournalEntry, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.rv_data = rv.data
        return super(JournalEntry, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(JournalEntry, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.rv_data = rv.data
        self.index = index


class AddJournalPopup(Popup):
    rv_data = ObjectProperty()
    index = 0
    date = datetime.date.today().strftime('%m/%d/%y')

    def __init__(self, j_data=None, **kwargs):
        if j_data is not None:
            self.rv_data = j_data.rv_data
            self.index = j_data.index
            print(j_data.rv_data)
        super(AddJournalPopup, self).__init__(**kwargs)


class ViewJournalPopup(Popup):
    rv_data = ObjectProperty()
    index = 0

    def __init__(self, j_data=None, **kwargs):
        if j_data is not None:
            self.rv_data = j_data.rv_data
            self.index = j_data.index
        super(ViewJournalPopup, self).__init__(**kwargs)


class EditJournalPopup(Popup):
    def __init__(self, j_data=None, **kwargs):
        if j_data is not None:
            self.rv_data = j_data.rv_data
            self.index = j_data.index
        super(EditJournalPopup, self).__init__(**kwargs)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


class JournalScreen(Screen):
    def __init__(self, **kwargs):
        super(JournalScreen, self).__init__(**kwargs)

    def insert(self, j_date, j_title, j_text):
        self.rv.data.insert(0, {'journal_date': j_date or 'default value',
                                'journal_title': j_title or 'default value',
                                'journal_text': j_text or 'default value'})

    def set(self, j_date, j_title, j_text, index):
        self.rv.data[index] = {'journal_date': j_date or 'default value',
                                'journal_title': j_title or 'default value',
                                'journal_text': j_text or 'default value'}


class JournalApp(App):
    pass


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    JournalApp().run()