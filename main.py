import os
import psutil
from typing import Union
import json
import requests

dst = "C:/Windows/System32/drivers/etc/hosts"

def is_website_available(url: str) -> bool:
    try:
        response = requests.get(url, timeout=5)  # Set a timeout for the request
        if response.status_code == 200:
            print(f"Website '{url}' is available (Status Code: {response.status_code})")
            return True
        else:
            print(f"Website '{url}' is not available (Status Code: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"Website '{url}' is unreachable (Connection Error)")
        return False
    except requests.exceptions.Timeout:
        print(f"Website '{url}' timed out (Timeout Error)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred while checking '{url}': {e}")
        return False

def read_only(file_path: str) -> None:
    os.chmod(file_path, 0o444)

def read_write(file_path: str) -> None:
    os.chmod(file_path, 0o666)

def is_app_running(app_name: str) -> bool:
    """Checks if an application with a given name is running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == app_name:
            return True
    return False

def is_admin() -> bool:
    testing_path: str = "C:/Windows/System32/test_admin.txt"

    try:
        with open(testing_path, 'w') as f:
            f.write("Test is complete.")
        os.remove(testing_path)
        return True
    except PermissionError:
        return False
    except IOError as e:
        print(f"An error occured while testing.\n{e = }")
        return False

def write_text_to(text: str, file_path: str) -> None:
    test = "" or []
    with open(file_path, 'r') as f:
        test = f.read()
        test = test.splitlines()

    with open(file_path, 'w') as f:
        test.append(text)
        f.write("\n".join(test))

def read_file_from(filepath: str) -> str:
    with open(filepath, 'r') as f:
        return str(f.read())

def read_json_from(filepath: str) -> Union[dict, list, None]:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def add_website(website: str) -> None:
    "This function add a website to blocked list in windows.Usage:-website: str => the website you want to block in string"
    if is_website_available(website):
        write_text_to(f"127.0.0.1   {website}", dst)

if __name__ == "__main__":
    print("""Usage:-
  1- Input the website and then the app will exit by itself (It must be like http/https://www.test.com)
  2- You can't open the websites again so be careful.
  3- You can find the source code in the same github repo.""")
    if is_admin():
        read_only(dst)
        test = str(input("Enter an available website (Must start with the protocol): "))
        read_write(dst)
        add_website(test)
        read_only(dst)
    
    exit()