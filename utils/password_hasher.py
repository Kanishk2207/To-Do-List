import hashlib


def hash_password(password):
    hashed_password = hashlib.sha256(str(password).encode()).hexdigest()

    return hashed_password
