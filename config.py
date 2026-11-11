import os
import tomllib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

CFG = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))

SECTIONS = {
    "union": ("gateway", "method", "elite_id", "page_size"),
    "mail": ("host", "port", "subject"),
    "path": ("db", "figures", "font_candidates", "font_keywords"),
    "report": ("days",),
    "name": ("enabled", "pattern", "anchor", "template", "fallback"),
    "runtime": ("timeout", "retries", "backoff"),
}

KEYS = ("JD_APPKEY", "JD_SECRET", "SMTP", "MAIL_FROM", "MAIL_TO", "GROUP_ID", "OWNER_UNION_ID")


def check_config() -> None:
    missing = [f"[{s}].{k}" for s, keys in SECTIONS.items() for k in keys if k not in CFG.get(s, {})]
    if missing:
        raise RuntimeError("配置缺失：" + "、".join(missing))


def check_secrets() -> None:
    missing = [k for k in KEYS if not os.environ.get(k)]
    if missing:
        raise RuntimeError("私有环境变量缺失：" + "、".join(missing))


check_config()

UNION = CFG["union"]
MAIL = CFG["mail"]
REPORT = CFG["report"]
NAME = CFG["name"]
RUNTIME = CFG["runtime"]

CST = timezone(timedelta(hours=8))


def now() -> datetime:
    return datetime.now(CST)


DB_PATH = ROOT / CFG["path"]["db"]
FIGURES_DIR = ROOT / CFG["path"]["figures"]
FONT_CANDIDATES = CFG["path"]["font_candidates"]
FONT_KEYWORDS = CFG["path"]["font_keywords"]

SMTP_HOST = MAIL["host"]
SMTP_PORT = MAIL["port"]
SUBJECT = MAIL["subject"]

BLUE = "#0F4D92"
RED = "#B64342"
