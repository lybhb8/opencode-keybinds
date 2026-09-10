# Hermes Keybindings Reference

This document contains the keybinding implementation details from Hermes Agent, which inspired the opencode keybindings skill.

## Overview

Hermes Agent uses Python's `prompt_toolkit` library for keybinding management. The keybindings are implemented in `cli.py`.

## Key Differences from opencode

| Feature | Hermes | opencode |
|---------|--------|----------|
| Framework | prompt_toolkit | OpenTUI |
| Ctrl+C | Copy | Copy (requires config) |
| Ctrl+V | Paste | Paste |
| Interrupt | Ctrl+Q | Ctrl+D |
| Config | config.yaml | opencode.jsonc + env var |

## Hermes Keybinding Implementation

### Ctrl+C = Copy (not interrupt)

```python
@kb.add('c-c')
def handle_ctrl_c(event):
    """Copy selected text to clipboard."""
    app = event.app
    focused = app.current_buffer
    if focused.selected_text:
        # Copy to clipboard
        clipboard = ClipboardService()
        clipboard.write(focused.selected_text)
        focused.clear_selection()
```

### Ctrl+Q = Interrupt (not exit)

```python
@kb.add('c-q')
def handle_ctrl_q(event):
    """Interrupt running agent."""
    app = event.app
    if app.is_running:
        app.interrupt()
```

### Ctrl+V = Paste

```python
@kb.add('c-v')
def handle_ctrl_v(event):
    """Paste from system clipboard."""
    app = event.app
    focused = app.current_buffer
    clipboard = ClipboardService()
    text = clipboard.read()
    if text:
        focused.insert_text(text)
```

## Hermes Configuration

In Hermes, keybindings are configured via `config.yaml`:

```yaml
# ~/.hermes/config.yaml
keybindings:
  copy: ctrl+c
  paste: ctrl+v
  interrupt: ctrl+q
```

## Clipboard Service (Hermes)

Hermes implements a clipboard service that handles platform-specific operations:

```python
import subprocess
import platform

class ClipboardService:
    def write(self, text: str):
        """Copy text to system clipboard."""
        system = platform.system()
        if system == "Darwin":  # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
        elif system == "Linux":
            try:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
            except FileNotFoundError:
                process = subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
        elif system == "Windows":
            # Use PowerShell on Windows
            command = f'echo {text} | clip'
            subprocess.run(command, shell=True)

    def read(self) -> str:
        """Read text from system clipboard."""
        system = platform.system()
        if system == "Darwin":  # macOS
            return subprocess.check_output(['pbpaste']).decode('utf-8')
        elif system == "Linux":
            try:
                return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode('utf-8')
            except FileNotFoundError:
                return subprocess.check_output(['xsel', '--clipboard', '--output']).decode('utf-8')
        elif system == "Windows":
            return subprocess.check_output(['powershell', '-command', 'Get-Clipboard']).decode('utf-8')
        return ""
```

## Source Code Location

The Hermes keybinding implementation is located at:
- `/Users/mac/.hermes/hermes-agent/cli.py`
- Lines 17707-17800 (ctrl+c copy)
- Lines 18729-18795 (ctrl+q interrupt)
- Lines 18797+ (ctrl+v paste)

## References

- [Hermes Agent GitHub](https://github.com/NousResearch/hermes-agent)
- [prompt_toolkit Documentation](https://python-prompt-toolkit.readthedocs.io/)
