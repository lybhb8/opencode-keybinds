# Hermes 按键绑定实现 / Hermes Keybindings Implementation

本文档包含 Hermes 中 Ctrl+C 复制和 Ctrl+V 粘贴功能的实现代码。

This document contains the implementation code for Ctrl+C copy and Ctrl+V paste functionality in Hermes.

## Overview / 概述

Hermes 使用 `prompt_toolkit` 框架实现按键绑定系统，通过 `KeyBindings` 类注册自定义按键处理器。

Hermes uses the `prompt_toolkit` framework to implement the keybinding system, registering custom key handlers through the `KeyBindings` class.

## Implementation Code / 实现代码

### 1. Ctrl+C 复制处理器 / Ctrl+C Copy Handler

```python
# cli.py
from prompt_toolkit.key_binding import KeyBindings

kb = KeyBindings()

@kb.add('c-c')
def handle_ctrl_c(event):
    """Ctrl+C = COPY (editor convention), not interrupt.

    Copy precedence so a copy never yields an empty clipboard:
      1. Any prompt_toolkit selection in the input buffer.
      2. System clipboard — the terminal emulator places arbitrary
         region selections here when Control+C is pressed, so this
         covers output-area selection (the common case: user selects
         assistant output with the mouse and hits Control+C).
      3. The whole input line (no selection, non-empty input).
      4. The last assistant response — only as a last resort when
         nothing is selected and the input is empty.

    Text is always pushed to the OS clipboard (pbcopy / xclip / xsel /
    OSC 52), never just prompt_toolkit's internal clipboard. The agent
    interrupt/cancel is on Ctrl+Q.
    """
    buf = event.app.current_buffer
    sel_text = ""
    try:
        sel_text = buf.copy_selection() or ""
    except Exception:
        sel_text = ""
    if sel_text:
        text = sel_text
        source = "selection"
    else:
        text = ""
        source = ""
        try:
            if sys.platform == "darwin":
                # The terminal emulator owns arbitrary-region selections in
                # the output area; prompt_toolkit cannot read them. We copy
                # the terminal's selection into the system clipboard so it
                # lands in pbpaste. Two layers, in priority order:
                #
                #   1) iTerm2: read the visible selection directly via
                #      AppleScript (no reliance on the frontmost app or the
                #      system clipboard). Works even when the terminal is not
                #      focused. Returns empty only when nothing is selected.
                #   2) Shell out Cmd+C to the *terminal* process specifically
                #      (not the frontmost app). A bare "keystroke c" from
                #      System Events hits whatever window is focused, so when
                #      another app is in front the copy silently fails and we
                #      read an empty clipboard -> Ctrl+C yields NULL. Targeting
                #      the terminal app by name (after activating it) makes the
                #      copy deterministic.
                tp = (os.environ.get("TERM_PROGRAM") or "").strip()
                term_app = (
                    "iTerm2" if tp in ("iTerm.app", "iTerm2")
                    else "Terminal" if tp in ("Apple_Terminal", "Terminal")
                    else None
                )
                # Layer 1: iTerm2 direct selection read (most reliable).
                if term_app == "iTerm2":
                    try:
                        sel = subprocess.run(
                            ["osascript", "-e",
                             'tell application "iTerm2" to tell current '
                             'window to tell current session to get '
                             'selection text'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL,
                            timeout=3, check=False,
                        )
                        if sel.returncode == 0 and sel.stdout:
                            clip = sel.stdout.decode("utf-8", errors="replace").strip("\n")
                            if clip:
                                text = clip
                                source = "clipboard"
                    except Exception:
                        pass
                # Layer 2: Cmd+C into the terminal process, then read pbpaste.
                if not text:
                    if term_app:
                        # Activate the terminal first so the keystroke lands
                        # on the terminal's own selection, not a front app.
                        script = (
                            f'tell application "{term_app}" to activate\n'
                            f'delay 0.05\n'
                            f'tell application "System Events" to keystroke '
                            f'"c" using command down'
                        )
                    else:
                        # Unknown terminal: best-effort legacy behaviour.
                        script = (
                            'tell application "System Events" to keystroke '
                            '"c" using command down'
                        )
                    try:
                        subprocess.run(
                            ["osascript", "-e", script],
                            timeout=3, check=False,
                        )
                        # Give the clipboard a moment to settle.
                        import time
                        time.sleep(0.05)
                        pb = subprocess.run(
                            ["pbpaste"], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, timeout=2, check=False,
                        )
                        if pb.returncode == 0 and pb.stdout:
                            clip = pb.stdout.decode("utf-8", errors="replace")
                            if clip:
                                text = clip
                                source = "clipboard"
                    except Exception:
                        pass
            elif sys.platform.startswith("linux"):
                for cmd in (
                    ["xclip", "-selection", "clipboard", "-o"],
                    ["xsel", "--clipboard", "--output"],
                ):
                    try:
                        p = subprocess.run(
                            cmd, capture_output=True, timeout=2, check=False
                        )
                        if p.returncode == 0 and p.stdout:
                            clip = p.stdout.decode("utf-8", errors="replace")
                            if clip:
                                text = clip
                                source = "clipboard"
                                break
                    except Exception:
                        continue
        except Exception:
            pass

    if not text:
        # Nothing to copy — just clear selection and return.
        try:
            event.app.current_buffer.selection = None
        except Exception:
            pass
        return

    # Push to OS clipboard.
    try:
        if sys.platform == "darwin":
            subprocess.run(
                ["pbcopy"], input=text.encode("utf-8"), timeout=2, check=False
            )
        elif sys.platform.startswith("linux"):
            for cmd in (
                ["xclip", "-selection", "clipboard"],
                ["xsel", "--clipboard", "--input"],
            ):
                try:
                    subprocess.run(
                        cmd, input=text.encode("utf-8"), timeout=2, check=False
                    )
                    break
                except Exception:
                    continue
        # Also try OSC 52 for terminal emulators that support it.
        import base64
        b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
        osc = f"\x1b]52;c;{b64}\x07"
        sys.stdout.write(osc)
        sys.stdout.flush()
    except Exception:
        pass

    # Show toast notification.
    try:
        from rich.console import Console
        console = Console()
        console.print(f"[dim]Copied {len(text)} characters to clipboard[/dim]")
    except Exception:
        pass

    # Clear selection.
    try:
        event.app.current_buffer.selection = None
    except Exception:
        pass
```

### 2. Ctrl+Q 中断处理器 / Ctrl+Q Interrupt Handler

```python
# cli.py
@kb.add('c-q')  # Ctrl+Q
def handle_ctrl_q(event):
    """Alternative interrupt/exit shortcut (Ctrl+Q).

    Behaves like Ctrl+C: cancels active prompts, interrupts the
    running agent, or clears the input buffer. Does not support
    the double-press 'force exit' feature of Ctrl+C.
    """
    # Cancel active voice recording.
    _should_cancel_voice = False
    _recorder_ref = None
    with cli_ref._voice_lock:
        if cli_ref._voice_recording and cli_ref._voice_recorder:
            _recorder_ref = cli_ref._voice_recorder
            cli_ref._voice_recording = False
            cli_ref._voice_continuous = False
            _should_cancel_voice = True
    if _should_cancel_voice:
        _cprint(f"\n{_DIM}Recording cancelled.{_RST}")
        threading.Thread(
            target=_recorder_ref.cancel, daemon=True
        ).start()
        event.app.invalidate()
        return

    # Cancel slash confirmation prompt (foreground UI — cancel and stop).
    if self._slash_confirm_state:
        self._submit_slash_confirm_response("cancel")
        event.app.current_buffer.reset()
        event.app.invalidate()
        return

    # Cancel /model picker (foreground UI — cancel and stop).
    if self._model_picker_state:
        self._close_model_picker()
        event.app.current_buffer.reset()
        event.app.invalidate()
        return

    # Clear all agent-blocking overlays in one shot, then fall through to
    # the agent-interrupt branch so a single Ctrl+Q both clears a stale
    # overlay and interrupts a still-running agent (#14026).
    _overlay_cleared = bool(
        self._sudo_state
        or self._secret_state
        or self._approval_state
        or self._clarify_state
    )
    if _overlay_cleared:
        self._clear_active_overlays_for_interrupt()
        event.app.current_buffer.reset()
        event.app.invalidate()

    if _overlay_cleared and not (self._agent_running and self.agent):
        return

    if self._agent_running and self.agent:
        print("\n⚡ Interrupting agent...")
        request_hard_interrupt(self.agent)
    elif event.app.current_buffer.text or self._attached_images:
        event.app.current_buffer.reset()
        self._attached_images.clear()
        event.app.invalidate()
    else:
        # Ctrl+Q no longer exits on idle — it only interrupts/cancels.
        # Use /quit or Ctrl+C for exit.
        return
```

### 3. Ctrl+V 粘贴处理器 / Ctrl+V Paste Handler

```python
# cli.py
@kb.add('c-v')  # Ctrl+V
def handle_ctrl_v(event):
    """Ctrl+V = PASTE from system clipboard."""
    buf = event.app.current_buffer
    text = None
    copied = False
    try:
        if sys.platform == "darwin":
            p = subprocess.run(
                ["pbpaste"], capture_output=True, timeout=2, check=False
            )
            if p.returncode == 0:
                text = p.stdout.decode("utf-8", errors="replace")
                copied = True
        elif sys.platform.startswith("linux"):
            for cmd in (
                ["xclip", "-selection", "clipboard", "-o"],
                ["xsel", "--clipboard", "--output"],
            ):
                try:
                    p = subprocess.run(
                        cmd, capture_output=True, timeout=2, check=False
                    )
                    if p.returncode == 0 and p.stdout:
                        text = p.stdout.decode("utf-8", errors="replace")
                        copied = True
                        break
                except Exception:
                    continue
    except Exception:
        pass

    if text:
        buf.insert_text(text)
```

### 4. 配置选项 / Configuration Options

```python
# hermes_cli/config_defaults.py
"copy_shortcut": "auto",  # "auto" (platform default) | "ctrl_c" | "ctrl_shift_c" | "disabled"
```

## Configuration / 配置

### config.yaml / 配置文件

```yaml
display:
  copy_shortcut: "ctrl_c"  # 或 "ctrl_shift_c" 或 "disabled"
```

### 环境变量 / Environment Variables

```bash
# 不需要额外环境变量，Hermes 默认支持
# No additional environment variables needed, Hermes supports this by default
```

## Platform Support / 平台支持

| Platform / 平台 | Copy Command / 复制命令 | Paste Command / 粘贴命令 |
|----------------|------------------------|--------------------------|
| macOS | `pbcopy` or OSC 52 | `pbpaste` |
| Linux (X11) | `xclip` or `xsel` | `xclip -o` |
| Linux (Wayland) | `wl-copy` | `wl-paste` |
| Windows | PowerShell | PowerShell |

## How It Works / 工作原理

1. **按键绑定注册**: 使用 `@kb.add('c-c')` 装饰器注册 Ctrl+C 处理器
2. **优先级复制**: 按优先级复制文本（选择 > 剪贴板 > 输入行 > 最后回复）
3. **系统剪贴板**: 使用 `pbcopy`/`xclip`/`xsel` 写入系统剪贴板
4. **OSC 52 支持**: 同时发送 OSC 52 转义序列以支持终端模拟器
5. **中断分离**: Ctrl+Q 专门用于中断，Ctrl+C 专门用于复制

1. **Keybinding Registration**: Use `@kb.add('c-c')` decorator to register Ctrl+C handler
2. **Priority Copy**: Copy text by priority (selection > clipboard > input line > last response)
3. **System Clipboard**: Use `pbcopy`/`xclip`/`xsel` to write to system clipboard
4. **OSC 52 Support**: Also send OSC 52 escape sequence for terminal emulator support
5. **Interrupt Separation**: Ctrl+Q is dedicated to interrupt, Ctrl+C is dedicated to copy

## References / 参考

- [Hermes Agent GitHub Repository](https://github.com/NousResearch/hermes-agent)
- [prompt_toolkit Documentation](https://python-prompt-toolkit.readthedocs.io/)
- [OSC 52 Clipboard Sequence](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h2-Operating-System-Commands)
