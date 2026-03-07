#!/usr/bin/env python3
import subprocess
import sys

def run_cmd(cmd):
    """运行命令并返回输出"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_cli():
    """测试 CLI 命令"""
    print("Test 1: CLI Help")
    code, out, err = run_cmd("uv run gemini-web --help")
    if code == 0 and "Gemini Web CLI" in out:
        print("✓ CLI help works\n")
    else:
        print(f"✗ Failed: {err}\n")
        return

    print("Test 2: Auth Show")
    code, out, err = run_cmd("uv run gemini-web auth show")
    if code == 0:
        print(f"✓ Auth status:\n{out}\n")
    else:
        print(f"✗ Failed: {err}\n")

    print("Test 3: Session List")
    code, out, err = run_cmd("uv run gemini-web session list")
    if code == 0:
        print(f"✓ Sessions:\n{out}\n")
    else:
        print(f"✗ Failed: {err}\n")

    print("Test 4: Generate (requires auth)")
    code, out, err = run_cmd('uv run gemini-web generate "1+1等于几？" 2>&1 | tail -5')
    if code == 0:
        print(f"✓ Generate:\n{out}\n")
    else:
        print(f"Note: Generate requires auth setup\n{err[:200]}\n")

    print("Test 5: Generate Image")
    code, out, err = run_cmd('uv run gemini-web generate "画一只可爱的猫" --image-output . 2>&1 | tail -10')
    if code == 0:
        print(f"✓ Image generation:\n{out}\n")
    else:
        print(f"✗ Failed: {err[:200]}\n")

    print("Test 6: Image Understanding")
    code, out, err = run_cmd('ls *.png 2>/dev/null | head -1 | xargs -I {} uv run gemini-web generate "描述这张图片" --file {} 2>&1 | tail -10')
    if code == 0 and out.strip():
        print(f"✓ Image understanding:\n{out}\n")
    else:
        print(f"Note: No image found\n")

    print("Test 7: File Upload")
    code, out, err = run_cmd('uv run gemini-web generate "总结这个文件的主要内容" --file README.md 2>&1 | tail -10')
    if code == 0:
        print(f"✓ File upload:\n{out}\n")
    else:
        print(f"✗ Failed: {err[:200]}\n")

if __name__ == "__main__":
    test_cli()
