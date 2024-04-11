from collections import Counter
from sense_hat import SenseHat
from PIL import Image

# Initialize Sense HAT
sense = SenseHat()
sense.clear()

# Open the image
im = Image.open('flag.jpg', 'r')
width, height = im.size

# Define boundary regions
topy1 = int(height * 0.875)
topy2 = height

bottomy1 = 0
bottomy2 = int(height * 0.125)

leftx1 = 0
leftx2 = int(width * 0.125)

rightx1 = int(width * 0.875)
rightx2 = width

# Define boundary subdivisions
topbot_items = 8
leftright_items = 6

# Calculate step sizes
top_step = width // topbot_items
left_step = height // leftright_items

# Initialize grid to store colors
grid = [[None for _ in range(8)] for _ in range(8)]

# Process boundary regions
for i in range(topbot_items):
    top_bound = (i * top_step, (i + 1) * top_step)
    top_boundary_pixels = [im.getpixel((x, y)) for y in range(topy1, topy2) for x in range(top_bound[0], top_bound[1])]
    common_color = Counter(top_boundary_pixels).most_common(1)[0][0]
    grid[0][i] = common_color

for i in range(leftright_items):
    left_bound = (i * left_step, (i + 1) * left_step)
    left_boundary_pixels = [im.getpixel((x, y)) for y in range(left_bound[0], left_bound[1]) for x in range(leftx1, leftx2)]
    common_color = Counter(left_boundary_pixels).most_common(1)[0][0]
    grid[i + 1][0] = common_color

for i in range(leftright_items):
    right_bound = (i * left_step, (i + 1) * left_step)
    right_boundary_pixels = [im.getpixel((x, y)) for y in range(right_bound[0], right_bound[1]) for x in range(rightx1, rightx2)]
    common_color = Counter(right_boundary_pixels).most_common(1)[0][0]
    grid[i + 1][7] = common_color

for i in range(topbot_items):
    bottom_bound = (i * top_step, (i + 1) * top_step)
    bottom_boundary_pixels = [im.getpixel((x, y)) for y in range(bottomy1, bottomy2) for x in range(bottom_bound[0], bottom_bound[1])]
    common_color = Counter(bottom_boundary_pixels).most_common(1)[0][0]
    grid[7][i] = common_color

# Display grid on Sense HAT
for y in range(8):
    for x in range(8):
        color = grid[y][x]
        if color is not None:
            sense.set_pixel(x, y, color[0], color[1], color[2])  # Pass RGB values as arguments
        else:
            sense.set_pixel(x, y, 0, 0, 0)  # If no color detected, turn off the LED
