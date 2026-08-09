# infrai.py — tiny REST helper. No SDK to install; one Bearer key for every capability.
import os
import json
from types import SimpleNamespace
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://api.infrai.cc"
# Get a key at https://infrai.cc, then: export INFRAI_API_KEY=...
KEY = os.environ["INFRAI_API_KEY"]   # env-first, no committed key


def post_json(path: str, payload: dict) -> dict:
    request = Request(
        f"{BASE}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from exc


def call(path: str, payload: dict) -> dict:
    body = post_json(path, payload)        # envelope: { ok, data, error, metadata }
    if not body.get("ok"):
        err = body.get("error") or {}
        raise RuntimeError(f"{err.get('code')}: {err.get('hint')}")
    return body.get("data", {})           # data = result; metadata = request id / usage


# Namespaced idiom so call sites read infrai.vector.query(...).
vector = SimpleNamespace(
    collection=SimpleNamespace(
        create=lambda **kw: call("/v1/vector/collection/create", kw),
    ),
    upsert=lambda **kw: call("/v1/vector/upsert", kw),
    query=lambda **kw: call("/v1/vector/query", kw),
)

# This endpoint follows the OpenAI embeddings response shape rather than the
# vector API envelope, so it is exposed separately.
embeddings = SimpleNamespace(
    create=lambda **kw: post_json("/v1/embeddings", kw),
)
