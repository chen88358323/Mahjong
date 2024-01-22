from argon2 import PasswordHasher


if __name__ == '__main__':
    ph = PasswordHasher()
    hash = ph.hash("correct horse battery staple")
    print('hash is '+hash)
    checktag=ph.verify(hash, "correct horse battery staple")
    print('checktag is ' + str(checktag))

    rehashcode =ph.check_needs_rehash(hash)
    print('rehashcode is ' + str(rehashcode))