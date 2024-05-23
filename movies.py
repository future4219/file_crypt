import atexit
import decrypt
import os
import shutil
from concurrent.futures import ProcessPoolExecutor

def decrypt_file_wrapper(args):
    return decrypt.decrypt_file(*args)

def cleanup():
    tmp_directory_path = "D:\\デスクトップ\\tmp"
    # 一時的に作ったディレクトリを削除
    if os.path.exists(tmp_directory_path):
        shutil.rmtree(tmp_directory_path)

def main():
    tmp_directory_path = "D:\\デスクトップ\\tmp"
    try:
        print("複合化するkey(数字)を入力してください")
        key = input()
        
        #　暗号化されているファイルがあるィレクトリのパスを指定
        encrypted_directory_path = "D:\\新しいフォルダー\\sakai"

        # ディレクトリが存在しない場合にのみ作成
        if not os.path.exists(tmp_directory_path):
            os.makedirs(tmp_directory_path)

        # 新しいディレクトリをエクスプローラで開く
        os.startfile(tmp_directory_path)
            
        # "D:\新しいフォルダー\sakai" の中のファイルをすべて配列に入れる
        encrypted_file_list = os.listdir(encrypted_directory_path)
    
        # プロセスプールを作成
        with ProcessPoolExecutor() as executor:
            args = [(encrypted_directory_path + "\\" + file, tmp_directory_path + "\\" + file + ".mp4", key) for _, file in enumerate(encrypted_file_list)]
            executor.map(decrypt_file_wrapper, args)
        
        print("All files decrypted successfully.")
        
        # ここで無限ループ(ctrl+cで終了, tmpフォルダを削除)
        while True:
            pass
    except KeyboardInterrupt:
        print("Ctrl+C was pressed. Exiting...")
    finally:
        cleanup()

if __name__ == "__main__":
    atexit.register(cleanup)
    main()