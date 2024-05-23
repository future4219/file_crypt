from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib

def decrypt_file(input_file, output_file, key):
    
    key = hashlib.sha256(key.encode('utf-8')).hexdigest()[-16:]
    # キーをバイト列に変換
    key = key.encode('utf-8')

    # 初期化ベクトル（IV）を生成
    iv = b'\x00' * 16  # 16バイトのゼロ

    # AES CBC復号化器を作成
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # パディングを削除するためのアンパディングオブジェクトを作成
    unpadder = padding.PKCS7(128).unpadder()

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(16)  # 16バイトずつ読み込む
            if not chunk:
                break
            decrypted_chunk = decryptor.update(chunk)  # チャンクを復号化
            unpadded_chunk = unpadder.update(decrypted_chunk)  # パディングを削除
            f_out.write(unpadded_chunk)

        # 最後のブロックのパディングを削除
        try:
            unpadded_chunk = unpadder.finalize()
            f_out.write(unpadded_chunk)
        except ValueError:
            pass