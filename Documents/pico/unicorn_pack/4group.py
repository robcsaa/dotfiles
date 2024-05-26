from picounicorn import PicoUnicorn
from time import sleep
import random

# Initialize Pico Unicorn display
picounicorn = PicoUnicorn()

# Define the number of pixels to be simultaneously lit in each group
num_pixels_lit_per_group = 4

# List to store all the active pixels with their colors
active_pixels = []

# Infinite loop to create a never-ending stream of pixels
x = 0
y = 0
color = (random.randint(0, 255), random.randint(0, 0), random.randint(0, 255))

while True:
    # Add the current pixel to the active_pixels list
    active_pixels.append((x, y, color[0], color[1], color[2]))
    
    # Move to the next pixel
    x += 1
    if x >= 16:
        x = 0
        y += 1
        if y >= 7:
            y = 0
        
    # Generate a new random color for every 4th pixel
    if len(active_pixels) % num_pixels_lit_per_group == 0:
        color = (random.randint(0, 255), random.randint(0, 0), random.randint(0, 255))

    # Display all active pixels
    for pixel in active_pixels:
        picounicorn.set_pixel(pixel[0], pixel[1], pixel[2], pixel[3], pixel[4])

    # Introduce a delay of 0.5 seconds
    sleep(0.1)
