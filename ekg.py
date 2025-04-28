#!/usr/bin/env python

#Python3 Library
from ADCPi import ADCPi
import tkinter as tk
import time
import mpu6050  # Accelerometer library
from tkinter import *
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

#ADC addresses and setup
adc = ADCPi(0x6A, 0x6B, 12)
adc.set_conversion_mode(1)

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

#GLOBAL VARIABLE
#xAxis
iCounter  = 0

#definition Analog Input Var. 
AI_5VpowerSupply = 0
AI_24VpowerSupply = 0

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()


class pgCharts(Page):
   def __init__(self, *args, **kwargs):

       Page.__init__(self, *args, **kwargs)

       self.fig = Figure(figsize=(5, 4), dpi=100)
       self.fig.patch.set_facecolor('grey')

       self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
       self.canvas.draw()
       self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

       self.toolbar = NavigationToolbar2Tk(self.canvas, self)
       self.toolbar.update()
       self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

       #verilerin kayit edilmesi
       self.tTimer = [] #time Counter
       self.t5V = [] #5V 
       self.t24V = [] #24V

       self.xSide = []
       self.ySide_1 = []
       self.ySide_2 = []


   def fsave_to_Charts(self):
        #saving sensor data
        global iCounter
        global AI_5VpowerSupply
        global AI_24VpowerSupply

        AI_5VpowerSupply = adc.read_voltage(1)
        AI_24VpowerSupply = adc.read_voltage(5)
        # AI_5VpowerSupply = rpi_dig_vol_converter(rpi_readAI(6))
        # AI_24VpowerSupply = rpi_dig_vol_converter(rpi_readAI(7))
        

        iCounter+=1 
        #time
     
      
        self.tTimer.append(iCounter)
        self.t5V.append(AI_5VpowerSupply)
        self.t24V.append(AI_24VpowerSupply)

        for i in range(len(self.tTimer)):

            self.xSide.append(self.tTimer[i])
            self.ySide_1.append(self.t5V[i])
            self.ySide_2.append(self.t24V[i]) # for 24V


        #self.fig.add_subplot(111).plot(self.xSide,self.ySide_1)
        #for 5V and 24V
        self.fig.add_subplot(111).plot(self.xSide,self.ySide_1,self.ySide_2)
     
        
        self.fig.suptitle("5VDC Voltage Real Time Charts")
        self.canvas.draw()
        self.fig.clf()
        #verilerin temizlenmesi
        self.tTimer.clear()
        self.t5V.clear()


#--------------------PGCLOUD-------------------------------------------
#cloud page 
class pgCloud(Page):
   def __init__(self, *args, **kwargs):

       Page.__init__(self, *args, **kwargs)

       self.fig = Figure(figsize=(5, 4), dpi=100)
       self.fig.patch.set_facecolor('blue')

       self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
       self.canvas.draw()
       self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

       self.toolbar = NavigationToolbar2Tk(self.canvas, self)
       self.toolbar.update()
       self.canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

       #verilerin kayit edilmesi
       self.tTimer = [] #time Counter
       self.t5V = [] #5V 
       self.t24V = [] #24V

       self.xSide = []
       self.ySide_1 = []
       self.ySide_2 = []

   def fsave_to_Charts(self):
        #saving sensor data
        global iCounter
        global AI_5VpowerSupply
        global AI_24VpowerSupply

        AI_5VpowerSupply = adc.read_voltage(1)
        AI_24VpowerSupply = adc.read_voltage(5)
        # AI_5VpowerSupply = rpi_dig_vol_converter(rpi_readAI(6))
        # AI_24VpowerSupply = rpi_dig_vol_converter(rpi_readAI(7))
        

        iCounter+=1 
        #time
    
        self.tTimer.append(iCounter)
        self.t5V.append(AI_5VpowerSupply)
        self.t24V.append(AI_24VpowerSupply)


        for i in range(len(self.tTimer)):

            self.xSide.append(self.tTimer[i])
            self.ySide_1.append(self.t5V[i])
            self.ySide_2.append(self.t24V[i]) # for 24V

        #self.fig.add_subplot(111).plot(self.xSide,self.ySide_1)
        #for 5V and 24V
        self.fig.add_subplot(111).plot(self.xSide,self.ySide_1,self.ySide_2)
     
        
        self.fig.suptitle("5VDC Voltage Real Time Charts")
        self.canvas.draw()
        self.fig.clf()
        #verilerin temizlenmesi
        self.tTimer.clear()
        self.t5V.clear()
#------------------------END OF PGCLOUD-------------------------------------------

#-------------------------MAINVIEW--------------------------------------
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)


        self.pCharts = pgCharts(self)

        #------------Addition: new pCloud frame-----------------
        self.pCloud = pgCloud(self)
        #-------------------------------------------------------
        
       # self.pCloud = pgCloud(self)

    
        buttonframe = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        #placing charts page
        self.pCharts.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.pCloud.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


        #charts button
        self.charts = Image.open("./pics/charts.png")
        self.photoImg_charts = ImageTk.PhotoImage(self.charts)
        buttonCharts = tk.Button(buttonframe, image=self.photoImg_charts,
        text="optional text" ,command=self.pCharts.lift)

        
        #cloud button
        self.cloud = Image.open("./pics/help.png")
        self.photoImg_cloud = ImageTk.PhotoImage(self.cloud)
        buttonCloud = tk.Button(buttonframe, image=self.photoImg_cloud,
        text="optional text" ,command=self.pCloud.lift)


        buttonCharts.pack(side="left", fill="both", expand=True)
        buttonCloud.pack(side = "left",fill = "both",expand = True)

        self.pCharts.show()
        #self.pCloud.show()
        self.fEmbeddedCall()

 
    def fEmbeddedCall(self):

        #anlık grafiklerin gosterilmesi
        self.pCharts.fsave_to_Charts()
        self.pCloud.fsave_to_Charts()
        self.after(1000,self.fEmbeddedCall)
#------------------END OF MAINVIEW--------------------------------------


# Define a function to read the Accelerometer data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()

    # Read temp
    temperature = mpu6050.get_temp()

    return accelerometer_data, gyroscope_data, temperature

'''
# Start a while loop to continuously read the sensor data
while True:

    # Read the sensor data
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()

    # Print the sensor data
    print("Accelerometer data:", accelerometer_data)
    print("Gyroscope data:", gyroscope_data)
    print("Temp:", temperature)

    # Wait for 1 second
    time.sleep(1)
'''
    
#--------------MAIN FUNCTION-------------------
if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x400")
    #root.attributes("-fullscreen",True)
    root.mainloop()
#-----------------END OF MAIN FUNCTION-------------------
