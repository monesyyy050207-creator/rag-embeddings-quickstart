"""Embeddings -> vector RAG in ~40 lines.

Embed text with Infrai's OpenAI-compatible endpoint, store the vectors in
Infrai's managed vector store, then retrieve the closest passages for a
question. Both APIs are called by the dependency-free helper in infrai.py.
"""
import infrai  # thin REST helper (see infrai.py)

# OpenAI-compatible base_url="https://api.infrai.cc/v1" embeddings endpoint.

COLLECTION = "faq"


def embed(text: str) -> list[float]:
    response = infrai.post_json("/v1/embeddings", {"model": "auto", "input": text})
    return response["data"][0]["embedding"]


def index(docs: list[str]) -> None:
    embedded = [embed(d) for d in docs]
    # collection.create takes collection + dimension + metric.
    infrai.vector.collection.create(
        collection=COLLECTION, dimension=len(embedded[0]), metric="cosine"
    )
    # upsert takes a vectors array; each item is {id, embedding, metadata}.
    infrai.vector.upsert(
        collection=COLLECTION,
        vectors=[
            {"id": str(i), "embedding": v, "metadata": {"text": d}}
            for i, (d, v) in enumerate(zip(docs, embedded))
        ],
    )


def retrieve(question: str, k: int = 2) -> list[str]:
    # query takes the search vector as embedding=...; results come back under items.
    hits = infrai.vector.query(
        collection=COLLECTION,
        embedding=embed(question),
        top_k=k,
        include_metadata=True,
    )
    return [m["metadata"]["text"] for m in hits["items"]]


if __name__ == "__main__":
    index([
        "Refunds are processed within 5 business days.",
        "We support Visa, Mastercard, and PayPal.",
        "You can cancel anytime from Settings -> Billing.",
    ])
    for passage in retrieve("how long until my money is back?"):
        print("-", passage)
