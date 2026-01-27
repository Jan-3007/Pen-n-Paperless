import os
import json



def _data_path(char_id):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, f'character_{char_id}_stats.json')



def load_data(char_id, key : str):
    p = _data_path(char_id)
    if os.path.exists(p):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)[key]
        except Exception:
            return {}
        
    # default
    return {
        'level': 1,
        'experience': 0,
        'hp': 10,
        'armor': 5,
        'strength': 10,
        'dexterity': 10,
        'intelligence': 10,
    }


def save_data(char_id, key : str, data : dict):
    path = _data_path(char_id)
    try:
        with open(path, 'w', encoding='utf-8') as f:

            match key:
                case "character" | "stats":
                    json_data = json.stringify({[key]: data})
                case _:
                    json_data = data

            # overwrite the existing data of the given key, or create new if not existing
            json.dump(json_data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass




