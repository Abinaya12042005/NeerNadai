"""
rag_chatbot.py
----------------
Idhu than namma "RAG chatbot" - Retrieval Augmented Generation.

How it works (2 steps):
  STEP 1 - RETRIEVAL: user kekkura question-ku, knowledge_base/ folder-la
           irundhu mostly-related chunks-a "sentence-transformers" (free,
           local, no API key needed) embeddings vachi FAISS-la thedi eduthukum.
  STEP 2 - GENERATION: andha retrieved chunks-a "context"-a kudutu, IBM
           Granite model (free Hugging Face Inference API) kitta final
           natural-language answer generate pannum.

If you don't have a Hugging Face token yet (or want a fully offline demo
for now), the code automatically falls back to an "extractive" answer
built directly from the retrieved chunks - so the chatbot always works,
even with zero API keys. This is documented in the README.

Get a FREE Hugging Face token: https://huggingface.co/settings/tokens
Then set it as an environment variable:  export HF_TOKEN="hf_xxxxx"
"""

import os
import glob
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import requests

# ---------- Config ----------
KB_DIR = "knowledge_base"
CHUNK_SIZE = 400          # characters per chunk
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"      # small, free, runs on CPU
HF_MODEL = "ibm-granite/granite-3.0-8b-instruct"  # IBM Granite - satisfies the
                                                    # internship's "Technologies
                                                    # Used" requirement
HF_TOKEN = os.environ.get("HF_TOKEN", "")

_embedder = None
_index = None
_chunks = []


def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL_NAME)
    return _embedder


def _load_and_chunk_docs():
    """Read every .txt file in knowledge_base/ and split into small chunks."""
    chunks = []
    for path in glob.glob(os.path.join(KB_DIR, "*.txt")):
        with open(path, "r") as f:
            text = f.read()
        for i in range(0, len(text), CHUNK_SIZE):
            chunk = text[i:i + CHUNK_SIZE].strip()
            if chunk:
                chunks.append(chunk)
    return chunks


def build_index():
    """Build (or rebuild) the FAISS vector index from the knowledge base.
    Call this once at app startup, and again anytime knowledge_base/ changes."""
    global _index, _chunks
    _chunks = _load_and_chunk_docs()
    embedder = _get_embedder()
    embeddings = embedder.encode(_chunks, convert_to_numpy=True, normalize_embeddings=True)
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)   # inner product on normalized vectors = cosine similarity
    _index.add(embeddings)
    print(f"RAG index built with {len(_chunks)} chunks.")


def _retrieve(query, top_k=3):
    embedder = _get_embedder()
    q_emb = embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    scores, idxs = _index.search(q_emb, top_k)
    return [_chunks[i] for i in idxs[0] if i < len(_chunks)]


def _generate_with_granite(query, context):
    """Call IBM Granite via the free Hugging Face Inference API."""
    prompt = (
        "You are a helpful assistant for a Chennai water-wastage awareness "
        "website. Answer the user's question using ONLY the context below. "
        "Keep the answer short (3-4 sentences) and practical.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200, "temperature": 0.3}}

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    result = resp.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        text = result[0]["generated_text"]
        # The API echoes the prompt back - strip it so we only return the new part
        return text.split("Answer:")[-1].strip()
    return str(result)


def _fallback_answer(query, retrieved_chunks):
    """Used when no HF_TOKEN is set, or the API call fails - still gives a
    useful, grounded answer built directly from the retrieved knowledge base
    text, so the chatbot never breaks."""
    joined = "\n\n".join(retrieved_chunks)
    return (
        "Here's what I found in the project's knowledge base related to "
        f"your question:\n\n{joined}\n\n"
        "(Tip: set the HF_TOKEN environment variable to enable full "
        "AI-generated answers using IBM Granite.)"
    )


def answer_query(query, top_k=3):
    """Main entry point used by app.py"""
    if _index is None:
        build_index()

    retrieved = _retrieve(query, top_k=top_k)
    context = "\n\n".join(retrieved)

    if HF_TOKEN:
        try:
            return _generate_with_granite(query, context)
        except Exception as e:
            print("Hugging Face API call failed, using fallback:", e)
            return _fallback_answer(query, retrieved)
    else:
        return _fallback_answer(query, retrieved)


if __name__ == "__main__":
    # Quick manual test: python rag_chatbot.py
    build_index()
    while True:
        q = input("\nAsk the water chatbot (or 'quit'): ")
        if q.lower() == "quit":
            break
        print("\n" + answer_query(q))
