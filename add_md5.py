import hashlib


def am5(src):
    m = hashlib.md5()
    m.update(src)
    src = m.hexdigest()
    return src