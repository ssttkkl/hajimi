#!/usr/bin/env python3
import asyncio
import json
import sys

async def send_request(writer, method, params=None, req_id=1):
    """发送 JSON-RPC 请求"""
    request = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method,
        "params": params or {}
    }
    writer.write(json.dumps(request).encode() + b'\n')
    await writer.drain()

async def read_response(reader):
    """读取 JSON-RPC 响应"""
    line = await reader.readline()
    return json.loads(line.decode())

async def test_mcp_server():
    """测试 MCP Server"""
    process = await asyncio.create_subprocess_exec(
        "uv", "run", "gemini-web-mcp",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd="/Users/huangwenlong/.openclaw/skills/baoyu-danger-gemini-web"
    )

    reader = process.stdout
    writer = process.stdin

    try:
        # 等待服务器启动
        await asyncio.sleep(2)

        # 启动 stderr 读取任务
        async def print_stderr():
            while True:
                line = await process.stderr.readline()
                if not line:
                    break
                print(f"[STDERR] {line.decode().strip()}")

        stderr_task = asyncio.create_task(print_stderr())

        print("Test 1: Initialize")
        await send_request(writer, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        })
        response = await asyncio.wait_for(read_response(reader), timeout=5)
        print(f"✓ Server: {response.get('result', {}).get('serverInfo', {}).get('name')}\n")

        print("Test 2: List Tools")
        await send_request(writer, "tools/list", {}, 2)
        response = await asyncio.wait_for(read_response(reader), timeout=5)
        tools = response.get('result', {}).get('tools', [])
        print(f"✓ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool['name']}")
        print()

        print("Test 3: List Models")
        await send_request(writer, "tools/call", {
            "name": "gemini_list_models",
            "arguments": {}
        }, 3)
        response = await asyncio.wait_for(read_response(reader), timeout=10)
        print(f"✓ {response.get('result', {}).get('content', [{}])[0].get('text', '')}\n")

        print("Test 4: Generate Content")
        await send_request(writer, "tools/call", {
            "name": "gemini_generate",
            "arguments": {"prompt": "记住这个数字：42"}
        }, 4)
        response = await asyncio.wait_for(read_response(reader), timeout=30)
        contents = response.get('result', {}).get('content', [])
        session_id = None
        for content in contents:
            if content.get('type') == 'text':
                text = content.get('text', '')
                if text.startswith('Session ID:'):
                    session_id = text.split('Session ID: ')[1].strip()
                else:
                    print(f"✓ {text}")
        print()

        print("Test 5: Multi-turn Conversation")
        await send_request(writer, "tools/call", {
            "name": "gemini_generate",
            "arguments": {
                "prompt": "我刚才让你记住的数字是什么？",
                "session_id": session_id
            }
        }, 5)
        response = await asyncio.wait_for(read_response(reader), timeout=30)
        contents = response.get('result', {}).get('content', [])
        for content in contents:
            if content.get('type') == 'text' and not content.get('text', '').startswith('Session ID:'):
                print(f"✓ {content.get('text')}")
        print()

        print("Test 6: Get Session History")
        await send_request(writer, "tools/call", {
            "name": "gemini_get_history",
            "arguments": {"session_id": session_id}
        }, 6)
        response = await asyncio.wait_for(read_response(reader), timeout=10)
        contents = response.get('result', {}).get('content', [])
        for content in contents:
            if content.get('type') == 'text':
                print(f"✓ History:\n{content.get('text')[:500]}...")
        print()

    except asyncio.TimeoutError:
        print("✗ Timeout")
        stderr_data = await process.stderr.read()
        print(f"stderr: {stderr_data.decode()}")
    except Exception as e:
        print(f"✗ Error: {e}")
        stderr_data = await process.stderr.read()
        print(f"stderr: {stderr_data.decode()}")
    finally:
        if process.returncode is None:
            process.terminate()
            await process.wait()
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
