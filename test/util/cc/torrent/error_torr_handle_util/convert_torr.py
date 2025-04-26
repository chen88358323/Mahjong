def convert_torr_clear_rn(oldfile,newfile):
    # 读取原始文件
    with open(oldfile, 'rb') as file:
        file_content = file.read()

    # 去除末尾的 \r\n
    if file_content.endswith(b'\r\n'):
        file_content = file_content[:-2]

    # 写入新文件
    with open(newfile, 'wb') as new_file:
        new_file.write(file_content)

if __name__ == "__main__":
    convert_torr_clear_rn(r'222\xx.torrent',r'222\xx_new.torrent')