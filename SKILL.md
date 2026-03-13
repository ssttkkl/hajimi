---
name: gemini-web-chat
description: Chat with Google Gemini AI, supporting text generation, image generation, file analysis, and multi-turn conversations.
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

Chat with Google Gemini AI, supporting:

- **Text Generation** - Answering questions, content creation, coding, etc.
- **Image Generation** - Generating images based on descriptions.
- **File Analysis** - Analyzing the content of images, PDFs, and other files.
- **Multi-turn Conversations** - Maintaining context for continuous dialogue.

**⚠️ Important**: This project uses uv for dependency management. All commands must be executed via `uv run`.

## Installation and Configuration

### 1. Install Dependencies

```bash
cd ~/.agents/skills/gemini-web
uv sync
```

### 2. Initial Configuration (First Time)

Run the following command to launch Chrome and automatically retrieve cookies:

```bash
cd ~/.agents/skills/gemini-web
uv run gemini-web auth login
```

This will start Chrome in debugging mode. You simply need to log in to your Google account and press Enter to automatically retrieve the cookies.

## Usage

**⚠️ All commands must be executed using `uv run`**

```bash
cd ~/.agents/skills/gemini-web

# Single-turn generation
uv run gemini-web generate "Explain quantum computing"

# Generation with image
uv run gemini-web generate "Draw a lone wolf in the snow" --image-output ~/Library/Application\ Support/gemini-web/images/

# Generation with file input
uv run gemini-web generate "Describe this image" --file photo.jpg

# Streaming output
uv run gemini-web generate "Tell a story" --stream

# Specify model
uv run gemini-web generate "Test" --model gemini-3.0-pro

# Save output
uv run gemini-web generate "Summarize" --output result.txt
```

## Image Generation

```bash
cd ~/.agents/skills/gemini-web
uv run gemini-web generate "Draw a lone wolf in the snow" --image-output ~/Library/Application\ Support/gemini-web/images/
```

Images are automatically saved to `~/Library/Application Support/gemini-web/images/` (macOS).

**📤 Send to Channel**: After generating an image, use the message tool to send the image to a channel:

```python
# Example: Send the generated image to the current channel
# 1. Find the latest generated image
latest_image = exec("ls -t ~/Library/Application\ Support/gemini-web/images/*.png | head -1")

# 2. Send using the message tool
message(
    action="send",
    channel="<current_channel_id>",  # Retrieve from context
    media=latest_image.strip(),
    caption="Generated image"
)
```

## Automatic Cookie Refresh

**The API's automatic Cookie refresh feature is enabled by default**, requiring no extra setup. It allows you to keep the API service running without worrying about Cookie expiration.

This feature might require you to re-login to your Google account in the browser. This is normal and will not affect the API's functionality.

### Best Practice: Use Incognito Mode to Get Cookies

To avoid logging in frequently, it is recommended to retrieve cookies from a separate browser session and close that session as soon as possible for the best experience:

1. Open Chrome Incognito mode
2. Visit https://gemini.google.com and log in
3. Retrieve the `__Secure-1PSID` and `__Secure-1PSIDTS` cookies
4. Close the Incognito mode window immediately
5. Cookies obtained this way can last for weeks

For more details, refer to: https://github.com/HanaokaYuzu/Gemini-API/issues/6

## Refresh Cookies

If you encounter an authentication failure or cookie expiration error, please re-run the authentication command:

```bash
cd ~/.agents/skills/gemini-web
uv run gemini-web auth login
```

This will start Chrome in debugging mode. You simply need to log in to your Google account and press Enter to automatically retrieve the new cookies.

## File Analysis

```bash
cd ~/.agents/skills/gemini-web
uv run gemini-web generate "Describe this image" --file photo.jpg
uv run gemini-web generate "Summarize this document" --file report.pdf
```

## Session Management

```bash
cd ~/.agents/skills/gemini-web

# List all sessions
uv run gemini-web session list

# View session history
uv run gemini-web session history session-xxx

# Delete a session
uv run gemini-web session delete session-xxx
```

## Available Models

- `gemini-3.0-flash` (Default) - Fast and efficient
- `gemini-3.0-pro` - The most powerful model
- `gemini-3.0-flash-thinking` - Chain-of-thought reasoning

## Troubleshooting

### Image Generation Failed

- Check if the cookie is valid (run `uv run gemini-web auth login` to refresh)
- Ensure the account has image generation permissions
- Try refreshing the cookie and attempt again

## Data Directories

- Config file: `~/.config/gemini-web/cookies.json`
- Session data: `~/Library/Application Support/gemini-web/sessions.db` (macOS)
- Generated images: `~/Library/Application Support/gemini-web/images/`

## Features

- ✅ Automated generative chat
- ✅ Image generation
- ✅ File analysis (Images, PDFs, etc.)
- ✅ Multi-turn conversation and context preservation
- ✅ Streaming response
- ✅ Web search capability
- ✅ Code execution and generation
- ✅ Automatic Cookie Refresh — Enabled by default, no extra configuration needed
