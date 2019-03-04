import serial
import warnings
import serial.tools.list_ports

class Arduino():

    def __init__(self):
        self.baud_rate = 9600
        self.data_points = 120
        self.cal_points = 70
        self.arduino = None
        self.cal = {}
        self.ser = None
        self.arduino_ports = None

    def find_arduino(self):
        self.arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description
        ]
        return self.arduino_ports

    def set_arduino(self, ser):
        self.ser = ser
        self.arduino = serial.Serial(self.ser, self.baud_rate, timeout=0.1)

    def low_calibration(self, channel_num):
        final_data = []
        while len(final_data) < self.data_points:
            data = self.arduino.readline().split(',')
            final_data.append(data[channel_num])
        final_data.sort()
        low_cal = sum(final_data[0:self.cal_points])/self.cal_points
        self.cal[channel_num] = [low_cal]
        return low_cal

    def high_calibration(self, channel_num):
        final_data = []
        while len(final_data) < self.data_points:
            data = self.arduino.readline().split(',')
            final_data.append(data[channel_num])
        final_data.sort()
        high_cal = sum(final_data[0:self.cal_points])/self.cal_points
        self.cal[channel_num].append(high_cal)
        self.arduino.write(str(channel_num) + "," + str(self.cal[channel_num[0]]) + "," + str(high_cal))
        return high_cal

    def test_comm(self):
        self.arduino.write('4')
        print(self.arduino.readline())

    if __name__ == '__main__':
        all_ar = find_arduino()
        if (len(all_ar) < 1):
            print("No Arduino found")
        else:
            if (len(all_ar) > 1):
                print("Multiple Arduino")
            set_arduino(all_ar[0])
            test_comm()