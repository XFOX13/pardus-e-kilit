import cv2
import pyzbar.pyzbar as pyzbar
import sqlite3

def read_qr():
    """Bilgisayar kamerası ile QR kod okur ve string olarak döndürür."""
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        for barcode in pyzbar.decode(frame):
            qr_data = barcode.data.decode('utf-8')
            cap.release()
            cv2.destroyAllWindows()
            return qr_data
        cv2.imshow('QR Okutunuz', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return None

def hex_to_6dec(qrdata):
    """QR string’den hexadecimal’e döndürüp son 6 rakamı verir."""
    hexcode = qrdata.encode('utf-8').hex()
    dec = int(hexcode, 16)
    return str(dec)[-6:]

def save_code(code):
    """Olusturulan kodu SQLite veritabanına yazar (codes.db)."""
    conn = sqlite3.connect('codes.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS codes (id INTEGER PRIMARY KEY, code TEXT)')
    c.execute('INSERT INTO codes (code) VALUES (?)', (code,))
    conn.commit()
    conn.close()
