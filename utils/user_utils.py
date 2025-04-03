import json, os
from datetime import datetime

USERS_FILE = 'data/users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_user_data(user_id):
    users = load_users()
    user = users.get(str(user_id), {
        "credits": 0,
        "package": "Free",
        "joined": datetime.now().isoformat()
    })
    return user

def add_credit(user_id, amount, package=None):
    users = load_users()
    uid = str(user_id)
    if uid not in users:
        users[uid] = {"credits": 0, "package": "Free", "joined": datetime.now().isoformat()}
    users[uid]['credits'] += amount
    if package:
        users[uid]['package'] = package
    save_users(users)

def process_command(user_id, command):
    user = get_user_data(user_id)
    if command == "/credits":
        return f"💳 You have {user['credits']} credits."
    elif command == "/perks":
        return "✨ Basic: 5 credits | Super: 50 credits | Premium: Unlimited"
    elif command == "/mykey":
        return f"🔑 Package: {user['package']}"
    elif command == "/use":
        if user['credits'] > 0:
            user['credits'] -= 1
            save_users({**load_users(), str(user_id): user})
            return "✅ 1 credit used."
        return "❌ No credits left!"
    else:
        return "❓ Unknown command."
