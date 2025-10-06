# Frequency-based Substitution Cipher Cracker

Program sederhana untuk menganalisis ciphertext Substitution Cipher tanpa kunci menggunakan **analisis frekuensi**.  
Program membaca `ciphertext.txt`, menampilkan tabel frekuensi huruf, membuat dugaan awal pemetaan berdasarkan frekuensi bahasa Inggris, menampilkan dekripsi awal, dan menyediakan mode interaktif untuk memperbaiki pemetaan secara manual. Hasil analisis dapat disimpan ke `result.txt`.

## Persyaratan
- Python 3.x
- Editor teks (mis. VS Code, Notepad++)
- Terminal / Command Prompt

## Struktur berkas
- `freq_substitution_cracker.py` — program utama (Python).
- `ciphertext.txt` — file input berisi ciphertext (disarankan ≥ 200 huruf).
- `result.txt` — file output yang berisi tabel frekuensi, mapping, dan hasil dekripsi (dibuat otomatis).
- `README.md` — dokumentasi ini.

## Cara menjalankan
1. Pastikan `freq_substitution_cracker.py` dan `ciphertext.txt` berada di folder yang sama.
2. Buka terminal pada folder tersebut.
3. Jalankan perintah:
```bash
python freq_substitution_cracker.py ciphertext.txt result.txt
```
4. command "help" untuk melihat perintah apa saja yang bisa dilakukan
