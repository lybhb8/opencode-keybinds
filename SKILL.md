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

# macOS/Linux 上启用 opencode Ctrl+C 复制和 Ctrl+V 粘贴

Enable Ctrl+C for copy and Ctrl+V for paste in opencode TUI on macOS/Linux. Windows already supports this by default.

在 macOS/Linux 上启用 opencode TUI 中 Ctrl+C 复制和 Ctrl+V 粘贴功能。Windows 默认已支持此功能。

## When to Use / 使用场景

Use this skill when you want to:
- Enable Ctrl+C to copy selected text instead of exiting (macOS/Linux only)
- Enable Ctrl+V to paste from clipboard
- Customize opencode keybindings for better productivity

使用此技能当您想要：
- 启用 Ctrl+C 复制选中文本而不是退出（仅 macOS/Linux）
- 启用 Ctrl+V 从剪贴板粘贴
- 自定义 opencode 按键绑定以提高生产力

## Prerequisites / 前置要求

- opencode installed (version 1.0.0 or later)
- Terminal emulator with clipboard support (iTerm2, Terminal.app, etc.)
- For macOS: `pbcopy` and `pbpaste` commands (built-in)
- For Linux: `xclip`, `xsel`, or `wl-copy` installed

- 已安装 opencode（版本 1.0.0 或更高）
- 支持剪贴板的终端模拟器（iTerm2、Terminal.app 等）
- macOS：内置 `pbcopy` 和 `pbpaste` 命令
- Linux：已安装 `xclip`、`xsel` 或 `wl-copy`

## How to Configure / 配置方法

### Step 1: Update opencode configuration / 更新 opencode 配置

Edit `~/.config/opencode/opencode.jsonc`:

编辑 `~/.config/opencode/opencode.jsonc`：

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

**What this does: / 配置说明：**
- Removes `ctrl+c` from `app_exit` (now only `ctrl+d` and `<leader>q`)
- Disables `input_clear` binding (was also `ctrl+c`)
- Keeps `ctrl+v` as paste shortcut

- 从 `app_exit` 中移除 `ctrl+c`（现在只有 `ctrl+d` 和 `<leader>q`）
- 禁用 `input_clear` 绑定（原来也是 `ctrl+c`）
- 保留 `ctrl+v` 作为粘贴快捷键

### Step 2: Enable copy intercept (macOS/Linux only) / 启用复制拦截（仅 macOS/Linux）

**Note: This step is only needed on macOS and Linux. Windows enables this by default.**

**注意：此步骤仅在 macOS 和 Linux 上需要。Windows 默认启用此功能。**

Add to `~/.zshrc` or `~/.bashrc`:

添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
export OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT=1
```

Then reload / 然后重新加载：

```bash
source ~/.zshrc
```

**What this does: / 配置说明：**
- Enables the intercept that handles Ctrl+C for copy when text is selected
- On Windows, this is enabled by default
- On macOS/Linux, this is disabled by default (the issue you encountered)

- 启用处理 Ctrl+C 复制选中文本的拦截器
- Windows 上默认启用此功能
- macOS/Linux 上默认禁用（您遇到的问题）

### Step 3: Restart opencode / 重启 opencode

Quit and restart opencode for changes to take effect.

退出并重启 opencode 使配置生效。

## Keybindings Reference / 按键绑定参考

| Shortcut / 快捷键 | Action / 操作 |
|----------|--------|
| `Ctrl+C` | Copy selected text to clipboard / 复制选中文本到剪贴板 |
| `Ctrl+V` | Paste from clipboard / 从剪贴板粘贴 |
| `Ctrl+D` | Exit application / 退出应用 |
| `Ctrl+X` then `Q` | Exit application (Leader+Q) / 退出应用（Leader+Q） |
| `Ctrl+Y` | Copy selection (alternative) / 复制选中文本（替代方案） |

## How It Works / 工作原理

opencode uses a keybinding system with intercepts:

opencode 使用带拦截器的按键绑定系统：

1. **Keybinding overrides** in `opencode.jsonc` modify default bindings
2. **Environment variable** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` enables the copy intercept
3. **Priority intercept** runs before default keybindings to handle copy

1. `opencode.jsonc` 中的**按键绑定覆盖**修改默认绑定
2. **环境变量** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` 启用复制拦截器
3. **优先级拦截器**在默认按键绑定之前运行以处理复制

The copy functionality uses:
- macOS: `pbcopy` command or OSC 52 escape sequence
- Linux: `xclip`, `xsel`, or `wl-copy`
- Windows: PowerShell or OSC 52

复制功能使用：
- macOS：`pbcopy` 命令或 OSC 52 转义序列
- Linux：`xclip`、`xsel` 或 `wl-copy`
- Windows：PowerShell 或 OSC 52

## Hermes Implementation / Hermes 实现

This skill is based on the keybinding implementation in Hermes Agent. For detailed implementation code, see [hermes-implementation.md](hermes-implementation.md).

此技能基于 Hermes Agent 中的按键绑定实现。详细的实现代码请参阅 [hermes-implementation.md](hermes-implementation.md)。

### Key Differences / 主要区别

| Feature / 功能 | Hermes / Hermes | opencode / opencode |
|----------------|----------------|---------------------|
| Framework / 框架 | prompt_toolkit | OpenTUI |
| Ctrl+C / Ctrl+C | Copy / 复制 | Copy / 复制（需要配置） |
| Ctrl+V / Ctrl+V | Paste / 粘贴 | Paste / 粘贴 |
| Interrupt / 中断 | Ctrl+Q | Ctrl+D |
| Configuration / 配置 | config.yaml | opencode.jsonc + 环境变量 |

### Hermes Keybindings / Hermes 按键绑定

```python
# Ctrl+C = Copy (not interrupt)
@kb.add('c-c')
def handle_ctrl_c(event):
    # Copy selected text to clipboard
    # 复制选中文本到剪贴板

# Ctrl+Q = Interrupt (not exit)
@kb.add('c-q')
def handle_ctrl_q(event):
    # Interrupt running agent
    # 中断运行中的 agent

# Ctrl+V = Paste
@kb.add('c-v')
def handle_ctrl_v(event):
    # Paste from system clipboard
    # 从系统剪贴板粘贴
```

## Hermes Implementation / Hermes 实现

This skill is based on the keybinding implementation in Hermes Agent. For detailed implementation code, see [hermes-implementation.md](hermes-implementation.md).

此技能基于 Hermes Agent 中的按键绑定实现。详细的实现代码请参阅 [hermes-implementation.md](hermes-implementation.md)。

### Key Differences / 主要区别

| Feature / 功能 | Hermes / Hermes | opencode / opencode |
|----------------|----------------|---------------------|
| Framework / 框架 | prompt_toolkit | OpenTUI |
| Ctrl+C / Ctrl+C | Copy / 复制 | Copy / 复制（需要配置） |
| Ctrl+V / Ctrl+V | Paste / 粘贴 | Paste / 粘贴 |
| Interrupt / 中断 | Ctrl+Q | Ctrl+D |
| Configuration / 配置 | config.yaml | opencode.jsonc + 环境变量 |

### Hermes Keybindings / Hermes 按键绑定

```python
# Ctrl+C = Copy (not interrupt)
@kb.add('c-c')
def handle_ctrl_c(event):
    # Copy selected text to clipboard
    # 复制选中文本到剪贴板

# Ctrl+Q = Interrupt (not exit)
@kb.add('c-q')
def handle_ctrl_q(event):
    # Interrupt running agent
    # 中断运行中的 agent

# Ctrl+V = Paste
@kb.add('c-v')
def handle_ctrl_v(event):
    # Paste from system clipboard
    # 从系统剪贴板粘贴
```

## Hermes Implementation / Hermes 实现

This skill is based on the keybinding implementation in Hermes Agent. For detailed implementation code, see [hermes-implementation.md](hermes-implementation.md).

此技能基于 Hermes Agent 中的按键绑定实现。详细的实现代码请参阅 [hermes-implementation.md](hermes-implementation.md)。

### Key Differences / 主要区别

| Feature / 功能 | Hermes / Hermes | opencode / opencode |
|----------------|----------------|---------------------|
| Framework / 框架 | prompt_toolkit | OpenTUI |
| Ctrl+C / Ctrl+C | Copy / 复制 | Copy / 复制（需要配置） |
| Ctrl+V / Ctrl+V | Paste / 粘贴 | Paste / 粘贴 |
| Interrupt / 中断 | Ctrl+Q | Ctrl+D |
| Configuration / 配置 | config.yaml | opencode.jsonc + 环境变量 |

### Hermes Keybindings / Hermes 按键绑定

```python
# Ctrl+C = Copy (not interrupt)
@kb.add('c-c')
def handle_ctrl_c(event):
    # Copy selected text to clipboard
    # 复制选中文本到剪贴板

# Ctrl+Q = Interrupt (not exit)
@kb.add('c-q')
def handle_ctrl_q(event):
    # Interrupt running agent
    # 中断运行中的 agent

# Ctrl+V = Paste
@kb.add('c-v')
def handle_ctrl_v(event):
    # Paste from system clipboard
    # 从系统剪贴板粘贴
```

## Hermes Implementation / Hermes 实现

This skill is based on the keybinding implementation in Hermes Agent. For detailed implementation code, see [hermes-implementation.md](hermes-implementation.md).

此技能基于 Hermes Agent 中的按键绑定实现。详细的实现代码请参阅 [hermes-implementation.md](hermes-implementation.md)。

### Key Differences / 主要区别

| Feature / 功能 | Hermes / Hermes | opencode / opencode |
|----------------|----------------|---------------------|
| Framework / 框架 | prompt_toolkit | OpenTUI |
| Ctrl+C / Ctrl+C | Copy / 复制 | Copy / 复制（需要配置） |
| Ctrl+V / Ctrl+V | Paste / 粘贴 | Paste / 粘贴 |
| Interrupt / 中断 | Ctrl+Q | Ctrl+D |
| Configuration / 配置 | config.yaml | opencode.jsonc + 环境变量 |

### Hermes Keybindings / Hermes 按键绑定

```python
# Ctrl+C = Copy (not interrupt)
@kb.add('c-c')
def handle_ctrl_c(event):
    # Copy selected text to clipboard
    # 复制选中文本到剪贴板

# Ctrl+Q = Interrupt (not exit)
@kb.add('c-q')
def handle_ctrl_q(event):
    # Interrupt running agent
    # 中断运行中的 agent

# Ctrl+V = Paste
@kb.add('c-v')
def handle_ctrl_v(event):
    # Paste from system clipboard
    # 从系统剪贴板粘贴
```

## Hermes Implementation / Hermes 实现

This skill is based on the keybinding implementation in Hermes Agent. For detailed implementation code, see [hermes-implementation.md](hermes-implementation.md).

此技能基于 Hermes Agent 中的按键绑定实现。详细的实现代码请参阅 [hermes-implementation.md](hermes-implementation.md)。

### Key Differences / 主要区别

| Feature / 功能 | Hermes / Hermes | opencode / opencode |
|----------------|----------------|---------------------|
| Framework / 框架 | prompt_toolkit | OpenTUI |
| Ctrl+C / Ctrl+C | Copy / 复制 | Copy / 复制（需要配置） |
| Ctrl+V / Ctrl+V | Paste / 粘贴 | Paste / 粘贴 |
| Interrupt / 中断 | Ctrl+Q | Ctrl+D |
| Configuration / 配置 | config.yaml | opencode.jsonc + 环境变量 |

### Hermes Keybindings / Hermes 按键绑定

```python
# Ctrl+C = Copy (not interrupt)
@kb.add('c-c')
def handle_ctrl_c(event):
    # Copy selected text to clipboard
    # 复制选中文本到剪贴板

# Ctrl+Q = Interrupt (not exit)
@kb.add('c-q')
def handle_ctrl_q(event):
    # Interrupt running agent
    # 中断运行中的 agent

# Ctrl+V = Paste
@kb.add('c-v')
def handle_ctrl_v(event):
    # Paste from system clipboard
    # 从系统剪贴板粘贴
```

## Verification / 验证方法

1. Start opencode
2. Type some text in the input field
3. Select the text with mouse or shift+arrow keys
4. Press `Ctrl+C` - should show "Copied to clipboard" message
5. Press `Ctrl+V` - should paste the copied text

1. 启动 opencode
2. 在输入框中输入一些文本
3. 使用鼠标或 Shift+方向键选中文本
4. 按 `Ctrl+C` - 应显示"已复制到剪贴板"消息
5. 按 `Ctrl+V` - 应粘贴复制的文本

## Troubleshooting / 故障排除

**Ctrl+C still exits opencode: / Ctrl+C 仍然退出 opencode：**
- Verify `app_exit` in config doesn't include `ctrl+c`
- Check environment variable is set: `echo $OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT`
- Restart terminal and opencode
- **Note: This is a known issue on macOS/Linux. Windows works by default.**

- 验证配置中的 `app_exit` 不包含 `ctrl+c`
- 检查环境变量是否已设置：`echo $OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT`
- 重启终端和 opencode
- **注意：这是 macOS/Linux 上的已知问题。Windows 默认正常工作。**

**Copy doesn't work: / 复制不工作：**
- Check clipboard tools are installed: `which pbcopy` (macOS) or `which xclip` (Linux)
- Try `Ctrl+Y` as alternative copy shortcut
- Check opencode version supports this feature

- 检查剪贴板工具是否已安装：`which pbcopy`（macOS）或 `which xclip`（Linux）
- 尝试 `Ctrl+Y` 作为替代复制快捷键
- 检查 opencode 版本是否支持此功能

**Paste doesn't work: / 粘贴不工作：**
- Verify `input_paste` is set to `ctrl+v` in config
- Check clipboard has content: `pbpaste` (macOS) or `xclip -o` (Linux)

- 验证配置中 `input_paste` 设置为 `ctrl+v`
- 检查剪贴板是否有内容：`pbpaste`（macOS）或 `xclip -o`（Linux）

## Quick Reference / 快速参考

```bash
# Check current config / 查看当前配置
cat ~/.config/opencode/opencode.jsonc

# Check environment variable / 查看环境变量
echo $OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT

# Reload shell config / 重新加载 shell 配置
source ~/.zshrc

# Test clipboard / 测试剪贴板
echo "test" | pbcopy && pbpaste  # macOS
echo "test" | xclip -selection clipboard && xclip -o  # Linux
```
