import click
import json
import os
from pathlib import Path
from ..client import get_config_path

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
