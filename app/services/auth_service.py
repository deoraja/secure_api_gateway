from app.core.security import hash_password, verify_password, normalize_password

users = []

def get_user(username: str):
    for u in users:
        if u["username"] == username:
            return u
    return None

def register_user(user):
    for u in users:
        if u["username"] == user.username:
            return None

    pwd = normalize_password(user.password)
    hashed = hash_password(pwd)

    new_user = {
        "username": user.username,
        "password": hashed
    }

    users.append(new_user)

    return new_user

def authenticate_user(user):
    db_user = get_user(user.username)

    if not db_user:
        return None

    if not verify_password(user.password, db_user["password"]):
        return None

    return db_user