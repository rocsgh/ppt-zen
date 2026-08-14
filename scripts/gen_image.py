#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate one slide image from a prompt, using ANY OpenAI-compatible images endpoint.

PPT-Zen ships no image model. This reads your own credentials from .env (or the
environment) and calls POST {BASE}/images/generations. Swap the endpoint/model
freely — OpenAI, a relay, or any compatible gateway.

Usage:
  python3 scripts/gen_image.py "your full-page prompt" out.jpg
  python3 scripts/gen_image.py --check          # verify config before a long run

Config lookup order: real environment variables first, then ./.env (current
directory), then <repo>/.env next to this script's parent. Keys: IMAGE_API_BASE_URL,
IMAGE_API_KEY, IMAGE_MODEL, IMAGE_SIZE. The endpoint must accept
POST {BASE}/images/generations with {model,prompt,size,n} and return
data[0].b64_json or data[0].url (the OpenAI images API shape).
"""
import base64, json, os, sys, urllib.request


def load_env():
    cfg = dict(os.environ)
    for name in (".env", os.path.join(os.path.dirname(__file__), "..", ".env")):
        if os.path.exists(name):
            for ln in open(name, encoding="utf-8"):
                ln = ln.strip()
                if ln and not ln.startswith("#") and "=" in ln:
                    k, v = ln.split("=", 1)
                    cfg.setdefault(k.strip(), v.strip())
    return cfg


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        c = load_env()
        src = "environment only"
        for name in (".env", os.path.join(os.path.dirname(__file__), "..", ".env")):
            if os.path.exists(name):
                src = os.path.abspath(name); break
        print("config   :", src)
        base = c.get("IMAGE_API_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        key = c.get("IMAGE_API_KEY", "")
        ok = bool(key) and not key.startswith("sk-your-key")
        print("endpoint :", base + "/images/generations")
        print("model    :", c.get("IMAGE_MODEL", "gpt-image-1"))
        print("size     :", c.get("IMAGE_SIZE", "1536x1024"), "(assembly cover-crops to 16:9)")
        print("api key  :", "set" if ok else "MISSING - copy .env.example to .env and fill it in")
        sys.exit(0 if ok else 1)
    if len(sys.argv) < 3:
        sys.exit("usage: gen_image.py \"<prompt>\" <out.jpg>   |   gen_image.py --check")
    prompt, out = sys.argv[1], sys.argv[2]
    c = load_env()
    base = c.get("IMAGE_API_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    key = c.get("IMAGE_API_KEY", "")
    model = c.get("IMAGE_MODEL", "gpt-image-1")
    size = c.get("IMAGE_SIZE", "1536x1024")
    if not key or key.startswith("sk-your-key"):
        sys.exit("Set IMAGE_API_KEY in .env (copy .env.example). PPT-Zen ships no image key.")
    body = json.dumps({"model": model, "prompt": prompt, "size": size, "n": 1}).encode()
    req = urllib.request.Request(base + "/images/generations", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=240))
    d = r["data"][0]
    img = base64.b64decode(d["b64_json"]) if d.get("b64_json") else urllib.request.urlopen(d["url"], timeout=90).read()
    open(out, "wb").write(img)
    print("wrote", out, len(img), "bytes")


if __name__ == "__main__":
    main()
