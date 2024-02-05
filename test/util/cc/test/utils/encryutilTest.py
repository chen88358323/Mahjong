import os
import hashlib
import time

def test_calc():


    # 低性能版本
    def calculate_md5_low_performance(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            md5_hash = hashlib.md5(content)
            return md5_hash.hexdigest()

    # 中性能版本
    def calculate_md5_medium_low_performance(file_path):
        block_size = 65536  # 64KB

        md5_hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            for block in iter(lambda: file.read(block_size), b''):
                md5_hasher.update(block)

        return md5_hasher.hexdigest()

    # 中高性能版本：
    def calculate_md5_medium_high_performance(file_path):
        block_size = 262144  # 256KB

        md5_hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            for block in iter(lambda: file.read(block_size), b''):
                md5_hasher.update(block)

        return md5_hasher.hexdigest()

    # 高性能版本
    def calculate_md5_high_performance(file_path):
        md5_hasher = hashlib.md5()
        with open(file_path, 'rb', buffering=0) as file:
            for chunk in iter(lambda: file.read(8192), b''):
                md5_hasher.update(chunk)

        return md5_hasher.hexdigest()

    # 更高性能
    import mmap
    def calculate_md5_mmap(file_path):
        with open(file_path, 'rb') as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                md5_hasher = hashlib.md5(mmapped_file)
                return md5_hasher.hexdigest()

    def calculate_md5_for_files(folder_path, algorithm):
        file_list = os.listdir(folder_path)
        result = []

        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                start_time = time.time()
                md5_value = algorithm(file_path)
                end_time = time.time()

                execution_time = end_time - start_time
                result.append(execution_time)
                print(f'{file_path} 的 MD5 值为：{md5_value}，计算时间为：{execution_time:.6f} 秒')

        avg_execution_time = sum(result) / len(result)
        min_execution_time = min(result)
        max_execution_time = max(result)

        print('--- 统计数据 ---')
        print(f'平均计算时间：{avg_execution_time:.6f} 秒')
        print(f'最快计算时间：{min_execution_time:.6f} 秒')
        print(f'最慢计算时间：{max_execution_time:.6f} 秒')

    def calc_file_hash(filename):
        bigsize = 300 * 1024 * 1024
        big_file_read_size = 100 * 1024 * 1024
        msize = 1 * 1024 * 1024
        size = os.path.getsize(filename)
        md5hasher = hashlib.md5()
        ''' 
        Calculate the file hash.
        In order to have better performance, if the file is larger than 4MiB,
        only the first and last 100MiB content of the file will take into consideration
        '''
        if size <= bigsize:
            with open(filename, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapfile:
                    md5hasher.update(mmapfile)
                    hcode = md5hasher.hexdigest()
                    # logger.log.info(hcode + '   ' + str(round(size / msize, 2)) + 'Mb     ' + filename)
                    return md5hasher.hexdigest()
        else:
            with open(filename, 'rb') as f:
                # 偏移量，大于300M的文件，读取前100M以及最后面的100M
                md5hasher.update(f.read(big_file_read_size))
                f.seek(size - big_file_read_size)
                md5hasher.update(f.read(big_file_read_size))
                hcode = md5hasher.hexdigest()
                # logger.log.info(hcode + '   ' + str(round(size / msize, 2)) + 'Mb     ' + filename)
                return hcode

    print('--- 低性能版本 ---')
    calculate_md5_for_files(folder_path, calculate_md5_low_performance)

    print('--- 中性能版本 ---')
    calculate_md5_for_files(folder_path, calculate_md5_medium_low_performance)

    print('--- 中高性能版本 ---')
    calculate_md5_for_files(folder_path, calculate_md5_medium_high_performance)

    print('--- 高性能版本 ---')
    calculate_md5_for_files(folder_path, calculate_md5_high_performance)

    print('--- 更高性能 ---')
    calculate_md5_for_files(folder_path, calculate_md5_mmap)

    print('--- 更高性能V8 ---')
    calculate_md5_for_files(folder_path, calc_file_hash)


if __name__ == "__main__":
    folder_path = 'E:\\test_folder'  # 将路径修改为之前生成文件的路径
    test_calc(folder_path)