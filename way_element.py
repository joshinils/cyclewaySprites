from math import floor
import settings


class WayElement:
    _width: float
    _height: float
    _distance: float
    colour: str
    background_colour: str

    def __init__(self: 'WayElement', width, height, colour="grey"):
        self._width = width
        self._height = height
        self._distance = None
        self.colour = colour
        self.background_colour = None

        if self._width == "?":
            self._width = 1
        elif not isinstance(self._width, (int, float)):
            print("error: _width is not number:", type(self._width), self._width)

        if self._height == "?":
            self._distance = 1
        elif not isinstance(self._height, (int, float)):
            print("error: _height is not number:", type(self._height), self._height)

        if self._distance == "?":
            self._distance = 1
        elif self._distance is not None and not isinstance(self._distance, (int, float)):
            print("error: _distance is not number:", type(self._distance), self._distance)

    def set_distance(self: 'WayElement', distance, background_colour: str) -> None:
        self._distance = distance
        self.background_colour = background_colour

    def __str__(self: 'WayElement') -> str:
        return "Way_Element: " + str(self.__dict__)

    def convert_meter_to_pixel(self: 'WayElement', val):
        # floor to avoid floating point inaccuracies and weird subpixel gaps in the rendered svg
        return floor(val * settings.Draw()["pixel_pro_meter"])

    def width(self: 'WayElement') -> float:
        return self.convert_meter_to_pixel(self._width)

    def height(self: 'WayElement') -> float:
        return self.convert_meter_to_pixel(self._height)

    def get_distance(self: 'WayElement') -> float:
        if self._distance is None:
            return None
        return self.convert_meter_to_pixel(self._distance)
