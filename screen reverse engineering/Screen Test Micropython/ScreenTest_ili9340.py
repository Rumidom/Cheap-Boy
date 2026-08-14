import machine
from machine import Pin
import time

_RDDSDR = const(0x0f) # Read Display Self-Diagnostic Result
_SLPOUT = const(0x11) # Sleep Out
_GAMSET = const(0x26) # Gamma Set
_DISPOFF = const(0x28) # Display Off
_DISPON = const(0x29) # Display On
_CASET = const(0x2a) # Column Address Set
_PASET = const(0x2b) # Page Address Set
_RAMWR = const(0x2c) # Memory Write
_RAMRD = const(0x2e) # Memory Read
_MADCTL = const(0x36) # Memory Access Control
_VSCRSADD = const(0x37) # Vertical Scrolling Start Address
_PIXSET = const(0x3a) # Pixel Format Set
_DTCTRLA = const(0xe8) # Driver Timing Control A
_DTCTRLB = const(0xea) # Driver Timing Control B
_PWRONCTRL = const(0xed) # Power on Sequence Control
_PRCTRL = const(0xf7) # Pump Ratio Control
_PWCTRL1 = const(0xc0) # Power Control 1
_PWCTRL2 = const(0xc1) # Power Control 2
_VMCTRL1 = const(0xc5) # VCOM Control 1
_VMCTRL2 = const(0xc7) # VCOM Control 2
_FRMCTR1 = const(0xb1) # Frame Rate Control 1
_DISCTRL = const(0xb6) # Display Function Control
_ENA3G = const(0xf2) # Enable 3G
_PGAMCTRL = const(0xe0) # Positive Gamma Control
_NGAMCTRL = const(0xe1) # Negative Gamma Control

BL_pin  =  machine.Pin(27,machine.Pin.OUT)
RST_pin = machine.Pin(26,machine.Pin.OUT)
CS_pin  =  machine.Pin(22,machine.Pin.OUT)
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

# ILI9340/ST7789V
sendScreenCommand(_SLPOUT)
sendScreenCommand(_DISPOFF)





























































































































































































































 

