---
name: opencode-keybinds
description: Configure Ctrl+C for copy and Ctrl+V for paste in opencode TUI.
version: 1.0.0
author: opencode user
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [keybinds, clipboard, productivity]
    category: configuration
---

# OpenCode Keybindings

Enable Ctrl+C for copy and Ctrl+V for paste in opencode TUI on macOS/Linux. Windows already supports this by default.

## When to Use

Use this skill when you want to:
- Enable Ctrl+C to copy selected text instead of exiting (macOS/Linux only)
- Enable Ctrl+V to paste from clipboard
- Customize opencode keybindings for better productivity

## Prerequisites

- opencode installed (version 1.0.0 or later)
- Terminal emulator with clipboard support (iTerm2, Terminal.app, etc.)
- For macOS: `pbcopy` and `pbpaste` commands (built-in)
- For Linux: `xclip`, `xsel`, or `wl-copy` installed

## Configuration

### Step 1: Update opencode configuration

Edit `~/.config/opencode/opencode.jsonc`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "keybinds": {
    "app_exit": "ctrl+d,<leader>q",
    "input_clear": "none",
    "input_paste": "ctrl+v"
  }
}
```

**What this does:**
- Removes `ctrl+c` from `app_exit` (now only `ctrl+d` and `<leader>q`)
- Disables `input_clear` binding (was also `ctrl+c`)
- Keeps `ctrl+v` as paste shortcut

### Step 2: Enable copy intercept (macOS/Linux only)

**Note: This step is only needed on macOS and Linux. Windows enables this by default.**

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT=1
```

Then reload:

```bash
source ~/.zshrc
```

**What this does:**
- Enables the intercept that handles Ctrl+C for copy when text is selected
- On Windows, this is enabled by default
- On macOS/Linux, this is disabled by default

### Step 3: Restart opencode

Quit and restart opencode for changes to take effect.

## Keybindings Reference

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Copy selected text to clipboard |
| `Ctrl+V` | Paste from clipboard |
| `Ctrl+D` | Exit application |
| `Ctrl+X` then `Q` | Exit application (Leader+Q) |
| `Ctrl+Y` | Copy selection (alternative) |

## How It Works

opencode uses a keybinding system with intercepts:

1. **Keybinding overrides** in `opencode.jsonc` modify default bindings
2. **Environment variable** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` enables the copy intercept
3. **Priority intercept** runs before default keybindings to handle copy

The copy functionality uses:
- macOS: `pbcopy` command or OSC 52 escape sequence
- Linux: `xclip`, `xsel`, or `wl-copy`
- Windows: PowerShell or OSC 52

## Hermes Comparison

This skill is inspired by the keybinding implementation in Hermes Agent. For detailed implementation code, see [hermes-implementation.md](hermes-implementation.md).

| Feature | Hermes | opencode |
|---------|--------|----------|
| Framework | prompt_toolkit | OpenTUI |
| Ctrl+C | Copy | Copy (requires config) |
| Ctrl+V | Paste | Paste |
| Interrupt | Ctrl+Q | Ctrl+D |
| Config | config.yaml | opencode.jsonc + env var |

## Verification

1. Start opencode
2. Type some text in the input field
3. Select the text with mouse or shift+arrow keys
4. Press `Ctrl+C` - should show "Copied to clipboard" message
5. Press `Ctrl+V` - should paste the copied text

## Troubleshooting

**Ctrl+C still exits opencode:**
- Verify `app_exit` in config doesn't include `ctrl+c`
- Check environment variable: `echo $OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT`
- Restart terminal and opencode

**Copy doesn't work:**
- Check clipboard tools: `which pbcopy` (macOS) or `which xclip` (Linux)
- Try `Ctrl+Y` as alternative copy shortcut

**Paste doesn't work:**
- Verify `input_paste` is set to `ctrl+v` in config
- Check clipboard content: `pbpaste` (macOS) or `xclip -o` (Linux)

## Quick Reference

```bash
# Check config
cat ~/.config/opencode/opencode.jsonc

# Check env var
echo $OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT

# Test clipboard (macOS)
echo "test" | pbcopy && pbpaste

# Test clipboard (Linux)
echo "test" | xclip -selection clipboard && xclip -o
```
