import json
import os

def load_json(filename, default):
    if not os.path.exists(filename):
        return default
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_leaderboard():
    return load_json('leaderboard.json', [])

def save_score(name, score, distance):
    lb = get_leaderboard()
    lb.append({"name": name, "score": score, "distance": round(distance, 2)})
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    save_json('leaderboard.json', lb)

def get_settings():
    return load_json('settings.json', {"sound": True, "color": "Red", "difficulty": "Normal"})

def save_settings(settings):
    save_json('settings.json', settings)