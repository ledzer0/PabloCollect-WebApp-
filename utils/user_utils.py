# utils/user_utils.py

import json
from datetime import datetime

DATA_FILE = 'data/storage.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_user_data(user_id):
    data = load_data()
    return data.get(str(user_id), {
        "package": "None",
        "credits": 0,
        "last_active": None
    })

def add_credit(user_id, amount, package="Manual"):
    data = load_data()
    user = data.get(str(user_id), {})
    user['credits'] = user.get('credits', 0) + amount
    user['package'] = package
    user['last_active'] = datetime.now().isoformat()
    data[str(user_id)] = user
    save_data(data)

def process_command(user_id, command):
    user = get_user_data(user_id)
    if command == "/credits":
        return f"You have {user.get('credits', 0)} credits."
    elif command == "/mykey":
        return f"Package: {user.get('package', 'None')}"
    elif command == "/use":
        if user.get('credits', 0) > 0:
            add_credit(user_id, -1)
            return "✅ Credit used!"
        return "❌ Not enough credits."
    else:
        return "Unknown command."
