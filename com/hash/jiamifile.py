

import base64
from cryptography.fernet import Fernet
import argon2


class XDEncrypt():
    def __init__(self):
        pass

    def encrypt(self, password, in_file, out_file):
        argon2_parameters = argon2.Parameters(type=argon2.low_level.Type.ID, version=19, salt_len=16, hash_len=32, time_cost=16,
                          memory_cost=2 ** 20, parallelism=8)
        hasher = argon2.PasswordHasher(time_cost=argon2_parameters.time_cost, memory_cost=argon2_parameters.memory_cost,
                                       parallelism=argon2_parameters.parallelism, hash_len=argon2_parameters.hash_len,
                                       salt_len=argon2_parameters.salt_len)
        pw_hash = hasher.hash(password)
        salt = pw_hash.split("$")[-2]
        raw_hash = argon2.low_level.hash_secret_raw(time_cost=argon2_parameters.time_cost,
                                                    memory_cost=argon2_parameters.memory_cost,
                                                    parallelism=argon2_parameters.parallelism,
                                                    hash_len=argon2_parameters.hash_len,
                                                    secret=bytes(password, "utf_16_le"), salt=bytes(salt, "utf_16_le"),
                                                    type=argon2_parameters.type)
        key = base64.urlsafe_b64encode(raw_hash)
        fernet = Fernet(key)
        with open(in_file, 'rb') as f_in,open(out_file, 'wb+') as f_out:
                data = f_in.read()
                enc_data = fernet.encrypt(data)
                pw_hash = pw_hash + '\n'
                f_out.write(bytes(pw_hash, "utf-8"))
                f_out.write(enc_data)
                print('加密完成')

    def decrypt(self, password, in_file):
        with open(in_file, 'r') as f:
            pw_hash = f.readline()[:-1]
        p = argon2.extract_parameters(pw_hash)
        hasher = argon2.PasswordHasher(time_cost=p.time_cost,
                                       memory_cost=p.memory_cost,
                                       parallelism=p.parallelism,
                                       hash_len=p.hash_len,
                                       salt_len=p.salt_len)
        try:
            hasher.verify(pw_hash, password)
            print("密码校验成功")
        except:
            print("密码校验失败")
            exit()
        salt = pw_hash.split("$")[-2]
        raw_hash = argon2.low_level.hash_secret_raw(time_cost=p.time_cost,
                                                    memory_cost=p.memory_cost,
                                                    parallelism=p.parallelism,
                                                    hash_len=p.hash_len,
                                                    secret=bytes(password, "utf_16_le"),
                                                    salt=bytes(salt, "utf_16_le"),
                                                    type=p.type)
        key = base64.urlsafe_b64encode(raw_hash)
        fernet = Fernet(key)
        dec_data = b''
        with open(in_file, 'rb') as f_in:
            enc_data = f_in.readlines()[1]
            try:
                dec_data = fernet.decrypt(enc_data)
                print("decryption succeed")
            except:
                print("decryption failed")
        return dec_data


if __name__ == '__main__':
    xde = XDEncrypt()
    xde.encrypt(password='123456', in_file=r'D:\clear.txt', out_file=r'D:\clear_crp.txt')
    res = xde.decrypt(password='123456', in_file=r'D:\clear_crp.txt')
    print(res)
    pass


