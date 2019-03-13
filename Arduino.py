import serial
import warnings
import serial.tools.list_ports
import time
import NewMyovate
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget


class Arduino:
    def __init__(self, **kwargs):
        self.baud_rate = 9600
        self.data_points = 4000
        self.cal_points = 100
        self.arduino = None
        self.cal = {}
        self.ser = None
        self.arduino_ports = None
        self.record = False
        self.neg_electrode = str(1 << 11)
        self.button_info = {}
        self.muscle_info = {}
        self.direction_code = {
            'KEY_LEFT_ARROW': 216,
            'KEY_UP_ARROW': 218,
            'KEY_SPACE_BAR': 32,
            'KEY_DOWN_ARROW': 217,

            'KEY_RIGHT_ARROW': 215,
        }
        self.button_code = {
            'KEY_LEFT_CTRL': 128,
            'KEY_LEFT_SHIFT': 129,
            'KEY_LEFT_ALT': 130,
            'KEY_BACKSPACE': 178,
            'KEY_RIGHT_ALT': 134,
            'KEY_RIGHT_SHIFT': 133,
            'KEY_RIGHT_CTRL': 132,

            'KEY_TAB': 179,
            'KEY_RETURN': 176,
            'KEY_ESC': 177,
            'KEY_INSERT': 209,
            'KEY_DELETE': 212,
            'KEY_PAGE_UP': 211,
            'KEY_PAGE_DOWN': 214,
            'KEY_HOME': 210,
            'KEY_END': 213,
            'KEY_CAPS_LOCK': 193
        }

    def find_arduino(self):
        self.arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()# if 'USB Serial' in p.description
        ]
        print(self.arduino_ports)
        return self.arduino_ports

    def set_arduino(self, ser):
        self.ser = ser
        self.arduino = serial.Serial(self.ser, self.baud_rate, timeout=0.1)

        return True

    def get_data(self):
        data = self.arduino.readline(1)
        while b'\r\n' not in data:
            data = data + self.arduino.readline(1)
        data = self.arduino.readline(1)
        while b'\r\n' not in data:
            data = data + self.arduino.readline(1)
        final_data = data.decode().split(',')
        return final_data

    def remove_electrode(self, channel_num):
        self.button_info.pop(channel_num)
        send = 'py,' + self.neg_electrode + ',' + self.neg_electrode
        send = send.encode()
        self.arduino.write(send)

    def low_calibration(self, channel_num):
        self.record = False
        final_data = []
        count = 0
        while count < self.data_points:
            data = self.get_data()
            final_data.append(int(data[channel_num]))
            count = count + 1
        final_data.sort(reverse=False)
        low_cal = sum(final_data[0:self.cal_points])/self.cal_points
        self.cal[channel_num] = [low_cal]
        self.record = True
        return low_cal

    def high_calibration(self, channel_num):
        self.record = False
        final_data = []
        count = 0
        while count < self.data_points:
            data = self.get_data()
            final_data.append(int(data[channel_num]))
            count = count + 1
        final_data.sort(reverse=True)
        print(final_data[0:self.cal_points])
        high_cal = sum(final_data[0:self.cal_points])/self.cal_points
        self.cal[channel_num].append(high_cal)
        self.record = True
        return high_cal

    def send_button_map(self, channel_num, button):
        code = ''
        if len(button) == 1:
            code = ord(button)
        else:
            try:
                code = self.button_code[button]
            except KeyError:
                code = self.direction_code[button]
        self.button_info[channel_num] = code
        sends = 'py,' + str(channel_num) + "," + str(self.button_info[channel_num])
        print(sends, sends.encode())
        sends = sends.encode()
        self.arduino.write(sends)

    def send_calibration(self, channel_num):
        lo_cal = str(int(self.cal[channel_num][0]))
        hi_cal = str(int(self.cal[channel_num][1]))
        sends = 'py,' + str(int(channel_num)) + "," + lo_cal + "," + hi_cal
        print(sends)
        sends = sends.encode()
        self.arduino.write(sends)

    def map_muscle(self, channel_num, muscle):
        self.muscle_info[channel_num] = muscle

    # def button_map(self, channel_num):
    #     sends = 'py,' + str(channel_num) + "," + str(self.button_info[channel_num])
    #     print(sends, sends.encode())
    #     sends = sends.encode()
    #     self.arduino.write(sends)

    def send_all_cals(self):
        for channel in self.cal:
            time.sleep(2)
            self.send_calibration(channel)

    def test_comm(self):
        self.arduino.write(b'py,1,200')
        print(self.arduino.readline())

# if __name__ == '__main__'a
#     a = Arduino()
#     all_ar = a.find_arduino()
#     if len(all_ar) < 1:
#         print("No Arduino found")
#     else:a
#         if len(all_ar) > 1:
#             print("Multiple Arduino"a
#         a.set_arduino(all_ar[0])
#         #a.test_comm()
#         time.sleep(10)a
#         a.send_button_map(1, 50)
