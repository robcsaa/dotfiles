from picounicorn import PicoUnicorn
from time import sleep

# Initialize Pico Unicorn display
picounicorn = PicoUnicorn()

# Define the number of pixels to be simultaneously lit in each row
num_pixels_lit_per_row = 4

# Loop through y-coordinate from 0 to 6
for y in range(7):
    # List to store the coordinates of the active pixels in this row
    active_pixels = []

    # Loop through x-coordinate from 0 to 15
    for x in range(16):
        # Clear the previous active pixels in this row
        for pixel in active_pixels:
            picounicorn.set_pixel(pixel[0], pixel[1], 0, 0, 0)  # Turn off the previous pixel

        # Add the new pixel to the list of active pixels
        active_pixels.append((x, y))

        # Limit the number of active pixels to num_pixels_lit_per_row
        if len(active_pixels) > num_pixels_lit_per_row:
            active_pixels.pop(0)

        # Set pixels at coordinates in active_pixels list to red
        for pixel in active_pixels:
            picounicorn.set_pixel(pixel[0], pixel[1], 255, 0, 0)  # Red color (255, 0, 0)

        # Introduce a delay of 0.5 seconds
        sleep(0.1)

    # Clear all pixels in this row at the end of the loop
    for pixel in active_pixels:
        picounicorn.set_pixel(pixel[0], pixel[1], 0, 0, 0)  # Turn off the last pixels