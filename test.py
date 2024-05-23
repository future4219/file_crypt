import encrypt
import os 


path = "D:\\デスクトップ\\一時的"

files = encrypted_file_list = os.listdir(path)
for file in files:
    encrypt.encrypt_file(path + "\\" + file, f"D:\\新しいフォルダー\\sakai\\{file}.aes", "sakai")