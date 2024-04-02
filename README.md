# rpiWebServer_RS485_ServoCtrl

Raspberry Pi 3B + [RS485 CAN HAT](https://www.waveshare.com/wiki/RS485_CAN_HAT)

[PDF from waveshare.com](https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf)

- [AC Servo Motor Information 1](https://amethyst-myrtle-52e.notion.site/Servo-Motor-Driver-2f7c21ac9d024b00933ec2252861ffcf)
- [AC Servo Motor Information 2-1](https://www.seec.com.tw/Content/Goods/PdfViwer.aspx?SiteID=10&MmmID=655575436061077370&Msid=2022102818050639313&fd=GoodsDownload_Files&pname=SDE%E4%BC%BA%E6%9C%8D%E9%A9%85%E5%8B%95%E5%99%A8%E8%AA%AA%E6%98%8E%E6%9B%B8_V1.07.pdf)
- [AC Servo Motor Information 2-2](https://www.seec.com.tw/Content/Goods/PdfViwer.aspx?SiteID=10&MmmID=655575436061077370&Msid=2020082410220029759&fd=GoodsDownload_Files&pname=%E5%A3%AB%E6%9E%97%E9%9B%BB%E6%A9%9FSDE%E7%B0%A1%E6%98%93%E8%AA%AA%E6%98%8E%E6%9B%B8(%E4%B8%AD%E8%8B%B1)LE106D04204.pdf)

# Reference
- [RS485 CAN HAT_ch](https://www.waveshare.net/wiki/RS485_CAN_HAT#.E5.89.8D.E7.BD.AE.E5.B7.A5.E4.BD.9C_2)
- [RS485 CAN HAT_uk](https://learn.sb-components.co.uk/RS485-CAN-HAT)

  ```
  sudo apt-get update
  sudo apt-get upgrade
  ```
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

  After restart, execute the command to verify that the RS485 CAN HAT is connected during boot.
  ```
  dmesg | grep -i '\(can\|spi\)'
  ```
  ![image](https://github.com/ChungChiuHung/rpiWebServer_RS485_ServoCtrl/assets/52248840/149436ad-a2ca-4dd2-9fa6-c44bf60b2702)

  
  ## Config the static IP for Raspberry Pi
  - Retrieve the currently defined router information
  ```
  ip r | grep default
  ```
  Make a note of the first IP:
  - Retrieve the current DNS server
  ```
  sudo nano /etc/resolv.conf
  ```
  Make a note of the IP next to "nameserver"
  - Modify the "dhcpcd.conf"
  ```
  sudo nano /etc/dhcpcd.conf
  ```
  -Set the static for your "eth0" or "wlan0"
  Replace <NETWORK> <STATICIP> <ROUTERIP> <DNSIP>
  ```
  interface <NETWORK>
  static ip_address=<STATICIP>/24
  static routers=<ROUTERIP>
  static domain_name_servers=<DNSIP>
  ```
  -Reboot Raspberry Pi
  ```
  sudo reboot
  ```
  ## Test the static IP
  ```
  hostname -I
  ```
  


