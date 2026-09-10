"""Hermes Agent Keybindings Implementation.

This module implements Ctrl+C for copy, Ctrl+Q for interrupt, and Ctrl+V for paste.
Source: /Users/mac/.hermes/hermes-agent/cli.py
"""

from prompt_toolkit.key_binding import KeyBindings
from .clipboard import ClipboardService

kb = KeyBindings()


@kb.add('c-c')
def handle_ctrl_c(event):
    """Copy selected text to clipboard."""
    app = event.app
    focused = app.current_buffer
    if focused.selected_text:
        clipboard = ClipboardService()
        clipboard.write(focused.selected_text)
        focused.clear_selection()


@kb.add('c-q')
def handle_ctrl_q(event):
    """Interrupt running agent."""
    app = event.app
    if app.is_running:
        app.interrupt()


@kb.add('c-v')
def handle_ctrl_v(event):
    """Paste from system clipboard."""
    app = event.app
    focused = app.current_buffer
    clipboard = ClipboardService()
    text = clipboard.read()
    if text:
        focused.insert_text(text)
