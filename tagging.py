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
