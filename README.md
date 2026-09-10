#  "Control + C" Keybinings

[English](README.md) | [中文](README.zh.md)

Enable Ctrl+C for copy and Ctrl+V for paste in opencode TUI on macOS/Linux. Windows already supports this by default.

---

## Part 1: OpenCode

### Quick Start

#### 1. Update opencode configuration

Copy the config file:

```bash
cp config/opencode.jsonc ~/.config/opencode/opencode.jsonc
```

Or edit manually - see [config/opencode.jsonc](config/opencode.jsonc)

#### 2. Enable copy intercept (macOS/Linux only)

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT=1
```

Then reload:

```bash
source ~/.zshrc
```

#### 3. Restart opencode

Quit and restart opencode for changes to take effect.

### Keybindings

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Copy selected text to clipboard |
| `Ctrl+V` | Paste from clipboard |
| `Ctrl+D` | Exit application |
| `Ctrl+X` then `Q` | Exit application (Leader+Q) |
| `Ctrl+Y` | Copy selection (alternative) |

### Installation

```bash
# Manual
mkdir -p ~/.opencode/skills/opencode-keybinds
cp SKILL.md ~/.opencode/skills/opencode-keybinds/

# Or git clone
cd ~/.opencode/skills
git clone https://github.com/lybhb8/mac-ctrl-c.git
```

### Usage

```
@opencode-keybinds
```

### How It Works

opencode uses a keybinding system with intercepts:

1. **Keybinding overrides** in `opencode.jsonc` modify default bindings
2. **Environment variable** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` enables the copy intercept
3. **Priority intercept** runs before default keybindings to handle copy

The copy functionality uses:
- macOS: `pbcopy` command or OSC 52 escape sequence
- Linux: `xclip`, `xsel`, or `wl-copy`
- Windows: PowerShell or OSC 52

### Troubleshooting

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

---

## Part 2: Hermes

### Overview

Hermes Agent uses Python's `prompt_toolkit` library for keybinding management.

### Key Differences

| Feature | Hermes | opencode |
|---------|--------|----------|
| Framework | prompt_toolkit | OpenTUI |
| Ctrl+C | Copy | Copy (requires config) |
| Ctrl+V | Paste | Paste |
| Interrupt | Ctrl+Q | Ctrl+D |
| Config | config.yaml | opencode.jsonc + env var |

### Hermes Keybindings

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Copy selected text to clipboard |
| `Ctrl+V` | Paste from clipboard |
| `Ctrl+Q` | Interrupt running agent |

### Configuration

See [code/hermes-config.yaml](code/hermes-config.yaml)

### Implementation Code

- [code/hermes-keybindings.py](code/hermes-keybindings.py) - Keybinding handlers
- [code/clipboard-service.py](code/clipboard-service.py) - Clipboard operations

### Source Code Location

The Hermes keybinding implementation is located at:
- `/Users/mac/.hermes/hermes-agent/cli.py`
- Lines 17707-17800 (ctrl+c copy)
- Lines 18729-18795 (ctrl+q interrupt)
- Lines 18797+ (ctrl+v paste)

### References

- [Hermes Agent GitHub](https://github.com/NousResearch/hermes-agent)
- [prompt_toolkit Documentation](https://python-prompt-toolkit.readthedocs.io/)

---

## Quick Reference

```bash
# Check opencode config
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
