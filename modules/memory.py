import os
import json

class MemoryManager:
    def __init__(self, dir_path="user_memory"):
        self.dir_path = dir_path
        os.makedirs(self.dir_path, exist_ok=True)

    def get_path(self, user_id):
        return os.path.join(self.dir_path, f"{user_id}.json")

    def load(self, user_id):
        path = self.get_path(user_id)
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return [{"role": "system", "content": "Kamu adalah asisten AI yang bisa berperan apa saja sesuai perintah user."}]

    def save(self, user_id, memory):
        path = self.get_path(user_id)
        with open(path, "w") as f:
            json.dump(memory[-15:], f)  # Simpan 15 terakhir
