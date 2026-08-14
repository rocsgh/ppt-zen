# Contributing to PPT-Zen · 贡献指南

Thank you for adding to the library. The most valuable contribution is a **style pack**.
感谢共建。最有价值的贡献是一个**风格包**。

## Contribute a style · 贡献一个风格

1. **Fork** this repo. Fork 本仓库。
2. Copy `styles/_template/` to `styles/<your-slug>/`. 复制 `styles/_template/` 到 `styles/<你的slug>/`。
3. Fill in `STYLE.md` (name / medium / hand / four-axis config / **one reproducible prompt formula** / source) and drop at least one 16:9 sample in `samples/`.
   填好 `STYLE.md`（名字/介质/手笔/四轴/**一条可复现的 prompt 配方**/出处），在 `samples/` 放至少一张 16:9 样张。
4. Run `python3 build_gallery.py` locally to refresh `GALLERY.md`. 本地跑一次刷新画廊。
5. Open a **Pull Request**. CI validates your pack; a maintainer reviews and merges; the gallery updates automatically.
   提 **Pull Request**。CI 自动校验，维护者审核合并，画廊自动更新。

**Not a coder?** Open an Issue with the "New style" template — attach your samples and fill the fields; a maintainer will turn it into a PR.
**不懂 git？** 用"New style"Issue 模板：拖样张 + 填字段，维护者帮你转成 PR。

## Checklist · 校验清单
- [ ] `styles/<slug>/STYLE.md` with all required fields (name, slug, medium, author, license, prompt_formula, samples)
- [ ] `slug` matches the folder name
- [ ] at least one 16:9 sample, referenced in `samples:`
- [ ] a **reproducible prompt formula** (SURFACE × SKELETON × DEVICE + the hard-rule tail)
- [ ] `license: CC-BY-4.0`; artwork is yours or properly attributed; **no client content, no copyrighted text**
- [ ] DCO sign-off on your commits (`git commit -s`)

## Sign-off (DCO)
We use the [Developer Certificate of Origin](https://developercertificate.org/). Add `-s` to your commits so each carries a `Signed-off-by:` line — this certifies you have the right to contribute what you submit. 我们用 DCO：提交加 `-s`，一行 `Signed-off-by:` 即可。

## Two-layer license · 两层许可
- **Judgment layer** (SKILL, docs, code): Apache-2.0. 判断层：Apache-2.0。
- **Style packs & gallery content** (`styles/`, images): CC-BY-4.0. 风格包与画廊内容：CC-BY-4.0。
