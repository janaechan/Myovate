from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.base import runTouchApp

from kivy.clock import Clock

import CircularProgressBar

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty

Builder.load_string('''
<SensorScreen>:
    AnchorLayout:
        anchor_x:'center'
        anchor_y:'center'
        
        BoxLayout:
            orientation:'vertical'
            Label:
                text:"Step 1: Place the red sensor on the targeted muscle"

            Label:
                text:"Step 2: Place the black sensor on a nearby bone"
            
    AnchorLayout:
        anchor_x:'right'
        anchor_y:'bottom'

        Button:
            text:'Next'
            on_press: root.manager.current = 'relax'
            size:100, 75
            size_hint: None, None


<RelaxScreen>:
    AnchorLayout:
        anchor_x:'right'
        anchor_y:'bottom'

        Button:
            text:'Next'
            on_press: root.manager.current = 'contract'
            size: 200, 150
            size_hint: None, None
            
    CircularProgressBar:
        id: cp
        size_hint:(None, None)
        height:200
        width:800
        max:80

<ContractScreen>:
    FloatLayout:
        AnchorLayout:
            anchor_x:'center'
            anchor_y:'top'

            Label:
                text:"Contract targeted muscle as much as possible and wait until the progress is finished"

        AnchorLayout:
            anchor_x:"center"
            anchor_y:"center"

            CircularProgressBar:
                id: cp
                size_hint:(None,None)
                height:400
                width:400
                max:80

        AnchorLayout:
            anchor_x:'right'
            anchor_y:'bottom'

            Button:
                text:'Next'
                on_press: root.manager.current = 'contract'
                size:100, 75
                size_hint: None, None
''')


class SensorScreen(Screen):
    pass


class RelaxScreen(Screen):
    pass


class ContractScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(SensorScreen(name='sensor'))
sm.add_widget(RelaxScreen(name='relax'))
sm.add_widget(ContractScreen(name='contract'))


class CalibrationModule(App):

    # def animate(self, dt):
    #     relaxProgress = self.root.get_screen('relax').ids.cp
    #     contractProgress = self.root.get_screen('contract').ids.cp
    #     if relaxProgress.value<80:
    #         relaxProgress.set_value(relaxProgress.value + 1)
    #     else:
    #         relaxProgress.set_value(0)

    def build(self):
        #Clock.schedule_interval(self.animate, 0.1)
        return sm
