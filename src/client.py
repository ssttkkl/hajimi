import os
import json
from pathlib import Path
from gemini_webapi import GeminiClient

def get_data_dir() -> Path:
    """获取平台特定的数据目录"""
    if os.name == 'nt':
        data_dir = Path(os.environ.get('APPDATA', '')) / "gemini-web"
    elif os.uname().sysname == 'Darwin':
        data_dir = Path.home() / "Library/Application Support/gemini-web"
    else:
        data_dir = Path.home() / ".local/share/gemini-web"

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_config_path() -> Path:
    """获取配置文件路径"""
    return Path.home() / ".config/gemini-web/cookies.json"

async def create_client() -> GeminiClient:
    """创建并初始化 GeminiClient"""
    secure_1psid = os.environ.get("GEMINI_COOKIE_1PSID")
    secure_1psidts = os.environ.get("GEMINI_COOKIE_1PSIDTS")

    if not secure_1psid or not secure_1psidts:
        config_path = get_config_path()
        if config_path.exists():
            cookies_data = json.loads(config_path.read_text())
            secure_1psid = secure_1psid or cookies_data.get("secure_1psid")
            secure_1psidts = secure_1psidts or cookies_data.get("secure_1psidts")

    if not secure_1psid or not secure_1psidts:
        raise ValueError("缺少必需的 Cookie: GEMINI_COOKIE_1PSID 和 GEMINI_COOKIE_1PSIDTS\n请运行 'gemini-web auth setup' 配置认证")

    client = GeminiClient(secure_1psid=secure_1psid, secure_1psidts=secure_1psidts)
    await client.init()
    return client
