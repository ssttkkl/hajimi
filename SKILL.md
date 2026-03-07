---
name: gemini-web
description: MCP server for Gemini Web API. Use when: (1) Need to generate text with Gemini, (2) Generate images from prompts, (3) Analyze files (images, PDFs), (4) Multi-turn conversation with Gemini, (5) Access Gemini's web search and code execution capabilities.
---

# Gemini Web MCP Server

An MCP (Model Context Protocol) server for Google Gemini, built with reverse-engineered asynchronous Python wrapper.

[中文文档](SKILL-zh.md)

## Quick Start

### Installation

```bash
cd ~/.openclaw/skills/gemini-web
uv sync
```

### Configure Cookies (Required)

**Method 1: Environment Variables**

Add to MCP config:

```json
{
  "mcpServers": {
    "gemini-web": {
      "command": "uv",
      "args": ["run", "gemini-web-mcp"],
      "env": {
        "GEMINI_COOKIE_1PSID": "your_1psid_value",
        "GEMINI_COOKIE_1PSIDTS": "your_1psidts_value"
      }
    }
  }
}
```

**Method 2: Config File**

Create `~/.config/gemini-web/cookies.json`:

```json
{
  "secure_1psid": "your_1psid_value",
  "secure_1psidts": "your_1psidts_value"
}
```

Then configure MCP (no env needed):

```json
{
  "mcpServers": {
    "gemini-web": {
      "command": "uv",
      "args": ["run", "gemini-web-mcp"]
    }
  }
}
```

## MCP Tools

### gemini_generate

Generate content (text, images, file analysis) with multi-turn conversation support.

**Parameters:**
- `prompt` (string, required): The prompt text
- `files` (array, optional): Local file paths (images, PDFs, etc.)
- `session_id` (string, optional): Session ID for multi-turn conversation
- `model` (string, optional): Model name (default: gemini-3.0-flash)

**Examples:**

Single-turn:
```json
{
  "prompt": "Hello, introduce yourself"
}
```

Multi-turn:
```json
{
  "prompt": "Continue the previous topic",
  "session_id": "session-1709836895-abc123def456"
}
```

File analysis:
```json
{
  "prompt": "Analyze these files",
  "files": ["/path/to/image.jpg", "/path/to/document.pdf"]
}
```

### gemini_list_models

List available Gemini models.

### gemini_list_sessions

List all Gemini conversation sessions.

### gemini_delete_session

Delete a conversation session.

**Parameters:**
- `session_id` (string, required): Session ID

### gemini_get_history

Get complete conversation history for a session.

**Parameters:**
- `session_id` (string, required): Session ID

## Features

- **Text Generation**: Support for multiple Gemini models
- **Image Generation**: Generate images from text prompts
- **File Processing**: Analyze images, PDFs, and other file formats
- **Multi-turn Conversation**: SQLite-based session management with automatic context preservation
- **Streaming Response**: Support for streaming output
- **Thinking Mode**: Support for Gemini chain-of-thought reasoning
- **Web Search**: Real-time web search capabilities
- **Code Execution**: Code generation and execution support

## Data Directory

Generated images are saved in the `images/` subdirectory:

- macOS: `~/Library/Application Support/gemini-web/images/`
- Linux: `~/.local/share/gemini-web/images/`
- Windows: `%APPDATA%\gemini-web\images\`

## Important Notes

### 🔐 How to Get Cookies (Required)

1. Visit https://gemini.google.com and log in with your Google account
2. Press F12 to open Developer Tools, switch to Network tab
3. Refresh the page
4. Click any request, find Cookies in Headers
5. Copy the values of these two cookies:
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`

Then configure these values in environment variables or `~/.config/gemini-web/cookies.json`.

### 🐛 Multi-turn Conversation Limitation

⚠️ **Known Issue**: Due to a bug in the upstream [Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) library, conversation history cannot be properly preserved. This is a library issue, not an implementation problem in this project.
