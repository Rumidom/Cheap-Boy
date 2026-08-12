# Sup 400 in 1 Info

This project focused on making a replacement board for the Sup 400 in 1 but, I think it might be worthwhile doing a little research on the console itself, according to the [bootleggames wiki](https://bootleggames.fandom.com/wiki/Sup_Game_Box) the console has 313 unique games 87 duplicate games, many of which are ports from the [Nintendo NES](https://en.wikipedia.org/wiki/Nintendo_Entertainment_System) these can be found for sale named as "Sup 400 in 1", or just "400 in 1 game console" it runs on a [VTxx](https://bootleggames.fandom.com/wiki/VTxx) chip which is a modified [SOC](https://en.wikipedia.org/wiki/System_on_a_chip) clone of the NES, I was able to sand the [COB](https://en.wikipedia.org/wiki/Chip_on_board) down and take a picture of the silicon die:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/400%20in%201%20Info/Images/COB_Silicon.jpeg" />
</p>
(from the V5 board)

There isn't much technical information online on the inner-workings of this console, but there is a project on [hackaday](https://hackaday.io/project/175322-dissecting-a-hand-held-noac-console-sup-400-in-1) and here on [Github](https://nyh-workshop.github.io/Custom-ROM-Sup-Game-Box-400in1/ROM_dump_analysis) aimed at dumping the systems ROM, both maintained by [YH-workshop](https://github.com/nyh-workshop). According to YH-workshop there are 3 types of screen initialization the last one accepting multiple screen drivers, which is problematic for this project, as I was hoping the console always used the same type of screen. but its likely that they all use the same 16 bit parallel protocol. I bought two of these consoles for reverse engineering they came on similar white label boxes:

<p align="center">
  <img src=https://github.com/Rumidom/Cheap-Boy/blob/main/400%20in%201%20Info/Images/boxes.jpg" />
</p>

one had markings indicating that it was a version 5 and the other a version 2:

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/400%20in%201%20Info/Images/board_markings.jpg" />
</p>

both devices have a single layer PCB and used a BL-C5 battery for power, V2 has external audio amplifier, the the v5 had a more streamlined design the audio amplifier was integrated in the COB and the ROM chip was on a what seemed like a SOIC package, Both screens where interchangeable on both the devices.

<p align="center">
  <img src="https://github.com/Rumidom/Cheap-Boy/blob/main/400%20in%201%20Info/Images/boards.jpg" />
</p>
