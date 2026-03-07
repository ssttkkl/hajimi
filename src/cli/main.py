import click
from .auth import auth_group
from .generate import generate_cmd
from .chat import chat_cmd
from .session import session_group

@click.group()
def cli():
    """Gemini Web CLI - 与 Gemini AI 交互的命令行工具"""
    pass

@cli.command()
def mcp():
    """启动 MCP 服务器"""
    from .mcp_server import run
    run()

cli.add_command(auth_group, name="auth")
cli.add_command(generate_cmd, name="generate")
cli.add_command(chat_cmd, name="chat")
cli.add_command(session_group, name="session")

def main():
    cli()
