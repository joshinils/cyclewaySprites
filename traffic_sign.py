import svgwrite


class TrafficSign:
    name: str

    def __init__(self: 'TrafficSign', name: str) -> 'TrafficSign':
        self.name: str = name

    def __repr__(self: 'TrafficSign') -> str:
        return "TrafficSign " + self.name

    def get_svg(self: 'TrafficSign') -> svgwrite.image.Image:
        return svgwrite.image.Image("../img_src/VZ_" + self.name + ".svg", insert=(0, 0), size=(100, 100))
