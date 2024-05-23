from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib

def encrypt_file(input_file, output_file, key):
    # keyをハッシュ化させて、下16バイトを取得
    key = hashlib.sha256(key.encode('utf-8')).hexdigest()[-16:]
    # キーをバイト列に変換
    key = key.encode('utf-8')  
    

    # 初期化ベクトル（IV）を生成
    iv = b'\x00' * 16  # 16バイトのゼロ

    # AES CBC暗号化器を作成
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # パディングを適用するためのパディングオブジェクトを作成
    padder = padding.PKCS7(128).padder()

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(16)  # 16バイトずつ読み込む
            if not chunk:
                break
            padded_chunk = padder.update(chunk)
            encrypted_chunk = encryptor.update(padded_chunk)  # チャンクを暗号化
            f_out.write(encrypted_chunk)

        # 最後のブロックのパディングを適用
        padded_chunk = padder.finalize()
        encrypted_chunk = encryptor.update(padded_chunk)
        f_out.write(encrypted_chunk)
