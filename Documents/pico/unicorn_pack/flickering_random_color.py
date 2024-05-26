import random
from time import sleep
from picounicorn import PicoUnicorn

# Initialize Pico Unicorn display
picounicorn = PicoUnicorn()

pixel_count = 0  # Counter to keep track of pixels turned on

while True:
    # Generate random coordinates
    x = random.randint(0, 15)
    y = random.randint(0, 6)
    
    # Generate random RGB color values
    r = random.randint(0, 255)
    g = random.randint(0, 0)
    b = random.randint(0, 255)
    
    # Print the generated values for debugging purposes
    print(x, y, r, g, b)
    
    # Set the pixel on the Pico Unicorn display
    picounicorn.set_pixel(x, y, r, g, b)
    
    pixel_count += 1
    
    # Turn off a pixel every two pixels turned on
    if pixel_count == 2:
        # Generate random coordinates to turn off a pixel
        x_off = random.randint(0, 15)
        y_off = random.randint(0, 6)
        
        # Turn off the pixel
        picounicorn.set_pixel(x_off, y_off, 0, 0, 0)
        
        pixel_count = 0  # Reset the pixel counter
    
    # Wait for 0.01 second before updating again
    sleep(0.01)
