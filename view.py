from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp


class MainScreen:

    def __init__(self):
        self.navigationdrawer = NavigationDrawer()

    def build(self):
        side_panel = BoxLayout(orientation='vertical')
        side_panel.add_widget(Label(text='Myovate Menu'))
        #side_panel.add_widget(Button(text='Back'))
        back_button = Button(text='Back')
        callibration_button = Button(text='Callibration')
        back_button.bind(on_press=lambda j: self.navigationdrawer.toggle_state())
        progress_button = Button(text='Progress')
        side_panel.add_widget(back_button)
        side_panel.add_widget(callibration_button)
        side_panel.add_widget(progress_button)
        self.navigationdrawer.add_widget(side_panel)
        self.navigationdrawer.toggle_main_above()
        self.navigationdrawer.toggle_state()
        self.navigationdrawer.anim_type = 'slide_above_simple'

        label_head = (
            'MYOVATE')
        main_panel = BoxLayout(orientation='vertical')
        label_bl = BoxLayout(orientation='horizontal')
        label = Label(text=label_head, font_size='24sp',
                      markup=True, halign='center', valign='top')
        label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
        label_bl.add_widget(label)
        label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
        main_panel.add_widget(Widget(size_hint_y=None, height=dp(10)))
        main_panel.add_widget(label_bl)
        main_panel.add_widget(Widget(size_hint_y=None, height=dp(10)))
        self.navigationdrawer.add_widget(main_panel)


        return self.navigationdrawer



