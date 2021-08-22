#!/usr/bin/env python3

import typing
import json
import os


class Tag_group(typing.Dict[str, str]):
    name: str
    direction: str

    def __init__(self: 'Tag_group', name: str, direction: str, tags: typing.Dict[str, str]) -> 'Tag_group':
        self.name = name
        self.direction = direction
        self.update(tags)


class Example(typing.List[Tag_group]):
    """ an Example is a list of Tag_group's plus metadata """
    name: str
    sort_weight: float

    def __init__(self: 'Example', example_name: str, example_data: dict) -> 'Example':
        self.name = example_name
        self.sort_weight = example_data.get("sort_weight", 0)

        way_group: dict
        for way_group in example_data.get("ways", []):
            self.append(Tag_group(way_group.get("name", None), way_group.get("direction", "up"), way_group.get("tags", {})))


def printlist(l: list, indent=0):
    for item in l:
        if type(item) is dict:
            print(indent * " " * 4, "{")
            printdict(item, indent + 1)
            print(indent * " " * 4, "}")
        elif type(item) is list:
            print(indent * " " * 4, "[")
            printlist(item, indent + 1)
            print(indent * " " * 4, "]")
        else:
            print(indent * " " * 4, item, type(item))


def printdict(d: dict, indent: int = 0):
    for key, value in d.items():
        if type(value) is dict:
            print(indent * " " * 4, key, ": {")
            printdict(value, indent + 1)
            print(indent * " " * 4, "}")
        elif type(value) is list:
            print(indent * " " * 4, key, ": [")
            printlist(value, indent + 1)
            print(indent * " " * 4, "]")
        else:
            print(indent * " " * 4, key, ":", value, type(value))


class Tags(typing.List[Example]):
    def __init__(self: 'Tags'):
        filenames = next(os.walk("tags"), (None, None, []))[2]  # [] if no file
        for filename in filenames:
            if not filename.endswith(".json"):
                # only read json files
                continue
            with open("tags" + os.sep + filename) as json_file:
                json_data = json.load(json_file)
            # print(json.dumps(tag_data, sort_keys = True, indent = 4, ensure_ascii=False))
            # printdict(tag_data)
            for example_name, example_data in json_data.items():
                self.append(Example(example_name, example_data))
        # sort by sort_weight
        self.sort(key=lambda x: x.sort_weight)


def get_tags() -> typing.Dict:
    # read settings data from json
    tag_data = None
    with open("tags/tags.json") as json_file:
        tag_data = json.load(json_file)
        #print(json.dumps(tag_data, sort_keys = True, indent = 4, ensure_ascii=False))
    return tag_data


def get_example_tags() -> typing.Dict:
    data = {"tags": list()}
    tags = data["tags"]

    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:both": "no",
            "sidewalk:both": "no",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:both": "no",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:left": "no",
            "cycleway:right": "separate",
            "bicycle:right": "optional_sidepath",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
            "foot": "designated",
            "bicycle": "yes",
            "maxspeed:bicycle": "walk",
            "traffic_sign": "DE:239;1022-10",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:left": "no",
            "cycleway:right": "lane",
            "cycleway:right:lane": "advisory",
            "cycleway:right:lane:bicycle": "yes",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "lanes": "2",
            "cycleway:left": "no",
            "cycleway:right": "lane",
            "cycleway:right:lane": "advisory",
            "cycleway:right:lane:bicycle": "yes",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "lanes": "2",
            "cycleway:left": "no",
            "cycleway:right": "lane",
            "cycleway:right:lane": "exclusive",
            "cycleway:right:lane:bicycle": "designated",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:left": "no",
            "sidewalk:left": "no",
            "cycleway:right": "separate",
            "bicycle:right": "use_sidepath",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "path",
            "footway": "sidewalk",
            "foot": "designated",
            "bicycle": "designated",
            "segregated": "no",
            "traffic_sign": "DE:240",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "optional_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "path",
            "bicycle": "yes",
            "bicycle:oneway": "yes",
            "foot": "designated",
            "footway": "sidewalk",
            "segregated": "yes",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "path",
            "bicycle": "designated",
            "bicycle:oneway": "yes",
            "foot": "designated",
            "footway": "sidewalk",
            "segregated": "yes",
            "traffic_sign": "DE:241-30",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "optional_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "yes",
            "bicycle:oneway": "yes",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "designated",
            "bicycle:oneway": "yes",
            "traffic_sign": "DE:237",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:both": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "designated",
            "bicycle:oneway": "no",
            "traffic_sign": "DE:237;1000-31",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:both": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "path",
            "bicycle": "designated",
            "foot": "designated",
            "bicycle:oneway": "no",
            "segregated": "yes",
            "footway": "sidewalk",
            "traffic_sign": "DE:241;1000-31",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "optional_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "yes",
            "bicycle:oneway": "yes",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "designated",
            "bicycle:oneway": "yes",
            "traffic_sign": "DE:237",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:both": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "designated",
            "bicycle:oneway": "no",
            "traffic_sign": "DE:237;1000-31",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })

    # print(data)

    return data
