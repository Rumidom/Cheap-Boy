## The Screen
The screen is 2.4 Inch 240*320 Dots TFT LCD 
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/HZ028QTCS04-A0.jpg" />
</p>

## reference links
[Alibaba HZ028QTCS04-A0](https://www.alibaba.com/product-detail/China-Manufacturer-s-ST7789V-240-X_1600553862839.html)  
[TWJ28167A0](https://www.alibaba.com/product-detail/2-8-Tft-Lcd-Display-Module_1600589508979.html)  
[TFT024B045](https://www.alibaba.com/product-detail/2-4-240-X-320-TFT_1600669828556.html)  

## Datasheets
[CT024TN01](https://github.com/Rumidom/Cheap-Boy/blob/main/datasheets/CT024TN01_INNOLUX_2.4__A-si_TFT-LCD_Panel_(EN).pdf) 
[ILI9340](https://github.com/Rumidom/Cheap-Boy/blob/main/datasheets/ILI9340.pdf) 
[ILI9341](https://github.com/Rumidom/Cheap-Boy/blob/main/datasheets/ILI9341.pdf) 
[ST7789V](https://github.com/Rumidom/Cheap-Boy/blob/main/datasheets/ST7789V.PDF)

## Screen Reverse Engineering

### 29/07/2026:
as per the reverse enginering done by [YH-workshop](http://hackaday.io/project/175322-dissecting-a-hand-held-noac-console-sup-400-in-1/log/184885-tft-connections) the screen seems to be based on the ST7789V chipset, and its 2.4 Inch 240*320 Dots, there are a few of these 24 pin screens on alibaba with the same dimensions and flex cable format.

The screen is probably using a 8080 parallel interface, the plan is to use two cascading shift registers to drive DB0 - DB15 and hook the control pins directly to the microcontroller, the NES processor (MOS 6502) has a 8bit data bus and 16bit address bus a portion of these might be exposed in the pins connected to the screen, this could give me more clues to what the processor is doing.

I connected all 24 pins in the connector to a logic analyzer, the numbering in the 24p FPC connector corresponds to the test pads as following:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Test_Pads.png" />
</p>

Capturing the signals on the logic analyzer I got something that resembles the pin-out provided by the first Alibaba screen manufacturer (reference code HZ028QTCS04-A0) the first two pins are indeed VCC(1) and GND(2).While the screen receives data LED(3) and RST(4) are always High, CS(5) is always Low, RS(6) is always High, WR(7) gets short bursts of pulses lasting about 10 microseconds spaced by a pause of about 15 microseconds at High signal. and RD(8) is always High. Apart from the WR pin, the other control pins do not seem to change.

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Logic_Control_Pins.png" />
</p>

The data pins are all active:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Logic_Data_Pins.png" />
</p>


The screen is constantly being updated since WR is active even on static screens, which is to be expected since the NES hardware is meant to be used with a CRT TV. 

According to the ST7789V datasheet there are 4 physical pins that determine the screen interface (IM3,IM2,IM1,IM0) ; these are probably inaccessible somewhere inside the screen. But since all 16 data pins are active I'm assuming that the screen is working in "80-16bit parallel I/F" mode:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/ST7789Vl_Interface_Table.png" />
</p>

If this is the case I should be able to set the logic analyzer to trigger on the D/CX (manufacturer's RS pin) rising edge and capture the start of a frame:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/ST7789Vl_80-16bit_Parallel_Mode.png" />
</p>

however, I haven't been able to do that yet.

### 30/07/2026:

It could be that the pulses I'm seeing on the WR pin are actually a full scanline. The NES operated at 60.0988 Hz according to NTSC standard. This means that each screen frame is drawn in 1/60 seconds, the NES renders 262 scanlines per frame, so each scanline takes (1/60)/262 seconds to draw. equal to 63.6132 microseconds, but that does not match what was measured. 10 microseconds burst + 15 microseconds of pause. At that speed my logic analyzer operating at 120 MHZ might not be fast enough to catch the RS (D/CX) low pulse. 

Under further inspection of the datasheet, I found that the ST7789V also has a VSYNC RGB mode which is more akin to how a CRT monitor works. But that interface requires VSYNC,HSYNC,ENABLE and DOTCLK pins which are not exposed in the connector (assuming that the manufacturer's pinout is correct).

I was also able to capture a long sequence of what seems like bundled data, lasting about 400 microseconds and starting with a long burst on the WR pin followed by a sequence of shorter bursts, but these might just be a result of the NES PPU (Picture Processing Unit) taking pauses to do operations. They do seem to be carrying color information. As you'll see next:

This is the start screen after a reset (where most of the screen is black):  
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Start_Screen_Photo.jpg" width="600"/>
</p>  
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Reset_Start_Screen_LA_Capture_120mhz.png" width="600" />
</p>  
  
And this is the Bubble Bubble 2 game start screen (where most of the screen is white):  
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Bubble_Bubble_Screen_Photo.jpg" width="600"/>
</p>  
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Bubble_Bubble_Start_Screen_Capture_120mhz.png" width="600" />
</p>  

I measured the screen and its actually 2.4 inch, but its indeed 240*320, I'm starting to suspect that this LCD might not be a ST7789V, however the pinout does seem to match


### 11/08/2026:

I tried using a different [logic analyzer firmware](https://github.com/gusmanb/logicanalyzer) on the pi pico I was using to capture the screen data and got better resolution:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering
/Screen_Data_Better_resolution.png" width="600" />
</p>  

Now I can see that each burst of the WR pin consistently takes 46.44 microseconds plus 17 microseconds of pause, 63.51 microseconds in total, which matches the timing for one scan line of the PPU on the NES. The WR pin has a unusual clock signature composed of short and long pulses:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering
/WR_Clock_Signature.png" width="600" />
</p>  

I manually counted the LOW pulses and got a count of 320 pulses which is exactly the number of pixels on each horizontal line on the lcd screen. It should be safe to assume that each burst of clock pulses is a scanline. I have noticed that the screen is actually stretched to fit the screen, this is particularly noticeable on the "Excitebike" game, where there is a checkerboard pattern. The screen is probably not driven directly by a NES PPU inside the [COB](https://en.wikipedia.org/wiki/Chip_on_board) chip on this unit. There should be a translation module or a modified PPU inside, this is most likely a heavily modified version of the nintendo original. So comparisons should be taken with a grain of salt.

Unfortunatly I was only able to capture 4 complete scanlines before the SUP 400 in 1 died, When I disconnected the VCC and GND wires from the PI pico they must have shortened out. I decided to remove the backlight on the LCD to see If I can find more clues on the LCD chipset, these are mirrored microscope photos of the back side close to the flex cable:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/Screen_Back_Microscope_1.jpeg" width="600" />
</p>  

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/Screen_Back_Microscope_2.jpeg" width="600" />
</p>  

Searching for CT024TN01_V4 online, I found the manufacturer "INNOLUX" which had only a spec-sheet for what seems like a similar screen, next step is to see if I can find what is the actual protocol this screen is, just a hunch but I think this might be a ILI9340/ILI9341 chipset which is just common on these low res screens. I'll try to see if the ILI9340 data sheet is a better match and maybe try to decode the new logic analyzer capture into a picture.
