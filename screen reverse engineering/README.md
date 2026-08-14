## The Screen
The screen is a 2.4 Inch 240*320 Dots TFT LCD 
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/HZ028QTCS04-A0.jpg" />
</p>

## Reference links
[Alibaba HZ028QTCS04-A0](https://www.alibaba.com/product-detail/China-Manufacturer-s-ST7789V-240-X_1600553862839.html)  
[TWJ28167A0](https://www.alibaba.com/product-detail/2-8-Tft-Lcd-Display-Module_1600589508979.html)  
[TFT024B045](https://www.alibaba.com/product-detail/2-4-240-X-320-TFT_1600669828556.html)  

## Datasheets
[CT024TN01 - Spec Sheet](https://github.com/Rumidom/Cheap-Boy/blob/main/datasheets/CT024TN01_INNOLUX_2.4__A-si_TFT-LCD_Panel_(EN).pdf)  
[ILI9340](https://github.com/Rumidom/Cheap-Boy/blob/main/datasheets/ILI9340.pdf)  
[ILI9341](https://github.com/Rumidom/Cheap-Boy/blob/main/datasheets/ILI9341.pdf)  
[ST7789V](https://github.com/Rumidom/Cheap-Boy/blob/main/datasheets/ST7789V.PDF)  

## Screen Reverse Engineering

### 29/07/2026:
as per the reverse enginering done by [YH-workshop](http://hackaday.io/project/175322-dissecting-a-hand-held-noac-console-sup-400-in-1/log/184885-tft-connections) the screen seems to be based on the ST7789V chipset, and its 2.4 Inch 240*320 Dots, there are a few of these 24 pin screens on alibaba with the same dimensions and flex cable format.

The screen is probably using a 8080 parallel interface, the plan is to use two cascading shift registers to drive DB0 - DB15 and hook the control pins directly to the microcontroller, the NES processor (MOS 6502) has a 8bit data bus and 16bit address bus a portion of these might be exposed in the pins connected to the screen, this could give me more clues to what the processor is doing.

I connected all 24 pins in the connector to a logic analyzer, the numbering in the 24p FPC connector corresponds to the test pads as following:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Test_Pads.png" />
</p>

Capturing the signals on the logic analyzer I got something that resembles the pin-out provided by the first Alibaba screen manufacturer (reference code HZ028QTCS04-A0) the first two pins are indeed VCC(1) and GND(2).While the screen receives data LED(3) and RST(4) are always High, CS(5) is always Low, RS(6) is always High, WR(7) gets short bursts of pulses lasting about 10 microseconds spaced by a pause of about 15 microseconds at High signal. and RD(8) is always High. Apart from the WR pin, the other control pins do not seem to change.

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Logic_Control_Pins.png" />
</p>

The data pins are all active:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Logic_Data_Pins.png" width="600"/>
</p>


The screen is constantly being updated since WR is active even on static screens, which is to be expected since the NES hardware is meant to be used with a CRT TV. 

According to the ST7789V datasheet there are 4 physical pins that determine the screen interface (IM3,IM2,IM1,IM0) ; these are probably inaccessible somewhere inside the screen. But since all 16 data pins are active I'm assuming that the screen is working in "80-16bit parallel I/F" mode:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/ST7789Vl_Interface_Table.png" />
</p>

If this is the case I should be able to set the logic analyzer to trigger on the D/CX (manufacturer's RS pin) rising edge and capture the start of a frame:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/ST7789Vl_80-16bit_Parallel_Mode.png" />
</p>

however, I haven't been able to do that yet.

### 30/07/2026:

It could be that the pulses I'm seeing on the WR pin are actually a full scanline. The NES operated at 60.0988 Hz according to NTSC standard. This means that each screen frame is drawn in 1/60 seconds, the NES renders 262 scanlines per frame, so each scanline takes (1/60)/262 seconds to draw. equal to 63.6132 microseconds, but that does not match what was measured. 10 microseconds burst + 15 microseconds of pause. At that speed my logic analyzer operating at 120 MHZ might not be fast enough to catch the RS (D/CX) low pulse. 

Under further inspection of the datasheet, I found that the ST7789V also has a VSYNC RGB mode which is more akin to how a CRT monitor works. But that interface requires VSYNC,HSYNC,ENABLE and DOTCLK pins which are not exposed in the connector (assuming that the manufacturer's pinout is correct).

I was also able to capture a long sequence of what seems like bundled data, lasting about 400 microseconds and starting with a long burst on the WR pin followed by a sequence of shorter bursts, but these might just be a result of the NES PPU (Picture Processing Unit) taking pauses to do operations. They do seem to be carrying color information. As you'll see next:

This is the start screen after a reset (where most of the screen is black):  
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Start_Screen_Photo.jpg" width="600"/>
</p>  
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Reset_Start_Screen_LA_Capture_120mhz.png" width="600" />
</p>  
  
And this is the Bubble Bubble 2 game start screen (where most of the screen is white):  
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Bubble_Bubble_Screen_Photo.jpg" width="600"/>
</p>  
<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Bubble_Bubble_Start_Screen_Capture_120mhz.png" width="600" />
</p>  

I measured the screen and its actually 2.4 inch, but its indeed 240*320, I'm starting to suspect that this LCD might not be a ST7789V, however the pin-out does seem to match


### 11/08/2026:

I tried using a different [logic analyzer firmware](https://github.com/gusmanb/logicanalyzer) on the pi pico I was using to capture the screen data and got better resolution:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Screen_Data_Better_resolution.png" width="600" />
</p>  

Now I can see that each burst of the WR pin consistently takes 46.44 microseconds plus 17 microseconds of pause, 63.51 microseconds in total, which matches the timing for one scan line of the PPU on the NES. The WR pin has a unusual clock signature composed of short and long pulses:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/WR_Clock_Signature.png" width="600" />
</p>  

I manually counted the LOW pulses and got a count of 320 pulses which is exactly the number of pixels on each horizontal line on the LCD screen. It should be safe to assume that each burst of clock pulses is a scanline. I have noticed that the games are actually stretched to fit the screen, this is particularly noticeable on the ["Excitebike"](https://gamesdb.launchbox-app.com/games/images/202-excitebike) game, where there is a checkerboard pattern. The screen is probably not driven directly by a NES PPU inside the [COB](https://en.wikipedia.org/wiki/Chip_on_board) on this unit. There should be a translation module or a modified PPU inside, this is most likely a heavily modified version of the Nintendo original. So comparisons should be taken with a grain of salt.

Unfortunately I was only able to capture 4 complete scanlines before the SUP 400 in 1 died, When I disconnected the VCC and GND wires from the Pi Pico they must have shortened out. I decided to remove the back-light on the LCD to see If I can find more clues on the LCD chipset, these are mirrored microscope photos of the back side close to the flex cable:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Screen_Back_Microscope_1.jpeg" width="600" />
</p>  

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Screen_Back_Microscope_2.jpeg" width="600" />
</p>  

Searching for CT024TN01_V4 online, I found the manufacturer "INNOLUX" which had only a spec-sheet for what seems like a similar screen, next step is to see if I can find what the actual protocol for this screen is, just a hunch, but I think this might be a ILI9340/ILI9341 chipset. Which is just common on these low res screens. I'll try to match the LI9340 datasheet and the new logic analyzer capture data and maybe try decode the capture into a image.

### 12/08/2026:
The ILI9340 datasheet is very similar to the ST7789V datasheet,and it has pretty much the same interfaces, searching for a 16-bit mode I found this table:  

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/ILI9340_16bit_RGB_interface_Table.png" width="600" />
</p>

DC/RS is pulled low a command is sent and then the colors are sent pixel by pixel until the end of the scanline, natively the screen is in portrait orientation thus the scanline on the table only goes to 240, during screen initialization a command is probably sent to put it in landscape orientation. Still I could not find any start scanline command, or the 
RS pin being pulled low, I made a python script to try to decode the Logic analyzers data, using the same color encoding as the table above, and triggering pixel recording on WR rising edge,I was able to get an image out but the colors seem to be a bit off and it does seem to be losing pixels with the current logic analyzer setup:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Capture%20Decoding/Decoded_Start_Screen.png" width="600" />
</p>

It would be nice if I could get a whole frame to compare, but as I metioned before the screen I was using in now broken, and the new logic analyzer firmware can only capture about 5 scanlines worth of data, at this point I should probably try driving the other screen I have with the interfaces I mentioned previously, I'll try to drive the 16bit bus with shift registers and a pi pico using SPI. each pixel is being drawn at about 11 Mhz maybe half that considering the long pulses the [pi pico](https://raspberrypi.stackexchange.com/questions/132758/what-is-the-pico-max-spi-frequency) maximum clock speed for SPI is 62.5MHz and the [shiftregister](https://e2e.ti.com/support/logic-group/logic/f/logic-forum/819554/sn74hc595-what-is-the-maximum-clock-frequency-when-vcc-3-3v-under-85-degree-ambient-temperature) maximum clock is about 12.5MHz, but this is to shift 1 bit into the 16bit bus, to shift all 16 bits would take 5*16 = 80MHZ, so maintaining 60 hz refresh rate like the NES might not be possible.

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Pixel_Draw_Rate.png" width="400" />
</p>

### 13/08/2026:

Looking at the ILI9340 command list on the datasheet I found this:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Memory_Write_Command.png" width="800" />
</p>

Which should be the command to start writing on the screen, the datasheet also states that there are two transfer modes available, the first one (if I understand correctly) sends a write command and then all the scanlines the second mode sends one command for each scanline (I'm assuming the "Image Data Frame" on the datasheet refers to one scanline). I belive the screen is working in transfer mode 1 since I haven't seen this write command yet, in mode 1 it should only happen once every Screen frame, this is exactly the same for the ST7789V, and the 'Memory Write' command is the same for both 
'XXXXXXXX00101100'.

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Data_Transfer_Modes.png"
width="800" />
</p>

I wrote a small test script in micro-python to send data to the screen using two cascading 74HC595 shift registers and a Pi  Pico, I'm also using another Pi Pico as a logic analyzer to double check the wiring and signals, and was able to send commands to the screen, . on a [micropython library for SPI](https://github.com/jeffmer/micropython-ili9341/tree/master) someone already copied the registers adresses from the datasheet so I'm using those and they seem to work as I was able to get the screen out of sleep and turn off. 


<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Screen_Test_0.png"
height="400" />
</p>


The Micropython library had lots of commands sent on initialization, I don't think they are all necessary or suitable for 16-bit mode, I'll have to test. This is the default state of the configuration registers after reset:

```python
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

# ILI9340/ST7789V
sendScreenCommand(_SLPOUT)
sendScreenCommand(_DISPOFF)
```

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/screen%20reverse%20engineering/Images/Config_Registers_After_Reset.png"
width="600" />
</p>

next I'll see if I can draw on the screen.
