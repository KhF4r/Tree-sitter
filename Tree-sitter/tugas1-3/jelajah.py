import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    for i, child in enumerate(node.children):
        if not child.is_named:
            continue
        jelajah(child, kedalaman + 1, node.field_name_for_child(i))


def jelajah_cursor(tree):
    """[Pengayaan] Versi TreeCursor, output harus identik dengan versi rekursif."""
    out = []
    cursor = tree.walk()
    kedalaman = 0
    while True:
        node = cursor.node
        if node.is_named:
            baris, kolom = node.start_point
            fn = cursor.field_name
            label = f"{fn}: " if fn else ""
            out.append("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
        if cursor.goto_first_child():
            # kedalaman hanya bertambah bila node induk bernama
            if node.is_named:
                kedalaman += 1
            continue
        while not cursor.goto_next_sibling():
            if not cursor.goto_parent():
                return out
            if cursor.node.is_named:
                kedalaman -= 1


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        tree = parser.parse(f.read())
    jelajah(tree.root_node)
