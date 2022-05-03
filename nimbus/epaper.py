"""Write the bus information to the e-paper screen"""

from PIL import Image,ImageDraw,ImageFont
from PIL.Image import Transpose
from TP_lib import epd2in13_V2

FONT_REGULAR_12 = ImageFont.truetype('fonts/Roboto-Regular.ttf', 12)
FONT_BOLD_20 = ImageFont.truetype('fonts/Roboto-Bold.ttf', 20)
FONT_CONDENSED_14 = ImageFont.truetype('fonts/RobotoCondensed-Regular.ttf', 14)
FONT_BOLD_24 = ImageFont.truetype('fonts/Roboto-Bold.ttf', 24)

COLOUR_BLACK = 0
COLOUR_WHITE = 255

DISPLAY = epd2in13_V2.EPD_2IN13_V2()

# Width and height reverse to rotate screen
WIDTH = DISPLAY.height
HEIGHT = DISPLAY.width

COUNT_FILE = '/tmp/epaper-refresh-count'

def _refresh_count():
    """Keep a count of the number of times we've refreshed"""

    try:
        with open(COUNT_FILE, encoding='utf-8') as count_file:
            count = int(count_file.read())
    except FileNotFoundError:
        count = 0

    with open(COUNT_FILE, 'w', encoding='utf-8') as count_file:
        count_file.write(str(count + 1))

    return count


def display(stop_name, buses, last_updated):
    """Display bus information to the screen"""

    image = Image.new('1', (WIDTH, HEIGHT), COLOUR_WHITE)

    draw = ImageDraw.Draw(image)
    draw.text((2, 0), stop_name, font = FONT_BOLD_24, fill = COLOUR_BLACK)
    (_, current_y) = FONT_BOLD_24.getsize(stop_name)
    current_y += 2

    draw.line((0, current_y, WIDTH, current_y), fill = COLOUR_BLACK)

    current_y += 2
    destination_x = 0

    for (bus, _, _) in buses:
        (text_width, text_height) = FONT_BOLD_20.getsize(bus)
        destination_x = max(destination_x, text_width)

    destination_x += 4
    destination_offset = FONT_BOLD_20.getsize("A")[1] - FONT_CONDENSED_14.getsize("A")[1]

    for (bus, destination, time) in buses:
        draw.text((2, current_y), bus,
            font = FONT_BOLD_20, fill = COLOUR_BLACK)
        draw.text((destination_x, current_y + destination_offset), destination,
            font = FONT_CONDENSED_14, fill = COLOUR_BLACK)
        (text_width, text_height) = FONT_BOLD_20.getsize(time)
        draw.text((WIDTH - text_width, current_y), time,
            font = FONT_BOLD_20, fill = COLOUR_BLACK)
        current_y += text_height + 3

    (text_width, text_height) = FONT_REGULAR_12.getsize(last_updated)
    draw.text((WIDTH - text_width, HEIGHT - text_height), last_updated,
        font = FONT_REGULAR_12, fill = COLOUR_BLACK)

    image = image.transpose(Transpose.ROTATE_180)
    display_image = DISPLAY.getbuffer(image)

    if _refresh_count() % 10 == 0:
        DISPLAY.init(DISPLAY.FULL_UPDATE)
        DISPLAY.displayPartBaseImage(display_image)
    else:
        DISPLAY.init(DISPLAY.PART_UPDATE)
        DISPLAY.displayPartial(display_image)
