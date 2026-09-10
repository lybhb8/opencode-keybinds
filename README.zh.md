# Mac 终端 Control + C  按键绑定

[English](README.md) | [中文](README.zh.md)

在 macOS/Linux 上启用 opencode TUI 中 Ctrl+C 复制和 Ctrl+V 粘贴功能。Windows 默认已支持。

---

## 第一部分：OpenCode

### 快速开始

#### 1. 更新 opencode 配置

复制配置文件：

```bash
cp config/opencode.jsonc ~/.config/opencode/opencode.jsonc
```

或手动编辑 - 参见 [config/opencode.jsonc](config/opencode.jsonc)

#### 2. 启用复制拦截（仅 macOS/Linux）

添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
export OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT=1
```

然后重新加载：

```bash
source ~/.zshrc
```

#### 3. 重启 opencode

退出并重启 opencode 使配置生效。

### 按键绑定

| 快捷键 | 操作 |
|--------|------|
| `Ctrl+C` | 复制选中文本到剪贴板 |
| `Ctrl+V` | 从剪贴板粘贴 |
| `Ctrl+D` | 退出应用 |
| `Ctrl+X` 然后 `Q` | 退出应用（Leader+Q） |
| `Ctrl+Y` | 复制选中文本（替代方案） |

### 安装

```bash
# 手动安装
mkdir -p ~/.opencode/skills/opencode-keybinds
cp SKILL.md ~/.opencode/skills/opencode-keybinds/

# 或 Git 克隆
cd ~/.opencode/skills
git clone https://github.com/lybhb8/mac-ctrl-c.git
```

### 使用方法

```
@opencode-keybinds
```

### 工作原理

opencode 使用带拦截器的按键绑定系统：

1. `opencode.jsonc` 中的**按键绑定覆盖**修改默认绑定
2. **环境变量** `OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT` 启用复制拦截器
3. **优先级拦截器**在默认按键绑定之前运行以处理复制

复制功能使用：
- macOS：`pbcopy` 命令或 OSC 52 转义序列
- Linux：`xclip`、`xsel` 或 `wl-copy`
- Windows：PowerShell 或 OSC 52

### 故障排除

**Ctrl+C 仍然退出 opencode：**
- 验证配置中的 `app_exit` 不包含 `ctrl+c`
- 检查环境变量：`echo $OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT`
- 重启终端和 opencode

**复制不工作：**
- 检查剪贴板工具：`which pbcopy`（macOS）或 `which xclip`（Linux）
- 尝试 `Ctrl+Y` 作为替代复制快捷键

**粘贴不工作：**
- 验证配置中 `input_paste` 设置为 `ctrl+v`
- 检查剪贴板内容：`pbpaste`（macOS）或 `xclip -o`（Linux）

---

## 第二部分：Hermes

### 概述

Hermes Agent 使用 Python 的 `prompt_toolkit` 库管理按键绑定。

### 主要区别

| 功能 | Hermes | opencode |
|------|--------|----------|
| 框架 | prompt_toolkit | OpenTUI |
| Ctrl+C | 复制 | 复制（需要配置） |
| Ctrl+V | 粘贴 | 粘贴 |
| 中断 | Ctrl+Q | Ctrl+D |
| 配置 | config.yaml | opencode.jsonc + 环境变量 |

### Hermes 按键绑定

| 快捷键 | 操作 |
|--------|------|
| `Ctrl+C` | 复制选中文本到剪贴板 |
| `Ctrl+V` | 从剪贴板粘贴 |
| `Ctrl+Q` | 中断运行中的 agent |

### 配置

参见 [code/hermes-config.yaml](code/hermes-config.yaml)

### 实现代码

- [code/hermes-keybindings.py](code/hermes-keybindings.py) - 按键绑定处理器
- [code/clipboard-service.py](code/clipboard-service.py) - 剪贴板操作

### 源码位置

Hermes 按键绑定实现位于：
- `/Users/mac/.hermes/hermes-agent/cli.py`
- 第 17707-17800 行（ctrl+c 复制）
- 第 18729-18795 行（ctrl+q 中断）
- 第 18797+ 行（ctrl+v 粘贴）

### 参考

- [Hermes Agent GitHub](https://github.com/NousResearch/hermes-agent)
- [prompt_toolkit 文档](https://python-prompt-toolkit.readthedocs.io/)

---

## 快速参考

```bash
# 查看 opencode 配置
cat ~/.config/opencode/opencode.jsonc

# 查看环境变量
echo $OPENCODE_EXPERIMENTAL_DISABLE_COPY_ON_SELECT

# 测试剪贴板（macOS）
echo "test" | pbcopy && pbpaste

# 测试剪贴板（Linux）
echo "test" | xclip -selection clipboard && xclip -o
```

## 许可证

MIT - 详见 [LICENSE](LICENSE)
