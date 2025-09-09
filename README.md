# PyOLEDMenu

A **MicroPython menu library** for OLED displays, featuring customizable pages and callback functions.

-----

## Installation

To install, simply place the `pymenu.py` file into the root directory of your MicroPython project or within the `/lib` folder.

-----

## Usage

First, you must initialize the display variable. This can be any display driver that supports `framebuf`, such as `ssd1306`.

Next, create the menu object, specifying the number of items to display on a single screen and the height of each item. For example, `4` lines with a height of `10px` each.

-----

## Menu Navigation

The `Menu` class provides several methods for navigating between menu pages and items:

  * `Menu.move(direction: -1|1)`: Moves the selection up or down.
  * `Menu.shift(direction: -1|1)`: Moves the selection to the right or left.
  * `Menu.click()`: Selects the current item and executes its associated callable function or navigates to another menu page.
  * `Menu.reset()`: Resets the current menu state and returns to the main screen.
  * `Menu.draw()`: Redraws the menu with its current state.

-----

## Menu Classes

This library includes a set of fundamental menu objects that can be used to construct your menu.

### MenuItems

This is the base class for all menu objects. It contains essential variables:

  * `name` (str): The name of the page, row, or button, which may be displayed on the screen.
  * `parent`: A reference to the parent menu object. The default value is `None`.
  * `display`: The display driver class used for drawing functions.
  * `visible`: A boolean value or a callable function that returns a boolean to control the visibility of the item. The default value is `None`. (For more details, see the **Visibility** section.)

Each subclass implements its own methods for specific functionality.

### `MenuView`

A child of `MenuItem`, this class provides the foundational methods for implementing menu screen behavior within a subclass.

### `MenuCallback`

A child of `MenuItem`, this class provides the foundational methods for implementing button behavior. It enables the execution of a method when a button is clicked. It also includes a `decorator` variable, which can be a static string or a callable function that returns a dynamic string, aligned to the right side of the screen.

### `MenuRow`

A child of `MenuCallback`, this class contains functions for drawing a row in a menu list.

### `MenuList`

A child of `MenuView`, this class represents a list menu page. It handles the rendering of the page and includes a method to add child menu pages to the list.

### `ToggleItem`

A child of `MenuCallback`, this class is a row within a list menu with built-in logic for handling toggle actions (e.g., on/off) and updating its decorator based on a state.

**Specific Arguments:**

  * `state_callback`: A callback to check the current state.
  * `change_callback`: A callback to toggle the current state (`True`/`False`).

### `BackItem`

A child of `MenuCallback`, this class provides the logic to navigate back to the previous menu page.

### `ListItem`

A child of `MenuRow`, this class is a wrapper for a list menu that contains the menu page to navigate to.

### `EnumItem`

A child of `MenuRow`, this class is a wrapper for a list menu that contains a set of choices. It includes logic to update the parent wrapper's decorator when a selection is made.

### `ConfirmItem`

A child of `MenuRow`, this class is a wrapper for a list menu that contains two options. When selected, it can trigger an action. This is useful for confirming a specific action. If the user selects the "no" option, the callback will not be triggered.

### `ButtonItem`

A child of `MenuRow`, this class is a button that executes an action with a parameter method.

### `MenuEnum`

A child of `MenuList`, this class represents a list menu page with an enumeration of selectable choices. Its decorator updates based on the selected item.

### `MenuConfirm`

A child of `MenuList`, this class represents a list menu page with a pair of choices (e.g., "yes" and "no").

**Specific Arguments:**

  * `items`: A tuple for the `yes` and `no` options, which overrides the default tuple `('yes', 'no')`.

### `MenuError`

A child of `MenuView`, this class represents an error page and handles its rendering.

### Custom Menu Pages

The repository provides several examples of custom menu pages that you can use as templates to create your own:

  * `MenuMonitoringSensor`
  * `MenuHeaterManage`
  * `MenuWifiInfo`
  * `MenuSetTimer`
  * `MenuSetDateTime`

-----

## Example Menu

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

-----

## Callbacks

Callbacks can be a single callable function if no parameters are needed. If parameters are required, a tuple should be used, where the first element is the callable and the second is a single argument or a tuple of arguments.

**Example 1: Single argument**

```python
CallbackItem('Print it!', (print, 'hello there'))
# This will call: print('hello there')
```

**Example 2: Tuple of arguments**

```python
CallbackItem('Print it!', (print, (1, 2, 3)))
# This will call: print(1, 2, 3)
```

-----

## Visibility

Any menu item can be hidden by setting the `visible` argument to `False` or by passing a callable function that returns `True` or `False` to dynamically check its visibility conditions.

-----

## Additional Information

You can try a live example of this menu on [Wokwi](https://wokwi.com/projects/418526558724341761).

This library is a fork of the original repository: [umenu](https://github.com/plugowski/umenu/tree/master).

-----

## License

Copyright (C) 2021, Paweł Ługowski

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
