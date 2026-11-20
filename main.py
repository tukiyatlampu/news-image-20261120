# Poster berita 20 Nov 2026 — pengubah berkas base64 menjadi PNG.
# Satu tugas saja: baca image.b64 di sebelah berkas ini, uraikan, simpan ke /output.
# Tidak ada jaringan, jam, atau acak di sini; keluaran selalu sama.

import base64
import sys
from pathlib import Path


def _direktori_paket():
    return Path(__file__).resolve().parent


def _ambil_teks_terkode(direktori):
    jalur = direktori.joinpath("image.b64")
    return jalur.read_text(encoding="utf-8")


def _bersihkan_spasi(teks):
    return "".join(teks.split())


def _uraikan_ke_byte(teks_bersih):
    return base64.b64decode(teks_bersih, validate=True)


def _simpan_hasil(byte_png):
    folder_keluar = Path("/output")
    folder_keluar.mkdir(parents=True, exist_ok=True)
    target = folder_keluar.joinpath("entry.png")
    target.write_bytes(byte_png)
    return target


def jalankan():
    paket = _direktori_paket()
    teks = _ambil_teks_terkode(paket)
    byte_png = _uraikan_ke_byte(_bersihkan_spasi(teks))
    target = _simpan_hasil(byte_png)
    print("poster tersimpan: {} ({} byte)".format(target, len(byte_png)))
    return 0


if __name__ == "__main__":
    sys.exit(jalankan())
