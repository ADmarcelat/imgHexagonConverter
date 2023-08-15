from PIL import Image

FILENAME = 'wallpaper'
BASE_FILENAME = './img/'+ FILENAME +'.jpeg'  # 'pxfuel.jpg'
SIZE = 80  # 43.3
SCAN_SIZE = 80  # 5
FLOAT_PRECISION = 10

hex_h = SIZE * (3 ** 0.5)
hex_w = 2 * SIZE

spacing_horiz = 3 * hex_w / 4
spacing_vert = hex_h


im = Image.open(BASE_FILENAME)

svg_contents = f'<svg width="{im.size[0] - int(hex_w) // 2}" height="{im.size[1] - int(hex_h) // 2}" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg">\n'

x = 0
row_parity = 0
while x < im.size[0]:

    y = 0 + row_parity * (spacing_vert / 2)
    row_parity = 1 - row_parity

    while y < im.size[1]:
        hexagon_colors = []
        for dx in range(SCAN_SIZE):
            for dy in range(SCAN_SIZE):
                try:
                    hexagon_colors.append(im.getpixel((int(x+dx), int(y+dy))))
                    im.putpixel((int(x+dx), int(y+dy)), (255, 255, 255))
                except IndexError:
                    pass 
        avg_color = []
        for i in range(3):
            avg_color.append(
                sum(x[i] for x in hexagon_colors) // len(hexagon_colors))
        im.putpixel((int(x+2), int(y+2)), tuple(avg_color))

        svg_contents += '  <polygon points="'

        svg_contents += f'{round(x - hex_w/4, FLOAT_PRECISION)},{round(y - hex_h/2, FLOAT_PRECISION)} '
        svg_contents += f'{round(x + hex_w/4, FLOAT_PRECISION)},{round(y - hex_h/2, FLOAT_PRECISION)} '
        svg_contents += f'{round(x + hex_w/2, FLOAT_PRECISION)},{round(y, FLOAT_PRECISION)} '
        svg_contents += f'{round(x + hex_w/4, FLOAT_PRECISION)},{round(y + hex_h/2, FLOAT_PRECISION)} '
        svg_contents += f'{round(x - hex_w/4, FLOAT_PRECISION)},{round(y + hex_h/2, FLOAT_PRECISION)} '
        svg_contents += f'{round(x - hex_w/2, FLOAT_PRECISION)},{round(y, FLOAT_PRECISION)}'

        svg_contents += '" fill="#'

        for color in avg_color:
            svg_contents += f'{color:02x}'

        svg_contents += '" />\n'
        y += spacing_vert
    x += spacing_horiz

svg_contents += '</svg>'

with open('./exports/'+ FILENAME+ '.svg', 'w') as fo:
    fo.write(svg_contents)

im.show()
