import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)
tree = parser.parse(open("contoh.py", "rb").read())

print("== 1. Nama fungsi dan jumlah parameter (matches) ==")
q = Query(PY, open("fungsi_param.scm").read())
for _, cap in QueryCursor(q).matches(tree.root_node):
    nama = cap["nama"][0].text.decode()
    jumlah = cap["params"][0].named_child_count
    print(nama, jumlah)

print("\n== 2. Pemanggilan print(...) ==")
q = Query(PY, open("print.scm").read())
for nama, nodes in QueryCursor(q).captures(tree.root_node).items():
    if nama == "fn":
        for n in nodes:
            print(f"baris {n.start_point[0] + 1}: print")

print("\n== 3. Nama modul import ==")
q = Query(PY, open("import.scm").read())
for n in sorted(QueryCursor(q).captures(tree.root_node).get("modul", []), key=lambda n: n.start_byte):
    print(f"baris {n.start_point[0] + 1}: {n.text.decode()}")

print("\n== 4. [Pengayaan] Docstring ==")
q = Query(PY, open("docstring.scm").read())
for n in QueryCursor(q).captures(tree.root_node).get("doc", []):
    print(f"baris {n.start_point[0] + 1}: {n.text.decode()}")
