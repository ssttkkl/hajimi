#!/usr/bin/env python3
"""
最小复现程序：测试 Gemini-API 多轮对话历史记录问题
"""
import asyncio
import os
import json
from pathlib import Path
from gemini_webapi import GeminiClient

async def test_conversation_history():
    """测试多轮对话历史是否能正确保留"""

    # 加载 cookies
    config_path = Path.home() / ".config" / "gemini-web" / "cookies.json"
    if config_path.exists():
        cookies_data = json.loads(config_path.read_text())
        secure_1psid = cookies_data.get("secure_1psid")
        secure_1psidts = cookies_data.get("secure_1psidts")
    else:
        secure_1psid = os.environ.get("GEMINI_COOKIE_1PSID")
        secure_1psidts = os.environ.get("GEMINI_COOKIE_1PSIDTS")

    if not secure_1psid or not secure_1psidts:
        print("错误: 未找到 cookies，请先运行 'gemini-web auth setup'")
        return

    # 初始化客户端
    client = GeminiClient(
        secure_1psid=secure_1psid,
        secure_1psidts=secure_1psidts
    )
    await client.init()

    print("=" * 60)
    print("Test 1: First turn - Ask AI to remember a number")
    print("=" * 60)

    # First turn
    response1 = await client.generate_content("Please remember this number: 42")
    print(f"AI Response: {response1.text}\n")

    # Save metadata
    metadata = response1.metadata
    print(f"Metadata: {metadata}\n")

    # Start chat with metadata
    chat = client.start_chat(metadata=metadata)

    print("=" * 60)
    print("Test 2: Second turn - Ask what number to remember")
    print("=" * 60)

    # Second turn
    response2 = await chat.send_message("What number did I ask you to remember?")
    print(f"AI Response: {response2.text}\n")

    print("=" * 60)
    print("Test 3: Read conversation history using read_chat")
    print("=" * 60)

    # Read conversation history
    history = await client.read_chat(metadata)
    print(f"History length: {len(history)}")
    for i, msg in enumerate(history, 1):
        role = "User" if msg.role == 0 else "AI"
        print(f"\nMessage {i} ({role}):")
        print(f"  Text: {msg.text[:100]}...")

    print("\n" + "=" * 60)
    print("Expected Results:")
    print("  - Second turn should answer '42'")
    print("  - History should contain 2 turns (4 messages total)")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_conversation_history())
