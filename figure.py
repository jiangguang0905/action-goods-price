import math
import re
from functools import lru_cache
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findSystemFonts

from config import BLUE, FONT_CANDIDATES, FONT_KEYWORDS, RED, REPORT

Row = tuple[str, float, float]


@lru_cache(maxsize=1)
def cjk_font() -> FontProperties:
    hits = [Path(p) for p in FONT_CANDIDATES if Path(p).is_file()]
    if not hits:
        hits = [Path(p) for p in findSystemFonts() if re.search(FONT_KEYWORDS, Path(p).name, re.I)]
    if not hits:
        raise RuntimeError("未找到中文字体，请检查 config.toml 的 [path] font_candidates")
    return FontProperties(fname=str(hits[0]))


def draw(rows: list[Row], out: Path) -> Path:
    font = cjk_font()
    plt.rcParams.update({
        "font.family": ["Arial", "DejaVu Sans", "sans-serif"],
        "font.size": 16,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": 2.5,
        "legend.frameon": False,
        "svg.fonttype": "none",
    })
    fig, ax = plt.subplots(figsize=(9, 4.8))
    x = list(range(len(rows)))
    ax.plot(x, [r[1] for r in rows], color=BLUE, linewidth=2.5, marker="o", markersize=7, label="JD price")
    ax.plot(x, [r[2] for r in rows], color=RED, linewidth=2.5, marker="o", markersize=7, label="Final price")
    step = max(1, math.ceil(len(rows) / 10))
    labels = [r[0][5:] if i % step == 0 or i == len(rows) - 1 else "" for i, r in enumerate(rows)]
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (CNY)")
    ax.set_title(f"近 {REPORT['days']} 日价格走势", fontproperties=font, fontsize=20)
    ax.legend()
    fig.tight_layout(pad=2)
    png = out.with_suffix(".png")
    fig.savefig(png, dpi=300)
    plt.close(fig)
    return png
