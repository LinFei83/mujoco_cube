"""Generate proper cube face textures for STL mesh."""

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
imsize = (res, res)  # Square texture
border = 10  # Border size
inner_size = res - 2 * border

pathlib.Path("assets").mkdir(parents=True, exist_ok=True)

# Center cubelets: 1 color - solid color for entire cube
for color in colors:
    img = Image.new("RGB", imsize, color=colors[color])
    img.save(f"assets/{color}.png")

# Edge cubelets: 2 colors - each face should show appropriate color
# For edge pieces, we need to create textures that work with cube UV mapping
for color1, color2 in itertools.combinations(colors, 2):
    color1, color2 = sorted([color1, color2])

    # Skip impossible combinations.
    if color1 == "white" and color2 == "yellow":
        continue
    if color1 == "red" and color2 == "orange":
        continue
    if color1 == "blue" and color2 == "green":
        continue

    # Create a texture where different UV regions map to different colors
    # This assumes standard cube UV mapping where different faces map to different texture regions
    img = Image.new("RGB", imsize, color=colors[color1])
    draw = ImageDraw.Draw(img)
    
    # Fill different regions with different colors for cube faces
    # Top half with color1, bottom half with color2
    draw.rectangle((0, 0, res, res//2), fill=colors[color1])
    draw.rectangle((0, res//2, res, res), fill=colors[color2])
    
    img.save(f"assets/{color1}_{color2}.png")

# Corner cubelets: 3 colors - divide into three regions
for comb in itertools.combinations(colors, 3):
    if "white" in comb and "yellow" in comb:
        continue
    if "red" in comb and "orange" in comb:
        continue
    if "blue" in comb and "green" in comb:
        continue
    color1, color2, color3 = sorted(comb)
    
    img = Image.new("RGB", imsize, color=colors[color1])
    draw = ImageDraw.Draw(img)
    
    # Divide texture into three regions
    third = res // 3
    draw.rectangle((0, 0, res, third), fill=colors[color1])
    draw.rectangle((0, third, res, 2*third), fill=colors[color2])
    draw.rectangle((0, 2*third, res, res), fill=colors[color3])
    
    img.save(f"assets/{color1}_{color2}_{color3}.png")

print("Cube-optimized textures generated successfully!")
