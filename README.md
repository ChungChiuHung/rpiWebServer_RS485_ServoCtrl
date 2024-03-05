# rpiWebServer_RS485_ServoCtrl

Raspberry Pi 3B + [RS485 CAN HAT](https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf)

# Reference
- [RS485 CAN HAT_ch](https://www.waveshare.net/wiki/RS485_CAN_HAT#.E5.89.8D.E7.BD.AE.E5.B7.A5.E4.BD.9C_2)
- [RS485 CAN HAT_uk](https://learn.sb-components.co.uk/RS485-CAN-HAT)
- 
  Open UART Port
  ```
  sudo raspi-config
  ```
  Select Interfacing Options -> Serial
  - Would you like a login shell to be accessible over serial? No
  - Would you like the serial port hardware to be enable? Yes

  Open file "/boot/config.txt"
  Add below line to the end of the file
  ```
  [all]
  dtparam=spi=on
  dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000
  enable_uart=1
  dtoverlay=disable-bt
  ```

  List the serial port
  ```
  ls -l /dev/serial*
  ```
  ![image](https://github.com/ChungChiuHung/rpiWebServer_RS485_ServoCtrl/assets/52248840/9da6fa95-6cb4-4160-8ef5-387343c84b57)

  Reboot
  ```
  sudo reboot
  ```
  
