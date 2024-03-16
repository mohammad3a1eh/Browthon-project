import os
import json


base_setting = {
    "home_url": "https://www.google.com/",
    "proxy": {
        "status": False,
        "host": "",
        "port": 8080,
        "login": {
            "status": False,
            "user": "",
            "pass": "",
        }
    }
}


def load_setting():
    if os.path.isfile("setting.json"):
        with open("setting.json", "r") as setting_file:
            setting_file = setting_file.read()
            setting_json = json.loads(setting_file)
            return setting_json
    else:
        return base_setting

