from app.utils import hash_password, verify_password

def test_password_hash_verfify():
    password = "secret_123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False
