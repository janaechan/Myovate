from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout


class CalibrationView:

    def __init__(self):
        sensor_list = ObjectProperty()


    def build(self):
        layout_main = FloatLayout()
        calibration_title = 'Calibration'
        add_sensor_button = Button(text='Add Sensor', font_size='30sp')
