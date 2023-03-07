# Lirc
Lirc is an IR rasberry pi compatible tool that requres a remote configuration and some pins to send IR commands as if the rasberry pi was the remote.
Connected to the pins are an infrared LED and a transistor. [INSERT PICTURE/WIRING DIAGRAM]
To use these lirc remotes they must present in the file located at /etc/lirc/lircd.conf
Make sure to also configure which pin is receiving and sending signals in /boot/config.txt

for example:
dtoverlay=gpio-ir-tx,gpio_pin=23
dtoverlay=gpio-ir,gpio_pin=18