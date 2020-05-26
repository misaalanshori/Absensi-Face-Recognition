
# Absensi Menggunakan Face Recognition

  

Sistem absensi otomatis yang menggunakan face recognition untuk mengetahui kehadiran seseorang.

  
  

## Modul yang digunakan

  

  

- face-recognition

- cv2

- numpy

- pygame

- tkinter


## Penjelasan Script dan Penggunaannya

### 1. addUser.py
Script ini berfungsi untuk menambah data nama dan wajah untuk face recognition, data ini akan di simpan ke dalam folder userData.

### 2. faceLogger.py
Script ini akan membaca file dari folder userData kemudian memulai face recognition, hasil dari script ini akan disimpan setiap ~2 menit atau ketika script ditutup, data ini akan disimpan ke folder sessions.

### 3. viewer.py
Script ini akan memberi pilihan untuk memilih file *.session dari folder sessions, kemudian akan menampilkan informasi dari sesi tersebut.

### 4. faceFind.py
Script ini berfungsi untuk memastikan face recognition berjalan dengan baik tanpa membuat file.