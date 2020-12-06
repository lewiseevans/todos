import unicornhathd
import time

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

# Get the width and height of the display
width, height = unicornhathd.get_shape()

# Select font and size
FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 8)


def display(todo):
    print(todo)

    # Set the rotation of the display
    unicornhathd.rotation(90)
    unicornhathd.brightness(0.6)

    # We want to draw our text 1 pixel in, and 2 pixels down from the top left corner
    text_x = 1
    text_y = 2

    # Grab our font file and size as defined at the top of the script
    font_file, font_size = FONT

    # Load the font using PIL's ImageFont
    font = ImageFont.truetype(font_file, font_size)

    # Ask the loaded font how big our text will be
    text_width, text_height = font.getsize(todo)

    # Make sure we accommodate enough width to account for our text_x left offset
    text_width += width + text_x

    # Now let's create a blank canvas wide enough to accomodate our text
    image = Image.new('RGB', (text_width, max(height, text_height)), (0, 0, 0))

    # To draw on our image, we must use PIL's ImageDraw
    draw = ImageDraw.Draw(image)

    # And now we can draw text at our desited (text_x, text_y) offset, using our loaded font
    draw.text((text_x, text_y), todo, fill=(0, 0, 255), font=font)

    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x + scroll, y))
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

        unicornhathd.show()

        time.sleep(0.01)


def readTodos():
    todoFile = open('todos.txt')
    todoLines = todoFile.readlines()
    return todoLines


todos = readTodos()

try:

    for todo in todos:
        display(todo.strip())

except KeyboardInterrupt:
    unicornhathd.off()

finally:
    unicornhathd.off()
