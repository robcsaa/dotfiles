from urandom import randint
from time import sleep
from picounicorn import PicoUnicorn

# Initialize Pico Unicorn display
picounicorn = PicoUnicorn()

while True:
    # Generate random coordinates
    x = randint(0, 15)
    y = randint(0, 6)
    
    # Generate random RGB color values
    r = randint(0, 255)
    g = randint(0, 0)
    b = randint(0, 255)
    
    # Print the generated values for debugging purposes
    print(x, y, r, g, b)
    
    # Set the pixel on the Pico Unicorn display
    picounicorn.set_pixel(x, y, r, g, b)
    
    # Wait for 1 second before updating again
    sleep(0.01)
