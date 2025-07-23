import requests
import pymysql
from utils.config_reader import read_json_config

def check_web_app():
    config_path = "data/config.json"
    config = read_json_config(config_path)
    url = config["environment"]["base_url"]
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def check_mobile_backend():
    config_path = "data/config.json"
    config = read_json_config(config_path)
    api_endpoint = config["environment"]["api_url"]
    try:
        response = requests.get(f"{api_endpoint}", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def check_api():
    config_path = "data/config.json"
    config = read_json_config(config_path)
    endpoint = config["environment"]["api_url"]
    try:
        response = requests.get(endpoint, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def check_database(host, user, password, db):
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=db, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False
