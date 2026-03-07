import click
import asyncio
from ..client import create_client, get_data_dir
from ..db import SessionDB

@click.group()
def session_group():
    """管理对话会话"""
    pass

@session_group.command()
def list():
    """列出所有会话"""
    asyncio.run(_list())

async def _list():
    try:
        db = SessionDB(get_data_dir() / "sessions.db")
        await db.init()
        sessions = await db.list_all()

        if not sessions:
            click.echo("没有找到会话")
            return

        click.echo("会话列表：\n")
        for s in sessions:
            click.echo(f"  {s['id']} (cid: {s['cid']})")

    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        raise click.Abort()

@session_group.command()
@click.argument('session_id')
def history(session_id):
    """显示会话历史"""
    asyncio.run(_history(session_id))

async def _history(session_id):
    try:
        client = await create_client()
        db = SessionDB(get_data_dir() / "sessions.db")
        await db.init()

        metadata = await db.load(session_id)
        if not metadata or not metadata[0]:
            click.echo(f"会话无历史记录: {session_id}")
            return

        turns = await client.read_chat(metadata[0])
        click.echo(f"会话 {session_id} 的历史记录：\n")
        for i, turn in enumerate(turns):
            click.echo(f"轮次 {i+1}:")
            click.echo(f"  {turn}\n")

    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        raise click.Abort()

@session_group.command()
@click.argument('session_id')
def delete(session_id):
    """删除会话"""
    asyncio.run(_delete(session_id))

async def _delete(session_id):
    try:
        db = SessionDB(get_data_dir() / "sessions.db")
        await db.init()
        await db.delete(session_id)
        click.echo(f"已删除会话: {session_id}")

    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        raise click.Abort()
