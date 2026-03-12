---
name: gemini-web-chat
description: Chat with Google Gemini via gemini-web CLI. Supports text generation, image generation, file analysis, and multi-turn conversations. Auto-refreshes cookies from Chrome.
metadata:
  {
    "openclaw":
      {
        "emoji": "🌟",
        "requires": { "bins": ["uv"] },
      },
  }
---

# Gemini Web Chat

Use Google Gemini through the gemini-web CLI for text generation, image creation, file analysis, and conversational AI.

**⚠️ 重要**：本项目使用 `uv` 管理依赖，所有命令需通过 `uv run` 执行。

## 安装与配置

### 1. 安装依赖

```bash
cd ~/.agents/skills/gemini-web
uv sync
```

### 2. 初始配置（首次）

1. 打开 Chrome 访问 https://gemini.google.com 并登录
2. 运行：
```bash
cd ~/.agents/skills/gemini-web
uv run gemini-web auth setup
```
3. 按提示输入 `__Secure-1PSID` 和 `__Secure-1PSIDTS`

## 使用方式

**⚠️ 必须使用 `uv run` 执行所有命令**

```bash
cd ~/.agents/skills/gemini-web

# 单轮生成
uv run gemini-web generate "Explain quantum computing"

# 带图片生成
uv run gemini-web generate "画一只雪中独狼" --image-output ~/Library/Application\ Support/gemini-web/images/

# 带文件输入
uv run gemini-web generate "描述这张图片" --file photo.jpg

# 流式输出
uv run gemini-web generate "讲个故事" --stream

# 指定模型
uv run gemini-web generate "测试" --model gemini-3.0-pro

# 保存输出
uv run gemini-web generate "总结" --output result.txt
```

## 图像生成

```bash
cd ~/.agents/skills/gemini-web
uv run gemini-web generate "画一只雪中独狼" --image-output ~/Library/Application\ Support/gemini-web/images/
```

图片自动保存到 `~/Library/Application Support/gemini-web/images/` (macOS)。

**📤 发送到 Channel**：生成图片后，使用 `message` 工具将图片发送到 channel：

```python
# 示例：发送生成的图片到当前 channel
# 1. 找到最新生成的图片
latest_image = exec("ls -t ~/Library/Application\ Support/gemini-web/images/*.png | head -1")

# 2. 使用 message 工具发送
message(
    action="send",
    channel="<current_channel_id>",  # 从上下文获取
    media=latest_image.strip(),
    caption="生成的图片"
)
```

## Cookie 自动刷新

**API 的自动 Cookie 刷新功能默认启用**，无需额外设置。它允许您保持 API 服务运行，而无需担心 Cookie 过期。

此功能可能需要您在浏览器中重新登录您的 Google 帐户。这是正常现象，不会影响 API 的功能。

### 最佳实践：使用隐私模式获取 Cookie

为避免频繁重新登录，建议从单独的浏览器会话中获取 cookie，并尽快关闭该会话以获得最佳使用体验：

1. 打开 Chrome **隐私模式（无痕模式）**
2. 访问 https://gemini.google.com 并登录
3. 获取 `__Secure-1PSID` 和 `__Secure-1PSIDTS` cookie
4. **立即关闭隐私模式窗口**
5. 这样获取的 cookie 可以持续使用数周

更多详情参考：https://github.com/HanaokaYuzu/Gemini-API/issues/6

## 手动刷新 Cookie

如果遇到 "您登录了吗？" 或 cookie 过期错误，需要手动刷新 cookie：

```bash
cd ~/.agents/skills/gemini-web
uv run python3 -c "
import browser_cookie3
import json
import os

cj = browser_cookie3.chrome(domain_name='google.com')
cookies = list(cj)

psid = [c for c in cookies if c.name == '__Secure-1PSID' and c.domain == '.google.com'][0].value
psidts = [c for c in cookies if c.name == '__Secure-1PSIDTS' and c.domain == '.google.com'][0].value

config = {'secure_1psid': psid, 'secure_1psidts': psidts}

os.makedirs(os.path.expanduser('~/.config/gemini-web'), exist_ok=True)
with open(os.path.expanduser('~/.config/gemini-web/cookies.json'), 'w') as f:
    json.dump(config, f, indent=2)

print('Cookie updated!')
"
```

**前提条件**：确保 Chrome 已登录 https://gemini.google.com

## 文件分析

```bash
cd ~/.agents/skills/gemini-web
uv run gemini-web generate "描述这张图片" --file photo.jpg
uv run gemini-web generate "总结这份文档" --file report.pdf
```

## 会话管理

```bash
cd ~/.agents/skills/gemini-web

# 列出所有会话
uv run gemini-web session list

# 查看会话历史
uv run gemini-web session history session-xxx

# 删除会话
uv run gemini-web session delete session-xxx
```

## 可用模型

- `gemini-3.0-flash` (默认) - 快速、高效
- `gemini-3.0-pro` - 最强大的模型
- `gemini-3.0-flash-thinking` - 思维链推理

## 故障排除

### Cookie 过期/无法获取

1. 确保 Chrome 已登录 https://gemini.google.com
2. 运行上面的 **手动刷新 Cookie** 命令
3. 重试原命令

**提示**：为避免频繁过期，建议使用 Chrome 隐私模式获取 cookie 并立即关闭窗口。

### 图片生成失败

- 检查 cookie 是否有效（运行手动刷新）
- 确保账户有图像生成权限
- 尝试刷新 cookie 后重试

## 数据目录

- 配置文件: `~/.config/gemini-web/cookies.json`
- 会话数据: `~/Library/Application Support/gemini-web/sessions.db` (macOS)
- 生成图片: `~/Library/Application Support/gemini-web/images/`

## 功能特性

- ✅ 自动生成式对话
- ✅ 图像生成
- ✅ 文件分析（图片、PDF 等）
- ✅ 多轮对话与上下文保持
- ✅ 流式响应
- ✅ 网络搜索能力
- ✅ 代码执行与生成
- ✅ **Cookie 自动刷新** — 默认启用，无需额外配置
