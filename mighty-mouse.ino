#include <Mouse.h>
#include <Keyboard.h>

// === Buttons includes
#include <Button.h>
#include <ButtonEventCallback.h>
#include <PushButton.h>
#include <Bounce2.h>

// === Display includes
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

const int JOYSTICK_X        = A0;
const int JOYSTICK_Y        = A1;
const int JOYSTICK_PADDING  = 10; // Dead zone to avoid jitter
const int BUTTON_MODE       = 4;
const int SPEED_REDUCTION   = 20; // More is slower
const int MOVE_DELAY        = 20; // More is slower
const int SCROLL_DELAY      = 20; // More is slower
const int SCROLL_VALUE      = 2;  // More is faster
const int BTN_HOLD_DELAY    = 300; // Milliseconds
const float MOUSE_OS_SPEED  = 2.4; // To compensate for OS mouse acceleration settings

const int MODE_PAN   = 1;
const int MODE_ORBIT = 2;
const int MODE_ZOOM  = 3;

PushButton btn_mode = PushButton(BUTTON_MODE, ENABLE_INTERNAL_PULLUP);

float displacedX = 0;
float displacedY = 0;
int currentMode = MODE_PAN;
int previousMode = MODE_PAN;
bool isMoving = false;

void setup() {
  // Init I2C display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Address 0x3C for 128x32 display

  //Init mouse and keyboard emulation
  Mouse.begin();
  Keyboard.begin();

  // Set mode button listeners
  btn_mode.onHold(BTN_HOLD_DELAY, onModeButtonHeld);
  btn_mode.onRelease(onModeButtonReleased);

  // Display the current mode
  displayMode();
}

void loop() {
  btn_mode.update();
  readJoystickValues();
}

void onModeButtonHeld(Button& btn){
  if(currentMode != MODE_ZOOM){
    previousMode = currentMode;
    currentMode = MODE_ZOOM;
  }

  displayMode();
}

void onModeButtonReleased(Button& btn, uint16_t duration){
  // Ignore when coming from a held button (Zoom mode)
  if(duration < BTN_HOLD_DELAY){
    switch(currentMode){
      case MODE_PAN:
        currentMode = MODE_ORBIT;
        break;
      case MODE_ORBIT:
        currentMode = MODE_PAN;
        break;
      case MODE_ZOOM:
        currentMode = previousMode;
        break;
    }
  }

  displayMode();
}

void readJoystickValues(){
  // The Mouse.move() function accepts a "signed char" (-128 to +127)
  // Convert joystick values (from 0 to 1023) to valid mouse values (from -127 to 127)
  int dX = map(analogRead(JOYSTICK_X), 0, 1023, -127, 127);
  int dY = map(analogRead(JOYSTICK_Y), 0, 1023, -127, 127);

  // Padding is used to prevent jitter
  if((abs(dX) >= JOYSTICK_PADDING) || (abs(dY) >= JOYSTICK_PADDING)){
    if(isMoving == false){
      isMoving = true;
      onStartMoving();
    }

    onMoving(dX, dY);
  } else if((abs(dX) < JOYSTICK_PADDING / 2) && (abs(dY) < JOYSTICK_PADDING / 2)){ // Lower threshold for debounce
    if(isMoving == true){
      isMoving = false;
      onStopMoving();
    }
  }
}

void onStartMoving(){
  displacedX = 0; // Reset X displacement
  displacedY = 0; // Reset Y displacement

  switch(currentMode){
    case MODE_PAN:
      Mouse.press(MOUSE_MIDDLE);
      break;
    case MODE_ORBIT:
      Keyboard.press(KEY_LEFT_SHIFT);
      Mouse.press(MOUSE_MIDDLE);
      break;
  }
}

void onMoving(int valX, int valY){
  int reducedX = valX / SPEED_REDUCTION;
  int reducedY = valY / SPEED_REDUCTION;

  switch(currentMode){
    case MODE_PAN:
    case MODE_ORBIT:
      Mouse.move(reducedX, reducedY);
      displacedX += reducedX;
      displacedY += reducedY;
      delay(MOVE_DELAY);
      break;
    case MODE_ZOOM:
      Mouse.move(0, 0, reducedY / SCROLL_VALUE * -1); // Inver axis
      delay(SCROLL_DELAY);
      break;
  }
}

void onStopMoving(){
  switch(currentMode){
    case MODE_PAN:
      Mouse.release(MOUSE_MIDDLE);
      moveToOrigin(displacedX, displacedY);
      break;
    case MODE_ORBIT:
      Keyboard.releaseAll();
      Mouse.release(MOUSE_MIDDLE);
      moveToOrigin(displacedX, displacedY);
      break;
  }
}

void moveToOrigin(int displacedX, int displacedY){
  // The Mouse library does not accept numbers on a range outside -127 to 127,
  // so we have to move several times to reach the origin
  int timesX = abs(displacedX / 127);
  int remainingX = ((displacedX % 127) * -1) / MOUSE_OS_SPEED; // Change symbol so it goes in the opposite direction
  int timesY = abs(displacedY / 127);
  int remainingY = ((displacedY % 127) * -1) / MOUSE_OS_SPEED; // Change symbol so it goes in the opposite direction
  int value = 127 / MOUSE_OS_SPEED; // Take into account OS mouse settings

  if(displacedX > 0){
    // Move left to go back to the origin
    for(int i=0; i < timesX; i++){
      Mouse.move(value * -1, 0);
    }
  } else {
    // Move right to go back to the origin
    for(int i=0; i < timesX; i++){
      Mouse.move(value, 0);
    }
  }

  if(displacedY > 0){
    // Move down to go back to the origin
    for(int i=0; i < timesY; i++){
      Mouse.move(0, value * -1);
    }
  } else {
    // Move up to go back to the origin
    for(int i=0; i < timesY; i++){
      Mouse.move(0, value);
    }
  }

  // Move the remaining positions
  Mouse.move(remainingX, 0);
  Mouse.move(0, remainingY);
}

void displayMode() {
  display.clearDisplay();

  display.setTextSize(1); // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(0, 0); // Start at top-left corner
  display.cp437(true); // Use full 256 char 'Code Page 437' font

  switch(currentMode){
    case MODE_PAN:
      display.println(F("MODE: Pan"));
      break;
    case MODE_ORBIT:
      display.println(F("MODE: Orbit"));
      break;
    case MODE_ZOOM:
      display.println(F("MODE: Zoom"));
      break;
  }

  display.display();
}
