from app import bcrypt
hash_salvo = "$2b$12$pEsecJCZXSyA1fBJUHJ5/eSzX875ctX6XmxLkHRPiSakJFmkjtJMO"
print(bcrypt.check_password_hash(hash_salvo, "123"))