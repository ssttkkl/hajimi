import os
import json
from pathlib import Path
from gemini_webapi import GeminiClient, AuthError

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

def get_auth_error_message() -> str:
    """获取认证错误提示信息"""
    return """认证失败或 Cookie 已过期。

请通过以下方式重新配置：

方式 1（推荐）- 自动登录：
    gemini-web auth login

方式 2 - 手动输入：
    gemini-web auth setup

方式 3 - 环境变量：
    export GEMINI_COOKIE_1PSID="YOUR_1PSID_VALUE"
    export GEMINI_COOKIE_1PSIDTS="YOUR_1PSIDTS_VALUE"
"""

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
        raise ValueError("缺少必需的 Cookie: GEMINI_COOKIE_1PSID 和 GEMINI_COOKIE_1PSIDTS\n\n" + get_auth_error_message())

    try:
        client = GeminiClient(secure_1psid=secure_1psid, secure_1psidts=secure_1psidts)
        await client.init()
        return client
    except AuthError as e:
        raise ValueError(f"认证失败: {e}\n\n{get_auth_error_message()}")
    except Exception as e:
        # 检查是否是认证相关的错误
        error_str = str(e).lower()
        if any(keyword in error_str for keyword in ['cookie', 'auth', 'token', 'unauthorized', '401', '403']):
            raise ValueError(f"认证失败: {e}\n\n{get_auth_error_message()}")
        raise
