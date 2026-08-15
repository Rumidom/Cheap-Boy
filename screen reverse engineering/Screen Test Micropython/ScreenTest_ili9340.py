import machine
from machine import Pin
import time

# ILI9340 Registers
_NOP = const(0x00)       # No Operation
_RDDSDR = const(0x0f)    # Read Display Self-Diagnostic Result
_SLPOUT = const(0x11)    # Sleep Out
_GAMSET = const(0x26)    # Gamma Set
_DISPOFF = const(0x28)   # Display Off
_DISPON = const(0x29)    # Display On
_CASET = const(0x2a)     # Column Address Set
_PASET = const(0x2b)     # Page Address Set
_RAMWR = const(0x2c)     # Memory Write
_RAMRD = const(0x2e)     # Memory Read
_MADCTL = const(0x36)    # Memory Access Control
_VSCRSADD = const(0x37)  # Vertical Scrolling Start Address
_PIXSET = const(0x3a)    # Pixel Format Set
_DTCTRLA = const(0xe8)   # Driver Timing Control A
_DTCTRLB = const(0xea)   # Driver Timing Control B
_PWRONCTRL = const(0xed) # Power on Sequence Control
_PRCTRL = const(0xf7)    # Pump Ratio Control
_PWCTRL1 = const(0xc0)   # Power Control 1
_PWCTRL2 = const(0xc1)   # Power Control 2
_VMCTRL1 = const(0xc5)   # VCOM Control 1
_VMCTRL2 = const(0xc7)   # VCOM Control 2
_FRMCTR1 = const(0xb1)   # Frame Rate Control 1
_DISCTRL = const(0xb6)   # Display Function Control
_ENA3G = const(0xf2)     # Enable 3G
_PGAMCTRL = const(0xe0)  # Positive Gamma Control
_NGAMCTRL = const(0xe1)  # Negative Gamma Control

BL_pin  =  machine.Pin(6,machine.Pin.OUT)
CS_pin  =  machine.Pin(7,machine.Pin.OUT)
RST_pin = machine.Pin(26,machine.Pin.OUT)

RS_pin  =  machine.Pin(20,machine.Pin.OUT)
WR_pin  =  machine.Pin(23,machine.Pin.OUT)
SHF_DataIn_pin  =  machine.Pin(3,machine.Pin.OUT)
SHF_Clck_pin  =  machine.Pin(2,machine.Pin.OUT)
SHF_OUT_EN_pin  =  machine.Pin(5,machine.Pin.OUT)
SHF_Latch_pin  =  machine.Pin(6,machine.Pin.OUT)
SHF_RST_pin  =  machine.Pin(7,machine.Pin.OUT)

def Clock_WR():
    WR_pin.value(0)
    time.sleep_us(1)
    WR_pin.value(1)

def ResetDataBus():
    SHF_RST_pin.value(0)
    time.sleep_us(1)
    SHF_RST_pin.value(1)

def WriteToDataBus(val,numbits):
    ResetDataBus()
    #hexadecimal 0x0000
    #binary 0b0000000000000000
    SHF_OUT_EN_pin.value(0)
    for BitIndex in range(numbits-1,-1,-1):
        SHF_Clck_pin.value(0)
        if (val >> BitIndex) & 1:
            SHF_DataIn_pin.value(1)
            #print(BitIndex,' - ',1)
        else:
            #print(BitIndex,' - ',0)
            SHF_DataIn_pin.value(0)
        time.sleep_us(1)
        SHF_Clck_pin.value(1)
    SHF_Latch_pin.value(1)
    time.sleep_us(1)
    SHF_Latch_pin.value(0)

def sendScreenCommand(command):
    RS_pin.value(0)
    WriteToDataBus(command,8)
    Clock_WR()
    RS_pin.value(1)

def sendScreenData_16(data):
    WriteToDataBus(data,16)
    Clock_WR()

def sendScreenData_8(data):
    WriteToDataBus(data,8)
    Clock_WR()

def setrect(x1,y1,x2,y2):#set coordinates to print on a regeon of the screen
    sendScreenCommand(0x2A);
    sendScreenData_16(x1);
    sendScreenData_16(x2);
    sendScreenCommand(0x2B);
    sendScreenData_16(y1);
    sendScreenData_16(y2);
    sendScreenCommand(0x2C);

#init Control Pins
BL_pin.value(1)
RST_pin.value(0)
RST_pin.value(1)
RS_pin.value(1)
WR_pin.value(1)
CS_pin.value(0)

#init Shift Registers
SHF_Clck_pin.value(0)
SHF_OUT_EN_pin.value(0)
SHF_Latch_pin.value(0)
ResetDataBus()

def screenInit():
    # ILI9340 Initialization
    sendScreenCommand(_SLPOUT)
    sendScreenCommand(_DISPOFF)

    time.sleep_ms(1000)

    #Power control A - Only present on ili9341
    sendScreenCommand(0xcb)
    sendScreenData_8(0x39)
    sendScreenData_8(0x2C)
    sendScreenData_8(0x00)
    sendScreenData_8(0x34)
    sendScreenData_8(0x02)

    #Power control B - Only present on ili9341
    sendScreenCommand(0xCF)
    sendScreenData_8(0x00)
    sendScreenData_8(0xC1)
    sendScreenData_8(0x30)

    #Driver timing control A
    sendScreenCommand(0xE8)
    sendScreenData_8(0x85)
    sendScreenData_8(0x00)
    sendScreenData_8(0x78)

    #Driver timing control B
    sendScreenCommand(0xEA)
    sendScreenData_8(0x00)
    sendScreenData_8(0x00)

    #Power on sequence control
    sendScreenCommand(0xED)
    sendScreenData_8(0x64)
    sendScreenData_8(0x03)
    sendScreenData_8(0x12)
    sendScreenData_8(0x81)

    #Pump ratio control
    sendScreenCommand(0xF7)
    sendScreenData_8(0x20)

    #Power control 1
    sendScreenCommand(0xC0)
    sendScreenData_8(0x23)

    #Power control 2
    sendScreenCommand(0xC1)
    sendScreenData_8(0x10)

    #vcm control
    sendScreenCommand(0xC5)
    sendScreenData_8(0x3E)
    sendScreenData_8(0x28)

    #vcm control 2
    sendScreenCommand(0xC7)
    sendScreenData_8(0x86)

    #memory access control
    sendScreenCommand(0x36)
    sendScreenData_8(0x48)

    #pixel format
    sendScreenCommand(0x3A)
    sendScreenData_8(0x55)

    #frameration control,normal mode full colours
    sendScreenCommand(0xB1)
    sendScreenData_8(0x00)
    sendScreenData_8(0x18)

    #display function control
    sendScreenCommand(0xB6)
    sendScreenData_8(0x08)
    sendScreenData_8(0x82)
    sendScreenData_8(0x27)

    #gamma function disable
    sendScreenCommand(0xF2)
    sendScreenData_8(0x00)

    #gamma curve selected
    sendScreenCommand(0x26)
    sendScreenData_8(0x01)

    #set positive gamma correction
    sendScreenCommand(0xE0)
    sendScreenData_8(0x0F)
    sendScreenData_8(0x31)
    sendScreenData_8(0x2B)
    sendScreenData_8(0x0C)
    sendScreenData_8(0x0E)
    sendScreenData_8(0x08)
    sendScreenData_8(0x4E)
    sendScreenData_8(0xF1)
    sendScreenData_8(0x37)
    sendScreenData_8(0x07)
    sendScreenData_8(0x10)
    sendScreenData_8(0x03)
    sendScreenData_8(0x0E)
    sendScreenData_8(0x09)
    sendScreenData_8(0x00)

    #set negative gamma correction
    sendScreenCommand(0xE1)
    sendScreenData_8(0x00)
    sendScreenData_8(0x0E)
    sendScreenData_8(0x14)
    sendScreenData_8(0x03)
    sendScreenData_8(0x11)
    sendScreenData_8(0x07)
    sendScreenData_8(0x31)
    sendScreenData_8(0xC1)
    sendScreenData_8(0x48)
    sendScreenData_8(0x08)
    sendScreenData_8(0x0F)
    sendScreenData_8(0x0C)
    sendScreenData_8(0x31)
    sendScreenData_8(0x36)
    sendScreenData_8(0x0F)

    #exit sleep
    sendScreenCommand(0x11)
    time.sleep_ms(120)

    #display on
    sendScreenCommand(0x29)

screenInit()

#draw stripes
sendScreenCommand(_RAMWR)
for i in range(240*30):
    sendScreenData_16(0b1111100000000000)
for i in range(240*30):
    sendScreenData_16(0b0000011111100000)
for i in range(240*30):
    sendScreenData_16(0b0000000000011111)
sendScreenCommand(0x00)























































































































































































































 

