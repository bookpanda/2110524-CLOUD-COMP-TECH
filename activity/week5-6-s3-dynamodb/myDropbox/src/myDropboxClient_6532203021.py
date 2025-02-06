import os
import sys

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


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        print("Error: Division by zero.")
        return None
    return x / y


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
        command = input(">>").strip().lower().split()
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

        elif command[0] == "put":
            if len(command) != 2:
                print("Invalid command. Type 'help' for usage.")
                continue
            print("Put file")
        else:
            # Try to process commands with arguments
            try:
                parts = command.split()
                if len(parts) != 3:
                    print("Invalid command. Type 'help' for usage.")
                    continue

                # Extract command and arguments
                cmd, x, y = parts[0], float(parts[1]), float(parts[2])

                if cmd == "add":
                    result = add(x, y)
                elif cmd == "subtract":
                    result = subtract(x, y)
                elif cmd == "multiply":
                    result = multiply(x, y)
                elif cmd == "divide":
                    result = divide(x, y)
                else:
                    print("Invalid command. Type 'help' for usage.")
                    continue

                if result is not None:
                    print(f"Result: {result}")
            except ValueError:
                print("Invalid input. Please enter numbers for x and y.")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
