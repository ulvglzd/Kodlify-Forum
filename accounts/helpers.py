import uuid

def get_random_hash():
    hash = str(uuid.uuid4())[:8].replace('-', '').lower()
    return hash