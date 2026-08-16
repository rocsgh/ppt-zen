<p align="center"><a href="CONTRIBUTING.md">English</a> · <b>简体中文</b></p>

# 贡献指南

感谢共建。最有价值的贡献是一个**风格包**。

## 贡献一个风格

1. **Fork** 本仓库。
2. 复制 `styles/_template/` 到 `styles/<你的slug>/`。
3. 填好 `STYLE.md`（名字 / 介质 / 手笔 / 四轴 / **一条可复现的 prompt 配方** / 出处），在 `samples/` 放至少一张 16:9 样张。
4. 本地跑 `python3 build_gallery.py` 刷新 `GALLERY.md`。
5. 提 **Pull Request**。CI 自动校验，维护者审核合并，风格库自动更新。

**不懂 git？** 用"New style"Issue 模板：拖样张 + 填字段，维护者帮你转成 PR。

## 校验清单
- [ ] `styles/<slug>/STYLE.md` 必填字段齐（name、slug、medium、author、license、prompt_formula、samples）
- [ ] `slug` 与文件夹名一致
- [ ] 至少一张 16:9 样张，写进 `samples:`
- [ ] 一条**可复现的 prompt 配方**（SURFACE × SKELETON × DEVICE + 硬规则收尾）
- [ ] `license: CC-BY-4.0`；作品是你自己的或已署名；**不含客户内容、不含版权文本**
- [ ] 提交带 DCO 签名（`git commit -s`）

## 签名（DCO）
我们用 [Developer Certificate of Origin](https://developercertificate.org/)：提交加 `-s`，每条带一行 `Signed-off-by:`，即证明你有权贡献所提交的内容。

## 两层许可
- **判断层**（SKILL / 文档 / 代码）：Apache-2.0。
- **风格包与风格库内容**（`styles/`、图片）：CC-BY-4.0。
