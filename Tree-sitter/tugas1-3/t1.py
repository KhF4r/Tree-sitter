import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

POTONGAN = {
    "fungsi": b"def sapa(nama):\n    return nama\n",
    "if_else": b"if x > 0:\n    y = 1\nelse:\n    y = 2\n",
    "kelas": b"class Hewan:\n    def bunyi(self):\n        return 'suara'\n",
    "fungsi_rusak (hapus ':')": b"def sapa(nama)\n    return nama\n",
    "kurung_rusak (hapus ')')": b"print(1 + 2\n",
}

for judul, kode in POTONGAN.items():
    tree = parser.parse(kode)
    print("=" * 60)
    print(judul)
    print(kode.decode())
    print("root_node :", tree.root_node)
    print("has_error :", tree.root_node.has_error)

# Node anonim vs bernama pada potongan fungsi
tree = parser.parse(POTONGAN["fungsi"])
fdef = tree.root_node.children[0]
print("=" * 60)
print("children dari function_definition:")
for c in fdef.children:
    print("  ", c.type, "bernama" if c.is_named else "anonim")
print("parameters children:")
for c in fdef.child_by_field_name("parameters").children:
    print("  ", c.type, "bernama" if c.is_named else "anonim")
print("len(children) =", len(fdef.children), "| len(named_children) =", len(fdef.named_children))
