from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import time
import Misc
from kivy.lang import Builder


class CalibrationSetupPopup(Popup):
    pass


class CalibrationRelaxPopup(Popup):
    progress_bar = ObjectProperty()
    cp = ObjectProperty()

    def __init__(self, **kwargs):
        super(CalibrationRelaxPopup, self).__init__(**kwargs)
        self.progress_bar = ProgressBar()  # instance of ProgressBar created.
        Clock.schedule_once(self.progress_bar_start)

    def progress_bar_start(self, instance):  # Provides initial value of of progress bar and lanches popup

        self.cp.value = 1  # Initial value of progress_bar

    def next(self, dt):  # Updates Project Bar
        # 1500 data points
        if self.cp.value >= 100:  # Checks to see if progress_bar.value has met 100
            self.add_next_button()
            time.sleep(1)
            self.r_cal.text = 'Current Calibration Complete'
            return False  # Returning False schedule is canceled and won't repeat

        # get new value from arduino global
        self.cp.value += 1  # Updates progress_bar's progress

    def add_next_button(self):
        ok_button = Misc.CustomizedButton(text='Next', pos_hint={'center_x': 0.75, 'center_y': 0.15},
                           size=(self.ids.layout.width / 2, self.ids.layout.height / 5),
                           size_hint=(None, None)
                           )
        ok_button.bind(on_press=self.clk)
        self.ids.layout.add_widget(ok_button)

    def clk(self, obj):
        popup = CalibrationContractPopup()
        popup.open()
        return super(CalibrationRelaxPopup, self).dismiss()
        # self.dismiss()

    def puopen(self):  # Called from bind.
        Clock.schedule_interval(self.next, .0005)  # Creates Clock event scheduling next() every 5-1000th of a second.


class CalibrationContractPopup(Popup):
    progress_bar = ObjectProperty()
    cp = ObjectProperty()

    def __init__(self, **kwargs):
        super(CalibrationContractPopup, self).__init__(**kwargs)
        self.progress_bar = ProgressBar()  # instance of ProgressBar created.
        Clock.schedule_once(self.progress_bar_start)

    def progress_bar_start(self, instance):  # Provides initial value of of progress bar and lanches popup
        self.cp.value = 1  # Initial value of progress_bar

    def next(self, dt):  # Updates Project Bar
        # 1500 data points
        if self.cp.value >= 100:  # Checks to see if progress_bar.value has met 100
            self.add_next_button()
            time.sleep(1)
            self.c_cal.text = 'Current Calibration Complete'
            return False  # Returning False schedule is canceled and won't repeat

        # get new value from arduino global
        self.cp.value += 1  # Updates progress_bar's progress

    def add_next_button(self):
        ok_button = Misc.CustomizedButton(text='Next', pos_hint={'center_x': 0.75, 'center_y': 0.15},
                           size=(self.ids.layout.width / 2, self.ids.layout.height / 5),
                           size_hint=(None, None)
                           )
        ok_button.bind(on_press=self.clk)
        self.ids.layout.add_widget(ok_button)

    def clk(self, obj):
        popup = CalibrationCompletePopup()
        popup.open()
        return super(CalibrationContractPopup, self).dismiss()
        # self.dismiss()

    def puopen(self):  # Called from bind.
        Clock.schedule_interval(self.next, .0005)  # Creates Clock event scheduling next() every 5-1000th of a second.


class CalibrationCompletePopup(Popup):
    pass
