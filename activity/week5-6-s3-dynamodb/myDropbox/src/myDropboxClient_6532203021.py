import mimetypes
import os
import readline  # enable input history

import requests
from dotenv import load_dotenv

load_dotenv()
lambda_url = os.getenv("LAMBDA_URL")


def view():
    response = requests.post(lambda_url, json={"command": "view"})
    if response.status_code == 200:
        files: list = response.json()["files"]

        return files
    else:
        print(response.json()["error"])
        return None


def get(key, owner):
    response = requests.post(
        lambda_url, json={"command": "get", "key": key, "owner": owner}
    )
    if response.status_code == 200:
        file_url = response.json()["presigned_url"]
        return file_url
    else:
        print(response.json()["error"])
        return None


def download_file(url, filename):
    """Downloads a file from the given URL and saves it locally."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # raise an error for bad status codes

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded successfully: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file: {e}")


def put(filepath):
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
            "key": filename,
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
                print(f"File uploaded successfully: {filename}")
            else:
                print(f"Failed to upload file: {upload_response.json()}")
        else:
            print(response.json()["error"])


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

    while True:
        raw_command = input(">>")
        command = raw_command.strip().lower().split()
        if len(command) == 0:
            continue

        if command[0] == "quit":
            print("======================================================")
            break

        elif command[0] == "view":
            files = view()
            if files is not None:
                for file in files:
                    print(file)

        elif command[0] == "get":
            if len(command) != 3:
                print("Invalid command, format: 'get <object_key> <owner>'")
                continue
            key, owner = command[1], command[2]
            file_url = get(key, owner)

            if file_url:
                filename = os.path.basename(key)
                download_file(file_url, filename)
            else:
                print("Failed to retrieve the file URL.")

        elif command[0] == "put":
            if len(command) != 2:
                print("Invalid command, format: 'put <filepath>'")
                continue
            filepath = command[1]
            put(filepath)

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
