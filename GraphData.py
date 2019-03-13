from kivy.lang import Builder
Builder.load_string('''
<MyThread>:
    Button:
        text: "use thread"
        on_release: root.run_thread()
    Button:
        text: "check values"
        on_release: root.read_it()
    Label:
        id: lbl
        text: "Numbers"
''')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
import threading
import random
import time

import serial  # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt  # import matplotlib library
from drawnow import *


class MyThread(BoxLayout):
    i = NumericProperty(0)

    tempF = []
    pressure = []
    arduinoData = serial.Serial('/dev/cu.usbmodemHIDPC1', 9600)  # Creating our serial object named arduinoData
    plt.ion()  # Tell matplotlib you want interactive mode to plot live data

    def makeFig(self):  # Create a function that makes our desired plot
        plt.ylim(0, 90)  # Set y min and max values
        plt.title('My Live Streaming Sensor Data')  # Plot the title
        plt.grid(True)  # Turn the grid on
        plt.ylabel('Temp F')  # Set ylabels
        plt.plot(self.tempF, 'ro-', label='Degrees F')  # plot the temperature
        plt.legend(loc='upper left')  # plot the legend
        plt2 = plt.twinx()  # Create a second y axis
        plt.ylim(0, 70)  # Set limits of second y axis- adjust to readings you are getting
        plt2.plot(self.pressure, 'b^-', label='Pressure (Pa)')  # plot pressure data
        plt2.set_ylabel('Pressrue (Pa)')  # label second y axis
        plt2.ticklabel_format(useOffset=False)  # Force matplotlib to NOT autoscale y axis
        plt2.legend(loc='upper right')  # plot the legend

    def get_data_test(self):
        cnt = 0
        while True:  # While loop that loops forever
            while (self.arduinoData.inWaiting() == 0):  # Wait here until there is data
                pass  # do nothing
            arduinoString = self.arduinoData.readline()  # read the line of text from the serial port
            arduinoString = arduinoString.decode()
            dataArray = arduinoString.split(',')  # Split it into an array called dataArray
            temp = int(dataArray[0])  # Convert first element to floating number and put in temp
            P = int(dataArray[0])  # Convert second element to floating number and put in P
            print(dataArray)
            self.tempF.append(temp)  # Build our tempF array by appending temp readings
            self.pressure.append(P)  # Building our pressure array by appending P readings
            drawnow(self.makeFig)  # Call drawnow to update our live graph
            plt.pause(.000001)  # Pause Briefly. Important to keep drawnow from crashing
            cnt = cnt + 1
            if (cnt > 50):  # If you have 50 or more points, delete the first one from the array
                self.tempF.pop(0)  # This allows us to just see the last 50 data points
                self.pressure.pop(0)

    def main_loop(self):
        while True:
            self.ids.lbl.text = "{}".format(self.i)
            print(self.i)
            self.i += 1
            time.sleep(random.randint(0,3))
            if self.i == 7:
                self.i = 0

    def run_thread(self):
        threading.Thread(target = self.get_data_test).start()

    def read_it(self):
        print ('started')
        if self.i == 2:
            print("Counter start")
        if self.i == 5:
            print("Counter stop")

class MyApp(App):
    def build(self):
        return MyThread()
MyApp().run()
