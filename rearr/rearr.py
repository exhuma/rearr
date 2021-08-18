import argparse
import sys
from os.path import exists
from shutil import copy
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

ITEM_WEIGHT = {
    "if_stmt": 10,
    "classdef": 20,
    "funcdef": 30,
    "simple_stmt": 40,
    "endmarker": 9999,
}

ITEM_WEIGHT_CLS = {
    "if_stmt": 10,
    "simple_stmt": -10,
    "classdef": 30,
    "funcdef": 40,
    "endmarker": 9999,
}


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--write",
        help="Write modified files to disk (use with caution)",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--no-backup",
        help="Don't keep backup files",
        action="store_true",
        default=False,
    )
    parser.add_argument("filename", nargs="+", help="Files to check/modify")
    return parser.parse_args()


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
    weight = ITEM_WEIGHT.get(item, 0)
    if "staticmethod" in deco_names:
        weight -= 2
    elif "classmethod" in deco_names:
        weight -= 1
    return weight


def _is_docstring_part(node) -> bool:
    if isinstance(node, Newline):
        return True
    if isinstance(node, PythonNode) and isinstance(node.children[0], String):
        return True
    return False


def sort_class(cls) -> None:
    suite = cls.get_suite()
    if not should_rearrange(suite):
        return
    preamble = []
    body = []
    in_body = False
    for c in suite.children:
        if _is_docstring_part(c) and not in_body:
            preamble.append(c)
        else:
            body.append(c)
            in_body = True
    suite.children = preamble + sorted(body, key=sortkey_cls)


def mk_sortkey(weights):
    def sortkey(item) -> Tuple[int, str]:
        weight = 0
        try:
            name = item.name.value
        except AttributeError:
            name = item.type

        if item.type == "decorated":
            weight = get_decorator_weights(item)
        else:
            weight = weights.get(item.type, 0)
        return (weight, name)
    return sortkey

sortkey_cls = mk_sortkey(ITEM_WEIGHT_CLS)
sortkey_mod = mk_sortkey(ITEM_WEIGHT)


def sort_node(node):
    if isinstance(node, Module):
        for child in node.children:
            if isinstance(child, Class):
                sort_class(child)
        if should_rearrange(node):
            node.children = sorted(node.children, key=sortkey_mod)


def modify_file(filename: str, data: str, keep_backup: bool) -> None:
    if keep_backup:
        backup_filename = f"{filename}.orig"
        if exists(backup_filename):
            print(
                f"!! File {backup_filename} already exists! Aborting to avoid "
                "data-loss!",
                file=sys.stderr,
            )
            return
        copy(filename, backup_filename)
    with open(filename, "w") as fptr:
        fptr.write(data)
    print(f"Changes written to {filename}")


def should_rearrange(tree) -> bool:
    for c in tree.children:
        if c.type != "simple_stmt":
            continue
        for line in parso.split_lines(c.get_code()):
            if line.strip().startswith("# rearr: enable"):
                return True
    return False


def main():
    args = parse_args()
    diffed_files = []
    for fname in args.filename:
        with open(fname) as fptr:
            code = fptr.read()

        tree = parso.parse(code)
        root = tree.get_root_node()

        sort_node(root)
        modified_code = root.get_code()
        if modified_code != code:
            diffed_files.append(fname)
            if args.write:
                modify_file(fname, root.get_code(), not args.no_backup)
            else:
                print(f"Changes detected in {fname}")
    return 1 if diffed_files else 0


if __name__ == "__main__":
    sys.exit(main())
