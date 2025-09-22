import ujson

CONFIG_FILE = "config.json"

# ----------------------------
# Config save/load
# ----------------------------
def save_config(data):
    try:
        with open(CONFIG_FILE, "w") as f:
            ujson.dump(data, f)
        print("Config saved")
    except Exception as e:
        print("Config save failed:", e)

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return ujson.load(f)
    except:
        return {}

