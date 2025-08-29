# -*- coding: utf-8 -*-
"""为 3x3 魔方生成小方块纹理。"""

from PIL import Image, ImageDraw
import itertools
import pathlib

# 定义魔方使用的颜色，采用 RGB 格式。
colors = {
    "white": (255, 255, 255),   # 白色
    "red": (137, 18, 20),       # 红色
    "blue": (13, 72, 172),      # 蓝色
    "orange": (255, 85, 37),    # 橙色
    "green": (25, 155, 76),     # 绿色
    "yellow": (254, 213, 47),   # 黄色
}

# --- 图像参数定义 ---
res = 256  # 纹理分辨率
imsize = (res * 4, res * 3)  # 生成的图片尺寸
rad = int(0.2 * res)  # 圆角矩形的半径
width = int(0.08 * res)  # 填充宽度
# 绘制圆角矩形时使用的通用参数
kwargs = dict(radius=rad, width=width, outline=(0, 0, 0))

# 创建用于存放纹理图片的 "assets" 目录，如果目录已存在则不进行任何操作。
pathlib.Path("assets").mkdir(parents=True, exist_ok=True)

# --- 生成中心块纹理：1个颜色 ---
# 中心块只有一个颜色。
for color in colors:
    # 创建一个黑色的背景图片。
    img = Image.new("RGB", imsize, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 在图片中心绘制一个带颜色的圆角矩形。
    draw.rounded_rectangle(
        (res, res, 2 * res, 2 * res), fill=colors[color], **kwargs
    )
    # 保存图片，以颜色名称命名。
    img.save(f"assets/{color}.png")

# --- 生成棱块纹理：2个颜色 ---
# 棱块有两个颜色。
for color1, color2 in itertools.combinations(colors, 2):
    # 对颜色进行排序，以确保文件名的一致性（例如，blue_red 和 red_blue 会被统一为 blue_red）。
    color1, color2 = sorted([color1, color2])

    # 跳过在标准魔方上不可能出现的颜色组合（相对面）。
    if color1 == "white" and color2 == "yellow":
        continue
    if color1 == "red" and color2 == "orange":
        continue
    if color1 == "blue" and color2 == "green":
        continue

    # 创建一个黑色的背景图片。
    img = Image.new("RGB", imsize, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制代表第一个颜色的圆角矩形。
    draw.rounded_rectangle(
        (res, res, 2 * res, 2 * res), fill=colors[color1], **kwargs
    )
    # 绘制代表第二个颜色的圆角矩形。
    draw.rounded_rectangle(
        (2 * res, res, 3 * res, 2 * res), fill=colors[color2], **kwargs
    )
    # 保存图片，以两种颜色的组合名称命名。
    img.save(f"assets/{color1}_{color2}.png")

# --- 生成角块纹理：3个颜色 ---
# 角块有三个颜色。
for comb in itertools.combinations(colors, 3):
    # 跳过在标准魔方上不可能出现的颜色组合（包含相对面）。
    if "white" in comb and "yellow" in comb:
        continue
    if "red" in comb and "orange" in comb:
        continue
    if "blue" in comb and "green" in comb:
        continue

    # 对颜色进行排序，以确保文件名的一致性。
    color1, color2, color3 = sorted(comb)

    # 创建一个黑色的背景图片。
    img = Image.new("RGB", imsize, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    # 绘制代表第一个颜色的圆角矩形。
    draw.rounded_rectangle(
        (res, res, 2 * res, 2 * res), fill=colors[color1], **kwargs
    )
    # 绘制代表第二个颜色的圆角矩形。
    draw.rounded_rectangle(
        (2 * res, res, 3 * res, 2 * res), fill=colors[color2], **kwargs
    )
    # 绘制代表第三个颜色的圆角矩形。
    draw.rounded_rectangle(
        (3 * res, res, 4 * res, 2 * res), fill=colors[color3], **kwargs
    )
    # 保存图片，以三种颜色的组合名称命名。
    img.save(f"assets/{color1}_{color2}_{color3}.png")
