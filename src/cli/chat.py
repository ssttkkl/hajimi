import click
import asyncio
import uuid
import time
from ..client import create_client, get_data_dir
from ..db import SessionDB

@click.command()
@click.option('--session', '-s', default=None, help='会话 ID（恢复已有会话）')
@click.option('--model', '-m', default='gemini-3.0-flash', help='模型名称')
def chat_cmd(session, model):
    """交互式多轮对话"""
    asyncio.run(_chat(session, model))

async def _chat(session_id, model):
    try:
        client = await create_client()
        db = SessionDB(get_data_dir() / "sessions.db")
        await db.init()

        if not session_id:
            session_id = f"session-{int(time.time())}-{uuid.uuid4().hex[:12]}"
            click.echo(f"[新会话: {session_id}]\n")
            chat = None
        else:
            metadata = await db.load(session_id)
            if metadata:
                chat = client.start_chat(metadata=metadata, model=model)
                click.echo(f"[已恢复会话: {session_id}]\n")
            else:
                click.echo(f"[会话不存在，创建新会话: {session_id}]\n")
                chat = None

        click.echo("输入 'exit' 或 'quit' 退出对话\n")

        while True:
            try:
                prompt = click.prompt("你", type=str, prompt_suffix=": ").strip()
                if prompt.lower() in ['exit', 'quit']:
                    break
                if not prompt:
                    continue

                if chat is None:
                    # 使用 start_chat + send_message 来保持对话一致性
                    chat = client.start_chat(model=model)
                    result = await chat.send_message(prompt)
                else:
                    result = await chat.send_message(prompt)

                await db.save(session_id, chat.metadata)

                if result.thoughts:
                    click.echo(f"\n[思考] {result.thoughts}\n")
                click.echo(f"Gemini: {result.text}\n")

                if result.images:
                    images_dir = get_data_dir() / "images"
                    images_dir.mkdir(parents=True, exist_ok=True)
                    for i, img in enumerate(result.images):
                        img_path = images_dir / f"{session_id}_{int(time.time())}_{i}.png"
                        await img.save(str(img_path))
                        click.echo(f"[图片: {img_path}]")

            except KeyboardInterrupt:
                click.echo("\n\n[对话已中断]")
                break
            except EOFError:
                break
            except Exception as e:
                click.echo(f"\n[错误: {e}]\n", err=True)

    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        raise click.Abort()
