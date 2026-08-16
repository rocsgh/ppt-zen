#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate one slide image from a prompt, using ANY OpenAI-compatible images endpoint.

PPT-Zen ships no image model: this reads your own credentials and POSTs
{model,prompt,size,n} to {BASE}/images/generations, reading back data[0].b64_json
(or data[0].url). Swap in OpenAI, a relay, or any compatible gateway.

  python3 scripts/gen_image.py "your full-page prompt" out.jpg
  python3 scripts/gen_image.py --check         # doctor: config + a live probe (bills one image)
  python3 scripts/gen_image.py --check-config  # the same report, no probe, nothing billed

Config: real environment variables first, then ./.env, then <repo>/.env beside this
script. Keys: IMAGE_API_BASE_URL, IMAGE_API_KEY, IMAGE_MODEL, IMAGE_SIZE, plus
IMAGE_MAX_ATTEMPTS (retry budget per page, default 3, clamped to 1..5).
"""
import base64, json, os, struct, sys, time, urllib.error, urllib.request

HELP = """gen_image.py — one slide image from one prompt, via any OpenAI-compatible images endpoint.

  gen_image.py "<full-page prompt>" out.jpg   generate one page
  gen_image.py --check                        config report + live probe — GENERATES ONE BILLABLE IMAGE
  gen_image.py --check-config                 config report only: nothing sent, nothing billed

Config keys (real env wins, then ./.env, then <repo>/.env beside this script):
  IMAGE_API_BASE_URL   API root, e.g. https://api.openai.com/v1 (the script appends /images/generations)
  IMAGE_API_KEY        your key — PPT-Zen ships none
  IMAGE_MODEL          default gpt-image-1
  IMAGE_SIZE           default 1536x1024; assembly cover-crops to 16:9
  IMAGE_MAX_ATTEMPTS   retry budget per page, default 3, clamped to 1..5

Retries cover 5xx and timeouts only (waits 10s, 30s, then 60s); a 4xx is your config
and won't fix itself, so it stops and points at --check. Output keeps the filename you
give it even if the endpoint answers PNG — assembly handles either.
Templates for OpenAI, relays and 火山方舟 / 豆包 Seedream: references/providers.md"""

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
    cfg, files = load_env()   # -> base, key, model, size, .env files read, note, attempts
    base = cfg.get("IMAGE_API_BASE_URL", "").rstrip("/")
    key, note = cfg.get("IMAGE_API_KEY", ""), ""
    # Zero-question path: an exported OPENAI_API_KEY is reused as-is — but only when the
    # base URL still points at OpenAI, so a foreign relay key is never sent to the wrong host.
    if not usable(key) and usable(cfg.get("OPENAI_API_KEY", "")) and base in ("", "https://api.openai.com/v1"):
        key, note = cfg["OPENAI_API_KEY"], "reusing your exported OPENAI_API_KEY"
    try:
        attempts = int(cfg.get("IMAGE_MAX_ATTEMPTS", 3))
    except ValueError:
        attempts = 3
    return (base or "https://api.openai.com/v1", key, cfg.get("IMAGE_MODEL", "gpt-image-1"),
            cfg.get("IMAGE_SIZE", "1536x1024"), files, note, max(1, min(5, attempts)))


def usable(key):
    return bool(key) and not key.startswith("sk-your-key")


def sniff(data):
    """What the endpoint actually sent back, by magic bytes."""
    if data[:4] == b"\x89PNG":
        return "PNG"
    if data[:2] == b"\xff\xd8":
        return "JPEG"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "WEBP"
    return None


def png_size(data):
    """Actual pixels from the IHDR — models quietly ignore an unsupported size."""
    if data[:4] == b"\x89PNG" and data[12:16] == b"IHDR":
        return struct.unpack(">II", data[16:24])
    return None


def named_format(path):
    return {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP"}.get(
        os.path.splitext(path)[1].lstrip(".").lower())


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


def report():
    """The config half of the doctor — no network. Returns the config tuple."""
    base, key, model, size, files, note, attempts = config()
    print("PPT-Zen image doctor\n  .env read : %s\n  endpoint  : %s/images/generations\n"
          "  model     : %s   (IMAGE_MODEL)\n  size      : %s   (IMAGE_SIZE; assembly cover-crops to 16:9)\n"
          "  attempts  : %d per page   (IMAGE_MAX_ATTEMPTS)\n  api key   : %s%s\n"
          % (" , ".join(files) if files else "none found — using environment variables only",
             base, model, size, attempts, key_line(key), ("   (%s)" % note) if note else ""))
    return base, key, model, size, files, note, attempts


def no_key():
    return fail("no usable key, so nothing can be generated yet.",
                "cp .env.example .env and put your own key in IMAGE_API_KEY — PPT-Zen ships\n"
                "         no key and no model, the pixels come from your endpoint.\n" + PROVIDERS +
                "\n  no key today? the judgment pack still ships: python3 scripts/judgment_pack.py --help")


def check_config():
    """Everything --check does except the probe: free, and it never touches the network."""
    base, key, model, size, files, note, attempts = report()
    if not usable(key):
        return no_key()
    if not base.startswith(("http://", "https://")):
        return fail("IMAGE_API_BASE_URL is not a URL: %s" % base,
                    "give the API root, scheme included — e.g. https://api.openai.com/v1\n" + PROVIDERS)
    for tail in ("/images/generations", "/chat/completions"):
        if base.endswith(tail):
            return fail("IMAGE_API_BASE_URL ends in %s — that's a route, not the root." % tail,
                        "drop the route: the script appends /images/generations itself.\n" + PROVIDERS)
    print("  ✓ config looks complete. Nothing was sent — run --check to probe (bills one image).")
    return 0


def check():
    base, key, model, size, files, note, attempts = report()
    if not usable(key):
        return no_key()
    print("  note: this check generates ONE billable test image at %s on your endpoint.\n"
          "        config-only, nothing billed: --check-config\n" % size)
    # Probe the configured size first — that's what the deck will use; a cheaper size passing
    # while the real one fails would green-light a run that dies on page 1.
    probes = [size] + (["1024x1024"] if size != "1024x1024" else [])
    for probe in probes:
        print("  probing the endpoint (1 test image, %s) ..." % probe)
        try:
            img = fetch_image(base, key, model, "test swatch, plain gray", probe, 90)
        except urllib.error.HTTPError as e:
            body = e.read()[:200].decode("utf-8", "replace").replace("\n", " ").strip()
            if e.code == 400 and probe == size and len(probes) > 1 and "size" in body.lower():
                print("  · your IMAGE_SIZE %s was rejected — testing 1024x1024 to see if the endpoint works at all" % size)
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
        if probe != size:
            return fail("the endpoint works, but your IMAGE_SIZE %s is not supported (1024x1024 is)." % size,
                        "set IMAGE_SIZE in .env to a size this endpoint serves — 1024x1024 just verified.")
        got, wh = sniff(img) or "an unrecognised format", png_size(img)
        print("  ✓ endpoint OK, 1 test image generated: %s%s, asked for %s."
              % (got, (" %dx%d" % wh) if wh else "", probe))
        if wh and "%dx%d" % wh != probe.lower().replace("×", "x"):
            print("    note: it returned %dx%d, not the %s you asked for — the deck will use what it sends."
                  % (wh[0], wh[1], probe))
        print("  You're ready to make a deck.")
        return 0


def generate(prompt, out):
    base, key, model, size, _, _, attempts = config()
    if not usable(key):
        sys.exit("gen_image: no usable IMAGE_API_KEY — run `python3 %s --check` for the fix." % sys.argv[0])
    for attempt in range(attempts):
        t0 = time.time()
        print("gen_image: requesting %s (attempt %d/%d) ..." % (out, attempt + 1, attempts),
              file=sys.stderr, flush=True)
        try:
            img = fetch_image(base, key, model, prompt, size, 240)
        except urllib.error.HTTPError as e:
            body = e.read()[:200].decode("utf-8", "replace").replace("\n", " ").strip()
            if e.code < 500:   # your config, not the weather — retrying can't help
                sys.exit("gen_image: HTTP %d — %s\n  run `python3 %s --check` for a diagnosis." % (e.code, body, sys.argv[0]))
            err = "HTTP %d %s" % (e.code, body)
        except NotJSON as e:
            sys.exit("gen_image: endpoint returned a non-JSON page (%s)\n  run `python3 %s --check`." % (e, sys.argv[0]))
        except (KeyError, IndexError, TypeError, ValueError) as e:
            sys.exit("gen_image: endpoint answered in the wrong shape (%s) — no usable data[0].b64_json / url.\n"
                     "  run `python3 %s --check` for a diagnosis." % (e, sys.argv[0]))
        except (urllib.error.URLError, OSError) as e:
            err = str(e)
        else:
            open(out, "wb").write(img)
            got = sniff(img)
            if got and got != named_format(out):
                print("note: endpoint returned %s; saved as %s unchanged (assembly handles it)." % (got, out),
                      file=sys.stderr)
            print("gen_image: wrote %s (%ds, %d bytes)" % (out, time.time() - t0, len(img)), file=sys.stderr)
            return
        if attempt == attempts - 1:
            sys.exit("gen_image: gave up after %d attempt(s) — %s" % (attempts, err))
        wait = (10, 30, 60, 60)[min(attempt, 3)]
        print("gen_image: %s — retrying in %ds" % (err, wait), file=sys.stderr, flush=True)
        time.sleep(wait)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--help"
    if arg in ("--help", "-h"):
        print(HELP)
        sys.exit(0)
    if arg == "--check":
        sys.exit(check())
    if arg == "--check-config":
        sys.exit(check_config())
    if len(sys.argv) < 3:
        sys.exit("usage: gen_image.py \"<prompt>\" <out.jpg>   |   --check   |   --check-config   |   --help")
    generate(sys.argv[1], sys.argv[2])
