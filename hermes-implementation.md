# OpenCode Keybindings Implementation / OpenCode 按键绑定实现

This document contains the implementation code for Ctrl+C copy and Ctrl+V paste functionality in opencode, similar to how Hermes implements it.

本文档包含 opencode 中 Ctrl+C 复制和 Ctrl+V 粘贴功能的实现代码，类似于 Hermes 的实现方式。

## Overview / 概述

opencode uses a keybinding system with intercepts to handle keyboard shortcuts. The copy functionality is implemented through:

opencode 使用带拦截器的按键绑定系统来处理键盘快捷键。复制功能通过以下方式实现：

1. **Keybinding overrides** in `opencode.jsonc` modify default bindings
2. **Environment variable** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` enables the copy intercept
3. **Priority intercept** runs before default keybindings to handle copy

1. `opencode.jsonc` 中的**按键绑定覆盖**修改默认绑定
2. **环境变量** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` 启用复制拦截器
3. **优先级拦截器**在默认按键绑定之前运行以处理复制

## Implementation Code / 实现代码

### 1. Clipboard Service / 剪贴板服务

```typescript
// packages/tui/src/clipboard.ts
import { execFile, spawn } from "node:child_process"
import { readFile, rm } from "node:fs/promises"
import { platform, release, tmpdir } from "node:os"
import path from "node:path"
import { promisify } from "node:util"

const exec = promisify(execFile)

function command(command: string, args: string[] = [], input?: string) {
  return new Promise<Buffer>((resolve, reject) => {
    const child = spawn(command, args, { 
      stdio: [input === undefined ? "ignore" : "pipe", "pipe", "ignore"] 
    })
    const output: Buffer[] = []
    child.on("error", reject)
    child.stdout?.on("data", (chunk: Buffer) => output.push(chunk))
    child.on("close", (code) => {
      if (code === 0) return resolve(Buffer.concat(output))
      reject(new Error(`${command} exited with code ${code}`))
    })
    if (input !== undefined) child.stdin?.end(input)
  })
}

function writeOsc52(text: string) {
  if (!process.stdout.isTTY) return
  const sequence = `\x1b]52;c;${Buffer.from(text).toString("base64")}\x07`
  const passthrough = `\x1bPtmux;\x1b${sequence}\x1b\\`
  process.stdout.write(process.env.TMUX ? sequence + passthrough : process.env.STY ? passthrough : sequence)
}

export async function read() {
  if (platform() === "darwin") {
    const file = path.join(tmpdir(), "opencode-clipboard.png")
    try {
      await exec("osascript", [
        "-e",
        'set imageData to the clipboard as "PNGf"',
        "-e",
        `set fileRef to open for access POSIX file "${file}" with write permission`,
        "-e",
        "set eof fileRef to 0",
        "-e",
        "write imageData to fileRef",
        "-e",
        "close access fileRef",
      ])
      return { data: (await readFile(file)).toString("base64"), mime: "image/png" }
    } catch {
      // Fall through to text clipboard.
    } finally {
      await rm(file, { force: true }).catch(() => {})
    }
  }

  if (platform() === "win32" || release().includes("WSL")) {
    const script =
      "Add-Type -AssemblyName System.Windows.Forms; $img = [System.Windows.Forms.Clipboard]::GetImage(); if ($img) { $ms = New-Object System.IO.MemoryStream; $img.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png); [System.Convert]::ToBase64String($ms.ToArray()) }"
    const image = await command("powershell.exe", ["-NonInteractive", "-NoProfile", "-command", script]).catch(() =>
      Buffer.alloc(0),
    )
    if (image.length) return { data: image.toString().trim(), mime: "image/png" }
  }

  if (platform() === "linux") {
    const wayland = await command("wl-paste", ["-t", "image/png"]).catch(() => Buffer.alloc(0))
    if (wayland.length) return { data: wayland.toString("base64"), mime: "image/png" }
    const x11 = await command("xclip", ["-selection", "clipboard", "-t", "image/png", "-o"]).catch(() =>
      Buffer.alloc(0),
    )
    if (x11.length) return { data: x11.toString("base64"), mime: "image/png" }
  }

  const { default: clipboardy } = await import("clipboardy")
  const text = await clipboardy.read().catch(() => undefined)
  if (text) return { data: text, mime: "text/plain" }
}

export function copyCommand(
  os: NodeJS.Platform,
  wayland: boolean,
  has: (name: string) => boolean,
): string[] | undefined {
  if (os === "darwin" && has("osascript")) return ["osascript"]
  if (os === "linux" && wayland && has("wl-copy")) return ["wl-copy"]
  if (os === "linux" && has("xclip")) return ["xclip", "-selection", "clipboard"]
  if (os === "linux" && has("xsel")) return ["xsel", "--clipboard", "--input"]
  if (os === "win32" && has("powershell.exe")) {
    return [
      "powershell.exe",
      "-NonInteractive",
      "-NoProfile",
      "-Command",
      "[Console]::InputEncoding = [System.Text.Encoding]::UTF8; Set-Clipboard -Value ([Console]::In.ReadToEnd())",
    ]
  }
}

let copyMethod: Promise<(text: string) => Promise<void>> | undefined

function getCopyMethod() {
  return (copyMethod ??= (async () => {
    const { which } = await import("@opencode-ai/core/util/which")
    const native = copyCommand(platform(), Boolean(process.env.WAYLAND_DISPLAY), (name) => Boolean(which(name)))
    if (native?.[0] === "osascript") {
      return async (text: string) => {
        const escaped = text.replace(/\\/g, "\\\\").replace(/"/g, '\\"')
        await command("osascript", ["-e", `set the clipboard to "${escaped}"`]).catch(() => undefined)
      }
    }
    if (native) {
      return async (text: string) => {
        await command(native[0], native.slice(1), text).catch(() => undefined)
      }
    }
    return async (text: string) => {
      const { default: clipboardy } = await import("clipboardy")
      await clipboardy.write(text).catch(() => undefined)
    }
  })())
}

export async function write(text: string) {
  writeOsc52(text)
  const method = await getCopyMethod()
  await method(text)
}
```

### 2. Selection Handler / 选择处理器

```typescript
// packages/tui/src/util/selection.ts
import type { ClipboardService } from "../context/clipboard"

type Toast = {
  show: (input: { message: string; variant: "info" | "success" | "warning" | "error" }) => void
  error: (err: unknown) => void
}

type FocusableSelectionTarget = {
  hasSelection: () => boolean
  getClipboardText?: (text: string) => string
}

type Renderer = {
  getSelection: () => { getSelectedText: () => string; selectedRenderables: FocusableSelectionTarget[] } | null
  clearSelection: () => void
  currentFocusedRenderable?: FocusableSelectionTarget | null
}

type SelectionKeyEvent = {
  ctrl?: boolean
  name: string
  preventDefault: () => void
  stopPropagation: () => void
}

export function copy(renderer: Renderer, toast: Toast, clipboard: ClipboardService): boolean {
  const selection = renderer.getSelection()
  if (!selection) return false

  const text = selection.getSelectedText()
  if (!text) return false

  const focus = renderer.currentFocusedRenderable
  const clipboardText =
    focus?.getClipboardText && selection.selectedRenderables.includes(focus) ? focus.getClipboardText(text) : text

  clipboard
    ?.write?.(clipboardText)
    .then(() => toast.show({ message: "Copied to clipboard", variant: "info" }))
    .catch(toast.error)

  renderer.clearSelection()
  return true
}

export function handleSelectionKey(
  renderer: Renderer,
  toast: Toast,
  event: SelectionKeyEvent,
  clipboard: ClipboardService,
) {
  const selection = renderer.getSelection()
  if (!selection) return

  if (event.ctrl && event.name === "c") {
    if (!copy(renderer, toast, clipboard)) {
      renderer.clearSelection()
      return
    }

    event.preventDefault()
    event.stopPropagation()
    return
  }

  if (event.name === "escape") {
    renderer.clearSelection()
    event.preventDefault()
    event.stopPropagation()
    return
  }

  const focus = renderer.currentFocusedRenderable
  if (focus?.hasSelection() && selection.selectedRenderables.includes(focus)) return

  renderer.clearSelection()
}

export * as Selection from "./selection"
```

### 3. Keybinding Configuration / 按键绑定配置

```typescript
// packages/tui/src/config/keybind.ts
export const Definitions = {
  // ... other keybindings ...
  
  app_exit: keybind("ctrl+d,<leader>q", "Exit the application"),
  input_clear: keybind("none", "Clear input field"),
  input_paste: keybind({ key: "ctrl+v", preventDefault: false }, "Paste from clipboard"),
  
  // ... other keybindings ...
}
```

### 4. Application Integration / 应用集成

```typescript
// packages/tui/src/app.tsx
// Let selection copy/dismiss win ahead of normal bindings when explicit copy is required.
const offSelectionKeys = keymap.intercept(
  "key",
  ({ event }) => {
    if (!Flag.OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT) return
    Selection.handleSelectionKey(renderer, toast, event, clipboard)
  },
  { priority: 1 },
)
onCleanup(() => {
  offSelectionKeys()
  attention.dispose()
})

// Wire up console copy-to-clipboard via opentui's onCopySelection callback
renderer.console.onCopySelection = async (text: string) => {
  if (!text || text.length === 0) return

  await clipboard
    .write?.(text)
    .then(() => toast.show({ message: "Copied to clipboard", variant: "info" }))
    .catch(toast.error)

  renderer.clearSelection()
}
```

## Configuration / 配置

### Environment Variables / 环境变量

```bash
# Enable copy intercept on macOS/Linux / 在 macOS/Linux 上启用复制拦截
export OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT=1
```

### Config File / 配置文件

`~/.config/opencode/opencode.jsonc`:

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

## Platform Support / 平台支持

| Platform / 平台 | Copy Command / 复制命令 | Paste Command / 粘贴命令 |
|----------------|------------------------|--------------------------|
| macOS | `pbcopy` or OSC 52 | `pbpaste` |
| Linux (X11) | `xclip` or `xsel` | `xclip -o` |
| Linux (Wayland) | `wl-copy` | `wl-paste` |
| Windows | PowerShell | PowerShell |

## How It Works / 工作原理

1. **Keybinding Override**: The `app_exit` binding is changed from `ctrl+c,ctrl+d,<leader>q` to `ctrl+d,<leader>q`, removing `ctrl+c` from the exit binding.

2. **Input Clear Disabled**: The `input_clear` binding is set to `none`, removing the `ctrl+c` binding that was clearing the input field.

3. **Copy Intercept**: The `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` environment variable enables an intercept that runs before default keybindings. When `ctrl+c` is pressed and text is selected, the intercept copies the text to clipboard.

4. **Clipboard Service**: The clipboard service handles platform-specific copy/paste operations using system commands.

1. **按键绑定覆盖**：将 `app_exit` 绑定从 `ctrl+c,ctrl+d,<leader>q` 改为 `ctrl+d,<leader>q`，从退出绑定中移除 `ctrl+c`。

2. **禁用输入清除**：将 `input_clear` 绑定设置为 `none`，移除清除输入字段的 `ctrl+c` 绑定。

3. **复制拦截器**：`OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` 环境变量启用一个在默认按键绑定之前运行的拦截器。当按下 `ctrl+c` 且有选中文本时，拦截器会将文本复制到剪贴板。

4. **剪贴板服务**：剪贴板服务使用系统命令处理特定平台的复制/粘贴操作。

## References / 参考

- [opencode GitHub Repository](https://github.com/anomalyco/opencode)
- [Hermes Agent Keybindings](https://github.com/NousResearch/hermes-agent)
- [OpenTUI Keymap Documentation](https://github.com/anomalyco/opencode/tree/dev/packages/tui)
