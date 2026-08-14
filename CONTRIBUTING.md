<p align="center"><b>English</b> · <a href="CONTRIBUTING.zh-CN.md">简体中文</a></p>

# Contributing to PPT-Zen

Thank you for adding to the library. The most valuable contribution is a **style pack**.

## Contribute a style

1. **Fork** this repo.
2. Copy `styles/_template/` to `styles/<your-slug>/`.
3. Fill in `STYLE.md` (name / medium / hand / four-axis config / **one reproducible prompt formula** / source) and drop at least one 16:9 sample in `samples/`.
4. Run `python3 build_gallery.py` locally to refresh `GALLERY.md`.
5. Open a **Pull Request**. CI validates your pack; a maintainer reviews and merges; the gallery updates automatically.

**Not a coder?** Open an Issue with the "New style" template — attach your samples and fill the fields; a maintainer will turn it into a PR.

## Checklist
- [ ] `styles/<slug>/STYLE.md` with all required fields (name, slug, medium, author, license, prompt_formula, samples)
- [ ] `slug` matches the folder name
- [ ] at least one 16:9 sample, referenced in `samples:`
- [ ] a **reproducible prompt formula** (SURFACE × SKELETON × DEVICE + the hard-rule tail)
- [ ] `license: CC-BY-4.0`; artwork is yours or properly attributed; **no client content, no copyrighted text**
- [ ] DCO sign-off on your commits (`git commit -s`)

## Sign-off (DCO)
We use the [Developer Certificate of Origin](https://developercertificate.org/). Add `-s` to your commits so each carries a `Signed-off-by:` line — this certifies you have the right to contribute what you submit.

## Two-layer license
- **Judgment layer** (SKILL, docs, code): Apache-2.0.
- **Style packs & gallery content** (`styles/`, images): CC-BY-4.0.
