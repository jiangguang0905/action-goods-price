from config import REPORT

Row = tuple[str, float, float]
Block = tuple[str, str, list[Row], str]

STYLE = """<style>
body{margin:0;padding:24px;background:#f4f6f9;font-family:"Microsoft YaHei",Arial,sans-serif;color:#243044}
.card{max-width:760px;margin:0 auto;background:#ffffff;border:1px solid #e2e7ef;border-radius:10px;padding:32px}
h1{font-size:21px;margin:0;color:#0F4D92;letter-spacing:1px}
.date{font-size:13px;color:#8892a4;margin:6px 0 0}
.block{margin-top:28px;padding-top:24px;border-top:1px solid #e8edf3}
.name{font-size:16px;font-weight:bold;color:#243044}
.meta{font-size:12px;color:#8892a4;margin:4px 0 18px}
.meta a{color:#0F4D92;text-decoration:none}
table{width:100%;border-collapse:collapse;font-size:13px;margin-bottom:16px}
th,td{padding:9px 12px;border-bottom:1px solid #edf1f6;text-align:right}
th:first-child,td:first-child{text-align:left}
th{background:#f5f8fc;color:#0F4D92;font-weight:normal}
td.val{color:#0F4D92;font-weight:bold}
img{width:100%;max-width:700px;border:1px solid #e8edf3;border-radius:6px;display:block}
</style>"""


def section(name: str, url: str, rows: list[Row], cid: str) -> str:
    cur = rows[-1]
    return f"""<section class="block">
<div class="name">{name}</div>
<div class="meta"><a href="{url}">查看商品</a></div>
<table><tr><th>指标</th><th>京东价</th><th>到手价</th></tr>
<tr><td>当日价格</td><td class="val">¥{cur[1]:,.2f}</td><td class="val">¥{cur[2]:,.2f}</td></tr></table>
<img src="cid:{cid}" alt="近 {REPORT['days']} 日价格走势">
</section>"""


def build(blocks: list[Block], day: str) -> str:
    body = "".join(section(*b) for b in blocks)
    return f"""<html><head><meta charset="utf-8">{STYLE}</head><body><div class="card">
<h1>京东显卡价格日报</h1>
<div class="date">{day}</div>
{body}
</div></body></html>"""
