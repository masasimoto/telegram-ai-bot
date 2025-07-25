
import os
def get_persona(user_id):
    path = f"storage/persona/{user_id}.txt"
    if os.path.exists(path):
        return open(path).read()
    return "You are a helpful, creative AI assistant. You speak naturally and casually."

def set_persona(user_id, new_persona):
    os.makedirs("storage/persona", exist_ok=True)
    with open(f"storage/persona/{user_id}.txt", "w") as f:
        f.write(new_persona)

