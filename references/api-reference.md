# API Reference

## Commands

All commands must use `uv run` prefix.

### Text Generation

```bash
uv run gemini-web generate "prompt"
```

Options:
- `--model MODEL` - Choose model (gemini-3.0-flash, gemini-3.0-pro, gemini-3.0-flash-thinking)
- `--stream` - Enable streaming output
- `--output FILE` - Save output to file

### Image Generation

```bash
uv run gemini-web generate "image description" --image-output /data/gemini-web-images/
```

Images saved to specified directory (default: `~/Library/Application Support/gemini-web/images/`)

### File Analysis

```bash
uv run gemini-web generate "question" --file /path/to/file
```

Supports: images, PDFs, and other document formats

### Long Text Input

For prompts >1000 characters:

```bash
cat > /tmp/prompt.md << 'EOF'
Your long prompt...
EOF

uv run gemini-web generate "Process this file" --file /tmp/prompt.md
```

### Session Management

```bash
# List sessions
uv run gemini-web session list

# View history
uv run gemini-web session history session-xxx

# Delete session
uv run gemini-web session delete session-xxx
```

## Available Models

- `gemini-3.0-flash` (Default) - Fast and efficient
- `gemini-3.0-pro` - Most powerful
- `gemini-3.0-flash-thinking` - Chain-of-thought reasoning

## Features

- ✅ Text generation
- ✅ Image generation (Imagen 3)
- ✅ File analysis
- ✅ Multi-turn conversations
- ✅ Streaming responses
- ✅ Web search
- ✅ Code execution
- ✅ Automatic cookie refresh
