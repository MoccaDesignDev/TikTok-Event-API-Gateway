import hashlib

def normalize_email(email:str):
    return email.strip().lower()


def normalize_phone(phone:str):
    return "".join(char for char in phone if char.isdigit())


def sha256_hash(value:str):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def hash_user_data(user_data:dict):
    hashed ={}

    if not user_data:
        return hashed
    
    if "email" in user_data and user_data["email"]:
        hashed["email"] = sha256_hash(normalize_email(user_data["email"]))

    if "ip" in user_data:
        hashed["ip"] = user_data["ip"]

    if "user_agent" in user_data:
        hashed["user_agent"] = user_data["user_agent"]

    return hashed

