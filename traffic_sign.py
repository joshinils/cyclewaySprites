import svgutils
import settings


class TrafficSign:
    name: str

    def __init__(self: 'TrafficSign', name: str, side_weight=1/2) -> 'TrafficSign':
        self.name: str = name
        self.svg = svgutils.transform.fromfile(self.get_path())
        self.svg_size = self.svg.get_size()
        self.side_weight = side_weight

        pixel_pro_meter = settings.Draw()["pixel_pro_meter"]
        groessenfaktor = settings.Draw()["schild"]["groessenfaktor"]
        breite = settings.Draw()["schild"]["breite"]["gross"]

        self.multiplier: float = pixel_pro_meter * groessenfaktor * breite / float(self.svg_size[0])
        self.size_multiplier = (self.multiplier, self.multiplier * float(self.svg_size[1]) / float(self.svg_size[0]))

        self._width = float(self.svg.width) * self.multiplier
        self._height = float(self.svg.height) * self.multiplier

    def get_svg(self: 'TrafficSign', offset_x: float = 0, offset_y: float = 0) -> svgutils.transform.SVGFigure:
        originalSVG = svgutils.compose.SVG(self.get_path())
        originalSVG.scale(self.multiplier)

        # final_size_placement = (self._width + offset_x, self._height + offset_y)

        offset_x -= float(self.svg_size[0]) / 2 * self.multiplier
        offset_y -= float(self.svg_size[1]) / 2 * self.multiplier

        originalSVG.move(offset_x, offset_y)

        #print("offset_x", offset_x, "offset_y", offset_y, "size_multiplier", self.size_multiplier, "final_size", final_size_placement)

        # final_svg_to_save = svgutils.compose.Figure(final_size_placement[0], final_size_placement[1], originalSVG)
        # final_svg_to_save.save(".ts_temp.svg")
        # print(self.name)
        return originalSVG

    def get_path(self: 'TrafficSign') -> str:
        return "img_src/VZ_" + self.name + ".svg"

    def get_height(self: 'TrafficSign') -> float:
        return self._height

    def get_width(self: 'TrafficSign') -> float:
        return self._width

    def __repr__(self: 'TrafficSign') -> str:
        return "TrafficSign " + self.name
