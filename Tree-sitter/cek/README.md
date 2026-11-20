# cek.py: pemeriksa kode Python berbasis tree-sitter

Tiga laporan untuk file `.py` dalam sebuah folder:

1. Komentar berisi `TODO` atau `FIXME` (query `(comment) @c` + predikat `#match?`).
2. Fungsi yang lebih dari 30 baris (query `function_definition`, lalu `end_point - start_point + 1`).
3. File yang pohonnya punya error sintaks (`root_node.has_error`, lalu cari node `ERROR`/`MISSING` pertama).

## Pasang dependensi

```bash
pip install tree-sitter tree-sitter-python
```

(Dibuat dan diuji dengan py-tree-sitter 0.25+, gaya `Parser(LANG)` dan `QueryCursor`.)

## Menjalankan

```bash
python cek.py uji/              # batas bawaan 30 baris
python cek.py <folder> --batas 50
```

Folder `venv/`, `.venv/`, `.git/`, `node_modules/`, dan `__pycache__/` dilewati.
Semua fungsi dihitung, termasuk method di dalam kelas dan fungsi bersarang.

## Contoh output (folder `uji/`)

```
uji/ada_todo.py:2: TODO/FIXME: # TODO: ganti dengan versi cepat
uji/ada_todo.py:5: TODO/FIXME: # FIXME angka ajaib
uji/fungsi_panjang.py:1: fungsi panjang: panjang() 36 baris
uji/rusak.py:1: sintaks bermasalah (ERROR)

4 file diperiksa, 4 temuan.
```

## Pengujian pada repo nyata

Repo: `pallets/itsdangerous` (15 file Python). Hasil lengkap ada di `hasil_repo_nyata.txt`:
1 TODO dan 6 fungsi panjang. Dicocokkan dengan `grep` (TODO) dan modul `ast` bawaan Python
(panjang fungsi): seluruh temuan identik.
