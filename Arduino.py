import serial


class Arduino():

    def __init__(self):
        self.baud_rate = 0
        self.serial_object = ""
        self.data_points = 120
        self.cal_points = 70
        self.arduino = None
        self.cal = {}

    def set_arduino(self, serial_id, baud_rate):
        self.serial_object = serial_id
        self.baud_rate = baud_rate
        self.arduino = serial.Serial(self.serial_object, self.baud_rate, timeout=0.1)

    def low_calibration(self, channel_num):
        final_data = []
        while len(final_data) < self.data_points:
            data = self.arduino.readline()
            final_data.append(data[channel_num])
        final_data.sort()
        low_cal = sum(final_data[0:self.cal_points])/self.cal_points
        self.cal[channel_num] = [low_cal]
        return low_cal

    def high_calibration(self, channel_num):
        final_data = []
        while len(final_data) < self.data_points:
            data = self.arduino.readline()
            final_data.append(data[channel_num])
        final_data.sort()
        high_cal = sum(final_data[0:self.cal_points])/self.cal_points
        self.cal[channel_num].append(high_cal)
        self.arduino.write(str(channel_num) + "," + str(self.cal[channel_num[0]]) + "," + str(high_cal))
        return high_cal

