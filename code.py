import board
import random

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.rgb import RGB
from kmk.modules.macros import Macros, Press, Release, Tap, Delay
from kmk.modules.layers import Layers
from kmk.modules.tapdance import TapDance
from kmk.modules.mouse_keys import MouseKeys

keyboard = KMKKeyboard()

keyboard.row_pins = (board.A0, board.A1)
keyboard.col_pins = (board.D2, board.D3, board.D4, board.D5)
keyboard.diode_orientation = DiodeOrientation.ROWS


keyboard.modules.append(Layers())

tapdance = TapDance()
tapdance.tap_time = 300
keyboard.modules.append(tapdance)

macros = Macros()
keyboard.modules.append(macros)


mouse_keys = MouseKeys(
    max_speed = 100,
)
keyboard.modules.append(mouse_keys)

class LayerRGB(RGB):
    def on_layer_change(self, layer):
        if layer == 0:
            self.set_hsv_fill(0, 0, 0)
        elif layer == 1:
            self.set_hsv_fill(170, 255, 255) # blue
        elif layer == 2:
            self.set_hsv_fill(43, 255, 255)  # yellow
        elif layer == 3:
            self.set_hsv_fill(0, 255, 255)   # red
        self.show()

class RGBLayers(Layers):
    def activate_layer(self, keyboard, layer, idx=None):
        super().activate_layer(keyboard, layer, idx)
        rgb.on_layer_change(layer)

    def deactivate_layer(self, keyboard, layer):
        super().deactivate_layer(keyboard, layer)
        rgb.on_layer_change(keyboard.active_layers[0])

keyboard.modules.append(RGBLayers())

rgb = LayerRGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    hue_default=0,
    sat_default=0,
    val_default=0,
)
keyboard.extensions.append(rgb)

def rgb_on(keyboard):
    rgb_ext = keyboard.extensions[0]
    rgb_ext.enable = True
    rgb_ext.set_hsv_fill(13, 255, 255)
    rgb_ext.show()
    return ""

def rgb_off(keyboard):
    rgb_ext = keyboard.extensions[0]
    rgb_ext.enable = False
    rgb_ext.show()
    return ""

def rgb_random(keyboard):
    rgb_ext = keyboard.extensions[0]
    rgb_ext.enable = True
    rgb_ext.set_hsv_fill(random.randint(0, 360), 255, 255)
    rgb_ext.show()
    return ""

VIBE_ON = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.SPACE),
    Release(KC.LGUI),
    "iTerm",
    Tap(KC.ENTER),
    Delay(500),
    Press(KC.LGUI),
    Tap(KC.N),
    Release(KC.LGUI),
    "DIR=~/Documents/vibe_code/$(date +\"%Y%m%d_%H%M%S\") && mkdir -p \"$DIR\" && cd \"$DIR\" && claude",
    Tap(KC.ENTER),
    rgb_on,
)

OPEN_TERMINAL = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.SPACE),
    Release(KC.LGUI),
    "iTerm",
    Tap(KC.ENTER),
    Delay(500),
    Press(KC.LGUI),
    Tap(KC.N),
    Release(KC.LGUI),
)

VTC = KC.MACRO(
    "vtc \"",
)

TOUCH_GRASS = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.SPACE),
    Release(KC.LGUI),
    "sleep",
    Tap(KC.ENTER),
)

CRLT_C = KC.MACRO(
    Press(KC.LCTL),
    Tap(KC.C),
    Release(KC.LCTL),
)

CLOSE_WINDOW = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.W),
    Release(KC.LGUI),
)

SWITCH_WINDOW = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.GRAVE),
    Release(KC.LGUI),
)

# Switch focus between apps (Cmd+Tab)
SWITCH_APP = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.TAB),
    Release(KC.LGUI),
)

# Move focused window to screen 2 and maximize (triggers Hammerspoon Ctrl+Alt+Cmd+9)
MOVE_SCREEN2_MAX = KC.MACRO(
    Press(KC.LCTL),
    Press(KC.LALT),
    Press(KC.LGUI),
    Tap(KC.N9),
    Release(KC.LGUI),
    Release(KC.LALT),
    Release(KC.LCTL),
)

RGB_RANDOM = KC.MACRO(
    rgb_random,
)

RGB_OFF = KC.MACRO(
    rgb_off,
)

CLAUDE_CHAT = KC.MACRO(
    Press(KC.LALT),
    Tap(KC.C),
    Release(KC.LALT),
)

CHAT_GPT_CHAT = KC.MACRO(
    Press(KC.LALT),
    Tap(KC.G),
    Release(KC.LALT),
)

OPEN_OLLAMA = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.SPACE),
    Release(KC.LGUI),
    "ollama",
    Tap(KC.ENTER),
)

RAYCAST = KC.MACRO(
    Press(KC.LGUI),
    Tap(KC.SPACE),
    Release(KC.LGUI),
)

# Triple tap ESC -> mouse layer (layer 3)
ESC_MOUSE_TD = KC.TD(
    KC.ESC,
    KC.ESC,
    KC.FD(3),
)

# Triple tap -> layer 2, single/double tap -> sleep
TOUCH_GRASS_TD = KC.TD(
    TOUCH_GRASS,
    TOUCH_GRASS,
    KC.FD(2),
)

# Triple tap ESC -> back to layer 0 (used in layer 2)
ESC_BACK_TD = KC.TD(
    KC.ESC,
    KC.ESC,
    KC.FD(0),
)

# Triple tap RMB -> back to layer 0 (used in layer 3)
RMB_LAYER_0 = KC.TD(
    KC.MB_RMB,
    KC.MB_RMB,
    KC.FD(0),
)

SLASH_LAYER_1 = KC.LT(1, KC.SLASH)

keyboard.keymap = [
    # Layer 0: Default
    [
        VIBE_ON,        SLASH_LAYER_1,  KC.UP,   ESC_MOUSE_TD,
        TOUCH_GRASS_TD, KC.RGUI,        KC.DOWN, KC.ENTER,
    ],

    # Layer 1: Terminal & editing
    [
        OPEN_TERMINAL, KC.SLASH,     VTC,     KC.BACKSPACE,
        SWITCH_WINDOW, CLOSE_WINDOW, CRLT_C,  KC.DQUO,
    ],

    # Layer 2: Window management (like layer 1 but with app switching & screen moves)
    [
        SWITCH_APP,       KC.SLASH,     VTC,     ESC_BACK_TD,
        MOVE_SCREEN2_MAX, CLOSE_WINDOW, CRLT_C,  KC.DQUO,
    ],

    # Layer 3: Mouse
    [
        KC.PGUP,   KC.MB_LMB,  KC.MS_UP,   RMB_LAYER_0,
        KC.PGDOWN, KC.MS_LEFT, KC.MS_DOWN, KC.MS_RIGHT,
    ],
]

if __name__ == '__main__':
    keyboard.go()
