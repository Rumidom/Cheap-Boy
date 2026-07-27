## The Screen

the screen is 2.8 Inch 240*320 Dots TFT LCD as per the reverse enginering done by 
[YH-workshop](http://hackaday.io/project/175322-dissecting-a-hand-held-noac-console-sup-400-in-1/log/184885-tft-connections)

it seems to be based on the ST7789V chipset, there are a few of these 24 pin screens on alibaba with the same dimensions and flex cable format.

## reference links
[Alibaba HZ028QTCS04-A0](https://www.alibaba.com/product-detail/China-Manufacturer-s-ST7789V-240-X_1600553862839.html)
[TWJ28167A0](https://www.alibaba.com/product-detail/2-8-Tft-Lcd-Display-Module_1600589508979.html)

## interface
the screen seems to use a 8080 interface, the plan is to use two cascading shift registers to drive D0 - D17

https://www.displaymodule.com/blogs/knowledge/the-interface-of-8080
