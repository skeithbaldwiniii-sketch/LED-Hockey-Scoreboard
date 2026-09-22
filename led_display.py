# ============================================================
# led_display.py
#
# Display abstraction for the 64x32 hockey scoreboard.
#
# This module defines the common interface that both the
# Windows simulator and Raspberry Pi LED hardware will use.
# ============================================================


class LEDDisplay:

    WIDTH = 64
    HEIGHT = 32

    def clear(self):
        """
        Clear the entire display.
        """
        raise NotImplementedError


    def set_pixel(
        self,
        x,
        y,
        color
    ):
        """
        Set one pixel.

        color should be an RGB tuple:
            (red, green, blue)
        """
        raise NotImplementedError


    def draw_frame(
        self,
        pixels
    ):
        """
        Draw a complete 64x32 frame.

        pixels should be:

            pixels[y][x] = (r, g, b)
        """
        raise NotImplementedError


    def close(self):
        """
        Shut down the display cleanly.
        """
        pass