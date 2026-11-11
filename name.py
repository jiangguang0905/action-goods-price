import re

from config import NAME

MODEL = re.compile(NAME["pattern"])


def shorten(brand: str, sku_name: str) -> str:
    hits = list(MODEL.finditer(sku_name)) if NAME["enabled"] else []
    if not hits:
        return f"{brand} {sku_name}".strip() if NAME["fallback"] == "brand" else sku_name
    hit = hits[-1] if NAME["anchor"] == "last" else hits[0]
    return NAME["template"].format(
        brand=brand,
        sku_name=sku_name,
        model=hit.group(0).strip(),
        tail=sku_name[hit.start():].strip(),
    ).strip()
