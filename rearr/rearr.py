from typing import Tuple

import parso
from parso.python.tree import (
    Class,
    Decorator,
    EndMarker,
    Function,
    Module,
    Newline,
    PythonNode,
    String,
)


def get_decorator_weights(item):
    decorators = [
        child for child in item.children if isinstance(child, Decorator)
    ]
    if (
        not decorators
        and item.children
        and isinstance(item.children[0], PythonNode)
    ):
        decorators = [
            child
            for child in item.children[0].children
            if isinstance(child, Decorator)
        ]
    deco_names = [deco.children[1].value for deco in decorators]
    weight = 0
    if "staticmethod" in deco_names:
        weight = -10
    elif "classmethod" in deco_names:
        weight = -5
    return weight


def _is_docstring_part(node) -> bool:
    if isinstance(node, Newline):
        return True
    if isinstance(node, PythonNode) and isinstance(node.children[0], String):
        return True
    return False


def sort_class(cls) -> None:
    suite = cls.get_suite()
    preamble = []
    body = []
    in_body = False
    for c in suite.children:
        if _is_docstring_part(c) and not in_body:
            preamble.append(c)
        else:
            body.append(c)
            in_body = True
    suite.children = preamble + sorted(body, key=sortkey)


def sortkey(item) -> Tuple[int, str]:
    weight = 0
    try:
        name = item.name.value
    except AttributeError:
        name = item.type

    if isinstance(item, EndMarker):
        weight += 9999
    elif isinstance(item, Class):
        weight += 1
    elif isinstance(item, Function):
        weight += 2
    elif isinstance(item, PythonNode) and item.type == "decorated":
        weight += get_decorator_weights(item)
    return (weight, name)


def sort_node(node):
    if isinstance(node, Module):
        for child in node.children:
            if isinstance(child, Class):
                sort_class(child)
        node.children = sorted(node.children, key=sortkey)


def main():
    import sys

    with open(sys.argv[1]) as fptr:
        code = fptr.read()

    tree = parso.parse(code)
    root = tree.get_root_node()

    sort_node(root)
    with open(sys.argv[1], "w") as fptr:
        fptr.write(root.get_code())
    print(f"Changes written to {sys.argv[1]}")


if __name__ == "__main__":
    main()
