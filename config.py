import json

default_database = "memo"

db_config = {}

endpoint = ""

can_register = False


def load_config():
    with open("config.json") as f:
        global db_config, default_database, endpoint, can_register
        config = json.load(f)
        db_config = config["db_connect_info"]
        default_database = config["db_name"]
        endpoint = config["endpoint"]
        can_register = config["can_register"]


def get_config():
    return db_config


def get_endpoint():
    return endpoint


def get_can_register():
    return can_register
