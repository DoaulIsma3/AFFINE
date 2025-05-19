import streamlit as st

def affine_encrypt(p, a, b):
    cip = ''
    for i in range(len(p)):
        if p[i].isalpha():
            base = 97 if p[i].islower() else 65
            c = chr(((a * (ord(p[i]) - base) + b) % 26) + base)
            cip += c
        else:
            cip += p[i]
    return cip

st.title("Affine Cipher Enkripsi")

# Input dari pengguna
plaintext = st.text_input("Masukkan Plaintext:")
a = st.number_input("Masukkan kunci a (harus relatif prima dengan 26):", min_value=1, step=1)
b = st.number_input("Masukkan kunci b:", min_value=0, step=1)

# Tombol enkripsi
if st.button("Enkripsi"):
    # Validasi: cek apakah a relatif prima terhadap 26
    from math import gcd
    if gcd(int(a), 26) != 1:
        st.error("Kunci a harus relatif prima terhadap 26 (misalnya: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)")
    else:
        ciphertext = affine_encrypt(plaintext, int(a), int(b))
        st.success(f"Ciphertext: {ciphertext}")
