from collections import Counter
from sense_hat import SenseHat
from PIL import Image

# Initialize Sense HAT
sense = SenseHat()
sense.clear()

# Load the image
im = Image.open('flag.jpg', 'r')
width, height = im.size
pixel_values = list(im.getdata())

# Convert pixel data into a 2D list
pixels = [[None] * width for _ in range(height)]
for i, pixel in enumerate(pixel_values):
    x = i % width
    y = i // width
    pixels[y][x] = pixel

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

# Define boundary regions
top_bounds = [(i * top_step, (i + 1) * top_step) for i in range(topbot_items)]
bottom_bounds = [(i * top_step, (i + 1) * top_step) for i in range(topbot_items)]
left_bounds = [(i * left_step, (i + 1) * left_step) for i in range(leftright_items)]
right_bounds = [(i * left_step, (i + 1) * left_step) for i in range(leftright_items)]

# Reverse left and right boundaries
left_bounds_reversed = list(reversed(left_bounds))
right_bounds_reversed = list(reversed(right_bounds))

# Initialize grid to store colors
grid = [[None for _ in range(8)] for _ in range(8)]

# Store most common colors in grid
for i, bound in enumerate(top_bounds):
    boundary_pixels = [pixels[y][x] for y in range(topy1, topy2) for x in range(bound[0], bound[1])]
    common_color = Counter(boundary_pixels).most_common(1)[0][0]
    grid[0][i] = common_color

for i, bound in enumerate(left_bounds_reversed):
    boundary_pixels = [pixels[y][x] for y in range(bound[0], bound[1]) for x in range(leftx1, leftx2)]
    common_color = Counter(boundary_pixels).most_common(1)[0][0]
    grid[i + 1][0] = common_color

for i, bound in enumerate(right_bounds_reversed):
    boundary_pixels = [pixels[y][x] for y in range(bound[0], bound[1]) for x in range(rightx1, rightx2)]
    common_color = Counter(boundary_pixels).most_common(1)[0][0]
    grid[i + 1][7] = common_color

for i, bound in enumerate(bottom_bounds):
    boundary_pixels = [pixels[y][x] for y in range(bottomy1, bottomy2) for x in range(bound[0], bound[1])]
    common_color = Counter(boundary_pixels).most_common(1)[0][0]
    grid[7][i] = common_color

# Display grid on Sense HAT
for y in range(8):
    for x in range(8):
        color = grid[y][x]
        if color is not None:
            r, g, b = color  # Unpack the color tuple
            sense.set_pixel(x, y, r, g, b)
        else:
            sense.set_pixel(x, y, 0, 0, 0)  # If no color detected, turn off the LED
