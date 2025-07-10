import random
import string
import uuid
from itertools import permutations, combinations
import datetime

FIRST_NAMES = ['John', 'Jane', 'Alice', 'Bob', 'David', 'Emma', 'Liam', 'Olivia']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
EMAIL_DOMAINS = ['example.com', 'test.com', 'mail.com', 'demo.org']

def random_string(length=8):
    try:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random string: {str(e)}")

def random_number(length=6):
    try:
        return ''.join(random.choices(string.digits, k=length))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random number: {str(e)}")

def random_alphabets(length=8):
    try:
        return ''.join(random.choices(string.ascii_letters, k=length))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random alphabets: {str(e)}")

def random_password(length=12):
    try:
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(characters, k=length))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random password: {str(e)}")

def random_integer(min_value=0, max_value=100):
    try:
        return random.randint(min_value, max_value)
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate random integer: {str(e)}")

def random_first_name():
    return random.choice(FIRST_NAMES)

def random_last_name():
    return random.choice(LAST_NAMES)

def random_email():
    try:
        fname = random_first_name().lower()
        lname = random_last_name().lower()
        domain = random.choice(EMAIL_DOMAINS)
        num = random.randint(100, 999)
        return f"{fname}.{lname}{num}@{domain}"
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate email: {str(e)}")

def generate_uuid():
    try:
        return str(uuid.uuid4())
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate UUID: {str(e)}")

def generate_combinations(input_list, r):
    try:
        return list(combinations(input_list, r))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate combinations: {str(e)}")

def generate_permutations(input_list, r):
    try:
        return list(permutations(input_list, r))
    except Exception as e:
        raise Exception(f"[ERROR] Failed to generate permutations: {str(e)}")

def get_current_datetime():
    try:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        raise Exception(f"[ERROR] Failed to get current datetime: {str(e)}")

def format_datetime(dt, format='%Y-%m-%d'):
    try:
        return dt.strftime(format)
    except Exception as e:
        raise Exception(f"[ERROR] Failed to format datetime: {str(e)}")
