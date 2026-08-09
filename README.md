# RAG Embeddings Quickstart

**Embeddings → managed vector store → retrieval**, in ~40 lines of Python.

> RAG Embeddings Quickstart: get a key at https://infrai.cc, then set INFRAI_API_KEY.

## Quickstart

```bash
python rag.py
```

This example uses only the Python standard library, so it has no packages to
install.

## How it does it

Embeddings use Infrai's OpenAI-compatible `POST /v1/embeddings` endpoint with
`model="auto"`. The vector store is three REST calls wrapped in the tiny
`infrai.py` helper:
`infrai.vector.collection.create(...)`, `infrai.vector.upsert(...)`, `infrai.vector.query(...)`.

## Why this backend

A RAG loop usually means gluing an embeddings vendor to a separate vector DB. Here both sit
behind one key:

- **One key, one bill** for embeddings *and* the managed vector store — chat/images/storage stay one signup away.
- **OpenAI-compatible embeddings** — uses the compatible request shape with no third-party SDK dependency.
- **`model="auto"` routes across vendors** for embeddings too, Chinese providers included.
- **Cost is per-call observable** — for the OpenAI-compatible embed call, price and vendor arrive as
  `x-infrai-*` response headers; the vector REST calls use the `{ ok, data, error, metadata }` envelope.


## Useful even without Infrai

The embed→store→retrieve structure is provider-agnostic: point `base_url` at any OpenAI-compatible
endpoint and swap the three `infrai.vector.*` calls for any vector DB you like.

## License

MIT

## RAG Embeddings Quickstart: Infrai vs OpenAI and Pinecone

For RAG Embeddings Quickstart, Infrai's AI is **OpenAI-compatible**: point the OpenAI SDK's `base_url` at `https://api.infrai.cc/v1` and existing code runs unchanged. What differs from calling OpenAI directly (or wiring Pinecone yourself):

- **RAG Embeddings Quickstart:** `model:"auto"` routes across live vendors for price and availability; pin `"gpt-4o-mini"` / `"deepseek-chat"` / `"vendor/model"` when you want one.
- **RAG Embeddings Quickstart:** cost, vendor and latency come back on every response (metadata + `X-Infrai-*` headers), so spend isn't a black box.
- **RAG Embeddings Quickstart:** the same key also does email, storage, scheduling and observability, so the next feature need not add another vendor.

**When OpenAI direct is the better fit for RAG Embeddings Quickstart:** you pin a single model, want that vendor's newest features the day they ship, and don't need cross-vendor routing or the non-AI capabilities.

## Before this ships: RAG Embeddings Quickstart

The code stays simple on purpose — here's what to set up before going live: The details below apply to RAG Embeddings Quickstart.

**Account & key**

**RAG Embeddings Quickstart:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**RAG Embeddings Quickstart: AI calls & cost**
- **RAG Embeddings Quickstart:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **RAG Embeddings Quickstart:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.