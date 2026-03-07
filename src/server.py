import os
import json
import time
import uuid
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent
from gemini_webapi import GeminiClient
from gemini_webapi.constants import Model
from .db import SessionDB

# 数据目录
if os.name == 'nt':
    data_dir = Path(os.environ.get('APPDATA', '')) / "gemini-web"
elif os.uname().sysname == 'Darwin':
    data_dir = Path.home() / "Library/Application Support/gemini-web"
else:
    data_dir = Path.home() / ".local/share/gemini-web"

data_dir.mkdir(parents=True, exist_ok=True)

client = None
db = SessionDB(data_dir / "sessions.db")
server = Server("gemini-web")

async def init_client():
    global client
    await db.init()

    secure_1psid = os.environ.get("GEMINI_COOKIE_1PSID")
    secure_1psidts = os.environ.get("GEMINI_COOKIE_1PSIDTS")

    if not secure_1psid or not secure_1psidts:
        config_path = Path.home() / ".config/gemini-web/cookies.json"
        if config_path.exists():
            cookies_data = json.loads(config_path.read_text())
            secure_1psid = secure_1psid or cookies_data.get("secure_1psid")
            secure_1psidts = secure_1psidts or cookies_data.get("secure_1psidts")

    if not secure_1psid or not secure_1psidts:
        raise ValueError("Missing required cookies: GEMINI_COOKIE_1PSID and GEMINI_COOKIE_1PSIDTS")

    client = GeminiClient(secure_1psid=secure_1psid, secure_1psidts=secure_1psidts)
    await client.init()

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="gemini_generate",
            description="Generate content using Gemini (text, images, file analysis). Supports multi-turn conversations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The prompt text"},
                    "files": {"type": "array", "items": {"type": "string"}, "description": "Local file paths (images, PDFs, etc.)"},
                    "session_id": {"type": "string", "description": "Session ID for multi-turn conversation (optional)"},
                    "model": {"type": "string", "description": "Model name (optional, default: gemini-3.0-flash)"}
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="gemini_list_models",
            description="List available Gemini models",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="gemini_list_sessions",
            description="List all Gemini conversation sessions",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="gemini_delete_session",
            description="Delete a Gemini conversation session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID to delete"}
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="gemini_get_history",
            description="Get conversation history for a session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID"}
                },
                "required": ["session_id"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "gemini_generate":
        prompt = arguments["prompt"]
        files = arguments.get("files", [])
        session_id = arguments.get("session_id", "")
        model = arguments.get("model", "gemini-3.0-flash")

        if not session_id:
            session_id = f"session-{int(time.time())}-{uuid.uuid4().hex[:12]}"
            metadata = None
        else:
            metadata = await db.load(session_id)

        if not metadata:
            output = await client.generate_content(prompt, files=files or None, model=model)
            temp_chat = client.start_chat(metadata=output.metadata, model=model)
            await db.save(session_id, temp_chat.metadata)
        else:
            chat = client.start_chat(metadata=metadata, model=model)
            output = await chat.send_message(prompt, files=files or None)
            await db.save(session_id, chat.metadata)

        contents = [
            TextContent(type="text", text=f"Session ID: {session_id}")
        ]

        if output.thoughts:
            contents.append(TextContent(type="text", text=f"Thoughts:\n{output.thoughts}"))

        contents.append(TextContent(type="text", text=output.text))

        if output.images:
            images_dir = data_dir / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
            for img in output.images:
                img_path = images_dir / f"{session_id}_{int(time.time())}.png"
                await img.save(str(img_path))
                contents.append(ImageContent(type="image", data=str(img_path), mimeType="image/png"))

        return contents

    elif name == "gemini_list_models":
        models = [m for m in dir(Model) if not m.startswith('_') and m != 'UNSPECIFIED']
        text = "Available Gemini Models:\n\n" + "\n".join([f"- {m}" for m in models])
        return [TextContent(type="text", text=text)]

    elif name == "gemini_list_sessions":
        sessions = await db.list_all()
        text = "Gemini Sessions:\n\n" + "\n".join([f"- {s['id']} (cid: {s['cid']})" for s in sessions])
        return [TextContent(type="text", text=text)]

    elif name == "gemini_delete_session":
        session_id = arguments["session_id"]
        await db.delete(session_id)
        return [TextContent(type="text", text=f"Deleted session: {session_id}")]

    elif name == "gemini_get_history":
        session_id = arguments["session_id"]
        metadata = await db.load(session_id)
        if not metadata or not metadata[0]:
            return [TextContent(type="text", text=f"No history found for session: {session_id}")]
        turns = await client.read_chat(metadata[0])
        text = f"History for session {session_id}:\n\n" + "\n\n".join([f"Turn {i+1}:\n{t.model_dump()}" for i, t in enumerate(turns)])
        return [TextContent(type="text", text=text)]

async def main():
    from mcp.server.stdio import stdio_server
    await init_client()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

def run():
    import asyncio
    asyncio.run(main())
