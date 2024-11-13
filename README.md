# TankBot

Simple RC Tank created with an ESP32-C3 and micropython.

Sets up a WiFi access point and using microdot and a basic DNS server, implements a captive 
portal to control the bot from a web browser. 

# Setup

**Dependencies**
```shell
pip install esptool
```

**Erase ESP**
```shell
ESP=/dev/ttyACM0 # or whatever port 
esptool.py -p $ESP erase_flash
```

**Install Firmware**
```shell
esptool.py --chip esp32c3 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 .files/ESP32_GENERIC_C3-20240602-v1.23.0.bin
```

# Usage

**REPL**

```shell
picocom $ESP
```

**Run main program**
```python
asyncio.run(main())
```