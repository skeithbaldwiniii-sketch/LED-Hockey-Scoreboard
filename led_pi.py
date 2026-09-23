# ============================================================
# led_pi.py
#
# Raspberry Pi HUB75 display backend.
# ============================================================

from led_display import LEDDisplay


class PiLEDDisplay(LEDDisplay):

    def __init__(
        self,
        rows=32,
        cols=64,
        chain=1,
        slowdown=4
    ):

        from rgbmatrix import (
            RGBMatrix,
            RGBMatrixOptions
        )


        options = RGBMatrixOptions()

        options.rows = rows
        options.cols = cols
        options.chain_length = chain
        options.parallel = 1

        options.gpio_slowdown = slowdown

        options.disable_hardware_pulsing = True

        options.hardware_mapping = "regular"

        # This is the panel configuration that
        # successfully worked with your Waveshare
        # P5 panel during our hardware test.
        options.panel_type = "FM6127"


        self.matrix = RGBMatrix(
            options=options
        )

        self.canvas = (
            self.matrix.CreateFrameCanvas()
        )


    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):

        self.canvas.Clear()

        self.canvas = (
            self.matrix.SwapOnVSync(
                self.canvas
            )
        )


    # ========================================================
    # SET PIXEL
    # ========================================================

    def set_pixel(
        self,
        x,
        y,
        color
    ):

        r, g, b = color

        self.canvas.SetPixel(
            x,
            y,
            r,
            g,
            b
        )


    # ========================================================
    # DRAW FRAME
    # ========================================================

    def draw_frame(
        self,
        pixels
    ):

        self.canvas.Clear()


        for y in range(
            self.HEIGHT
        ):

            for x in range(
                self.WIDTH
            ):

                r, g, b = pixels[y][x]


                if (
                    r == 0
                    and g == 0
                    and b == 0
                ):

                    continue


                self.canvas.SetPixel(
                    x,
                    y,
                    r,
                    g,
                    b
                )


        self.canvas = (
            self.matrix.SwapOnVSync(
                self.canvas
            )
        )


    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        self.canvas.Clear()

        self.canvas = (
            self.matrix.SwapOnVSync(
                self.canvas
            )
        )
