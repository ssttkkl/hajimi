# Hajimi - Gemini Web CLI & MCP Server

A command-line tool and MCP (Model Context Protocol) server for Google Gemini, built with Python + uv + gemini-webapi.

This project is built on [Gemini-API](https://github.com/HanaokaYuzu/Gemini-API), a reverse-engineered asynchronous Python wrapper for the Google Gemini web app (formerly Bard).

[中文文档](README-zh.md)

## Installation

```bash
git clone https://github.com/ssttkkl/hajimi.git
cd hajimi
uv sync
```

## Configuration

**Set Gemini Cookies (Required):**

Method 1: Using CLI command
```bash
gemini-web auth setup
```

Method 2: Environment Variables
```bash
export GEMINI_COOKIE_1PSID="YOUR_1PSID_VALUE"
export GEMINI_COOKIE_1PSIDTS="YOUR_1PSIDTS_VALUE"
```

Method 3: Config File `~/.config/gemini-web/cookies.json`
```json
{
  "secure_1psid": "YOUR_1PSID_VALUE",
  "secure_1psidts": "YOUR_1PSIDTS_VALUE"
}
```

## Usage

### CLI Mode

**Authentication:**
```bash
# Setup cookies
gemini-web auth setup

# Check auth status
gemini-web auth show
```

**Generate Content:**
```bash
# Single-turn generation
gemini-web generate "Hello, introduce yourself"

# With file input
gemini-web generate "Describe this image" --file image.jpg

# Streaming output
gemini-web generate "Tell me a story" --stream

# Specify model
gemini-web generate "Test" --model gemini-3.0-pro

# Save output
gemini-web generate "Summary" --output result.txt

# Save images to specific directory
gemini-web generate "Draw a cat" --image-output ./images
```

**Interactive Chat:**
```bash
# Start new chat
gemini-web chat

# Resume existing session
gemini-web chat --session session-xxx

# Use specific model
gemini-web chat --model gemini-3.0-flash-thinking
```

**Session Management:**
```bash
# List all sessions
gemini-web session list

# View session history
gemini-web session history session-xxx

# Delete session
gemini-web session delete session-xxx
```

### MCP Server Mode

Start MCP server:
```bash
gemini-web mcp
```

Add to your `mcp.json`:

**If using Method 2 (Environment Variables):**

```json
{
  "mcpServers": {
    "gemini-web": {
      "command": "uv",
      "args": ["--directory", "/path/to/hajimi", "run", "gemini-web", "mcp"],
      "env": {
        "GEMINI_COOKIE_1PSID": "YOUR_1PSID_VALUE",
        "GEMINI_COOKIE_1PSIDTS": "YOUR_1PSIDTS_VALUE"
      }
    }
  }
}
```

**If using Method 3 (Config File):**

```json
{
  "mcpServers": {
    "gemini-web": {
      "command": "uv",
      "args": ["--directory", "/path/to/hajimi", "run", "gemini-web", "mcp"]
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
