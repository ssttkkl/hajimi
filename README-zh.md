# Gemini Web MCP Server

基于 MCP (Model Context Protocol) 的 Gemini 代理服务器，使用 Python + uv + gemini-webapi 实现。

本项目基于 [Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) 构建，通过逆向工程实现了对 Google Gemini 网页版（原 Bard）的异步 Python 封装，让你可以在本地通过 MCP 协议调用 Gemini 的完整能力。

## 安装

```bash
git clone https://github.com/ssttkkl/gemini-web-mcp.git
cd gemini-web-mcp
uv sync
```

## 配置

**设置 Gemini Cookie（必需）：**

方式 1：自动登录（推荐）
```bash
# 启动调试模式 Chrome，登录后自动获取 cookie
gemini-web auth login
```

方式 2：手动配置
```bash
gemini-web auth setup
```

方式 3：环境变量
```bash
export GEMINI_COOKIE_1PSID="YOUR_1PSID_VALUE"
export GEMINI_COOKIE_1PSIDTS="YOUR_1PSIDTS_VALUE"
```

方式 4：配置文件 `~/.config/gemini-web/cookies.json`
```json
{
  "secure_1psid": "YOUR_1PSID_VALUE",
  "secure_1psidts": "YOUR_1PSIDTS_VALUE"
}
```

## 使用

在 `mcp.json` 中添加：

**如果使用方式 1（环境变量）配置 Cookie：**

```json
{
  "mcpServers": {
    "gemini-web": {
      "command": "uv",
      "args": ["--directory", "/path/to/gemini-web-mcp", "run", "gemini-web-mcp"],
      "env": {
        "GEMINI_COOKIE_1PSID": "YOUR_1PSID_VALUE",
        "GEMINI_COOKIE_1PSIDTS": "YOUR_1PSIDTS_VALUE"
      }
    }
  }
}
```

**如果使用方式 2（配置文件）配置 Cookie：**

```json
{
  "mcpServers": {
    "gemini-web": {
      "command": "uv",
      "args": ["--directory", "/path/to/gemini-web-mcp", "run", "gemini-web-mcp"]
    }
  }
}
```

## MCP Tools

### gemini_generate

生成内容（文本、图像、文件分析），支持多轮对话。

**参数：**
- `prompt` (string, required): 提示文本
- `files` (array, optional): 本地文件路径列表（图像、PDF 等）
- `session_id` (string, optional): 会话 ID，用于多轮对话

**示例：**

单轮对话：
```json
{
  "prompt": "你好，介绍一下自己"
}
```

多轮对话：
```json
{
  "prompt": "继续上一个话题",
  "session_id": "session-1709836895-abc123def456"
}
```

文件分析：
```json
{
  "prompt": "分析这些文件",
  "files": ["/path/to/image.jpg", "/path/to/document.pdf"]
}
```

### gemini_list_sessions

列出所有 Gemini 会话。

### gemini_delete_session

删除指定会话。

**参数：**
- `session_id` (string, required): 会话 ID

### gemini_get_history

获取会话的完整历史记录。

**参数：**
- `session_id` (string, required): 会话 ID

## 核心功能

- **文本生成**：支持多种 Gemini 模型
- **图像生成**：根据文本提示生成图像
- **文件处理**：支持图像、PDF 等多种文件格式的分析
- **多轮对话**：基于 SQLite 的会话管理，自动保持上下文
- **流式响应**：支持流式输出
- **思维链模式**：支持 Gemini 思维链推理
- **联网搜索**：支持实时网络搜索
- **代码执行**：支持代码生成和执行

## 技术栈

- **Python 3.11+**：运行时
- **uv**：包管理器
- **MCP**：Model Context Protocol
- **gemini-webapi**：Gemini Web API 客户端
- **aiosqlite**：异步 SQLite 数据库

## 数据目录

- macOS: `~/Library/Application Support/gemini-web/`
- Linux: `~/.local/share/gemini-web/`
- Windows: `%APPDATA%\gemini-web\`

生成的图像保存在数据目录的 `images/` 子目录。

