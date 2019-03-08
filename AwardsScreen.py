from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
import Misc
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


class AwardsScreen(Screen):

    def __init__(self, **kwargs):
        super(AwardsScreen, self).__init__(**kwargs)

    def insert(self, award_source, award_name):
        self.rv.data.insert(0, {'award_source': award_source,
                                'award_name': award_name})


class Award(RecycleDataViewBehavior, BoxLayout):
    rv_data = ObjectProperty(None)
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    index = None

    def __init__(self, **kwargs):
        super(Award, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.rv_data = rv.data
        return super(Award, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(Award, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.rv_data = rv.data
        self.index = index


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class AwardPopup(Popup):
    pass


class AwardApp(App):

    def build(self):
        return Builder.load_file('AwardsScreen.kv')


if __name__ == '__main__':
    Window.fullscreen = 'auto'
    award = AwardApp()
    award.run()

