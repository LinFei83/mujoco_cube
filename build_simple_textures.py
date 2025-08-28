"""Generate simple cubelet textures for STL mesh."""

from PIL import Image, ImageDraw
import itertools
import pathlib

colors = {
    "white": (255, 255, 255),
    "red": (137, 18, 20),
    "blue": (13, 72, 172),
    "orange": (255, 85, 37),
    "green": (25, 155, 76),
    "yellow": (254, 213, 47),
}

res = 256  # Texture resolution.
imsize = (res, res)  # Simple square texture
rad = int(0.1 * res)  # Smaller rounded rectangle radius.
width = int(0.05 * res)  # Thinner fill width.
kwargs = dict(radius=rad, width=width, outline=(0, 0, 0))

pathlib.Path("assets").mkdir(parents=True, exist_ok=True)

# Center cubelets: 1 color - fill entire texture
for color in colors:
    img = Image.new("RGB", imsize, color=colors[color])
    draw = ImageDraw.Draw(img)
    # Add a border to make it look like a cube face
    draw.rounded_rectangle((10, 10, res-10, res-10), fill=colors[color], **kwargs)
    img.save(f"assets/{color}.png")

# Edge cubelets: 2 colors - split texture
for color1, color2 in itertools.combinations(colors, 2):
    color1, color2 = sorted([color1, color2])

    # Skip impossible combinations.
    if color1 == "white" and color2 == "yellow":
        continue
    if color1 == "red" and color2 == "orange":
        continue
    if color1 == "blue" and color2 == "green":
        continue

    img = Image.new("RGB", imsize, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Split the texture in half
    draw.rounded_rectangle((10, 10, res//2-5, res-10), fill=colors[color1], **kwargs)
    draw.rounded_rectangle((res//2+5, 10, res-10, res-10), fill=colors[color2], **kwargs)
    img.save(f"assets/{color1}_{color2}.png")

# Corner cubelets: 3 colors - split texture in three
for comb in itertools.combinations(colors, 3):
    if "white" in comb and "yellow" in comb:
        continue
    if "red" in comb and "orange" in comb:
        continue
    if "blue" in comb and "green" in comb:
        continue
    color1, color2, color3 = sorted(comb)
    
    img = Image.new("RGB", imsize, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Split the texture in thirds
    third = res // 3
    draw.rounded_rectangle((10, 10, third-5, res-10), fill=colors[color1], **kwargs)
    draw.rounded_rectangle((third+5, 10, 2*third-5, res-10), fill=colors[color2], **kwargs)
    draw.rounded_rectangle((2*third+5, 10, res-10, res-10), fill=colors[color3], **kwargs)
    img.save(f"assets/{color1}_{color2}_{color3}.png")

print("Simple textures generated successfully!")
