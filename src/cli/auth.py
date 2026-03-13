import click
import json
import os
import subprocess
import time
import tempfile
from pathlib import Path
from ..client import get_config_path, get_data_dir

@click.group()
def auth_group():
    """管理 Gemini 认证"""
    pass

@auth_group.command()
def setup():
    """交互式配置 Cookie"""
    click.echo("请输入 Gemini Cookie（从浏览器获取）：\n")

    secure_1psid = click.prompt("__Secure-1PSID", type=str)
    secure_1psidts = click.prompt("__Secure-1PSIDTS", type=str)

    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    cookies_data = {
        "secure_1psid": secure_1psid.strip(),
        "secure_1psidts": secure_1psidts.strip()
    }

    config_path.write_text(json.dumps(cookies_data, indent=2))
    click.echo(f"\n✓ Cookie 已保存到: {config_path}")

@auth_group.command()
def login():
    """启动调试 Chrome 自动获取 Cookie"""
    import asyncio
    asyncio.run(_login())

async def _login():
    """启动调试 Chrome 并自动获取 Gemini Cookie"""
    try:
        import psutil
    except ImportError:
        click.echo("错误: 需要 psutil 库，请运行 'uv add psutil'")
        return

    # 使用持久化的用户数据目录
    chrome_profile_dir = get_data_dir() / "chrome-profile"
    chrome_profile_dir.mkdir(parents=True, exist_ok=True)
    click.echo(f"启动调试 Chrome...")
    click.echo(f"Chrome Profile 目录: {chrome_profile_dir}")

    # 检测操作系统并启动 Chrome
    system = os.uname().sysname if hasattr(os, 'uname') else 'Windows'

    chrome_paths = {
        'Darwin': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chrome.app/Contents/MacOS/Chrome',
        ],
        'Linux': [
            '/usr/bin/google-chrome',
            '/usr/bin/chrome',
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
        ],
        'Windows': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ]
    }

    chrome_path = None
    for path in chrome_paths.get(system, []):
        if Path(path).exists():
            chrome_path = path
            break

    if not chrome_path:
        click.echo("错误: 未找到 Chrome，请手动安装 Chrome 浏览器")
        return

    # 启动 Chrome 调试模式
    debug_port = 9222
    cmd = [
        chrome_path,
        f'--remote-debugging-port={debug_port}',
        f'--user-data-dir={chrome_profile_dir}',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-default-apps',
        'https://gemini.google.com'
    ]

    click.echo(f"\n正在启动 Chrome: {chrome_path}")
    click.echo("请在浏览器中登录 Google 账号并访问 Gemini")
    click.echo("登录完成后，按 Enter 键自动获取 Cookie...")
    click.echo("(按 Ctrl+C 取消，或等待 10 分钟后自动关闭)\n")

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # 等待用户确认，设置 10 分钟超时
        import select
        import sys

        click.echo("等待登录...", nl=False)
        timeout_seconds = 600  # 10 分钟

        # 使用 select 实现带超时的 input
        if system == 'Windows':
            # Windows 不支持 select on stdin，使用普通 input
            input()
        else:
            # Unix-like 系统使用 select
            ready, _, _ = select.select([sys.stdin], [], [], timeout_seconds)
            if ready:
                sys.stdin.readline()
            else:
                click.echo("\n\n超时: 10 分钟未操作，自动关闭")
                return

        # 尝试从 Chrome 获取 cookie
        click.echo("正在获取 Cookie...")

        # 使用 browser_cookie3 尝试获取
        try:
            import browser_cookie3
            # 从 Chrome 获取指定域名的 cookie
            cj = browser_cookie3.chrome(domain_name='.google.com')

            secure_1psid = None
            secure_1psidts = None

            for cookie in cj:
                if cookie.name == '__Secure-1PSID':
                    secure_1psid = cookie.value
                elif cookie.name == '__Secure-1PSIDTS':
                    secure_1psidts = cookie.value

            if secure_1psid:
                config_path = get_config_path()
                config_path.parent.mkdir(parents=True, exist_ok=True)

                cookies_data = {
                    "secure_1psid": secure_1psid,
                    "secure_1psidts": secure_1psidts or ""
                }

                config_path.write_text(json.dumps(cookies_data, indent=2))
                click.echo(f"\n✓ Cookie 已保存到: {config_path}")
                click.echo(f"  __Secure-1PSID: {secure_1psid[:20]}...")
                if secure_1psidts:
                    click.echo(f"  __Secure-1PSIDTS: {secure_1psidts[:20]}...")
            else:
                click.echo("\n✗ 未找到 __Secure-1PSID cookie")
                click.echo("请确保已登录 Google 账号并访问了 Gemini")

        except Exception as e:
            click.echo(f"\n✗ 获取 Cookie 失败: {e}")
            click.echo("请手动运行 'gemini-web auth setup' 配置")

    except KeyboardInterrupt:
        click.echo("\n\n已取消")
    finally:
        # 关闭 Chrome
        click.echo("\n关闭 Chrome...")
        try:
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
        except:
            pass

@auth_group.command()
def show():
    """显示当前认证状态"""
    env_1psid = os.environ.get("GEMINI_COOKIE_1PSID")
    env_1psidts = os.environ.get("GEMINI_COOKIE_1PSIDTS")

    config_path = get_config_path()
    config_exists = config_path.exists()

    click.echo("认证状态：\n")
    click.echo(f"环境变量 GEMINI_COOKIE_1PSID: {'✓ 已设置' if env_1psid else '✗ 未设置'}")
    click.echo(f"环境变量 GEMINI_COOKIE_1PSIDTS: {'✓ 已设置' if env_1psidts else '✗ 未设置'}")
    click.echo(f"配置文件 {config_path}: {'✓ 存在' if config_exists else '✗ 不存在'}")

    if env_1psid and env_1psidts:
        click.echo("\n✓ 认证已配置（使用环境变量）")
    elif config_exists:
        click.echo("\n✓ 认证已配置（使用配置文件）")
    else:
        click.echo("\n✗ 认证未配置，请运行 'gemini-web auth setup'")
