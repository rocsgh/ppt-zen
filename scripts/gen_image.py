#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate one slide image from a prompt, using ANY OpenAI-compatible images endpoint.

PPT-Zen ships no image model: this reads your own credentials and POSTs
{model,prompt,size,n} to {BASE}/images/generations, reading back data[0].b64_json
(or data[0].url). Swap in OpenAI, a relay, or any compatible gateway.

  python3 scripts/gen_image.py "your full-page prompt" out.jpg
  python3 scripts/gen_image.py --check    # doctor: config + a live endpoint probe

Config: real environment variables first, then ./.env, then <repo>/.env beside this
script. Keys: IMAGE_API_BASE_URL, IMAGE_API_KEY, IMAGE_MODEL, IMAGE_SIZE.
"""
import base64, json, os, sys, time, urllib.error, urllib.request

SHAPE = ('  it must accept : POST <BASE>/images/generations  {"model":"…","prompt":"…","size":"1024x1024","n":1}\n'
         '  and return     : {"data":[{"b64_json":"…"}]}   or   {"data":[{"url":"…"}]}')
PROVIDERS = "  ready-to-paste .env templates: references/providers.md"


class NotJSON(Exception):
    """Endpoint answered 200 with something that isn't JSON — usually an HTML page."""


def load_env():
    """Real env wins, then ./.env, then <repo>/.env. Returns (config, files read)."""
    cfg, files = dict(os.environ), []
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (os.path.abspath(".env"), os.path.abspath(os.path.join(here, "..", ".env"))):
        if not os.path.exists(path) or path in files:
            continue
        files.append(path)
        for ln in open(path, encoding="utf-8"):
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1)
                cfg.setdefault(k.strip(), v.strip())
    return cfg, files


def config():
    cfg, files = load_env()   # -> base, key, model, size, .env files read, note
    base = cfg.get("IMAGE_API_BASE_URL", "").rstrip("/")
    key, note = cfg.get("IMAGE_API_KEY", ""), ""
    # Zero-question path: an exported OPENAI_API_KEY is reused as-is — but only when the
    # base URL still points at OpenAI, so a foreign relay key is never sent to the wrong host.
    if not usable(key) and usable(cfg.get("OPENAI_API_KEY", "")) and base in ("", "https://api.openai.com/v1"):
        key, note = cfg["OPENAI_API_KEY"], "reusing your exported OPENAI_API_KEY"
    return (base or "https://api.openai.com/v1", key, cfg.get("IMAGE_MODEL", "gpt-image-1"),
            cfg.get("IMAGE_SIZE", "1536x1024"), files, note)


def usable(key):
    return bool(key) and not key.startswith("sk-your-key")


def key_line(key):
    if not usable(key):
        return "placeholder — still the .env.example value" if key else "NOT SET"
    return (key[:6] + "…" + key[-4:]) if len(key) > 12 else "set (suspiciously short)"


def fetch_image(base, key, model, prompt, size, timeout):
    body = json.dumps({"model": model, "prompt": prompt, "size": size, "n": 1}).encode()
    req = urllib.request.Request(base + "/images/generations", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    raw = urllib.request.urlopen(req, timeout=timeout).read()
    try:
        d = json.loads(raw)["data"][0]
    except ValueError:
        raise NotJSON(raw[:160].decode("utf-8", "replace").replace("\n", " "))
    return base64.b64decode(d["b64_json"]) if d.get("b64_json") else urllib.request.urlopen(d["url"], timeout=90).read()


def fail(verdict, fix):
    print("  ✗ " + verdict + "\n    fix: " + fix)
    return 1


def http_verdict(code, body, base):
    if code in (401, 403):
        return fail("HTTP %d — the endpoint refused your key.\n    %s" % (code, body),
                    "the key is wrong, expired, or has no image quota at %s." % base)
    if code in (404, 405):
        return fail("HTTP %d — this base URL does not implement the OpenAI images API.\n" % code +
                    "    Chat-only relays proxy /chat/completions and nothing else.\n" + SHAPE,
                    "point IMAGE_API_BASE_URL at an endpoint that serves images.\n" + PROVIDERS)
    if code >= 500:
        return fail("HTTP %d — failing on the endpoint's own side.\n    %s" % (code, body),
                    "retry in a minute; if it persists the gateway is down, not your config.")
    return fail("HTTP %d — request rejected.\n    %s" % (code, body),
                "usually IMAGE_MODEL isn't a model this endpoint serves, or IMAGE_SIZE is unsupported.")


def check():
    base, key, model, size, files, note = config()
    print("PPT-Zen image doctor\n  .env read : %s\n  endpoint  : %s/images/generations\n"
          "  model     : %s   (IMAGE_MODEL)\n  size      : %s   (IMAGE_SIZE; assembly cover-crops to 16:9)\n"
          "  api key   : %s%s\n" % (" , ".join(files) if files else "none found — using environment variables only",
                                base, model, size, key_line(key), ("   (%s)" % note) if note else ""))
    if not usable(key):
        return fail("no usable key, so nothing can be generated yet.",
                    "cp .env.example .env and put your own key in IMAGE_API_KEY — PPT-Zen ships\n"
                    "         no key and no model, the pixels come from your endpoint.\n" + PROVIDERS)
    for probe in ("1024x1024", size):
        print("  probing the endpoint (1 test image, %s) ..." % probe)
        try:
            fetch_image(base, key, model, "test swatch, plain gray", probe, 90)
        except urllib.error.HTTPError as e:
            body = e.read()[:200].decode("utf-8", "replace").replace("\n", " ").strip()
            if e.code == 400 and probe != size and "size" in body.lower():
                print("  · %s not supported here — retrying at your IMAGE_SIZE" % probe)
                continue
            return http_verdict(e.code, body, base)
        except NotJSON as e:
            return fail("answered 200 but not JSON — a web page, not an images API.\n    %s\n" % e +
                        "    Chat-only gateways and dashboard URLs both look like this.\n" + SHAPE,
                        "check IMAGE_API_BASE_URL (it should end in something like /v1).\n" + PROVIDERS)
        except (KeyError, IndexError, TypeError) as e:
            return fail("answered JSON in the wrong shape (%s) — no data[0].b64_json / data[0].url.\n" % e + SHAPE,
                        "ask your provider for an endpoint that returns the OpenAI images shape.")
        except (urllib.error.URLError, OSError) as e:
            return fail("could not reach the endpoint: %s" % e,
                        "unreachable, slow or blocked here — check IMAGE_API_BASE_URL, network, proxy.")
        print("  ✓ endpoint OK, 1 test image generated (%s). You're ready to make a deck." % probe)
        return 0


def generate(prompt, out):
    base, key, model, size, _, _ = config()
    if not usable(key):
        sys.exit("gen_image: no usable IMAGE_API_KEY — run `python3 %s --check` for the fix." % sys.argv[0])
    for attempt in range(3):
        t0 = time.time()
        print("gen_image: requesting %s (attempt %d/3) ..." % (out, attempt + 1), file=sys.stderr, flush=True)
        try:
            img = fetch_image(base, key, model, prompt, size, 240)
        except urllib.error.HTTPError as e:
            body = e.read()[:200].decode("utf-8", "replace").replace("\n", " ").strip()
            if e.code < 500:   # your config, not the weather — retrying can't help
                sys.exit("gen_image: HTTP %d — %s\n  run `python3 %s --check` for a diagnosis." % (e.code, body, sys.argv[0]))
            err = "HTTP %d %s" % (e.code, body)
        except NotJSON as e:
            sys.exit("gen_image: endpoint returned a non-JSON page (%s)\n  run `python3 %s --check`." % (e, sys.argv[0]))
        except (urllib.error.URLError, OSError) as e:
            err = str(e)
        else:
            open(out, "wb").write(img)
            print("gen_image: wrote %s (%ds, %d bytes)" % (out, time.time() - t0, len(img)), file=sys.stderr)
            return
        if attempt == 2:
            sys.exit("gen_image: gave up after 3 attempts — %s" % err)
        wait = (10, 30)[attempt]
        print("gen_image: %s — retrying in %ds" % (err, wait), file=sys.stderr, flush=True)
        time.sleep(wait)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        sys.exit(check())
    if len(sys.argv) < 3:
        sys.exit("usage: gen_image.py \"<prompt>\" <out.jpg>   |   gen_image.py --check")
    generate(sys.argv[1], sys.argv[2])
