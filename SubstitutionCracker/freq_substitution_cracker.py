#!/usr/bin/env python3
"""
freq_substitution_cracker.py

Analisis frekuensi sederhana untuk mencoba menebak substitution cipher tanpa kunci.
- Baca ciphertext dari file (default: ciphertext.txt)
- Tampilkan tabel frekuensi
- Bandingkan dengan frekuensi bahasa Inggris
- Buat dugaan awal pemetaan (most-frequent -> ETAOIN...)
- Beri antarmuka interaktif untuk memperbaiki pemetaan
- Simpan hasil ke file (default: result.txt)

Cara pakai:
    python freq_substitution_cracker.py [input_file] [output_file]
Contoh:
    python freq_substitution_cracker.py ciphertext.txt result.txt
"""

import string
from collections import Counter
import argparse
import sys

# Urutan frekuensi huruf bahasa Inggris (paling sering ke paling jarang)
ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# Persentase frekuensi (dipakai hanya untuk perbandingan & tampilan)
ENGLISH_FREQ = {
    'E':12.70,'T':9.06,'A':8.17,'O':7.51,'I':6.97,'N':6.75,'S':6.33,'H':6.09,'R':6.00,
    'D':4.25,'L':4.03,'C':2.78,'U':2.76,'M':2.41,'W':2.36,'F':2.23,'G':2.02,'Y':1.97,
    'P':1.93,'B':1.49,'V':0.98,'K':0.77,'J':0.15,'X':0.15,'Q':0.10,'Z':0.07
}

def read_ciphertext(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def letter_frequency(text):
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters)
    counter = Counter(letters)
    # return list of tuples: (letter, count, percent)
    freq_list = []
    for ch in string.ascii_uppercase:
        cnt = counter.get(ch, 0)
        pct = (cnt / total * 100) if total > 0 else 0.0
        freq_list.append((ch, cnt, pct))
    # sort by count desc
    freq_sorted = sorted(freq_list, key=lambda x: x[1], reverse=True)
    return freq_sorted, total

def print_frequency_table(freq_sorted, total):
    print(f"\nTotal letters: {total}\n")
    print(f"{'Rank':>4} {'Letter':>6} {'Count':>8} {'Percent':>10}")
    print("-" * 34)
    for i, (ch, cnt, pct) in enumerate(freq_sorted, start=1):
        print(f"{i:>4} {ch:>6} {cnt:8d} {pct:9.3f}%")
    print()

def initial_mapping_from_freq(freq_sorted):
    # freq_sorted: list of (letter, count, pct), descending
    cipher_order = [ch for (ch, _, _) in freq_sorted]  # all 26 letters in order by freq
    # Map each cipher-letter to english most-frequent letters
    mapping = {}
    for c_cipher, c_plain in zip(cipher_order, ENGLISH_FREQ_ORDER):
        mapping[c_cipher] = c_plain
    # mapping now is a dict: cipher_letter -> guessed plaintext letter
    return mapping

def apply_mapping(text, mapping):
    # map letters, preserve case, non-letters left as-is
    out_chars = []
    for ch in text:
        if ch.isalpha():
            mapped = mapping.get(ch.upper(), '?')
            if ch.islower():
                out_chars.append(mapped.lower())
            else:
                out_chars.append(mapped)
        else:
            out_chars.append(ch)
    return ''.join(out_chars)

def print_mapping(mapping):
    # Show mapping in readable two-row format
    letters = list(string.ascii_uppercase)
    row1 = "cipher: "
    row2 = "plain : "
    for ch in letters:
        row1 += ch + " "
        row2 += mapping.get(ch, '?') + " "
    print("\n" + row1)
    print(row2 + "\n")

def save_results(ciphertext, mapping, freq_sorted, total, filename):
    dec_text = apply_mapping(ciphertext, mapping)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=== Frequency table (ciphertext) ===\n")
        f.write(f"Total letters: {total}\n\n")
        f.write(f"{'Rank':>4} {'Letter':>6} {'Count':>8} {'Percent':>10}\n")
        f.write("-" * 34 + "\n")
        for i, (ch, cnt, pct) in enumerate(freq_sorted, start=1):
            f.write(f"{i:>4} {ch:>6} {cnt:8d} {pct:9.3f}%\n")
        f.write("\n=== English frequency (reference) ===\n")
        for ch in ENGLISH_FREQ_ORDER:
            f.write(f"{ch}: {ENGLISH_FREQ.get(ch, 0):.2f}%\n")
        f.write("\n=== Current mapping (cipher -> plain) ===\n")
        for ch in string.ascii_uppercase:
            f.write(f"{ch} -> {mapping.get(ch, '?')}\n")
        f.write("\n=== Decrypted text (using current mapping) ===\n\n")
        f.write(dec_text)
    print(f"Saved analysis & decrypted text to '{filename}'")

def interactive_loop(ciphertext, mapping, freq_sorted, total, default_outfile):
    print("\nMasuk mode interaktif. Ketik 'help' untuk daftar perintah.")
    initial_map = mapping.copy()
    while True:
        try:
            cmdline = input("command> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar interaktif.")
            break
        if not cmdline:
            continue
        parts = cmdline.split()
        cmd = parts[0].lower()

        if cmd in ('quit', 'exit'):
            print("Keluar program.")
            break

        elif cmd == 'help':
            print("""Perintah:
  show                - tampilkan tabel pemetaan (cipher -> plain)
  apply               - tampilkan seluruh teks hasil dekripsi sekarang
  preview [n]         - tampilkan n karakter awal dari dekripsi (default 300)
  set C P             - set/pasang: huruf ciphertext C -> huruf plaintext P (akan swap jika P sudah dipakai)
  swap C1 C2          - tukar mapping dua huruf ciphertext C1 <-> C2
  reset               - kembali ke dugaan awal mapping
  save [filename]     - simpan hasil analisis & dekripsi ke file (default: result.txt)
  freq                - tampilkan tabel frekuensi lagi
  help                - tampilkan pesan ini
  quit / exit         - keluar
Contoh:
  set X E
  swap X Y
  preview 200
  save myresult.txt
""")

        elif cmd == 'show':
            print_mapping(mapping)

        elif cmd == 'freq':
            print_frequency_table(freq_sorted, total)

        elif cmd == 'apply':
            out = apply_mapping(ciphertext, mapping)
            print("\n=== Decrypted text (current) ===\n")
            print(out)
            print()

        elif cmd == 'preview':
            n = 300
            if len(parts) >= 2 and parts[1].isdigit():
                n = int(parts[1])
            out = apply_mapping(ciphertext, mapping)
            print("\n--- preview (first {} chars) ---\n".format(n))
            print(out[:n])
            print("\n--- end preview ---\n")

        elif cmd == 'set' and len(parts) == 3:
            c = parts[1].upper()
            p = parts[2].upper()
            if c not in string.ascii_uppercase or p not in string.ascii_uppercase:
                print("Huruf tidak valid. Gunakan huruf A-Z.")
                continue
            # cari cipher letter yang sudah memetakan ke p (jika ada)
            prev = None
            for k, v in mapping.items():
                if v == p:
                    prev = k
                    break
            # swap / reassign
            if prev is None:
                mapping[c] = p
            else:
                # tukar nilai prev dan c
                mapping[prev], mapping[c] = mapping[c], p
            print(f"Set: {c} -> {p} (jika diperlukan, swap dilakukan)")

        elif cmd == 'swap' and len(parts) == 3:
            a = parts[1].upper()
            b = parts[2].upper()
            if a not in string.ascii_uppercase or b not in string.ascii_uppercase:
                print("Huruf tidak valid. Gunakan huruf A-Z.")
                continue
            mapping[a], mapping[b] = mapping[b], mapping[a]
            print(f"Swapped: {a} <-> {b}")

        elif cmd == 'reset':
            mapping = initial_map.copy()
            print("Mapping dikembalikan ke dugaan awal.")

        elif cmd == 'save':
            fname = parts[1] if len(parts) >= 2 else default_outfile
            save_results(ciphertext, mapping, freq_sorted, total, fname)

        else:
            print("Perintah tidak dikenali. Ketik 'help' untuk panduan.")

def main():
    parser = argparse.ArgumentParser(description="Frequency-based Substitution Cipher cracker (interactive).")
    parser.add_argument('input', nargs='?', default='ciphertext.txt', help='file input ciphertext (default: ciphertext.txt)')
    parser.add_argument('output', nargs='?', default='result.txt', help='file output hasil analisis (default: result.txt)')
    args = parser.parse_args()

    try:
        ciphertext = read_ciphertext(args.input)
    except FileNotFoundError:
        print(f"File '{args.input}' tidak ditemukan. Buat file bernama '{args.input}' berisi ciphertext (>= 200 huruf) lalu jalankan lagi.")
        sys.exit(1)

    freq_sorted, total = letter_frequency(ciphertext)
    if total < 200:
        print(f"Peringatan: jumlah huruf dalam ciphertext hanya {total} (disarankan >= 200 untuk analisis frekuensi lebih akurat).")

    print("\n=== TABEL FREKUENSI (ciphertext) ===")
    print_frequency_table(freq_sorted, total)

    print("=== FREKUENSI BAHASA INGGRIS (referensi) ===")
    for ch in ENGLISH_FREQ_ORDER:
        print(f"{ch}: {ENGLISH_FREQ.get(ch, 0):5.2f}% ", end='')
    print("\n")

    # buat dugaan mapping awal
    mapping = initial_mapping_from_freq(freq_sorted)
    print("=== DUGAAN AWAL PEMETAAN (cipher -> plain) ===")
    print_mapping(mapping)

    # tampilkan dekripsi awal (preview)
    preview = apply_mapping(ciphertext, mapping)
    print("\n=== Dekripsi awal (preview 500 chars) ===\n")
    print(preview[:500])
    print("\n(untuk melihat seluruh hasil gunakan perintah 'apply' di mode interaktif)\n")

    # simpan initial result otomatis
    save_results(ciphertext, mapping, freq_sorted, total, args.output)

    # masuk mode interaktif untuk perbaikan manual
    interactive_loop(ciphertext, mapping, freq_sorted, total, args.output)

if __name__ == "__main__":
    main()
