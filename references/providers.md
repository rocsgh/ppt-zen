# Provider templates — `.env` blocks that are known to work

PPT-Zen ships no key and no model. It needs **one endpoint that implements the OpenAI
images API** — `POST {BASE}/images/generations` taking `{model, prompt, size, n}` and
returning `data[0].b64_json` or `data[0].url`.

A gateway that only proxies `/chat/completions` does **not** qualify, however
"OpenAI-compatible" it calls itself. Settle it in ten seconds:

```bash
cp .env.example .env          # then edit .env
python3 scripts/gen_image.py --check
```

`--check` prints which `.env` it read, masks your key, generates one test image, and
turns any failure into a plain verdict with the fix.

Fill in your own key. Never commit `.env` — it is gitignored.

---

## OpenAI (official)

The reference implementation; the gallery samples were made with this class of model.

```
IMAGE_API_BASE_URL=https://api.openai.com/v1
IMAGE_API_KEY=sk-REPLACE_ME
IMAGE_MODEL=gpt-image-1
IMAGE_SIZE=1536x1024
```

`gpt-image-1` renders text well, which is what makes full-image slides legible.
Plain diffusion models garble titles — that is a model choice, not a bug you can prompt away.

## Any OpenAI-compatible relay / gateway

Same shape, different host. Most relays keep the `/v1` suffix and the `sk-` key format,
and pass the model id straight through to whatever they front.

```
IMAGE_API_BASE_URL=https://your-relay.example.com/v1
IMAGE_API_KEY=REPLACE_ME
IMAGE_MODEL=gpt-image-1
IMAGE_SIZE=1536x1024
```

Two things to verify with your provider: that the **images** route is enabled on your key
(chat and images are often billed and enabled separately), and which model ids it exposes —
`IMAGE_MODEL` must be one of theirs, not the OpenAI name it maps to.

## 火山方舟 / Doubao Seedream (China-accessible)

Volcengine Ark serves the Seedream image models on the OpenAI images route, so it works
without any code change — it is only a different `BASE_URL`, key and model id.

```
IMAGE_API_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
IMAGE_API_KEY=REPLACE_ME            # Ark API key from the console
IMAGE_MODEL=REPLACE_ME              # the Seedream model id / endpoint id shown in the console
IMAGE_SIZE=1024x1024
```

`IMAGE_MODEL` is the part people get wrong: Ark identifies models by a versioned id (or an
inference endpoint id you created), not by a friendly name — copy it from the console.
Sizes are a fixed list per model; if `--check` reports the size was rejected, take a
supported landscape size from the model's docs. Chinese titles render well here, which is
the reason to use it for a Chinese deck.

---

## Choosing `IMAGE_SIZE`

Generate **landscape**; assembly cover-crops to 16:9. `1536x1024` (3:2) is the safe default,
`1024x1024` the safe fallback for endpoints with a short size list. Keep titles and key
content clear of the top/bottom ~8% either way — that band is what the crop eats.

## Still stuck?

`python3 scripts/gen_image.py --check` names the failure. And you are not blocked meanwhile:
ask for the deck anyway and the skill produces the **judgment pack** — `slides/PLAN.md` with a
ready-to-paste prompt per page, placeholder pages, and an assembled `draft.pptx`. Paste any
prompt card into Midjourney / 即梦 / Doubao by hand, drop the image into `slides/`, reassemble.
