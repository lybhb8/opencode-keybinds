# macOS/Linux 上启用 opencode Ctrl+C 复制和 Ctrl+V 粘贴

Enable Ctrl+C for copy and Ctrl+V for paste in opencode TUI on macOS/Linux. Windows already supports this by default.

在 macOS/Linux 上启用 opencode TUI 中 Ctrl+C 复制和 Ctrl+V 粘贴功能。Windows 默认已支持此功能。

## Overview / 概述

This skill provides instructions for customizing opencode's keybindings to use Ctrl+C for copy and Ctrl+V for paste, similar to modern text editors and other AI coding tools like Hermes.

此技能提供自定义 opencode 按键绑定的说明，使用 Ctrl+C 复制和 Ctrl+V 粘贴，类似于现代文本编辑器和其他 AI 编码工具（如 Hermes）。

**Note: This is primarily needed on macOS and Linux. Windows enables this feature by default.**

**注意：此功能主要在 macOS 和 Linux 上需要。Windows 默认启用此功能。**

## Installation / 安装

Copy the `SKILL.md` file to your opencode skills directory:

将 `SKILL.md` 文件复制到您的 opencode 技能目录：

```bash
mkdir -p ~/.opencode/skills/opencode-keybinds
cp SKILL.md ~/.opencode/skills/opencode-keybinds/
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

## License / 许可证

MIT
