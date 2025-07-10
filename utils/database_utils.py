import pymysql
import json

def read_json_config(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] Config file not found: {path}")
    except json.JSONDecodeError:
        raise ValueError(f"[ERROR] Invalid JSON format in config: {path}")
    except Exception as e:
        raise Exception(f"[ERROR] Failed to read config file: {str(e)}")

def connect_to_mysql_from_config(config_path):
    try:
        config = read_json_config(config_path)
        connection = pymysql.connect(
            host=config.get("host", "localhost"),
            port=int(config.get("port", 3306)),
            user=config["username"],
            password=config["password"],
            database=config["database"],
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"[PASS] Connected to MySQL database: {config['database']} at {config['host']}")
        return connection
    except KeyError as ke:
        raise KeyError(f"[ERROR] Missing required config key: {ke}")
    except pymysql.MySQLError as e:
        raise Exception(f"[ERROR] MySQL connection failed: {str(e)}")

def run_query_from_file(conn, query_file_path):
    try:
        with open(query_file_path, 'r') as f:
            query = f.read()
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        print(f"[PASS] Query executed successfully.")
        return results
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] Query file not found: {query_file_path}")
    except pymysql.MySQLError as e:
        raise Exception(f"[ERROR] SQL execution failed: {str(e)}")
