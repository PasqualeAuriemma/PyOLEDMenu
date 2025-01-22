from machine import Pin, I2C, ADC
import random
from pymenu import *
import ssd1306
from time import sleep

i2c = I2C(1, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v

pot1 = ADC(Pin(35))
pot1.atten(ADC.ATTN_11DB)       #Full range: 3.3v

pot2 = ADC(Pin(25))
pot2.atten(ADC.ATTN_11DB)       #Full range: 3.3v

pot3 = ADC(Pin(33))
pot3.atten(ADC.ATTN_11DB)       #Full range: 3.3v

pot4 = ADC(Pin(32))
pot4.atten(ADC.ATTN_11DB)       #Full range: 3.3v

class Config:

    def __init__(self, name):
        self.relays_status = {}
        self.statuses = {}

    def set_mode(self, *args):
        print('la scelta e '+ str(args[0]))

    def get_ec_status(self, *args):
        try:
            return self.statuses[args[0]]
        except KeyError:
            self.statuses[args[0]] = False
            return False

    def get_status(self, *args):
        try:
            return self.relays_status[args[0]]
        except KeyError:
            self.relays_status[args[0]] = False
            return False

    def toggle(self, *args):
        self.relays_status[args[0]] = not self.relays_status[args[0]]
        self.get_status(*args)

    def ec_toggle(self, *args):
        self.statuses[args[0]] = not self.statuses[args[0]]
        self.get_ec_status(*args)    

config = Config('Config')
menu = Menu()

menu.set_main_screen(MenuList(display, 'MENU')
    .add(MenuEnum(display, 'MODE', ['AUTO', 'MAINTENANCE', 'STAND BY'], print))
    .add(MenuList(display, 'RELAYS')
        .add(ToggleItem(display, 'LIGHTS', (config.get_status, 0), (config.toggle, 0), ('ON', 'OFF')))
        .add(ToggleItem(display, 'FILTER', (config.get_status, 1), (config.toggle, 1), ('ON', 'OFF')))
        .add(ToggleItem(display, 'HEATER', (config.get_status, 2), (config.toggle, 2), ('ON', 'OFF')))
        .add(ToggleItem(display, 'FEEDER', (config.get_status, 3), (config.toggle, 3), ('ON', 'OFF')))
        .add(BackItem(display))    
        )
    .add(MenuList(display, 'SENSORS')
        .add(MenuList(display, 'EC')
            .add(ToggleItem(display, 'ACTIVATION', (config.get_status, 4), (config.toggle, 4)))
            .add(MenuMonitoringSensor(display, 'MONITORING', visible=(config.get_status, 4)))
            .add(ToggleItem(display, 'WEB SERVER', (config.get_status, 5), (config.toggle, 5), visible=(config.get_status, 4)))
            .add(MenuEnum(display, "WEB RATE", ['1', '2', '3', '4', '6', '8', '12', '24'], print, visible=(config.get_status, 4)))  
            .add(MenuConfirm(display, "SEND TO WEB", ('-> SEND', '<- BACK'), print, visible=(config.get_status, 4))) 
            .add(BackItem(display))
        )
        .add(MenuList(display, 'PH')
            .add(ToggleItem(display, 'ACTIVATION', (config.get_status, 6), (config.toggle, 6)))
            .add(MenuMonitoringSensor(display, 'MONITORING', visible=(config.get_status, 6)))
            .add(ToggleItem(display, 'WEB SERVER', (config.get_status, 7), (config.toggle, 7), visible=(config.get_status, 6)))
            .add(MenuEnum(display, "WEB RATE", ['1', '2', '3', '4', '6', '8', '12', '24'], print, visible=(config.get_status, 6)))  
            .add(MenuConfirm(display, "SEND TO WEB", ('-> SEND', '<- BACK'), print, visible=(config.get_status, 6))) 
            .add(BackItem(display))
        )
        .add(MenuList(display, 'THERMOMETER')
            .add(ToggleItem(display, 'ACTIVATION', (config.get_status, 8), (config.toggle, 8)))
            .add(ToggleItem(display, 'WEB SERVER', (config.get_status, 9), (config.toggle, 9), visible=(config.get_status, 8)))
            .add(MenuEnum(display, "WEB RATE", ['1', '2', '3', '4', '6', '8', '12', '24'], print, visible=(config.get_status, 8)))  
            .add(MenuConfirm(display, "SEND TO WEB", ('-> SEND', '<- BACK'), print, visible=(config.get_status, 8))) 
            .add(BackItem(display))
        )
        .add(BackItem(display))
    )
    .add(MenuList(display, 'SETTINGS')
        .add(MenuList(display, 'WIFI')
            .add(MenuWifiInfo(display, 'INFO'))
            .add(MenuConfirm(display, "CONNECTING", ('-> YES', '<- NO'), print)) 
            .add(BackItem(display))
        )
        .add(MenuSetDateTime(display, 'DATE/TIME', print))
        .add(MenuSetTimer(display, 'LIGHT TIMER', print))
        .add(MenuList(display, 'HEATER AUTO')
            .add(ToggleItem(display, 'ACTIVATION', (config.get_status, 10), (config.toggle, 10)))
            .add(MenuHeaterManage(display, 'SETTING', print, visible=(config.get_status, 10)))
            .add(BackItem(display))
        )
        .add(MenuList(display, 'FILTER AUTO')
            .add(ToggleItem(display, 'ACTIVATION', (config.get_status, 11), (config.toggle, 11)))
            .add(MenuEnum(display, "RATE", ['1', '2', '3', '4', '6', '8', '12', '24'], print, visible=(config.get_status, 11)))
            .add(BackItem(display))
        )
                    .add(MenuConfirm(display, "RECOVERY", ('-> YES', '<- NO'), print)) 
        .add(BackItem(display))
    )



    .add(BackItem(display))    
)

menu.draw()

while True:
    key=0  
    if pot.read() > 2000:
        key=1
    if pot4.read() > 2000:
        key=2
    if pot2.read() > 2000:
        key=5
    if pot3.read() > 2000:
        key=4
    if pot1.read() > 2000:
        key=3      

    if key == 1: 
        menu.move(-1)
    if key == 2:
        menu.move(1)    
    if key == 5:
        menu.click() 
    if key == 4:     
        menu.shift(1)
    if key == 3:     
        menu.shift(-1)    

    sleep(0.1)
