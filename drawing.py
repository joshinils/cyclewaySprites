#!/usr/bin/env python3
# pylint: disable=line-too-long

import typing
from math import floor
import svgwrite
import settings
from way import Way
from way_element import WayElement
import tagging


class Drawing:
    """ temporarily stores data to draw and can output it to svg and an html table referenceing the svg file """
    ways: typing.List
    svg_obj: svgwrite.Drawing
    file_name: str

    # static class member
    file_name_counter = 0

    def __init__(self: 'Drawing', file_name: typing.Optional[str] = "svg/default.svg") -> 'Drawing':
        if file_name == "svg/default.svg":
            file_name = "svg/default" + str(Drawing.file_name_counter) + ".svg"
            Drawing.file_name_counter += 1
        self.ways = []
        self.file_name = file_name

    def add_group(self: 'Drawing', example: tagging.Example) -> None:
        """ add an example to draw """
        tag_group: tagging.Tag_group
        count = 0
        for tag_group in example:
            self.add_way(tag_group.name, tag_group, count, len(example))
            count += 1

    def draw(self: 'Drawing'):
        """ if all data to be used is set, call draw() """
        width = 0
        widths = list()

        way: Way
        for way in self.ways:
            elem: WayElement
            thisWidth = 0
            for elem in way.get_elements():
                width += elem.width()
                thisWidth += elem.width()
            widths.append(thisWidth)

        self.svg_obj = svgwrite.Drawing(self.file_name, profile='full', size=(floor(width), floor(settings.Draw()["draw_height_meter"] * settings.Draw()["pixel_pro_meter"])))

        way: Way
        x_offset = 0
        for way in self.ways:
            elem: WayElement
            for elem in way.get_elements():
                # print(elem)

                # overlap is used to draw elements over one-another to avoid issues with gaps
                # between elements at differing zoom scales while viewing in-browser
                overlap = 3.14

                # is dashable elem
                if elem.get_distance() is not None:
                    # draw dashed

                    y_offset = 0
                    # initially half at top
                    self.svg_obj.add(self.svg_obj.rect((x_offset, y_offset), (elem.width()+overlap, elem.height()/2+overlap), fill=elem.colour))
                    y_offset += elem.height()/2
                    while y_offset < settings.Draw()["draw_height_meter"] * settings.Draw()["pixel_pro_meter"]:
                        self.svg_obj.add(self.svg_obj.rect((x_offset, y_offset), (elem.width()+overlap, elem.get_distance()+overlap), fill=elem.background_colour))
                        y_offset += elem.get_distance()
                        self.svg_obj.add(self.svg_obj.rect((x_offset, y_offset), (elem.width()+overlap, elem.height()+overlap), fill=elem.colour))
                        y_offset += elem.height()
                else:  # solid
                    self.svg_obj.add(self.svg_obj.rect((x_offset, 0), (elem.width()+overlap, elem.height()+overlap), fill=elem.colour))
                x_offset += elem.width()

    def add_way(self: 'Drawing', name: str, tags: tagging.Tag_group, count: int, total: int) -> None:
        self.ways.append(Way(name, tags, count, total))

    def add_test_elems(self: 'Drawing') -> None:
        self.svg_obj.add(self.svg_obj.line((0, 0), (100, 10), stroke=svgwrite.rgb(10, 10, 16, '%')))
        self.svg_obj.add(self.svg_obj.text('Test', insert=(10, 10.2), fill='red'))
        self.svg_obj.add(self.svg_obj.rect((0, 0), (10, 10), fill='blue'))

    def save(self: 'Drawing') -> None:
        self.svg_obj.save()

    @staticmethod
    def html_row(key, value, background_key=None, background_value=None) -> str:
        """ get html row for given tags, if background is given, style cell with color """
        res = """\n                <tr>\n                    <td style="text-align: right;"""
        if background_key is not None:
            res += "background:" + background_key + ";"
        res += """\"><code>"""
        res += key
        res += """</code></td>\n                    <td"""
        if background_value is not None:
            res += " style=\"background:" + background_value + ";\""
        res += """><code>"""
        res += value
        res += """</code></td>\n                </tr>"""
        return res

    def get_html(self: 'Drawing') -> str:
        """ return representation as HTML table row """
        res = """\n    <tr>\n        <td><img src=\""""
        res += self.file_name
        res += """\" height=\""""
        res += str(300)
        res += """px"></td>\n"""
        way: Way
        for way in self.ways:
            res += """        <td>\n            <table border=1 frame=void>"""
            for key, value in way.tags.items():
                background_key = None
                if key not in Way.recognized_tags:
                    if key in Way.ignored_tags:
                        background_key = "lightgrey"
                    else:
                        background_key = "red"
                background_value = None
                if key not in Way.recognized_tags or value not in Way.recognized_tags[key]:
                    if key in Way.ignored_tags and value in Way.ignored_tags[key]:
                        background_value = "lightgray"
                    else:
                        background_value = "yellow"
                res += Drawing.html_row(key, value, background_key, background_value)

            for key, value in way.filtered_tags.items():
                if key in way.tags:
                    continue
                background_key = "grey"
                if key not in Way.recognized_tags:
                    if key in Way.ignored_tags:
                        background_key = "darkgrey"
                    else:
                        background_key = "orange"
                background_value = "grey"
                if key not in Way.recognized_tags or value not in Way.recognized_tags[key]:
                    if key in Way.ignored_tags and value in Way.ignored_tags[key]:
                        background_value = "darkgray"
                    else:
                        background_value = "orange"
                res += Drawing.html_row(key, value, background_key, background_value)
            res += """\n            </table>\n        </td>\n"""
        res += """    </tr>"""
        return res
