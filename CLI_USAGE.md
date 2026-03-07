# Gemini Web CLI 使用指南

## 安装

```bash
cd ~/.agents/skills/gemini-web
uv pip install -e .
```

## 配置认证

首先需要配置 Gemini Cookie：

```bash
gemini-web auth setup
```

按提示输入从浏览器获取的 Cookie：
- `__Secure-1PSID`
- `__Secure-1PSIDTS`

查看认证状态：

```bash
gemini-web auth show
```

## 使用命令

### 单轮生成

```bash
# 基本使用
gemini-web generate "你好，介绍一下自己"

# 附加文件
gemini-web generate "描述这张图片" --file image.jpg

# 流式输出
gemini-web generate "讲个故事" --stream

# 指定模型
gemini-web generate "测试" --model gemini-3.0-pro

# 保存到文件
gemini-web generate "总结" --output result.txt
```

### 交互式对话

```bash
# 开始新对话
gemini-web chat

# 恢复已有会话
gemini-web chat --session session-xxx

# 指定模型
gemini-web chat --model gemini-3.0-flash-thinking
```

在对话中输入 `exit` 或 `quit` 退出。

### 会话管理

```bash
# 列出所有会话
gemini-web session list

# 查看会话历史
gemini-web session history session-xxx

# 删除会话
gemini-web session delete session-xxx
```

## 支持的模型

- `gemini-3.0-flash` (默认)
- `gemini-3.0-pro`
- `gemini-3.0-flash-thinking`

## 数据存储

- 配置文件: `~/.config/gemini-web/cookies.json`
- 会话数据: `~/Library/Application Support/gemini-web/sessions.db` (macOS)
- 生成图片: `~/Library/Application Support/gemini-web/images/`

## MCP 服务器

原有的 MCP 服务器功能保持不变：

```bash
gemini-web-mcp
```
