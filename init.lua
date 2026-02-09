-- ── Window Grid (KMK Keyboard) ──
-- Ctrl+Alt+Cmd+1‑8 snaps focused window to 2×4 grid on MacBook screen
--   [1] [2] [3] [4]
--   [5] [6] [7] [8]

local macScreen = 1  -- MacBook Built-in Retina Display (use screen ID, not name)

local grid = {
  -- Row 1
  {x=0,    y=0,   w=0.25, h=0.5},  -- key 1: top-left
  {x=0.25, y=0,   w=0.25, h=0.5},  -- key 2: top-center-left
  {x=0.5,  y=0,   w=0.25, h=0.5},  -- key 3: top-center-right
  {x=0.75, y=0,   w=0.25, h=0.5},  -- key 4: top-right
  -- Row 2
  {x=0,    y=0.5, w=0.25, h=0.5},  -- key 5: bottom-left
  {x=0.25, y=0.5, w=0.25, h=0.5},  -- key 6: bottom-center-left
  {x=0.5,  y=0.5, w=0.25, h=0.5},  -- key 7: bottom-center-right
  {x=0.75, y=0.5, w=0.25, h=0.5},  -- key 8: bottom-right
}

local mods = {"ctrl", "alt", "cmd"}

for i, rect in ipairs(grid) do
  hs.hotkey.bind(mods, tostring(i), function()
    local win = hs.window.focusedWindow()
    if not win then return end
    local screen = hs.screen.find(macScreen)
    if screen then
      win:moveToScreen(screen)
      win:moveToUnit(rect, 0)
    end
  end)
end


-- ── Move to Screen 2 + Maximize (KMK Layer 2) ──
-- Ctrl+Alt+Cmd+9 moves focused window to second screen and maximizes it

hs.hotkey.bind(mods, "9", function()
  local win = hs.window.focusedWindow()
  if not win then return end
  local screens = hs.screen.allScreens()
  if #screens > 1 then
    win:moveToScreen(screens[2])
    win:maximize(0)
  end
end)
