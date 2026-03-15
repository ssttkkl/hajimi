---
name: gemini-web-chat
description: Chat with Google Gemini AI via web interface, supporting text generation, image generation, file analysis, and multi-turn conversations. Use when: (1) Generating images with Gemini/Imagen 3, (2) Analyzing files (images/PDFs), (3) Long-form content generation, (4) Multi-turn conversations requiring context, (5) Tasks requiring Gemini-specific capabilities (thinking mode, web search).
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

⚠️ **All commands must use `uv run` prefix**

## Quick Reference

| User Intent | Command Template |
|-------------|------------------|
| Generate text | `uv run gemini-web generate "prompt"` |
| Generate image | `uv run gemini-web generate "描述" --image-output /data/gemini-web-images/` |
| Analyze file | `uv run gemini-web generate "question" --file /path/to/file` |
| Long text (>1000 chars) | Write to /tmp/prompt.md, use `--file /tmp/prompt.md` |
| Specify model | Add `--model gemini-3.0-pro` |
| Stream output | Add `--stream` |

## Setup

**First time only:**

```bash
uv sync
uv run gemini-web auth login
```

For manual configuration or troubleshooting, see [references/setup.md](references/setup.md)

## Image Generation Workflow

### 1. Generate image to /data directory

```bash
uv run gemini-web generate "一盘精致的日式草莓大福" --image-output /data/gemini-web-images/
```

### 2. Send image via send_sandbox_image tool

```bash
# List latest image
ls -t /data/gemini-web-images/*.png | head -1

# Copy the filename and use with send_sandbox_image tool
# Example: send_sandbox_image(image_path="/data/gemini-web-images/20260315145246_xxx.png")
```

## Long Text Input

For prompts >1000 characters:

```bash
cat > /tmp/prompt.md << 'EOF'
Your very long prompt here...
EOF

uv run gemini-web generate "Process this content" --file /tmp/prompt.md
```

## Available Models

- `gemini-3.0-flash` (Default) - Fast
- `gemini-3.0-pro` - Most powerful
- `gemini-3.0-flash-thinking` - Chain-of-thought

## Troubleshooting

**Cookie expired?** Run `uv run gemini-web auth login`

For detailed error messages and solutions, see [references/troubleshooting.md](references/troubleshooting.md)

## Full Documentation

- [Setup Guide](references/setup.md) - Installation and authentication
- [API Reference](references/api-reference.md) - Complete command reference
- [Troubleshooting](references/troubleshooting.md) - Error messages and solutions
