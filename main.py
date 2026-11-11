import logging
import sys

from config import DB_PATH, FIGURES_DIR, REPORT, SUBJECT, check_secrets, now
from figure import draw
from mailer import send
from name import shorten
from report import build
from store import init, recent, save_all
from union import rows


def run() -> None:
    check_secrets()
    day = now().date().isoformat()
    logging.info("日报开始，日期%s，时区东八区", day)
    init(DB_PATH)
    FIGURES_DIR.mkdir(exist_ok=True)
    items = rows()
    display = [(spuid, shorten(brand, raw), jd, final, url) for spuid, raw, brand, jd, final, url in items]
    print("\n".join(f"{name}\t{jd:.2f}" for _, name, jd, _, _ in display))
    save_all(DB_PATH, [(spuid, day, jd, final) for spuid, _, jd, final, _ in display])
    blocks = []
    images = []
    for spuid, name, _, _, url in display:
        history = recent(DB_PATH, spuid, REPORT["days"])
        cid = f"trend_{spuid}"
        png = draw(history, FIGURES_DIR / f"{spuid}_{day}")
        blocks.append((name, url, history, cid))
        images.append((cid, png))
    send(SUBJECT.format(date=day), build(blocks, day), images)
    logging.info("日报完成，商品%d件", len(items))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    try:
        run()
    except Exception:
        logging.exception("日报运行失败")
        sys.exit(1)
