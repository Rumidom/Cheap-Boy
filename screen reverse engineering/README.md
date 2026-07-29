## The Screen
The screen is 2.8 Inch 240*320 Dots TFT LCD as per the reverse enginering done by 
[YH-workshop](http://hackaday.io/project/175322-dissecting-a-hand-held-noac-console-sup-400-in-1/log/184885-tft-connections)

it seems to be based on the ST7789V chipset, there are a few of these 24 pin screens on alibaba with the same dimensions and flex cable format.

## reference links
[Alibaba HZ028QTCS04-A0](https://www.alibaba.com/product-detail/China-Manufacturer-s-ST7789V-240-X_1600553862839.html)  
[TWJ28167A0](https://www.alibaba.com/product-detail/2-8-Tft-Lcd-Display-Module_1600589508979.html)  

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/HZ028QTCS04-A0.jpg" />
</p>

## Screen Reverse Engineering

### 29/07/2026:
The screen is probably using a 8080 parallel interface, the plan is to use two cascading shift registers to drive DB0 - DB15 and hook the control pins directly to the microcontroler, the NES processor (MOS 6502) has a 8bit data bus and 16bit address bus a portion of these might be exposed in the pins connected to the screen, this could give me more clues to what the processor is doing.

I connected all 24 pins in the connector to a logic analyzer, the numbering in the 24p FPC connector corresponds to the test pads as following:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Test_Pads.jpg" />
</p>

Capturing the signals on the logic analyzer I got something that resembles the pin-out provided by the first Alibaba screen manufacturer (reference code HZ028QTCS04-A0) the first two pins are indeed VCC(1) and GND(2).While the screen receives data LED(3) and RST(4) are always High, CS(5) is always Low, RS(6) is always High, WR(7) gets short bursts of pulses lasting about 10 microseconds spaced by about 15 microseconds of High signal. and RD(8) is always High. Apart from the WR pin, the other control pins do not seem to change.

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Logic_Control_Pins.png" />
</p>

The data pins are all active:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Logic_Data_Pins.png" />
</p>


The screen is constantly being updated since WR is active even on static screens, which is to be expected since the NES hardware is meant to be used with a CRT TV. 

Acording to the ST7789V datasheet there are 4 physical pins that determine the screen interface (IM3,IM2,IM1,IM0) these are probably inacessable somewhere inside the screen. But since all 16 data pins are active I'm assuming that the screen is working in "80-16bit parallel I/F" mode:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/ST7789Vl_Interface_Table.png" />
</p>

If this is the case I should be able to set the logic analyzer to trigger on the D/CX (manufacturer's RS pin) rising edge and capture the start of a frame:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/ST7789Vl_80-16bit_Parallel_Mode.png" />
</p>

however, I haven't been able to do that yet.
