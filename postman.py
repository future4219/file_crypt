import requests
import os
import uuid
import sys
import encrypt
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor

def print_line():
    print("--------------------------------------------------------")

def is_mp4_url(url):
    return url.lower().endswith('.mp4')

def check_monsnode_in_url(url):
    if "monsnode" in url:
        return True
    else:
        return False

def download_and_encrypt(url, i, key, folder_path):
    if check_monsnode_in_url(url):
        print_line()
        print(f"{i}.")
        print("Invalid URL")
        print_line()
        return 1

    response = requests.get(url, stream=True)

    if response.status_code != 200:
        print_line()
        print("Request Failed (is not code 200)")
        print("Specified URL:", url)
        print_line()
        return 1
    else:
        filename = str(uuid.uuid4())
        file_path = os.path.join(folder_path, filename + ".mp4")
        print_line()
        print(f"{i}.")
        print("Request success")
        print("Generating within: ",file_path)
        print_line()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(file_path)


        with tempfile.NamedTemporaryFile(delete=False, suffix=".aes") as temp:
            temp_filename = temp.name

        # 一時ファイルの名前を使用して暗号化
        encrypt.encrypt_file(file_path, temp_filename, key) #　暗号化
        # 一時ファイルを自分のディレクトリにコピー
        destination_path = f"D:\\新しいフォルダー\\sakai\\{filename}.aes"
        shutil.copy(temp_filename, destination_path)
        os.remove(file_path)

    return 0

def download_mp4():
    folder_path = "D:\新しいフォルダー\sakai"
    url_list = sys.argv
    fail_counter = 0

    print("暗号化するkeyを入力してください")
    key = input()

    if len(url_list) <= 1:
        print("Please specify argument")
        return

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_and_encrypt, url_list[i], i, key, folder_path) for i in range(1, len(url_list))]
        for future in futures:
            fail_counter += future.result()

    if fail_counter > 0:
        print(fail_counter, "times failed")
    else: 
        print("Download Completed!")

#　実行
download_mp4()