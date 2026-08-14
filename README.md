# Cheap-Boy
Cheap-Boy is a motherboard replacement mod for the [SUP 400 in 1](https://bootleggames.fandom.com/wiki/Sup_Game_Box) portable [famiclone](https://en.wikipedia.org/wiki/Famiclone) , the 'SUP 400 in 1' handheld is an interesting piece of Chinese engineering on its own. It has a full NES on a chip, a rechargeable battery, Game-Boy DMG inspired shell, AV output, and can be found on Aliexpress for about U$10 or lower.

I thought it would be interesting to try to replace the main board on this device with one featuring a micro-controller such as the Raspberry Pi Pico, to emulate Game-Boy games. There are already a few emulator projects online leveraging the power of modern micro-controllers for gameboy and retro emulation: [RP2040-GB ](https://github.com/deltabeard/RP2040-GB), [Pico GB](https://github.com/YouMakeTech/Pico-GB), [Walnut-CGB](https://github.com/Mr-PauI/Walnut-CGB
), [retro-go](https://github.com/ducalex/retro-go), [Microbyte](https://hackaday.io/project/176182-microbyte)

Using the components of the sup 400 in 1 should yield an ultra cheap and reasonably powerful handheld. The sup 400 in 1 has already been [reversed enginered](https://hackaday.io/project/175322-dissecting-a-hand-held-noac-console-sup-400-in-1) to support a custom ROM. But as far as I'm aware this is the first attempt at running Game-Boy games on it. 

If you are allergic to cheap white label hardware and would like a more polished and authentic gaming experience, I recommend the [Super DMG](https://github.com/kamicane/Super-DMG-01) which restores new life to actual Nintendo silicon, or the [Gamebub](https://github.com/elipsitz/gamebub) which replicates the Game-Boy hardware on a FPGA aiming at high accuracy, in keeping with the theme, on this project I'll try to reuse as many components from the the SUP 400 in 1 as possible, add a few inexpensive new ones, and try to keep the total cost low. While having a complete feature set.

# Micro-controlers alternatives 

This board is designed for the Raspberry Pi Pico or any of the generic RP2040 variants, but different flavors of micro-controller could be used. There are a few dev board alternatives that share the same form factor and should be compatible. such as the [Wallnut Pico W](https://wiki.walnutpi.com/en/docs/walnutpi_picow/intro/wpi_picow), [ESP32-S3 Pico](https://www.waveshare.com/wiki/ESP32-S3-Pico) or any of the [Raspberry Pico series](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pico2)

## TODO:
- [x] Reverse Engineer 16-bit screen protocol
- [ ] Write a Screen library for the ILI934X (might need multiple later on, for other types of screen)
- [ ] Create first revision of the PCB   

## License:
This project is MIT licensed.

## Support
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M41NQV7I)
