import click
import asyncio
import glob
from pathlib import Path
from ..client import create_client, get_data_dir

@click.command()
@click.argument('prompt')
@click.option('--file', '-f', multiple=True, help='附加文件（支持 glob 模式，可多次使用）')
@click.option('--model', '-m', default='gemini-3.0-flash', help='模型名称')
@click.option('--stream/--no-stream', default=False, help='流式输出')
@click.option('--output', '-o', type=click.Path(), help='保存响应到文件')
@click.option('--image-output', '-i', type=click.Path(), help='图片保存目录')
def generate_cmd(prompt, file, model, stream, output, image_output):
    """生成内容（单轮对话）"""
    asyncio.run(_generate(prompt, file, model, stream, output, image_output))

async def _generate(prompt, files, model, stream, output, image_output):
    try:
        # 展开 glob 模式
        expanded_files = []
        for pattern in files:
            matches = glob.glob(pattern)
            if matches:
                expanded_files.extend(matches)
            elif Path(pattern).exists():
                expanded_files.append(pattern)
            else:
                click.echo(f"警告: 文件不存在或模式无匹配: {pattern}", err=True)

        client = await create_client()

        if stream:
            async for chunk in client.generate_content_stream(prompt, files=expanded_files or None, model=model):
                if chunk.text_delta:
                    click.echo(chunk.text_delta, nl=False)
            click.echo()
        else:
            result = await client.generate_content(prompt, files=expanded_files or None, model=model)

            if result.thoughts:
                click.echo(f"\n[思考过程]\n{result.thoughts}\n")

            click.echo(result.text)

            if result.images:
                if image_output:
                    images_dir = Path(image_output)
                else:
                    images_dir = get_data_dir() / "images"
                images_dir.mkdir(parents=True, exist_ok=True)
                for i, img in enumerate(result.images):
                    # gemini-webapi 的 save() 方法接受目录路径，会自动生成文件名
                    await img.save(str(images_dir))
                    # 查找刚保存的图片
                    saved_files = sorted(images_dir.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
                    if saved_files:
                        click.echo(f"\n[图片已保存: {saved_files[0]}]")

            if output:
                Path(output).write_text(result.text)
                click.echo(f"\n[已保存到: {output}]")

    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        raise click.Abort()
