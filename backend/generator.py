from typing import List

import svgutils
from qrcodegen import QrCode


def create_qr_code(link, options=None, save_to_svg_file=False) -> str:
    """

    Creates a single QR Code, then prints it to the console.

    """

    # Make and print the QR Code symbol
    qr = QrCode.encode_text(link, QrCode.Ecc.HIGH)

    # Check if color_scheme is valid (besj, black or white) or not set
    if options is not None and 'color_scheme' in options and options['color_scheme'] not in ['besj', 'black']:
        raise ValueError("Invalid color scheme")

    color_scheme = 'besj' if options is None or 'color_scheme' not in options else options['color_scheme']

    # Save QR code as SVG
    svg_text = to_svg_str(qr, border=2, color_scheme=color_scheme)

    if save_to_svg_file:
        with open('qr_code.svg', 'w') as f:
            f.write(svg_text)

    return svg_text


def to_svg_str(qr: QrCode, border: int = 0, logo_size: int = 8, color_scheme="besj") -> str:
    """

    Returns a string of SVG code for an image depicting the given QR Code, with the given number
    of border modules. The string always uses Unix newlines (\n), regardless of the platform.

    """

    if border < 0:
        raise ValueError("Border must be non-negative")

    if logo_size < 0:
        raise ValueError("Logo size must be non-negative")

    # Load logo as SVG
    if color_scheme == "besj":
        besj_logo = svgutils.compose.SVG('besj_logo.svg')
        besj_logo.scale(0.0037 * logo_size, 0.0037 * logo_size)
    if color_scheme == "black":
        besj_logo = svgutils.compose.SVG('besj_logo_bw.svg')
        besj_logo.scale(0.015 * logo_size, 0.015 * logo_size)
    
    besj_logo.moveto(border + qr.get_size() / 2.0 - logo_size / 2.0, border + qr.get_size() / 2.0 - logo_size / 2.0)

    # Compute the width and height of the SVG image
    qr_parts: List[str] = []
    qr_corners: List[str] = []

    for y in range(qr.get_size()):
        for x in range(qr.get_size()):
            if qr.get_module(x, y):

                # Ignore a square in the very middle of the image
                if qr.get_size() // 2 - logo_size // 2 <= x <= qr.get_size() // 2 + logo_size // 2 \
                        and qr.get_size() // 2 - logo_size // 2 <= y <= qr.get_size() // 2 + logo_size // 2:
                    continue

                # check if it's a corner
                if x == 0 and y <= 6 or y == 0 and x <= 6 or y == 6 and x <= 6 or x == 6 and y <= 6 \
                        or x >= qr.get_size() - 7 and (y == 0 or y == 6) or (
                        x == qr.get_size() - 1 or x == qr.get_size() - 7) and y <= 6 \
                        or y >= qr.get_size() - 7 and (x == 0 or x == 6) or (
                        y == qr.get_size() - 1 or y == qr.get_size() - 7) and x <= 6:
                    qr_corners.append(f"M{x + border},{y + border}h1v1h-1z")
                else:
                    qr_parts.append(f"M{x + border},{y + border}h1v1h-1z")

    besj_logo_string = str(besj_logo.tostr())


    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 {qr.get_size() + border * 2} {qr.get_size() + border * 2}" stroke="none">
        
        <path d="{" ".join(qr_parts)}" fill="{
            '#21366b' if color_scheme == 'besj' else '#000000'
        }"/>
        <path d="{" ".join(qr_corners)}" fill="{
            '#f7db38' if color_scheme == 'besj' else '#000000'
        }"/>

        { besj_logo_string }

    </svg>
    """


# Run the main program
if __name__ == "__main__":
    svg_text = create_qr_code("https://besj.ch")
