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
            self.set_hsv_fill(0, 0, 0)       # off (grid)
        elif layer == 1:
            self.set_hsv_fill(170, 255, 255)  # blue (macros)
        elif layer == 2:
            self.set_hsv_fill(0, 255, 255)    # red (mouse)
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

# Top-right TapDance: triple tap toggles layer 0 <-> layer 2
# Layer 0: single/double = grid pos 4, triple = mouse layer
GRID4_TO_L2 = KC.TD(
    KC.LCTL(KC.LALT(KC.LGUI(KC.N4))),
    KC.LCTL(KC.LALT(KC.LGUI(KC.N4))),
    KC.FD(2),
)

# Layer 2: single/double = RMB, triple = back to grid
RMB_TO_L0 = KC.TD(
    KC.MB_RMB,
    KC.MB_RMB,
    KC.FD(0),
)

# Bottom-left Layer 0: hold = momentary layer 1, tap = move to screen 2 + maximize
SCREEN2_HOLD_L1 = KC.LT(1, KC.LCTL(KC.LALT(KC.LGUI(KC.N9))))

keyboard.keymap = [
    # Layer 0: Window grid, hold bottom-left -> layer 1, triple tap top-right -> layer 2
    [
        KC.LCTL(KC.LALT(KC.LGUI(KC.N1))), KC.LCTL(KC.LALT(KC.LGUI(KC.N2))), KC.LCTL(KC.LALT(KC.LGUI(KC.N3))), GRID4_TO_L2,
        SCREEN2_HOLD_L1,                   KC.LCTL(KC.LALT(KC.LGUI(KC.N6))), KC.LCTL(KC.LALT(KC.LGUI(KC.N7))), KC.LCTL(KC.LALT(KC.LGUI(KC.N8))),
    ],

    # Layer 1: Macros (momentary, active while holding bottom-left)
    [
        KC.LCTL(KC.LALT(KC.LGUI(KC.N0))), KC.SLASH, KC.UP, KC.ESC,
        KC.TRNS,       KC.RGUI,   KC.DOWN, KC.ENTER,
    ],

    # Layer 2: Mouse, triple tap top-right -> back to layer 0
    [
        KC.PGUP,   KC.MB_LMB,  KC.MS_UP,   RMB_TO_L0,
        KC.PGDOWN, KC.MS_LEFT, KC.MS_DOWN, KC.MS_RIGHT,
    ],
]

if __name__ == '__main__':
    keyboard.go()
