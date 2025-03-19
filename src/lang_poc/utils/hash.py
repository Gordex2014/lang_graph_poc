import hashlib

def hash_md5(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()
