import sys
import time
import ftd2xx as ftd
from tkinter import *
import tkinter as tk
import tkinter.ttk  as ttk






class MainWin(tk.Tk):
    def __init__(self,mainBgColor):
         super().__init__()
         self.bg_color = mainBgColor
         self.UserInterface()

    def UserInterface(self):
        
        self.geometry("400x200")
        self.title("HEXoFILL")
        self.iconbitmap('icons/SCLT.ico')

        self.BttFrame = Frame(self,bg = self.bg_color)
        self.BttFrame.pack(side = LEFT, anchor = NE,expand = True)

        self.InfFrame = Frame(self,bg = "green")
        self.InfFrame.pack(side = LEFT,fill = Y)

      

        
        self.startImg = PhotoImage(file = "icons/play.png") 
        self.stopImg  = PhotoImage(file = "icons/stop.png")
        self.scanImg  = PhotoImage(file = "icons/search.png")
        self.loadImg  = PhotoImage(file = "icons/load.png")

        self.scanBtt = Button(self.BttFrame, text = "SCAN", image = self.scanImg, borderwidth = 0, command = self.print_info)
        self.scanBtt.pack(side = TOP,anchor=W)
        
        self.starBtt = Button(self.BttFrame, image = self.startImg, borderwidth = 0, command = self.FTDI_BOOT_ON)
        self.starBtt.pack(side = TOP,anchor=W)

        self.stopBtt = Button(self.BttFrame, image = self.stopImg, borderwidth = 0, command = self.FTDI_BOOT_OFF)
        self.stopBtt.pack(side = TOP,anchor=W)

        self.infoTxt = Text(self.InfFrame)
        self.infoTxt.pack(fill = Y, expand = True)

        

    
    def FTDI_BOOT_ON(self):

        d = ftd.open(0)
        print(d.getDeviceInfo())

        mode = 0x20
        d.setBitMode(0xf1,mode) #Set all pins to output with bit 0 high: 0xF1(0b1111[mask] 0001[data])
        d.setBitMode(0xFF,mode) #Set bits 1 to 4 to output and make bits 1 to 3 high: 0xFF(0b1111[mask] 1111[data])

        time.sleep(0.1)

        d.setBitMode(0xFD,mode) #0xFD(0b1111[mask] 1101[data])

        state = d.getBitMode()
        print(state)
        d.close()

    def FTDI_BOOT_OFF(self):

        d = ftd.open(0)
        print(d.getDeviceInfo())

        mode = 0x20
        d.setBitMode(0xf1,mode)
        d.setBitMode(0xF2,mode) #0xFD(0b1111[mask] 0010[data])

        time.sleep(0.1)

        d.setBitMode(0x00,mode)

        state = d.getBitMode()
        print(state)
        d.close()

    def print_info(self):
        
        self.infoTxt.delete(1.0,END)
        dev = ftd.listDevices()

        for i in range(len(dev)):
            device = ftd.getDeviceInfoDetail(i)
            index  = device["index"]
            descr  = device["description"]
            serial = device["serial"]
            device = ftd.open(i)
            comNum = device.getComPortNumber()
            device.close()
            self.infoTxt.insert(INSERT, f"{index}|{descr}|{serial}|COM:{comNum}\n")

def main():
    app = MainWin("#282c34")
    app.mainloop()
        
if __name__ == '__main__':
    main()
   





