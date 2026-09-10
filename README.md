# OpenCode Keybindings

Enable Ctrl+C for copy and Ctrl+V for paste in opencode TUI on macOS/Linux. Windows already supports this by default.

## Quick Start

### 1. Update opencode configuration

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

### 2. Enable copy intercept (macOS/Linux only)

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT=1
```

Then reload:

```bash
source ~/.zshrc
```

### 3. Restart opencode

Quit and restart opencode for changes to take effect.

## Keybindings

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Copy selected text to clipboard |
| `Ctrl+V` | Paste from clipboard |
| `Ctrl+D` | Exit application |
| `Ctrl+X` then `Q` | Exit application (Leader+Q) |
| `Ctrl+Y` | Copy selection (alternative) |

## Installation

### Option 1: Manual

```bash
mkdir -p ~/.opencode/skills/opencode-keybinds
cp SKILL.md ~/.opencode/skills/opencode-keybinds/
```

### Option 2: Git clone

```bash
cd ~/.opencode/skills
git clone https://github.com/lybhb8/opencode-keybinds.git
```

## Usage

Load this skill in opencode by referencing it:

```
@opencode-keybinds
```

## How It Works

opencode uses a keybinding system with intercepts:

1. **Keybinding overrides** in `opencode.jsonc` modify default bindings
2. **Environment variable** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` enables the copy intercept
3. **Priority intercept** runs before default keybindings to handle copy

The copy functionality uses:
- macOS: `pbcopy` command or OSC 52 escape sequence
- Linux: `xclip`, `xsel`, or `wl-copy`
- Windows: PowerShell or OSC 52

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

## License

MIT - see [LICENSE](LICENSE)
