import serial
import warnings
import serial.tools.list_ports
import time


class Arduino():

    def __init__(self):
        self.baud_rate = 9600
        self.data_points = 120
        self.cal_points = 70
        self.arduino = None
        self.cal = {}
        self.ser = None
        self.arduino_ports = None
        self.button_info = {}
        self.button_code = {

            'KEY_DOWN_ARROW': 217,
            'KEY_UP_ARROW':216,
            'KEY_LEFT_ARROW':215,
            'KEY_RIGHT_ARROW':214
        }

    def find_arduino(self):
        self.arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'USB Serial' in p.description
        ]
        return self.arduino_ports

    def set_arduino(self, ser):
        self.ser = ser
        self.arduino = serial.Serial(self.ser, self.baud_rate, timeout=0.1)

    def low_calibration(self, channel_num):
        final_data = []
        while len(final_data) < self.data_points:
            data = self.arduino.readline().split(',')
            final_data.append(int(data[channel_num]))
        final_data.sort()
        low_cal = sum(final_data[0:self.cal_points])/self.cal_points
        self.cal[channel_num] = [low_cal]
        return low_cal

    def high_calibration(self, channel_num):
        final_data = []
        while len(final_data) < self.data_points:
            data = self.arduino.readline().split(',')
            final_data.append(int(data[channel_num]))
        final_data.sort()
        high_cal = sum(final_data[0:self.cal_points])/self.cal_points
        self.cal[channel_num].append(high_cal)
        return high_cal

    def send_calibration(self, channel_num):
        lo_cal = str(self.cal[channel_num][0])
        hi_cal = str(self.cal[channel_num][1])
        sends = 'py,' + str(channel_num) + "," + lo_cal + "," + hi_cal
        sends = sends.encode()
        self.arduino.write(sends)

    def send_button_map(self, channel_num, button):
        self.button_info[channel_num] = button
        sends = 'py,' + str(channel_num) + "," + str(button)
        sends = sends.encode()
        self.arduino.write(sends)

    def test_comm(self):
        self.arduino.write(b'py,1,200')
        print(self.arduino.readline())

if __name__ == '__main__':
    a = Arduino()
    all_ar = a.find_arduino()
    if len(all_ar) < 1:
        print("No Arduino found")
    else:
        if len(all_ar) > 1:
            print("Multiple Arduino")
        a.set_arduino(all_ar[0])
        #a.test_comm()
        time.sleep(10)
        a.send_button_map(1, 50)
