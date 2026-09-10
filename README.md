# macOS/Linux 上启用 opencode Ctrl+C 复制和 Ctrl+V 粘贴

Enable Ctrl+C for copy and Ctrl+V for paste in opencode TUI on macOS/Linux. Windows already supports this by default.

在 macOS/Linux 上启用 opencode TUI 中 Ctrl+C 复制和 Ctrl+V 粘贴功能。Windows 默认已支持此功能。

## Overview / 概述

This skill provides instructions for customizing opencode's keybindings to use Ctrl+C for copy and Ctrl+V for paste, similar to modern text editors and other AI coding tools like Hermes.

此技能提供自定义 opencode 按键绑定的说明，使用 Ctrl+C 复制和 Ctrl+V 粘贴，类似于现代文本编辑器和其他 AI 编码工具（如 Hermes）。

**Note: This is primarily needed on macOS and Linux. Windows enables this feature by default.**

**注意：此功能主要在 macOS 和 Linux 上需要。Windows 默认启用此功能。**

## Quick Start / 快速开始

### 1. Update opencode configuration / 更新 opencode 配置

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

### 2. Enable copy intercept (macOS/Linux only) / 启用复制拦截（仅 macOS/Linux）

Add to `~/.zshrc` or `~/.bashrc`:

添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
export OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT=1
```

Then reload / 然后重新加载：

```bash
source ~/.zshrc
```

### 3. Restart opencode / 重启 opencode

Quit and restart opencode for changes to take effect.

退出并重启 opencode 使配置生效。

## Keybindings / 按键绑定

| Shortcut / 快捷键 | Action / 操作 |
|----------|--------|
| `Ctrl+C` | Copy selected text to clipboard / 复制选中文本到剪贴板 |
| `Ctrl+V` | Paste from clipboard / 从剪贴板粘贴 |
| `Ctrl+D` | Exit application / 退出应用 |
| `Ctrl+X` then `Q` | Exit application (Leader+Q) / 退出应用（Leader+Q） |
| `Ctrl+Y` | Copy selection (alternative) / 复制选中文本（替代方案） |

## Installation / 安装

### Option 1: Manual installation / 手动安装

Copy the `SKILL.md` file to your opencode skills directory:

将 `SKILL.md` 文件复制到您的 opencode 技能目录：

```bash
mkdir -p ~/.opencode/skills/opencode-keybinds
cp SKILL.md ~/.opencode/skills/opencode-keybinds/
```

### Option 2: Git clone / Git 克隆

```bash
cd ~/.opencode/skills
git clone https://github.com/YOUR_USERNAME/opencode-keybinds.git
```

## Usage / 使用方法

Load this skill in opencode by referencing it:

在 opencode 中通过引用加载此技能：

```
@opencode-keybinds
```

Or follow the manual configuration steps in the SKILL.md file.

或按照 SKILL.md 文件中的手动配置步骤操作。

## Features / 功能

- Ctrl+C for copy (instead of exit) / Ctrl+C 复制（而不是退出）
- Ctrl+V for paste / Ctrl+V 粘贴
- Ctrl+D for exit / Ctrl+D 退出
- Cross-platform support (macOS, Linux, Windows) / 跨平台支持（macOS、Linux、Windows）
- **Note: macOS/Linux require additional configuration. Windows works by default.**

- **注意：macOS/Linux 需要额外配置。Windows 默认正常工作。**

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

## How It Works / 工作原理

opencode uses a keybinding system with intercepts:

opencode 使用带拦截器的按键绑定系统：

1. **Keybinding overrides** in `opencode.jsonc` modify default bindings
2. **Environment variable** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` enables the copy intercept
3. **Priority intercept** runs before default keybindings to handle copy

1. `opencode.jsonc` 中的**按键绑定覆盖**修改默认绑定
2. **环境变量** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` 启用复制拦截器
3. **优先级拦截器**在默认按键绑定之前运行以处理复制

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

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交 Pull Request。

欢迎贡献！请随时提交 Pull Request。

## License / 许可证

MIT License - see the [LICENSE](LICENSE) file for details.

MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。
