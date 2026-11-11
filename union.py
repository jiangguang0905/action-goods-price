import hashlib
import json
import logging
import os
import time

import requests

from config import RUNTIME, UNION, now

Row = tuple[str, str, str, float, float, str]


def sign(secret: str, params: dict[str, str]) -> str:
    body = secret + "".join(k + v for k, v in sorted(params.items())) + secret
    return hashlib.md5(body.encode("utf-8")).hexdigest().upper()


def post(params: dict[str, str]) -> dict:
    for attempt in range(RUNTIME["retries"] + 1):
        try:
            resp = requests.post(UNION["gateway"], data=params, timeout=RUNTIME["timeout"])
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, ValueError) as exc:
            if attempt == RUNTIME["retries"]:
                raise RuntimeError(f"取价失败，已重试{attempt + 1}次：{exc}") from exc
            delay = RUNTIME["backoff"] * (attempt + 1)
            logging.warning("取价请求第%d次失败（%s），%d秒后重试", attempt + 1, exc, delay)
            time.sleep(delay)
    raise RuntimeError("取价重试耗尽")


def query() -> list[dict]:
    biz = {"goodsReq": {"eliteId": UNION["elite_id"], "groupId": int(os.environ["GROUP_ID"]), "ownerUnionId": int(os.environ["OWNER_UNION_ID"]), "pageIndex": 1, "pageSize": UNION["page_size"]}}
    params = {
        "v": "1.0",
        "method": UNION["method"],
        "app_key": os.environ["JD_APPKEY"],
        "sign_method": "md5",
        "format": "json",
        "timestamp": now().strftime("%Y-%m-%d %H:%M:%S"),
        "param_json": json.dumps(biz, ensure_ascii=False, separators=(",", ":")),
    }
    params["sign"] = sign(os.environ["JD_SECRET"], params)
    obj = post(params)
    key = next((k for k in obj if k.endswith("_response")), None)
    if key is None:
        raise RuntimeError(f"联盟网关未返回响应体：{obj}")
    result = json.loads(obj[key]["result"])
    if result.get("code") != 200 or not isinstance(result.get("data"), list):
        raise RuntimeError(f"联盟网关业务异常：{result}")
    fields = ("spuid", "skuName", "brandName", "priceInfo", "purchasePriceInfo", "materialUrl")
    data = result["data"]
    bad = [str(i) for i, d in enumerate(data) if any(k not in d for k in fields)]
    if bad:
        raise RuntimeError(f"商品字段缺失，序号：{'、'.join(bad)}")
    logging.info("选品库返回商品%d件", len(data))
    return data


def rows() -> list[Row]:
    return list(map(lambda d: (
        str(d["spuid"]),
        d["skuName"],
        d["brandName"],
        float(d["priceInfo"]["price"]),
        float(d["purchasePriceInfo"]["purchasePrice"]),
        "https://" + d["materialUrl"],
    ), query()))
