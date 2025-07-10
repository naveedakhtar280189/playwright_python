import json
import yaml

def read_json_config(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] JSON file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"[ERROR] Invalid JSON format in file: {file_path}")
    except Exception as e:
        raise Exception(f"[ERROR] Unexpected error reading JSON: {str(e)}")

def read_yaml_config(file_path):
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] YAML file not found: {file_path}")
    except yaml.YAMLError:
        raise ValueError(f"[ERROR] Invalid YAML format in file: {file_path}")
    except Exception as e:
        raise Exception(f"[ERROR] Unexpected error reading YAML: {str(e)}")

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] Text file not found: {file_path}")
    except Exception as e:
        raise Exception(f"[ERROR] Error reading text file: {str(e)}")

def write_text_file(file_path, text):
    try:
        with open(file_path, 'w') as f:
            f.write(text)
        print(f"[PASS] Text written successfully: {file_path}")
    except Exception as e:
        raise Exception(f"[ERROR] Error writing text file: {str(e)}")
