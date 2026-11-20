"""cek.py <folder>: pendeteksi TODO/FIXME, fungsi panjang, dan file bersintaks rusak.

Dipakai: python cek.py <folder> [--batas 30]
"""
import sys
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

BATAS_BARIS = 30
FOLDER_DILEWATI = {"venv", ".venv", ".git", "node_modules", "__pycache__"}

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")


def node_error_pertama(node):
    """Cari node ERROR/MISSING pertama (urutan dokumen) secara rekursif."""
    if node.type == "ERROR" or node.is_missing:
        return node
    for child in node.children:
        if child.has_error or child.is_missing:
            hasil = node_error_pertama(child)
            if hasil is not None:
                return hasil
    return None


def cek_file(path):
    tree = parser.parse(path.read_bytes())
    temuan = 0

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: TODO/FIXME: {teks}")
        temuan += 1

    # Fitur 2: fungsi lebih dari BATAS_BARIS baris (semua fungsi dihitung,
    # termasuk method di dalam kelas dan fungsi bersarang)
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > BATAS_BARIS:
            print(f"{path}:{fungsi.start_point[0] + 1}: fungsi panjang: {nama}() {jumlah} baris")
            temuan += 1

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        bermasalah = node_error_pertama(tree.root_node)
        if bermasalah is not None:
            baris = bermasalah.start_point[0] + 1
            jenis = "MISSING " + bermasalah.type if bermasalah.is_missing else "ERROR"
            print(f"{path}:{baris}: sintaks bermasalah ({jenis})")
        else:
            print(f"{path}: sintaks bermasalah")
        temuan += 1
    return temuan


def main():
    global BATAS_BARIS
    args = sys.argv[1:]
    if not args:
        print("Pemakaian: python cek.py <folder> [--batas N]")
        sys.exit(2)
    if "--batas" in args:
        BATAS_BARIS = int(args[args.index("--batas") + 1])
    akar = Path(args[0])

    total_file = total_temuan = 0
    for path in sorted(akar.rglob("*.py")):
        if FOLDER_DILEWATI & set(path.parts):
            continue
        total_file += 1
        total_temuan += cek_file(path)
    print(f"\n{total_file} file diperiksa, {total_temuan} temuan.")


if __name__ == "__main__":
    main()
