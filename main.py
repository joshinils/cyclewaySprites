#!/usr/bin/env python3

""" generate example data, draw data """

import tagging
from tagging import Tags
import settings
import drawing


def main():
    """ generate example data, draw data """

    # generate default draw settings,
    # add default draw settings
    settings.Draw.set_default_settings()

    # save draw settings
    settings.Draw.write_draw_settings()

    html = "<table><td style=\"    vertical-align: top;\">"
    html += "<table border=1 frame=void>\n"
    html += """    <tr>
        <th>svg</th>
        <th>Way 1</th>
        <th>Way 2</th>
        <th>Way 3</th>
    </tr>"""

    tags = Tags()
    example: tagging.Example
    # draw each group of tags separately
    for example in tags:
        d_file = drawing.Drawing()

        # add tags
        d_file.add_group(example)

        # process tags
        d_file.draw()

        # save processed tags to a file (with default, indexed name)
        d_file.save()

        html += d_file.get_html()
    html += "</table>\n"

    html += "<td></td>"

    html += "<td style=\"vertical-align: top;\">"
    with open("tagging.html") as infile:
        html += infile.read()
    html += "</td>"

    html += "</td></table>\n"

    with open("tagging_generated.html", "w") as outfile:
        outfile.write(html)


if __name__ == "__main__":
    main()
