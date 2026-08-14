---
# --- A PPT-Zen style pack. Copy this folder to styles/<your-slug>/ and fill it in. ---
# --- 一个 PPT-Zen 风格包。把本文件夹复制到 styles/<你的slug>/ 并填写。 ---
name: Example Style              # 风格显示名
slug: example-style              # 文件夹名(小写-连字符)，须与目录一致
medium: 介质名                    # 介质(what it's made of): 电影 / 航海图 / 达芬奇铜版 / 青花瓷 …
hand: ""                         # 手笔(可选, master hand): e.g. Christopher Nolan / Denis Villeneuve
world: ""                        # 世界(可选, the setting the audience enters)
tags: [dark, cinematic]          # 标签，用于画廊筛选
author: your-handle              # 贡献者
license: CC-BY-4.0               # 内容许可(固定 CC-BY-4.0)
axes:                            # 四轴里"这个风格"固定的两轴(详略/器物逐页由判断层跑)
  material: >                    # 材质配方 SURFACE(笔触/介质/调色/质感)
    <describe the surface: medium, palette, texture, lighting DNA>
  skeleton: auto                 # 骨架: auto=按页面职能自动派 / 或指定一个大师构图
  device_examples: >            # 器物词汇表(这个世界里"论点画成什么")举例
    <e.g. a monolith for scale, a clockwork machine for complexity>
prompt_formula: |                # 一条可复现的标准 prompt 配方(三轴相乘 + 全图硬规则收尾)
  SURFACE:  <material recipe>
  SKELETON: <geometry, or "auto by page role">
  DEVICE:   <the per-page thing; leave the slot, filled per page>
  END:      Full-bleed 16:9, render DEVICE in SURFACE material, SKELETON composition.
  CRITICAL: exact Chinese char count for the title; NEVER invent extra Chinese;
            decorative marks = geometric/number/dimension only; no UI, no data cards, no captions.
source: >                        # 出处/灵感(受什么启发)。绝不夹带受版权文本；只写自己的话
  <inspiration / reference, in your own words>
samples:                         # 样张(相对本文件夹)，至少 1 张 16:9
  - samples/01.jpg
---

# Example Style

**One line: what it is, and what judgment it demonstrates.**
**一句话：它是什么、它演示了哪条判断。**

A few sentences on the vibe, when to use it, and the "world setting" it gives the audience.
几句话说清它的气质、适合什么场合、给观众什么世界设定。

<!-- Include your sample slide(s) below so they render on GitHub. 把样张放下面，GitHub 上能直接看。 -->
![sample](samples/01.jpg)
