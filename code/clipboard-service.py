"""Clipboard Service for Hermes Agent.

Handles platform-specific copy/paste operations.
Source: /Users/mac/.hermes/hermes-agent/cli.py
"""

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
