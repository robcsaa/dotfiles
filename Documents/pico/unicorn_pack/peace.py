from picounicorn import PicoUnicorn
import time

picounicorn = PicoUnicorn()

# Coordinates of pixels to light up
pixels_to_light = [
    (3, 0), (4, 0), (5, 0), (6, 0),
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
    (2, 6), (1, 6),
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 6),
    (1, 3), (2, 3), (4, 3), (5, 3), (6, 3), (6, 4), (6, 5), (6, 6),
    (12, 0), (13, 0), (14, 0), (15, 0),
    (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6),
    (11, 6), (10, 6),
    (9, 0), (9, 1), (9, 2), (9, 3), (9, 6),
    (10, 3), (11, 3), (13, 3), (14, 3), (15, 3), (15, 4), (15, 5), (15, 6)
]

# Define the colors to transition
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Define the number of steps for color transition
num_steps = 50

# Interpolate between the colors
def interpolate_color(start_color, end_color, step, num_steps):
    r = start_color[0] + (end_color[0] - start_color[0]) * step / num_steps
    g = start_color[1] + (end_color[1] - start_color[1]) * step / num_steps
    b = start_color[2] + (end_color[2] - start_color[2]) * step / num_steps
    return int(r), int(g), int(b)

while True:
    for i in range(len(colors)):
        start_color = colors[i]
        end_color = colors[(i + 1) % len(colors)]  # Wrap around for last color
        for step in range(num_steps):
            current_color = interpolate_color(start_color, end_color, step, num_steps)
            for x, y in pixels_to_light:
                picounicorn.set_pixel(x, y, *current_color)
            time.sleep(0.01)  # Adjust speed of transition by changing sleep duration
