import streamlit as st
import sqlite3
import pandas as pd
from io import StringIO

# Caesar Cipher
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

# Database setup
conn = sqlite3.connect('pasien_encrypted.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS pasien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        umur INTEGER,
        jenis_kelamin TEXT,
        alamat TEXT,
        diagnosa TEXT
    )
''')
conn.commit()

# Fungsi tambah data pasien (nama terenkripsi)
def tambah_pasien(nama, umur, jk, alamat, diagnosa, shift):
    nama_encrypted = caesar_encrypt(nama, shift)
    c.execute('INSERT INTO pasien (nama, umur, jenis_kelamin, alamat, diagnosa) VALUES (?, ?, ?, ?, ?)',
              (nama_encrypted, umur, jk, alamat, diagnosa))
    conn.commit()

# Fungsi ambil semua data pasien, nama didekripsi dulu
def ambil_data_pasien(shift):
    c.execute('SELECT * FROM pasien')
    rows = c.fetchall()
    decrypted_rows = []
    for row in rows:
        id_, nama_enc, umur, jk, alamat, diagnosa = row
        nama_dec = caesar_decrypt(nama_enc, shift)
        decrypted_rows.append((id_, nama_dec, umur, jk, alamat, diagnosa))
    return decrypted_rows

# Fungsi hapus data pasien
def hapus_pasien(id):
    c.execute('DELETE FROM pasien WHERE id=?', (id,))
    conn.commit()

# Streamlit UI
st.title("📋 Data Pasien dengan Enkripsi Nama (Caesar Cipher)")

shift = st.sidebar.number_input("Shift Caesar Cipher (0-25)", min_value=0, max_value=25, value=3)
menu = st.sidebar.selectbox("Menu", ["Tambah Data", "Lihat Data"])

if menu == "Tambah Data":
    st.subheader("Tambah Data Pasien")
    nama = st.text_input("Nama Pasien")
    umur = st.number_input("Umur", min_value=0)
    jk = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    alamat = st.text_input("Alamat")
    diagnosa = st.text_input("Diagnosa")

    if st.button("Simpan"):
        if nama.strip() == "":
            st.error("Nama pasien tidak boleh kosong!")
        else:
            tambah_pasien(nama, umur, jk, alamat, diagnosa, shift)
            st.success("Data pasien berhasil disimpan dengan nama terenkripsi!")

elif menu == "Lihat Data":
    st.subheader("Daftar Pasien (Nama sudah didekripsi)")

    data = ambil_data_pasien(shift)
    if len(data) == 0:
        st.info("Belum ada data pasien.")
    else:
        for row in data:
            st.write(f"ID: {row[0]}, Nama: {row[1]}, Umur: {row[2]}, JK: {row[3]}, Alamat: {row[4]}, Diagnosa: {row[5]}")
            if st.button(f"Hapus Data ID {row[0]}"):
                hapus_pasien(row[0])
                st.warning(f"Data pasien dengan ID {row[0]} berhasil dihapus!")
                st.experimental_rerun()

        # Buat DataFrame untuk download CSV
        df = pd.DataFrame(data, columns=["ID", "Nama", "Umur", "Jenis Kelamin", "Alamat", "Diagnosa"])

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Data Pasien (CSV)",
            data=csv,
            file_name='data_pasien_decrypted.csv',
            mime='text/csv',
        )
