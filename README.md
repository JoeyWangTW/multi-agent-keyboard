# Window Grid Control Center

An 8-key macro keyboard that snaps the focused window into a 2×4 grid on your MacBook screen. Built for multitasking — kick off tasks on your main monitor and press a button to tile them on your secondary screen.

```
┌────────────────────────────────┐
│  [1]  │  [2]  │  [3]  │  [4]  │  ← top row
│───────┼───────┼───────┼───────│
│  [5]  │  [6]  │  [7]  │  [8]  │  ← bottom row
└────────────────────────────────┘
       MacBook Built-in Display
```

## How It Works

1. **KMK Keyboard** sends `Ctrl+Alt+Cmd+1–8` when you press each key
2. **Hammerspoon** listens for those hotkeys and snaps the focused window to the corresponding grid cell on your MacBook screen

## Hardware

- Any 2×4 matrix keyboard running [KMK](http://kmkfw.io/) on CircuitPython
- Tested with RP2040-based board (Adafruit KB2040, etc.)

### Wiring

| | Col 0 (D2) | Col 1 (D3) | Col 2 (D4) | Col 3 (D5) |
|---|---|---|---|---|
| **Row 0 (A0)** | Key 1 | Key 2 | Key 3 | Key 4 |
| **Row 1 (A1)** | Key 5 | Key 6 | Key 7 | Key 8 |

## Setup

### 1. KMK Firmware

Copy `kmk/code.py` to your CircuitPython board as `code.py`.

Make sure [KMK](http://kmkfw.io/docs/Getting_Started/) is installed on your board.

### 2. Hammerspoon

Install [Hammerspoon](https://www.hammerspoon.org/) if you haven't:

```bash
brew install --cask hammerspoon
```

Copy the window grid config to your Hammerspoon directory:

```bash
cp hammerspoon/init.lua ~/.hammerspoon/init.lua
```

> **Note:** If you already have a `~/.hammerspoon/init.lua`, merge the window grid section into your existing config (it's the block after the comment `-- ── Window Grid (KMK Keyboard) ──`).

Grant Hammerspoon **Accessibility** permissions:
- System Settings → Privacy & Security → Accessibility → Enable Hammerspoon

Reload the config: `Cmd+Alt+Ctrl+R` or Hammerspoon menu → Reload Config.

### 3. Configure Your Screen

The config finds your MacBook screen by ID (`1`). If windows aren't moving to the right screen, find your screen IDs in the Hammerspoon console:

```lua
for _, s in ipairs(hs.screen.allScreens()) do print(s:name(), s:id()) end
```

Then update the `macScreen` variable in `hammerspoon/init.lua`.

## Customization

### Different Grid Layouts

Edit the `grid` table in `hammerspoon/init.lua`. Values are unit rects (0–1 range):

```lua
-- Example: 2×2 grid (4 larger windows)
{x=0,   y=0,   w=0.5, h=0.5},  -- top-left
{x=0.5, y=0,   w=0.5, h=0.5},  -- top-right
{x=0,   y=0.5, w=0.5, h=0.5},  -- bottom-left
{x=0.5, y=0.5, w=0.5, h=0.5},  -- bottom-right
```

### Target a Different Screen

Change `macScreen` to your external monitor's ID or name:

```lua
local macScreen = "ROG XG27UQ"  -- by name
local macScreen = 4             -- by ID
```

## License

MIT
