# Gemini Web MCP Server

An MCP (Model Context Protocol) server for Google Gemini, built with Python + uv + gemini-webapi.

This project is built on [Gemini-API](https://github.com/HanaokaYuzu/Gemini-API), a reverse-engineered asynchronous Python wrapper for the Google Gemini web app (formerly Bard), enabling you to access Gemini's full capabilities locally via MCP protocol.

[中文文档](README-zh.md)

## Installation

```bash
git clone https://github.com/ssttkkl/gemini-web-mcp.git
cd gemini-web-mcp
uv sync
```

## Configuration

**Set Gemini Cookies (Required):**

Method 1: Environment Variables
```bash
export GEMINI_COOKIE_1PSID="YOUR_1PSID_VALUE"
export GEMINI_COOKIE_1PSIDTS="YOUR_1PSIDTS_VALUE"
```

Method 2: Config File `~/.config/gemini-web/cookies.json`
```json
{
  "secure_1psid": "YOUR_1PSID_VALUE",
  "secure_1psidts": "YOUR_1PSIDTS_VALUE"
}
```

## Usage

Add to your `mcp.json`:

**If using Method 1 (Environment Variables):**

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

**If using Method 2 (Config File):**

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
  - ⚠️ **Known Issue**: Due to a bug in the upstream [Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) library, conversation history cannot be properly preserved. This is a library issue, not an implementation problem in this project.
- **Streaming Response**: Support for streaming output
- **Thinking Mode**: Support for Gemini chain-of-thought reasoning
- **Web Search**: Real-time web search capabilities
- **Code Execution**: Code generation and execution support

## Tech Stack

- **Python 3.11+**: Runtime
- **uv**: Package manager
- **MCP**: Model Context Protocol
- **gemini-webapi**: Gemini Web API client
- **aiosqlite**: Async SQLite database

## Data Directory

- macOS: `~/Library/Application Support/gemini-web/`
- Linux: `~/.local/share/gemini-web/`
- Windows: `%APPDATA%\gemini-web\`

Generated images are saved in the `images/` subdirectory.
