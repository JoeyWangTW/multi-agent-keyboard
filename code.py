import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.rgb import RGB
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

# Shorthand for Hammerspoon grid hotkeys (Ctrl+Alt+Cmd+N)
def grid_key(n):
    return KC.LCTL(KC.LALT(KC.LGUI(getattr(KC, f'N{n}'))))

# Top-right TapDance: triple tap toggles layer 0 <-> layer 2
GRID4_TO_L2 = KC.TD(grid_key(4), grid_key(4), KC.FD(2))

# Layer 2: single/double = RMB, triple = back to grid
RMB_TO_L0 = KC.TD(KC.MB_RMB, KC.MB_RMB, KC.FD(0))

# Bottom-left Layer 0: hold = momentary layer 1, tap = move to screen 2 + maximize
SCREEN2_HOLD_L1 = KC.LT(1, grid_key(9))

keyboard.keymap = [
    # Layer 0: Window grid, hold bottom-left -> layer 1, triple tap top-right -> layer 2
    [
        grid_key(1),    grid_key(2), grid_key(3), GRID4_TO_L2,
        SCREEN2_HOLD_L1, grid_key(6), grid_key(7), grid_key(8),
    ],

    # Layer 1: Macros (momentary, active while holding bottom-left)
    [
        grid_key(0), grid_key(9), KC.UP,   KC.ESC,
        KC.TRNS,     KC.RGUI,     KC.DOWN, KC.ENTER,
    ],

    # Layer 2: Mouse, triple tap top-right -> back to layer 0
    [
        KC.PGUP,   KC.MB_LMB,  KC.MS_UP,   RMB_TO_L0,
        KC.PGDOWN, KC.MS_LEFT, KC.MS_DOWN, KC.MS_RIGHT,
    ],
]

if __name__ == '__main__':
    keyboard.go()
