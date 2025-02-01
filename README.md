# PyOLEDMenu
MicroPython Menu for Oled monitor with callbacks and customable menu pages. 

## Installation

Adding `pymenu.py` into your root dir, or just in a `/lib` folder. 

## Usage

The first thing to do is to initialize the display variable (can be any driver which supports `framebuf`, I use ssd1306).

Then create menu object, specify how many items you want to display on one screen and size of one element.
In my example I use 4 lines and 10px height each.

## Menu Navigation
To walk through menu pages or cells you have to trigger methods from `Menu` class.

- `Menu.move(direction: -1|1)` with go to up or down.
- `Menu.shift(direction: -1|1)` with go to right or left. 
- `Menu.click()` select current item and execute callable, or go into other menu pages.
- `Menu.reset()` reset current menu state and go to very beginning.
- `Menu.draw()` redraw menu with current state.

## Menu Classes
This package contains some basic Menu objects which can be used to build your menu.

### MenuItems
Low-level menu object, every objects inherit it. It contains principals variables like:
  - name (str): the page or row or button name, sometime it defines the visible nmme on screen;
  - parent: parent dependency, the default value is None;
  - display: class with draw functions;
  - visible: value or function that return a boolean to show the button or row, default value is None;
             (read more in Visibility section)
    
Futhermore, every class will implement its methods to work.

### `MenuView`
MenuItem's child, it contains functions to implements the menu screen behaviour in a child class.

### `MenuCallback`
MenuItem's child, it contains functions to implements the menu button behaviour in the child class.
It is posible to execute a method when a button is clicked and it contains the decorator variable that is a text or symbol aligned to right side of screen, can be also callable which return a dinamic symbol. 
Futhermore, there is also callback a callable method to trigger on click on item (more in section Callback).

### `MenuRow`
MenuCallback's child, it contains functions to draw a row in the menu list.

### `MenuList`
MenuView's child, it is the list menu page. It contains the rendering of the page and the method to add menu pages to visit in the list.  

### `ToggleItem`
MenuCallback's child, it is the row of a list menu with logic to handle toggles, like on/off actions to update the decorator.
In the click method there is the logic to update the row decorator when it is selected related a method result state. It is possible to specify state, and callback which will be called to change state.

**Specific Arguments:**
- `state_callback` - callback to check current state
- `change_callback` - callback to toggle current state (True/False)

### `BackItem`
MenuCallback's child, it is the row of a list menu with logic go back in the menu pages. 

### 'ListItem'
MenuRow's child, it is the wrapper row of a list menu that contains the menu page to go through.

### 'EnumItem'
MenuRow's child, it is the wrapper row of a list menu which contains a set of choices to select.
In the click method there is the logic when this row is selected to update the decorator of the parent's wrapper row. 

### `ConfirmItem`
MenuRow's child, it is the wrapper row of a list menu which contains a two options to select.
In the click method there is the logic when this row is selected to execute an action. 
Can be used when there is a need to confirm a specific action. If user select "no" option, callback won't be triggered.

### `ButtonItem`
MenuRow's child, it is the button to execute an action with a parameter method.

### 'MenuEnum'
MenuList's child, it is a list menu page with an enumerate of choices to select. Its decorator updating is based on your selected item.  

### 'MenuConfirm'
MenuList's child, it is a list menu page with a couple of choices to select.  
**Specific Arguments:**
- `items` - tuple for `yes` and `no`, it'll simply override default tuple ('yes', 'no')

### 'MenuError'
MenuView's child, it is the menu error page. It contains the rendering of the page.

### 'Custom menu page'
There are some custom menu pages like examples to create a own menu page. They are:
- MenuMonitoringSensor
- MenuHeaterManage
- MenuWifiInfo
- MenuSetTimer
- MenuSetDateTime
  
## Example menu
```python
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
    )
)
menu.draw()
```

## Callbacks

The callbacks can be single callable if no parameters should be passed, or tuple where wirst element is 
callable, and second is a single arg or tuple with `*args`. For example:

```python
CallbackItem('Print it!', (print, 'hello there'))
# will print: hello there > like print('hello there')
```

```python
CallbackItem('Print it!', (print, (1, 2, 3)))
# will print: 1 2 3 > like print(*args) where *args are taken from tuple
```

## Visibility

Every item can be hidden separately by setting named argument `visible` to False or
by passing callable to check conditions if element should be vissible. Callable should return True or False.

## More

It is possible to try it on:  
https://wokwi.com/projects/418526558724341761

The original repository is
https://github.com/plugowski/umenu/tree/master

## License

Copyright (C) 2021, Paweł Ługowski

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
