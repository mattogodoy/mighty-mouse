# Mighty Mouse

An open source 3D mouse inspired in the 3Dconnexion SpaceMouse Compact.

![Mighty Mouse](img/mighty_mouse.jpeg?raw=true "Title")

## How it works

The idea is to make a plug & play USB device that requires no driver installation in the host computer and works in all operative systems.

![Mighty Mouse in real life](img/mm.jpg?raw=true "Title")

To achieve this, an Arduino Pro Micro is used to emulate a regular mouse and keyboard. The mouse is used to preform clicks, move the pointer and spin the mouse wheel. The keyboard is to perform key presses.

There are 3 different modes:

- **Pan**: For panning the 3D model. This mode is selected by default.
- **Orbit**: For spinning the 3D model. You can set this mode by a single click of the mode button.
- **Zoom**: For zooming in and out. Moving the joystick up zooms in and down zooms out. You can set this mode by long-pressing the mode button. With a single click while in zoom mode, you go back to the same mode you had previously.

The current mode is shown un the OLED display.

## Compatible CAD software

The Mighty Mouse has been created with Autodesk Fusion 360 in mind. It is currently the only compatible software, but it's very easy to change the code and adapt it to be used in many others.

## Setup

The project is Arduino based, so all you need is the Arduino IDE.

Some libraries are required. Most of them are already included in the Arduino IDE. The rest can be installed from the IDE using the library manager:

- [r89m Push Button](https://github.com/r89m/PushButton): For the mode change button
- [Adafruit GFX](https://github.com/adafruit/Adafruit-GFX-Library): The graphics library for the OLED display
- [Adafruit_SSD1306](https://github.com/adafruit/Adafruit_SSD1306): The drivers for the OLED display

## Drawbacks

Nothing is perfect...

### Single pointer

Since the Mighty Mouse acts as a regular USB mouse, it moves your pointer. This means you can't use both the Mighty Mouse and your regular mouse / trackpad at the same time.

Ideally you should stop moving your regular mouse while using the Mighty Mouse. It should not be a big deal.

### Mouse accelleration

To make the problem of the single pointer a bit less painfull, what Mighty Mouse does is to return the position of the pointer of where it was before it started moving.

The only problem with this is that most modern operative systems have settings for mouse speed and acceleration, which causes an undesired effect when returning the pointer to the original position.

There are two ways to fix this:

1. Reduce / disable mouse acceleration: If you turn off (or set to the minimum) mouse pointer speed, this is no longer an issue and Mighty Mouse returns to the origin perfectly every time. The problem is that those settings will affect your real mouse (unless you use a trackpad). If you shoose this option, set the variable `MOUSE_OS_SPEED` to `1`.
2. Adjust for your speeds: If you actually want to set mouse speeds in your operative system (which is the most probable) you can adjust the `MOUSE_OS_SPEED` variable to a value that works for you. I've found that in a MacBook laptop with around 75% mouse speed, a value of `2.4` is perfect. You can adjust the value in the code until the pointer goes back to the origin with no overshoot or being short.

### Screen size

Since Mighty Mouse is not different than a regular USB mouse, the pointer cannot exceed the limits of the screen. This means that you can't pan or orbit a model indefinitely. If the pointer reaches the end of the screen, it will stop and so will the model movement.

Moving the pointer to the center of the screen before using the Mighty Mouse is usually enough to pan or orbit a 3D model.

## Bill of materials

The required materials are few, cheap and widely available:

- Arduino Pro Micro
- Dual axis joystick
- 128x32 SPI OLED display

## Wiring

The power for the entire circuit is provided by the USB cable.

| Arduino pin | Connected to |
|-------------|--------------|
| VCC         | Display VCC  |
| VCC         | Joystick 5V  |
| GND         | Display GND  |
| GND         | Joystick GND |
| 2           | Display SDA  |
| 3           | Display SCK  |
| 4           | Joystick SW  |
| A0          | Joystick VRx |
| A1          | Joystick VRy |

## Enclosure

The enclosure is designed to be printed in an SLA (resine) printer.

Fun fact: I used the prototype of the Mighty Mouse in a breadboard to design its own enclosure.

You can find the STL files of the enclosure in the `stl` directory of this repository.

You can also find the files in Thingiverse:
TODO: Link to thingiverse

## Next steps

This is an open source project and, as such, pull requests and suggestions are more than welcome.

There is plenty of room for improvements in this project. Some of the features I'd like to see in the future are:

- **Profiles**: The ability to change between profiles to add compatibility with other CAD software and be able to easily switch between them.
- **GUI**: Having the OLED display is a grat advantage. A graphical user interface could be really useful for things like adjusting some settings like the speed, or selecting profiles.
- **Drivers**: Right now Mighty Mouse is an open loop system. This means that it has no feedback of what's happening in the computer screen. Installing drivers in the host computer would allow to make it a closed loop system and open the door to fix all of the aforementioned drawbacks. On the other hand it woul add complexity to the project.

## License

This project is under the v3 of the [GNU's General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).
