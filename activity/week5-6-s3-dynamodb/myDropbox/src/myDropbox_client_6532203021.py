import mimetypes
import os
import readline  # enable input history

import requests
from dotenv import load_dotenv

load_dotenv()
lambda_url = os.getenv("LAMBDA_URL")


def view(user: str):
    """Retrieves a list of files in the user's folder."""
    response = requests.post(
        lambda_url, json={"command": "view", "folder_prefix": user}
    )
    if response.status_code == 200:
        print("OK")
        files: list = response.json()["files"]
        formatted_files = []
        for file in files:
            filename = file["filename"]
            size = file["size"]
            last_modified = file["lastModifiedDate"].replace("T", " ")
            owner = file["owner"]
            formatted_files.append(f"{filename} {size} {last_modified} {owner}")

        return formatted_files
    else:
        print(response.json()["error"])
        return None


def get(key: str, owner: str, current_user: str):
    """Retrieves a presigned URL for the given file key."""
    onwer_key = f"{owner}/{key}"
    response = requests.post(
        lambda_url,
        json={"command": "get", "key": onwer_key, "currentUser": current_user},
    )
    if response.status_code == 200:
        print("OK")
        file_url = response.json()["presigned_url"]
        return file_url
    else:
        print(response.json()["error"])
        return None


def download_file(url: str, filename: str, owner: str):
    """Downloads a file from the given URL and saves it locally."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # raise an error for bad status codes

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            print(f"File not found: {filename} owned by {owner}")
        else:
            print(f"Failed to download file: {e}")


def put(filepath: str, user: str):
    """Uploads a file to the user's folder."""
    if not os.path.isfile(filepath):
        print(f"File '{filepath}' does not exist.")
        return

    content_type, _ = mimetypes.guess_type(filepath)
    if content_type is None:
        print(f"Could not determine the content type of '{filepath}'.")
        return

    filename = os.path.basename(filepath)
    response = requests.post(
        lambda_url,
        json={
            "command": "put",
            "key": f"{user}/{filename}",
            "content_type": content_type,
        },
    )

    with open(filepath, "rb") as file:
        if response.status_code == 200:
            upload_url = response.json()["upload_url"]
            upload_response = requests.put(
                upload_url, data=file, headers={"Content-Type": content_type}
            )

            if upload_response.status_code == 200:
                print("OK")
            else:
                print(f"Failed to upload file: {upload_response.json()}")
        else:
            print(response.json()["error"])


def share(key: str, username: str, owner: str):
    """Shares a file with the given username."""
    response = requests.post(
        lambda_url,
        json={"command": "share", "key": f"{owner}/{key}", "username": username},
    )
    if response.status_code == 201:
        print("OK")
    else:
        print(response.json()["error"])


def newuser(username: str, password: str):
    """Creates a new user with the given username and password."""
    response = requests.post(
        lambda_url,
        json={"command": "newuser", "username": username, "password": password},
    )
    if response.status_code == 201:
        print("OK")
    else:
        print(response.json()["error"])


def login(username: str, password: str):
    """Logs in the user with the given username and password."""
    response = requests.post(
        lambda_url,
        json={"command": "login", "username": username, "password": password},
    )
    if response.status_code == 200:
        print("OK")
        return username
    else:
        print(response.json()["error"])
        return None


def main():
    print(
        """
Welcome to myDropbox Application
======================================================
Please input command (newuser username password password, login
username password, put filename, get filename, view, or logout).
If you want to quit the program just type quit.
======================================================
"""
    )

    current_user: str = None

    while True:
        prompt = ">>" if current_user is None else f"{current_user}>>"
        raw_command = input(prompt)
        command = raw_command.strip().lower().split()
        if len(command) == 0:
            continue

        if command[0] == "quit":
            print("======================================================")
            break

        elif command[0] == "newuser":
            if len(command) != 4:
                print(
                    "Invalid command, format: 'newuser <username> <password> <confirm_password>'"
                )
                continue
            username, password, confirm_password = command[1], command[2], command[3]
            if password != confirm_password:
                print("Passwords do not match.")
                continue
            newuser(username, password)

        elif command[0] == "login":
            if len(command) != 3:
                print("Invalid command, format: 'login <username> <password>'")
                continue
            username = command[1]
            password = command[2]
            current_user = login(username, password)

        elif command[0] == "logout":
            current_user = None
            print("OK")

        else:
            if current_user is None:
                print("Please login first.")
                continue

            if command[0] == "view":
                files = view(current_user)
                if files is not None:
                    for file in files:
                        print(file)

            elif command[0] == "get":
                if len(command) != 3:
                    print("Invalid command, format: 'get <object_key> <owner>'")
                    continue
                key, owner = command[1], command[2]
                file_url = get(key, owner, current_user)

                if file_url:
                    filename = os.path.basename(key)
                    download_file(file_url, filename, owner)
                else:
                    print("Failed to retrieve the file URL.")

            elif command[0] == "put":
                if len(command) != 2:
                    print("Invalid command, format: 'put <filepath>'")
                    continue
                filepath = command[1]
                put(filepath, current_user)

            elif command[0] == "share":
                if len(command) != 3:
                    print("Invalid command, format: 'share <object_key> <username>'")
                    continue
                key, username = command[1], command[2]
                share(key, username, current_user)

            else:
                print(
                    "Invalid command. Current supported commands: view, get, put, newuser, login, logout, quit"
                )


if __name__ == "__main__":
    main()
